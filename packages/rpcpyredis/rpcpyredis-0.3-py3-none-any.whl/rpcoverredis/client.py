from rpcoverredis import rpcpyredis


def main():


    # Create new client object, specifying redis server and channel
    remote_calculator = rpcpyredis.Proxy("Calculator")
   ## sokrates = rpcpyredis.Proxy("localhost", "Sokrates", port=6379)

    # Calling any method with client object
    result = remote_calculator.add(3,4, "ammar")
    ##sokr_result = sokrates.dummy_string()

    if "Exception" not in str(result):
        print(result)
        ##print(sokr_result)
        print("Data transmission successful.")
    else:
        print(result)



if __name__== '__main__':
    main()