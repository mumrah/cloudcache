# -*- coding: utf-8 -*-
import sys
sys.path.append(".")
import random,hashlib,time
from cloudcache import Client
from ConfigParser import ConfigParser
config = ConfigParser()
config.read('my.conf')

def lrange(count):
    i = 0
    while i < count:
        yield i
        i+=1

class TestCloudCache:
    def __init__(self):
        self.client = Client(config.get('aws','access_key_id'),
                config.get('aws','secret_access_key') )
    def rand_data(self,count=100):
        return "".join([chr(random.randint(48,122)) for i in lrange(count)])
    def rand_name(self):
        return hashlib.md5("%s"%time.time()).hexdigest()
    def get_key(self,key,data_in):
        data_out = self.client.get(key)
        assert data_out == data_in
    def test_string(self):
        for size in (0,1,2,3,4,5,10,15,20):
            data_in = self.rand_data(2**size)
            key = self.rand_name()
            assert self.client.put(key,data_in,60,True) == True
            yield self.get_key, key, data_in 
    def test_int(self):
        data_in = random.randint(0,2**32) 
        key = self.rand_name()
        assert self.client.put(key,data_in,60,True) == True
        yield self.get_key, key, data_in
    def test_long(self):
        data_in = random.randint(2**32,2**64) 
        key = self.rand_name()
        assert self.client.put(key,data_in,60,True) == True
        yield self.get_key, key, data_in
    def test_dict(self):
        data_in = {} 
        for i in range(10):
            data_in[self.rand_name()] = self.rand_data(512)
        key = self.rand_name()
        assert self.client.put(key,data_in,60,True) == True
        yield self.get_key, key, data_in
    def test_unicode(self):
        data_in = "¡Ünîcø∂é, bítçh!"
        key = self.rand_name()
        assert self.client.put(key,data_in,60,True) == True
        yield self.get_key, key, data_in
    def test_timeout(self):
        data_in = "Some Awesome Data"
        key = self.rand_name()
        assert self.client.put(key,data_in,1,True) == True
        time.sleep(2)
        data_out = self.client.get(key)
        assert data_out == None
    def test_replace_false(self):
        data_in = "Some Awesome Data"
        key = self.rand_name()
        assert self.client.put(key,data_in,60,True) == True
        data_in1 = "Some other data"
        assert self.client.put(key,data_in1,60,False) == True
        data_out = self.client.get(key)
        assert data_out == data_in
    def test_replace_true(self):
        data_in = "Some Awesome Data"
        key = self.rand_name()
        assert self.client.put(key,data_in,60,True) == True
        data_in1 = "Some other data"
        assert self.client.put(key,data_in1,60,True) == True
        data_out = self.client.get(key)
        assert data_out == data_in1


#from httplib2 import Http
#class test_CRUD:
#    def __init__(self):
#        self.http = Http()
#    def test_put(self):
#        data = "Testing 1 2 3"
#        resp = http.request("http://localhost:8080","PUT",body="Testing",headers={"Content-type":"text/plain","Content-Length":"7"})
