# A caching engine using S3, requires an AWS account
# David Arthur, 2009
# http://cloudcached.com

import boto
from cPickle import loads, dumps
import datetime,hashlib

class Client:
    "Client interface to CloudCached"
    _STR     = 0
    _INT     = 1
    _LONG    = 2
    _COMPLEX = 4
    _FLOAT   = 5
    _PICKLE  = 6
    def __init__(self,aws_access_key_id,aws_secret_access_key):
        "Create S3 connections"
        self.__s3_conn = boto.connect_s3(aws_access_key_id,aws_secret_access_key)
        self.__bucket = self.__s3_conn.get_bucket("cloudcache")

    def _dumpObject(self,v):
        "Convert the requested object to a string and store determine the type"
        flag = Client._STR
        if isinstance(v,basestring):
            pass
        elif isinstance(v,int):
            flag = Client._INT
            v = str(v)
        elif isinstance(v,long):
            flag = Client._LONG
            v = str(v)
        elif isinstance(v,complex):
            flag = Client._COMPLEX
            v = str(v)
        elif isinstance(v,float):
            flag = Client._FLOAT
            v = str(v)
        else:
            flag = Client._PICKLE
            v = dumps(v,-1)
        return v,flag

    def _loadObject(self,v,flag):
        "Given a string and a type, convert the object back into its original type"
        if flag == Client._STR:
            pass
        elif flag == Client._INT:
            v = int(v)
        elif flag == Client._LONG:
            v = long(v)
        elif flag == Client._COMPLEX:
            v = complex(v)
        elif flag == Client._FLOAT:
            v = float(v)
        else:
            v = loads(v)
        return v

    def get(self,k):
        "Retrieve an object given its key"
        s3_key = self.__bucket.get_key(k)
        if not s3_key:
            return None
        now = datetime.datetime.today().isoformat()
        if s3_key.metadata.has_key('expires') and s3_key.metadata['expires'] <= now:
            return None
        v = s3_key.get_contents_as_string()
        flag = int(s3_key.metadata['type'])
        v = self._loadObject(v,flag)
        return v

    def put(self, key, value, time_to_expire=3600, replace=False):
        "Send an object and save it to a given key for a certain amount of time"
        value,flag = self._dumpObject(value)
        s3_key = self.__bucket.new_key(key)
        if s3_key.exists() and replace is False:
            return True
        now = datetime.datetime.today()
        expires = (now+datetime.timedelta(seconds=time_to_expire)).isoformat()
        s3_key.set_metadata('expires',expires)
        s3_key.set_metadata('type',str(flag))
        s3_key.set_contents_from_string(value, replace=True) 
        if s3_key.md5 == hashlib.md5(value).hexdigest():
            return True
        else:
            return False
        
    def update(self, key, value, time_to_expire=3600):
        "Replace an existing object given its key, or create one if it doesn't exist"
        return self.put(key,value,time_to_expire,True)

    def delete(self, key):
        "Delete an object given its key"
        s3_key = self.__bucket.get_key(k)
        if not s3_key:
            return None
        s3_key.delete()
        return True
