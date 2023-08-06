import os
import sys
from rpcoverredis import rpcpyredis
import threading
import dill
import atexit
import pkg_resources


DATA_PATH = pkg_resources.resource_filename(__package__, 'resources/')
DB_FILE = pkg_resources.resource_filename(__package__, 'resources/shared.pkl')
DB_SERVER = pkg_resources.resource_filename(__package__, 'resources/server.pkl')


shared_dict = dict()
channel_list = []
server = None


def bind(name, remote_object):
    global shared_dict
    try:
        if os.path.isfile(DB_FILE):
            fp = open(DB_FILE, "rb")
            fp.seek(0)
            shared_dict = dill.load(fp)
            shared_dict.update({name: remote_object})
            fp = open(DB_FILE, "wb")
            dill.dump(shared_dict, fp)
        else:
            fp = open(DB_FILE, "wb")
            shared_dict.update({name: remote_object})
            print(shared_dict)
            dill.dump(shared_dict, fp)
    except Exception as e:
        pass
    finally:
        fp.close()

def lookup(name):
    try:
        fp = open(DB_FILE, "rb")
        if os.stat(DB_FILE).st_size == 0:
            dill.dump(shared_dict, fp)
        else:
            fp.seek(0)
            shared = dill.load(fp)
            return shared[name]
    except Exception as e:
        print("Exception caught: " + str(e))


def expose(obj):
    global server
    bind(obj.__class__.__name__, obj)
    channel_list = create_channel_name(obj.__class__.__name__)
    print(type(channel_list))
    if server is None:
        raise ValueError
    server.update_channels(channel_list)


def create_channel_name(name):
    global channel_list
    channel_name = ''.join(['channel/', name])
    channel_list.append(channel_name)
    return channel_list

def shutdown(thread, event):
      try:
        print('Event running.clear()')
        event.clear()
        print('Wait until Thread is terminating')
        thread.join()
        print("EXIT __main__")
      except KeyboardInterrupt:
            pass
def start_server(host="localhost", port=6379):
    global server
    try:
        if not os.path.isfile(DB_SERVER):
            fp = open(DB_SERVER, "wb")
            server = rpcpyredis.Server(host=host, port=port)
            dill.dump(server, fp)
        else:
            fp = open(DB_SERVER, "rb")
            fp.seek(0)
            server = dill.load(fp)
            print("Server is already up and running")
        event = threading.Event()
        event.set()
        t_server = threading.Thread(target=server.start, args=(event,))
        t_server.start()
        atexit.register(shutdown, thread=t_server, event=event)
    except (KeyboardInterrupt, SystemExit):
        print('Event running.clear()')
        event.clear()
        print('Wait until Thread is terminating')
        t_server.join()
        print("EXIT __main__")

    finally:
        fp.close()

