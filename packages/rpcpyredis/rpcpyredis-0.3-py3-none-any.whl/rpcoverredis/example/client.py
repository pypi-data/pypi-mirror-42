from rpcoverredis import rpcpyredis


def main():


    # Create new client object, specifying redis server and channel
    remote_calculator = rpcpyredis.Proxy("Calculator")
   ## sokrates = rpcpyredis.Proxy("localhost", "Sokrates", port=6379)

   # Calling any method with client object
    result = remote_calculator.testFunction()
    ##sokr_result = sokrates.dummy_string()


    print("Data transmission successful.")



if __name__== '__main__':
    main()