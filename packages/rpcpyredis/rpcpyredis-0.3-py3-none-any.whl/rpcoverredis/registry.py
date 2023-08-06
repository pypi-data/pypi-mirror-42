import os
from rpcoverredis import rpcpyredis
import threading
import dill
import signal
import redis

redis_server = redis.Redis()
shared_dict = dict()
channel_list = []
server = None


def bind(name, remote_object):
    global shared_dict
    global redis_server
    try:
        shared_dict = redis_server.get('dict')
        if shared_dict is not None:
            shared_dict = dill.loads(shared_dict)
            print(shared_dict)
            shared_dict.update({name: remote_object})
            shared_dict = dill.dumps(shared_dict)
            redis_server.set('dict', shared_dict)
        else:
            shared = dict()
            shared.update({name:remote_object})
            shared_dict = shared
            shared_dict = dill.dumps(shared_dict)
            redis_server.set('dict', shared_dict)


        # if os.path.isfile(DB_FILE):
        #     fp = open(DB_FILE, "rb")
        #     fp.seek(0)
        #     shared_dict = dill.load(fp)
        #     shared_dict.update({name: remote_object})
        #     fp = open(DB_FILE, "wb")
        #     dill.dump(shared_dict, fp)
        # else:
        #     fp = open(DB_FILE, "wb")
        #     shared_dict.update({name: remote_object})
        #     print(shared_dict)
        #     dill.dump(shared_dict, fp)
    except Exception as e:
        pass


def lookup(name):
    shared = redis_server.get("dict")
    if shared is not None:
        shared = dill.loads(shared)
        print(shared)
        return shared[name]


        # fp = open(DB_FILE, "rb")
        # if os.stat(DB_FILE).st_size == 0:
        #     dill.dump(shared_dict, fp)
        # else:
        #     fp.seek(0)
        #     shared = dill.load(fp)
        #     return shared[name]


def expose(obj):
    global server
    bind(obj.__class__.__name__, obj)
    channel_list = create_channel_name(obj.__class__.__name__)
    if server is not None:
        server.update_channels(channel_list)


def create_channel_name(name):
    global channel_list
    channel_name = ''.join(['channel/', name])
    channel_list.append(channel_name)
    return channel_list

def handler(signum, frame):
    close_server()

def start_server(host="localhost", port=6379):
    global server
    global channel_list
    server = rpcpyredis.Server(host=host, port=port)
    server.update_channels(channel_list)
    signal.signal(signal.SIGINT, handler)
    t_server = threading.Thread(target=server.start)
    t_server.start()


def run_server(host="localhost", port=6379):
    global server
    global channel_list
    server = rpcpyredis.Server(host=host, port=port)
    print(channel_list)
    server.update_channels(channel_list)
    server.start()

def close_server():
    global server
    server.shutdown()

