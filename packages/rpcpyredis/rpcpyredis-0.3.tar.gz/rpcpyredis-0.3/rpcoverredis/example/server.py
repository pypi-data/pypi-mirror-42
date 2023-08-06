from rpcoverredis import registry
import sys

class Calculator(object):


    def add(self,a,b, name):
        raise Exception

    def testFunction(self):
        return 23

    def change_list(self, list):
        list.append(1)
        return list

    def manipulate_dict(self, dict):
        for key in dict:
            dict[key] = "Changed!"
        return dict

class Mobile:

    def __init__(self):
        pass

def shutdown():
    registry.close_server()

def main():
    calculatorObject = Calculator()
    registry.expose(calculatorObject)

    registry.start_server()

    mobile = Mobile()
    registry.expose(mobile)



    print("YEAAAAAAAAAAAAAAAAAAA")


if __name__ == '__main__':
    main()