import random
import time
import hashlib

data = str(random.getrandbits(100)) + str(time.time())
hash = hashlib.sha256(data).hexdigest()

print hash
