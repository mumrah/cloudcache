# -*- coding: utf-8 -*-
import sys
sys.path.append(".")
import random,hashlib,time,re
from cloudcache import Client
from collections import defaultdict
from ConfigParser import ConfigParser
config = ConfigParser()
config.read('my.conf')

class CloudCacheBenchmark:
    """
    Test runner for CloudCached benchmarks

    Test should be named 'test_%method_%name' where the method is one of
    get, put, delete, update. Any custom methods should be added to
    self.test_types and can be run manually with the run_tests method.
    """
    def __init__(self):
        self.client = Client(config.get('aws','access_key_id'),
                config.get('aws','secret_access_key') )
        self.key = hashlib.md5("CloudCacheTest").hexdigest()
        self.tests = defaultdict(list)
        self.test_types = ('put','get')
        self.timings = defaultdict(tuple)
        self.__collect_tests()
    def __collect_tests(self):
        # Collect tests
        for method in dir(self):
            if method[0:5] == "test_":
                match = re.match(r'test_(\w+?)_.*',method)
                if match and match.group(1) in self.test_types:
                    self.tests[match.group(1)] += [method]
    def __run_test(self,test,n):
        test_base =  test[test.find("_",5)+1:]
        print "Running %s (%s iterations)" % (test,n),
        t1 = time.time()
        for i in range(n):
            print ".",
            key = "%s_%s_%s" % (self.key,test_base,i)
            getattr(self,test)(key)
        t2 = time.time()
        print ""
        self.timings[test] = ( (t2-t1)/n, (t2-t1) )
    def run_tests(self,method=None,n=10):
        if method:
            for test in self.tests[method]:
                self.__run_test(test,n)
        # Run PUT tests first
        for test in self.tests['put']:
            self.__run_test(test,n) 
        # Then GETs
        for test in self.tests['get']:
            self.__run_test(test,n) 
    def test_put_small_string(self,key):
        data = "1"*32
        self.client.put(key,data,3600,True)
    #def test_put_large_string(self,key):
    #    data = "1"*524288
    #    self.client.put(key,data,3600,True)
    def test_put_int(self,key):
        data = random.randint(0,2**30)
        self.client.put(key,data,3600,True)
    def test_get_small_string(self,key):
        self.client.get(key)
    #def test_get_large_string(self,key):
    #    self.client.get(key)
    def test_get_int(self,key):
        self.client.get(key)

if __name__ == "__main__":
    test = CloudCacheBenchmark()
    test.run_tests()
    print "Test".rjust(30),"\tAverage (s)\tTotal (s)"
    print "-"*80
    for test,timing in test.timings.items():
        print "%s\t%s\t%s" % (test.rjust(30),timing[0],timing[1])
