import sys 

import redis

# Contains functions that stores the mapping from document IDs to URLs (originally in a text document) in redis.
# The flask application, however, continues to use the mapping from the text document and not redis.

URL_DOCID_PATH = 'ClueWeb12_B13_DocID_To_URL.txt'  # Change this path as necessary.


def save_hash(r, n):
    """Inserts n rows into redis using xxx as hash keys."""
    with open(URL_DOCID_PATH, 'r') as f:
        i = 0
        for line in f:
            if i >= n:
                break
            i += 1

            num, url = map(lambda x: x.strip(), line.split(',', 1))
            num = num.split('-', 1)[1]  # Strip `clueweb12-` from all keys to save space.
            hash_key, record_num = num.rsplit('-', 1)        

            r.hset(hash_key, record_num, url)


def save_redis(r, n):
    """Inserts n rows into  redis."""
    with open(URL_DOCID_PATH, 'r') as f:
        i = 0
        for line in f:
            if i >= n:
                break
            i += 1  

            num, url = map(lambda x: x.strip(), line.split(',', 1))
            num = num.split('-', 1)[1]  # Strip `clueweb12-` from all keys to save space.
            r.set(num, url)

def reset_redis(r):
    """Deletes all keys from Redis."""
    keys = r.keys()
    if len(keys) > 0:
        r.delete(*keys)


if __name__ == '__main__':
    # Gets command line argument for number of rows to insert into redis. Defaults to 5000.
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    else:
        n = 5000

    r = redis.Redis()
    # Compares the memory used by redis with and without hashes.
    for func in [save_redis, save_hash]:
        func(r, n)
        print('dbsize:', r.dbsize())
        for k, v in r.info('Memory').items():
            if k.endswith('human'):
                print(k, v)
        reset_redis(r)
