from rpcoverredis import registry

class Calculator(object):


    def add(self,a,b, name):
        print(a)
        print(b)
        print(name)

    def testFunction(self,b):
        return registry.bind("ammar", b)

    def change_list(self, list):
        list.append(1)
        return list

    def manipulate_dict(self, dict):
        for key in dict:
            dict[key] = "Changed!"
        return dict

def main():


    registry.start_server()
    calculatorObject = Calculator()
    registry.expose(calculatorObject)


    print("Heh")


if __name__ == '__main__':
    main()