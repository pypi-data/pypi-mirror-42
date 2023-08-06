import redis
import dill
from rpcoverredis import registry

class TooManyArgumentsException(Exception):
    """Raised when the number of argument is larger than expected"""
    pass

class InvalidArgument(Exception):
    pass



class Proxy(object):

    def __init__(self, remote_object, host="localhost", **kwargs):
        self.host = host
        self.remote_object = remote_object
        if kwargs:
            try:
                if len(kwargs) > 1:
                    raise TooManyArgumentsException("Only one argument(port) allowed.")

                else:
                    if kwargs.get("port") is not None:
                        self.port = kwargs.get("port")
                    else:
                        raise InvalidArgument("Argument called port expected but was: " + str(kwargs))
            except TooManyArgumentsException:
                print("Only one argument(port) allowed")
            except InvalidArgument:
                print("Argument called port expected but was: " + str(kwargs))
        else:
            self.port = 6379  # default redis port

        self.redis_server = redis.Redis(host=self.host, port=self.port)
        self.channel = "channel/" + str(remote_object)

    def remote_call(self, method_name, *args, **kwargs):
        try:
            object_to_sent = dict(function=method_name, params=args, object_name=self.remote_object)
            rpc_request = dill.dumps(object_to_sent)
            is_exposed = self.is_object_exposed(self.remote_object)
            subscribe_service = self.redis_server.pubsub()
            self.redis_server.publish(self.channel, rpc_request)
            subscribe_service.subscribe(self.channel)
            while True:
                message = subscribe_service.get_message(True)
                if message:
                    raw_response = message['data']
                    decoded_data = dill.loads(raw_response)
                    return decoded_data['response']
        except Exception as e:
            pass

    def __getattr__(self, method_name):
        return curry(self.remote_call, method_name)

    def is_object_exposed(self, remote_object):
        return registry.lookup(remote_object)

class curry:

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
            try:
                if len(kwargs) > 1:
                    raise TooManyArgumentsException
                else:
                    if kwargs.get("port") is not None:
                        self.port = kwargs.get("port")
                    else:
                        raise InvalidArgument
            except TooManyArgumentsException:
                print("Only one argument(port) allowed.")
            except InvalidArgument:
                print("Argument called port expected but was: " + str(kwargs))

        else:
            self.port = 6379  # default redis port

        self.redis_server = redis.Redis(host=self.host, port=self.port)
        self.pubsub = self.redis_server.pubsub()

    def execute_code(self, unwrapped_request, class_type):
        d = None
        counter = 0
        l = locals()
        list_of_params = []
        object = class_type
        args = unwrapped_request["params"]
        for i in args:
            if hasattr(i, '__dict__'):
                l["object" + str(counter)] = i
                list_of_params.append('object' + str(counter))
                counter += 1
            elif isinstance(i,str):
                list_of_params.append('"' + i + '"')
            else:
                list_of_params.append('' + str(i))
        final_string = ','.join(list_of_params)
        method_name = (unwrapped_request["function"])
        calling_function = '%s(%s)' % (method_name, final_string)
        final_function_call = 'self.result = object.' + calling_function
        exec(final_function_call)
        return self.result


    # def make_function(self, request):
    #     args = request["params"]
    #     arguments = ",".join((str(i) for i in args))
    #     method_name = (request["function"])
    #     return '%s(%s)' % (method_name, arguments)


    def update_channels(self, channels):
        for i in channels:
            self.pubsub.subscribe(i)


    def start(self, event):
        # Listening on a certain channel(s)
        last_sent_response = ''
        print("Waiting for connection...")
        try:
            while True:
                if event.is_set():
                    if self.pubsub.channels:
                        ##print("It enters here")
                        message = self.pubsub.get_message(True)
                        if message:
                            try:
                                raw_request = message['data']  # Get data from message
                                unwrapped_request = dill.loads(raw_request)
                                if unwrapped_request != last_sent_response:
                                    print("Handling the message...")
                                    print(raw_request)
                                    object_to_lookup_for = unwrapped_request['object_name']
                                    class_type = registry.lookup(object_to_lookup_for)
                                    # calling_function = self.make_function(unwrapped_request)
                                    rpc_response = self.execute_code(unwrapped_request, class_type)
                                    if (rpc_response is None):
                                        rpc_response = "Operaction successfully executed"
                                    rpc_response_formatted = dict(response=rpc_response)
                                    response_to_be_sent = dill.dumps(rpc_response_formatted)
                                    self.redis_server.publish("channel/" + str(object_to_lookup_for), response_to_be_sent)
                                    last_sent_response = rpc_response_formatted
                            except Exception as e:
                                rpc_response = "Exception occurred: " + str(e)
                                rpc_response_formatted = dict(response=rpc_response)
                                response_to_be_sent = dill.dumps(rpc_response_formatted)
                                self.redis_server.publish("channel/" + str(object_to_lookup_for), response_to_be_sent)
                                last_sent_response = rpc_response_formatted
                else:
                    return
        except Exception as e:
            print(str(e))
            self.pubsub.close()  # shutting down everything, including disconnecting and cleaning out the channels/patterns dicts.



