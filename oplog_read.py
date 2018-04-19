import time
import pymongo
from pymongo import MongoClient
from pymongo.cursor import CursorType

c = pymongo.MongoClient("mongodb://localhost:27017/")

# Uncomment this for master/slave.
#oplog = c.local.oplog['$main']
# Uncomment this for replica sets.
oplog = c.local.oplog.rs
first = next(oplog.find().sort('$natural', pymongo.DESCENDING).limit(-1))
ins = 'i'
namep = 'manoj'
ts = first['ts']
while True:
    cursor = oplog.find({'ts': {'$gt': ts}}, cursor_type=CursorType.TAILABLE_AWAIT, oplog_replay=True)
    while cursor.alive:
        for doc in cursor:
            if ins in doc['op']:
                data = doc['o']
                if namep in data['name']:
                    print(data)
                
	    # Work with doc here
            ts = doc['ts']