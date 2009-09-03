from cloudcache import Client
from cPickle import loads,dumps
import datetime
import nose

class DummyClass:
    def __init__(self):
        self.foo  = "bar"
        self.spam = "eggs"
    def __repr__(self):
        return "%s %s" % (self.foo,self.spam)

class TestCloudCache(Client):
    def __init__(self):
        pass
    def test_str(self):
        obj = "Testing"
        v,flag = self._dumpObject(obj)
        assert v == str(obj)
        assert flag == Client._STR
    def test_unicode(self):
        obj = u"Testing"
        v,flag = self._dumpObject(obj)
        assert v == str(obj)
        assert flag == Client._STR
    def test_int(self):
        obj = 1234
        v,flag = self._dumpObject(obj)
        assert v == str(obj)
        assert flag == Client._INT
    def test_long(self):
        obj = 2**33
        v,flag = self._dumpObject(obj)
        assert v == str(obj)
        assert flag == Client._LONG
    def test_float(self):
        obj = 1.234
        v,flag = self._dumpObject(obj)
        assert v == str(obj)
        assert flag == Client._FLOAT
    def test_complex(self):
        obj = complex(1,2)
        v,flag = self._dumpObject(obj)
        assert v == str(obj)
        assert flag == Client._COMPLEX
    def test_bool(self):
        obj = True 
        v,flag = self._dumpObject(obj)
        assert v == str(obj)
        assert flag == Client._INT
    def test_dict(self):
        obj = {'foo':"bar"}
        v,flag = self._dumpObject(obj)
        assert v == dumps(obj,-1)
        assert flag == Client._PICKLE
    def test_user_object(self):
        obj = DummyClass() 
        v,flag = self._dumpObject(obj)
        assert v == dumps(obj,-1)
        assert flag == Client._PICKLE
        obj = loads(v)
        assert obj.foo == "bar"
        assert obj.spam == "eggs"
        assert str(obj) == "bar eggs"
    def test_lib_object(self):
        obj = datetime.datetime.today()
        v,flag = self._dumpObject(obj)
        assert v == dumps(obj,-1)
        assert flag == Client._PICKLE
        obj = loads(v)
        assert type(obj) == datetime.datetime

        

