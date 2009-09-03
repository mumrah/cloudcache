from cloudcache import cached
import nose
from ConfigParser import ConfigParser
config = ConfigParser()
config.read('my.conf')

cached.aws_access_key_id = config.get('aws','access_key_id')
cached.aws_secret_access_key = config.get('aws','secret_access_key')

#
# Yea, so this doesn't really test anything. My bad.
#

@cached(expires=60)
def testing(a,b,c):
    return a+b+c

print testing(1,2,3)
print testing(2,3,4)
