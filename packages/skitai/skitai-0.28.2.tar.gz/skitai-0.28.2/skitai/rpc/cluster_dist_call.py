import time
from aquests.athreads import socket_map
from aquests.athreads import trigger
from rs4.cbutil import tuple_cb
from aquests.client.asynconnect import AsynSSLConnect, AsynConnect
from aquests.dbapi.dbconnect import DBConnect
import threading
from aquests.protocols.http import request as http_request
from aquests.protocols.http import request_handler as http_request_handler
from aquests.protocols.http2 import request_handler as http2_request_handler
from aquests.protocols.grpc.request import GRPCRequest
from aquests.protocols.http import response as http_response
from aquests.protocols.ws import request_handler as ws_request_handler
from aquests.protocols.ws import request as ws_request
from . import rcache
from skitai import lifetime
import asyncore
import sys
import inspect
from skitai import exceptions
from skitai import REQFAIL, UNSENT, TIMEOUT, NETERR, NORMAL

DEFAULT_TIMEOUT = 10
WAIT_POLL = False

class OperationError (Exception):
	pass

class Result (rcache.Result):
	def __init__ (self, id, status, response, ident = None):
		rcache.Result.__init__ (self, status, ident)
		self.node = id
		self.__response = response
		
	def __getattr__ (self, attr):
		return getattr (self.__response, attr)
	
	def reraise (self):		
		if self.status != NORMAL:
			self.__response.raise_for_status ()
			
	def cache (self, timeout = 300):
		if self.status != NORMAL:
			return
		rcache.Result.cache (self, timeout)
	
	def close (self):
		self.__response = None	


class Results (rcache.Result):
	def __init__ (self, results, ident = None):
		self.results = results
		self.status_code = [rs.status_code for rs in results]
		rcache.Result.__init__ (self, [rs.status for rs in self.results], ident)
		
	def __iter__ (self):
		return self.results.__iter__ ()
	
	def cache (self, timeout = 300):
		if self.is_cached:
			return
		if rcache.the_rcache is None or not self.ident: 
			return
		if [_f for _f in [rs.status != 3 for rs in self.results] if _f]:
			return				
		rcache.Result.__timeout = timeout
		rcache.Result.__cached_time = time.time ()
		
		rcache.the_rcache.cache (self)


class Dispatcher:
	def __init__ (self, cv, id, ident = None, filterfunc = None, cachefs = None, callback = None):
		self._cv = cv
		self.id = id
		self.ident = ident
		self.filterfunc = filterfunc
		self.cachefs = cachefs
		self.callback = callback		
		self.creation_time = time.time ()
		self.status = UNSENT	
		self.result = None
		self.handler = None
			
	def get_id (self):
		return self.id
	
	def get_status (self):
		with self._cv:
			return self.status
		
	def set_status (self, code, result = None):
		with self._cv:
			self.status = code
			if result:		
				self.result = result
		return code
		
	def get_result (self):
		if not self.result:
			if self.get_status () == REQFAIL:
				self.result = Result (self.id, REQFAIL, http_response.FailedResponse (731, "Request Failed"), self.ident)
			else:	
				self.result = Result (self.id, TIMEOUT, http_response.FailedResponse (730, "Timeout"), self.ident)
		return self.result

	def do_filter (self):
		if self.filterfunc:
			self.filterfunc (self.result)
		
	def handle_cache (self, response):
		self.set_status (NORMAL, Result (self.id, status, response, self.ident))		
							
	def handle_result (self, handler):
		if self.get_status () == TIMEOUT:
			# timeout, ignore
			return
	
		response = handler.response
		# DON'T do_filter here, it blocks select loop		
		if response.code >= 700:
			if response.code == 702:
				status = TIMEOUT
			else:
				status = NETERR
		else:
			status = NORMAL
		
		result = Result (self.id, status, response, self.ident)
		
		cakey = response.request.get_cache_key ()
		if self.cachefs and cakey and response.max_age:
			self.cachefs.save (
				cakey,
				response.get_header ("content-type"), response.content, 
				response.max_age, 0
			)

		handler.asyncon = None
		handler.callback = None
		handler.response = None
		self.set_status (status, result)
		tuple_cb (self, self.callback)
		

class ClusterDistCall:
	def __init__ (self,
		cluster, 
		uri,
		params = None,
		reqtype = "get",
		headers = None,
		auth = None,	
		meta = None,	
		use_cache = False,	
		mapreduce = True,
		filter = None,
		callback = None,
		timeout = 10,
		origin = None,
		cachefs = None,
		logger = None
		):
		
		self._cluster = cluster
		self._uri = uri
		self._params = params
		self._headers = headers
		self._reqtype = reqtype
			
		self._auth = auth		
		self._meta = meta or {}
		self._use_cache = use_cache
		self._mapreduce = mapreduce
		self._filter = filter
		self._callback = callback
		self._timeout = timeout
		self._origin = origin
		self._cachefs = cachefs
		self._logger = logger
	
		self._requests = {}
		self._results = []
		self._canceled = 0
		self._init_time = time.time ()
		self._cv = None
		self._retry = 0		
		self._cached_request_args = None		
		self._numnodes = 0
		self._cached_result = None
		self._request = None
			
		if self._cluster:
			nodes = self._cluster.get_nodes ()
			self._numnodes = len (nodes)
			if self._mapreduce:
				self._nodes = nodes
			else: # anyone of nodes
				self._nodes = [None]
			
		if not self._reqtype.lower ().endswith ("rpc"):
			self._build_request ("", self._params)
	
	def __del__ (self):
		self._cv = None
		self._results = []
	
	def _get_ident (self):
		cluster_name = self._cluster.get_name ()
		if cluster_name == "__socketpool__":
			_id = "%s/%s" % (self._uri, self._reqtype)
		else:
			_id = "%s/%s/%s" % (cluster_name, self._uri, self._reqtype)		
		_id += "/%s/%s" % self._cached_request_args
		_id += "%s" % (
			self._mapreduce and "/M" or ""			
			)
		return _id
	
	def _add_header (self, n, v):
		if self._headers is None:
			self._headers = {}
		self._headers [n] = v
	
	def _handle_request (self, request, rs, asyncon, handler):
		if self._cachefs:
			# IMP: mannual address setting
			request.set_address (asyncon.address)		
			cakey = request.get_cache_key ()
			if cakey:			
				cachable = self._cachefs.is_cachable (
					request.get_header ("cache-control"),
					request.get_header ("cookie") is not None, 
					request.get_header ("authorization") is not None,
					request.get_header ("pragma")
				)
				
				if cachable:
					hit, compressed, max_age, content_type, content = self._cachefs.get (cakey, undecompressible = 0)			
					if hit:
						header = "HTTP/1.1 200 OK\r\nContent-Type: %s\r\nX-Skitaid-Cache-Lookup: %s" % (
							content_type, hit == 1 and "MEM_HIT" or "HIT"
						)		
						response = http_response.Response (request, header)
						response.collect_incoming_data (content)
						response.done ()
						asyncon.set_active (False)
						rs.handle_cache (response)						
						return 0
	
		r = handler (asyncon, request, rs.handle_result)
		if asyncon.get_proto () and asyncon.isconnected ():			
			asyncon.handler.handle_request (r)
		else:				
			r.handle_request ()
		
		return 1
		 						
	def _build_request (self, method, params):
		self._cached_request_args = (method, params) # backup for retry
		if self._use_cache and rcache.the_rcache:
			self._cached_result = rcache.the_rcache.get (self._get_ident (), self._use_cache)
			if self._cached_result is not None:
				self._callback and tuple_cb (self._cached_result, self._callback)
				return
		
		requests = 0
		while self._avails ():
			if self._cluster.get_name () != "__socketpool__":
				asyncon = self._get_connection (None)
			else:
				asyncon = self._get_connection (self._uri)
			self._auth = self._auth or asyncon.get_auth ()
			
			_reqtype = self._reqtype.lower ()
			rs = Dispatcher (
				self._cv, asyncon.address, 
				ident = not self._mapreduce and self._get_ident () or None, 
				filterfunc = self._filter, cachefs = self._cachefs, 
				callback = self._collect
			)
			self._requests [rs] = asyncon	
			
			try:
				if _reqtype in ("ws", "wss"):
					handler = ws_request_handler.RequestHandler					
					request = ws_request.Request (self._uri, params, self._headers, self._auth, self._logger, self._meta)
												
				else:				
					if not self._use_cache:
						self._add_header ("Cache-Control", "no-cache")
					
					handler = http_request_handler.RequestHandler					
					if _reqtype in ("rpc", "xmlrpc"):
						request = http_request.XMLRPCRequest (self._uri, method, params, self._headers, self._auth, self._logger, self._meta)
					elif _reqtype == "jsonrpc":
						request = http_request.JSONRPCRequest (self._uri, method, params, self._headers, self._auth, self._logger, self._meta)					
					elif _reqtype == "grpc":
						request = GRPCRequest (self._uri, method, params, self._headers, self._auth, self._logger, self._meta)						
					elif _reqtype == "upload":
						request = http_request.HTTPMultipartRequest (self._uri, _reqtype, params, self._headers, self._auth, self._logger, self._meta)
					else:
						request = http_request.HTTPRequest (self._uri, _reqtype, params, self._headers, self._auth, self._logger, self._meta)				
				
				requests += self._handle_request (request, rs, asyncon, handler)
					
			except:
				self._logger ("Request Creating Failed", "fail")
				self._logger.trace ()
				rs.set_status (-1)
				asyncon.set_active (False)
				continue
			
		if requests:
			self._request = request # sample for unitest
			trigger.wakeup ()
		
		if _reqtype [-3:] == "rpc":
			return self
			
	def _avails (self):
		return len (self._nodes)
	
	def _get_connection (self, id = None):
		if id is None: id = self._nodes.pop ()
		else: self._nodes = []
		asyncon = self._cluster.get (id)		
		self._setup (asyncon)
		return asyncon
	
	def _setup (self, asyncon):
		asyncon.set_timeout (self._timeout)
		if self._cv is None:
			self._cv = asyncon._cv
				
	def _cancel (self):
		self._canceled = 1
	
	#---------------------------------------------------------
	def cache (self, timeout = 300, validation = None):
		if self._cached_result is None:
			raise ValueError("call getwait, getswait first")		
		
		if validation:
			if isinstance (self._cached_result, Results):
				status_code = set (self._cached_result.status_code)
				if len (status_code) != 1 or status_code.pop () not in validation:
					return
			elif self._cached_result.status_code not in validation:
				return
			
		self._cached_result.cache (timeout)
	
	def _wait (self, timeout = DEFAULT_TIMEOUT):		
		if self._timeout != timeout:
			for rs, asyncon in self._requests.items ():
				asyncon.set_timeout (timeout)
		
		while self._requests and not self._canceled:
			remain = timeout - (time.time () - self._init_time)
			if remain <= 0: break						
			self._cv.acquire ()
			self._cv.wait (remain)
			self._cv.release ()
		# timeouts
		for rs, asyncon in list(self._requests.items ()):
			asyncon.handle_abort () # abort imme
			rs.set_status (TIMEOUT)
			self._cluster.report (asyncon, False) # maybe dead
			self._results.append (rs)
			del self._requests [rs]
		
	def _fail_log (self, status):
		if self._origin:
			self._logger ("backend status is {}, {} at {} LINE {}: {}".format (
				status, self._origin [3], self._origin [1], self._origin [2], self._origin [4][0].strip ()
			), "debug")			
		
	def wait (self, timeout = DEFAULT_TIMEOUT, reraise = True):
		self.getswait (timeout, reraise)
		self._cached_result = None
	
	def getwait (self, timeout = DEFAULT_TIMEOUT, reraise = False, cache = None, cache_if = (200,), wait = True):
		if self._cached_result is not None:
			return self._cached_result
		wait and self._wait (timeout)
		
		if len (self._results) > 1:
			raise ValueError("Multiple results, use getswait")		
		self._cached_result = self._results [0].get_result ()
		cache and self.cache (cache, cache_if)
		if self._cached_result.status != NORMAL:
			self._fail_log (self._cached_result.status)
			reraise and self._cached_result.reraise ()
		return self._cached_result
	
	def getswait (self, timeout = DEFAULT_TIMEOUT, reraise = False, cache = None, cache_if = (200,), wait = True):
		if self._cached_result is not None:
			return self._cached_result
		wait and self._wait (timeout)
		
		rss = [rs.get_result () for rs in self._results]
		for rs in rss:
			if rs.status == NORMAL:
				continue		
			self._fail_log (rs.status)
			reraise and rs.reraise ()			
		self._cached_result = Results (rss, ident = self._get_ident ())
		cache and self.cache (cache, cache_if)		
		return self._cached_result
	
	def _collect (self, rs):
		asyncon = self._requests [rs]
		status = rs.get_status ()			
		if status == REQFAIL:
			del self._requests [rs]
			self._results.append (rs)
			self._cluster.report (asyncon, True) # not asyncons' Fault
		elif not self._mapreduce and status == NETERR and self._retry < (self._numnodes - 1):
			self._logger ("Cluster Response Error, Switch To Another...", "fail")
			self._cluster.report (asyncon, False) # exception occured
			del self._requests [rs]
			self._retry += 1
			self._nodes = [None]
			self._request (*self._cached_request_args)
		elif status >= NETERR:
			del self._requests [rs]
			self._results.append (rs)
			if status == NETERR:
				self._cluster.report (asyncon, False) # exception occured
			else:	
				self._cluster.report (asyncon, True) # well-functioning
				rs.do_filter ()
		
		if not self._requests:
			if self._callback:
				self._do_callback (self._callback)
			else:
				self._cv.acquire ()
				self._cv.notifyAll ()
				self._cv.release ()					
	
	def _do_callback (self, callback):
		result = self._mapreduce and self.getswait (wait = False) or self.getwait (wait = False)
		tuple_cb (result, callback)		
		
	def set_callback (self, callback, reqid = None):
		if reqid is not None:
			self._meta ["__reqid"] = reqid
		if not self._requests:
			return self._do_callback (callback)			
		self._callback = callback
					
	def _or_throw (self, func, status, timeout, cache):
		try:
			response = func (timeout, reraise =True, cache = cache)
		except:
			raise exceptions.HTTPError (status, sys.exc_info ())
		return response
	
	def wait_or_throw (self, status, timeout = DEFAULT_TIMEOUT):
		return self._or_throw (self.wait, status, timeout, cache)
	
	def getwait_or_throw (self, status, timeout = DEFAULT_TIMEOUT, cache = None, cache_if = (200,)):
		return self._or_throw (self.getwait, status, timeout, cache)
	
	def getswait_or_throw (self, status, timeout = DEFAULT_TIMEOUT, cache = None, cache_if = (200,)):
		return self._or_throw (self.getswait, status, timeout, cache)
			

# Cluster Base Call ---------------------------------------

class _Method:
	def __init__(self, send, name):
		self.__send = send
		self.__name = name
		
	def __getattr__(self, name):
		return _Method(self.__send, "%s.%s" % (self.__name, name))
		
	def __call__(self, *args):
		return self.__send(self.__name, args)

		
class Proxy:
	def __init__ (self, __class, *args, **kargs):
		self.__class = __class
		self.__args = args
		self.__kargs = kargs		
	
	def __getattr__ (self, name):	  
		return _Method (self.__request, name)
	
	def __request (self, method, params):		
		cdc = self.__class (*self.__args, **self.__kargs)
		cdc._build_request (method, params)
		return cdc
			
class ClusterDistCallCreator:
	def __init__ (self, cluster, logger, cachesfs):
		self.cluster = cluster				
		self.logger = logger
		self.cachesfs = cachesfs		
	
	def __getattr__ (self, name):	
		return getattr (self.cluster, name)
		
	def Server (self, uri, params = None, reqtype="rpc", headers = None, auth = None, meta = None, use_cache = True, mapreduce = False, filter = None, callback = None, timeout = DEFAULT_TIMEOUT, caller = None):
		if type (headers) is list:
			h = {}
			for n, v in headers:
				h [n] = v
			headers = h
		
		if reqtype.endswith ("rpc"):
			return Proxy (ClusterDistCall, self.cluster, uri, params, reqtype, headers, auth, meta, use_cache, mapreduce, filter, callback, timeout, caller, self.cachesfs, self.logger)
		else:	
			return ClusterDistCall (self.cluster, uri, params, reqtype, headers, auth, meta, use_cache, mapreduce, filter, callback, timeout, caller, self.cachesfs, self.logger)
		
	
