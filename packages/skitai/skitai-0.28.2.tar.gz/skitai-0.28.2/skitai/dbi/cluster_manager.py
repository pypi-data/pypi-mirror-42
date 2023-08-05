from skitai.rpc import cluster_manager
from aquests.dbapi import asynpsycopg2, synsqlite3, asynredis, asynmongo
from skitai import DB_PGSQL, DB_SQLITE3, DB_REDIS, DB_MONGODB

class ClusterManager (cluster_manager.ClusterManager):
    backend_keep_alive = 1200
    backend = True
    
    def __init__ (self, name, cluster, dbtype = DB_PGSQL, access = [], logger = None):
        self.dbtype = dbtype
        self._cache = []
        cluster_manager.ClusterManager.__init__ (self, name, cluster, 0, access, logger)
            
    def match (self, request):
        return False # not serverd by url
    
    def create_asyncon (self, member):        
        if self.dbtype == DB_SQLITE3:
            asyncon = synsqlite3.SynConnect (member, None, self.lock, self.logger)
            nodeid = member
            self._cache.append (((member, 0), "", ("", "")))
        
        else:
            if member.find ("@") != -1:
                auth, netloc = self.parse_member (member)
                try:
                    server, db = netloc.split ("/", 1)
                except ValueError:
                    server, db = netloc, ""
                    
            else:                
                db, user, passwd = "", "", ""
                args = member.split ("/", 3)
                if len (args) == 4:     server, db, user, passwd = args
                elif len (args) == 3:     server, db, user = args
                elif len (args) == 2:     server, db = args        
                else: server = args [0]
                auth = (user, passwd)
                
            try: 
                host, port = server.split (":", 1)
                server = (host, int (port))
            except ValueError: 
                server = (server, 5432)
            
            if self.dbtype == DB_PGSQL:
                conn_class = asynpsycopg2.AsynConnect
            elif self.dbtype == DB_REDIS:
                conn_class = asynredis.AsynConnect
            elif self.dbtype == DB_MONGODB:
                conn_class = asynmongo.AsynConnect    
            else:
                raise TypeError ("Unknown DB type: %s" % self.dbtype)
            
            asyncon = conn_class (server, (db, auth), self.lock, self.logger)    
            self.backend and asyncon.set_backend (self.backend_keep_alive)            
            nodeid = server
            self._cache.append ((server, db, auth))
                
        return nodeid, asyncon # nodeid, asyncon
    
    def get_endpoints (self):
        return make_endpoints (self.dbtype, self._cache)
        

def make_endpoints (dbtype, from_list):
        import sqlite3
        import psycopg2
        import redis
        import pymongo
        
        endpoints = []        
        for server, db, auth in from_list:
            user, password = "", ""
            if auth:
                if len (auth) == 2:
                    user, password = auth
                else:
                    user = auth [0]    
            if isinstance (server, str):
                try: 
                    host, port = server.split (":", 1)
                except ValueError:
                    host, port = server, None
            else:
                 host, port = server
            
            kargs = {}
            if port: kargs ["port"] = port
            if password: kargs ["password"] = password
            
            if dbtype == DB_SQLITE3:
                conn = sqlite3.connect (host)
            elif dbtype == DB_PGSQL:
                if user: kargs ["user"] = user
                conn = psycopg2.connect (host = host, database = db, **kargs)
            elif dbtype == DB_REDIS:
                conn = redis.Redis (host = host, port = port, db = db)
            elif dbtype == DB_MONGODB:
                if user: kargs ["username"] = user
                conn = pymongo.MongoClient (host = host, **kargs)
            endpoints.append (conn)
        return endpoints

       
              