import random
import string

import dill
import redis

from rpcoverredis import registry


class TooManyArgumentsException(Exception):
    """Raised when the number of argument is larger than expected"""
    pass


class InvalidArgument(Exception):
    pass


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class Proxy(object):

    def __init__(self, remote_object, host="localhost", **kwargs):
        self.host = host
        self.remote_object = remote_object
        if kwargs:
            if len(kwargs) > 1:
                raise TooManyArgumentsException(
                    "Only one argument(port) allowed.")

            else:
                if kwargs.get("port") is not None:
                    self.port = kwargs.get("port")
                else:
                    raise InvalidArgument()
        else:
            self.port = 6379  # default redis port

        self.redis_server = redis.Redis(host=self.host, port=self.port)
        self.pub_channel = "channel/" + str(remote_object)
        self.sub_channel = "channel/" + id_generator()

    def remote_call(self, method_name, *args, **kwargs):
        object_to_send = dict(function=method_name, params=args,
                              object_name=self.remote_object,
                              return_channel=self.sub_channel)
        rpc_request = dill.dumps(object_to_send)
        self.is_object_exposed(self.remote_object)
        subscribe_service = self.redis_server.pubsub()
        self.redis_server.publish(self.pub_channel, rpc_request)
        subscribe_service.subscribe(self.sub_channel)
        while True:
            message = subscribe_service.get_message(True)
            if message:
                raw_response = message['data']
                decoded_data = dill.loads(raw_response)
                if isinstance(decoded_data['response'], str) \
                        and decoded_data['response'].startswith("Exception"):
                    raise Exception
                else:
                    return decoded_data['response']

    def __getattr__(self, method_name):
        return Curry(self.remote_call, method_name)

    @staticmethod
    def is_object_exposed(remote_object):
        return registry.lookup(remote_object)


class Curry:

    def __init__(self, fun, *args, **kwargs):
        self.fun = fun
        self.pending = args[:]
        self.kwargs = kwargs.copy()

    def __call__(self, *args, **kwargs):
        if kwargs and self.kwargs:
            kw = self.kwargs.copy()
            kw.update(kwargs)
        else:
            kw = kwargs or self.kwargs
            return self.fun(*(self.pending + args), **kw)


class Server(object):

    def __init__(self, host, **kwargs):
        self.host = host
        if kwargs:
            if len(kwargs) > 1:
                raise TooManyArgumentsException
            else:
                if kwargs.get("port") is not None:
                    self.port = kwargs.get("port")
                else:
                    raise InvalidArgument
        else:
            self.port = 6379  # default redis port

        self.redis_server = redis.Redis(host=self.host, port=self.port)
        self.pubsub = self.redis_server.pubsub()

    def execute_code(self, unwrapped_request, remote_object):
        d = None
        counter = 0
        l = locals()
        list_of_params = []
        object = remote_object
        args = unwrapped_request["params"]
        for i in args:
            if hasattr(i, '__dict__'):
                l["object" + str(counter)] = i
                list_of_params.append('object' + str(counter))
                counter += 1
            elif isinstance(i, str):
                list_of_params.append('"' + i + '"')
            else:
                list_of_params.append('' + str(i))
        final_string = ','.join(list_of_params)
        method_name = (unwrapped_request["function"])
        calling_function = '%s(%s)' % (method_name, final_string)
        final_function_call = 'self.result = object.' + calling_function
        exec(final_function_call)
        return self.result

    def update_channels(self, channels):
        for i in channels:
            self.pubsub.subscribe(i)

    def handle_request(self, unwrapped_request):
        last_sent_response = None
        object_to_lookup_for = unwrapped_request['object_name']
        remote_object = registry.lookup(object_to_lookup_for)
        return_channel = unwrapped_request['return_channel']
        try:
            rpc_response = self.execute_code(unwrapped_request, remote_object)
            if rpc_response is None:
                rpc_response = "Operation successfully executed"

            rpc_response_formatted = dict(response=rpc_response)
            response_to_be_sent = dill.dumps(rpc_response_formatted)
            print(return_channel)
            self.redis_server.publish(return_channel,
                                      response_to_be_sent)
            last_sent_response = rpc_response_formatted
            return last_sent_response
        except Exception as e:
            rpc_response = "Exception"
            rpc_response_formatted = dict(response=rpc_response)
            response_to_be_sent = dill.dumps(rpc_response_formatted)
            self.redis_server.publish(return_channel, response_to_be_sent)
            last_sent_response = rpc_response_formatted
            return last_sent_response

    def start(self):
        print("Waiting for connection...")
        response = None
        while True:
            if self.pubsub.channels:
                try:
                    message = self.pubsub.get_message(True)
                    if message:
                        raw_request = message['data']  # Get data from message
                        unwrapped_request = dill.loads(raw_request)
                        if unwrapped_request != response:
                            print("Handling the message...")
                            response = self.handle_request(unwrapped_request)
                except Exception as e:
                    break

    def shutdown(self):
        try:
            self.pubsub.close()
        except AttributeError:
            return