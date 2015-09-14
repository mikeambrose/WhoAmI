import apiRequest

def APITests(v=False):

    #tests basic calls with the 10 second restriction
    API = apiRequest.APICalls(open('apikey.txt').read())
    test(API._callCheck(True) == 0, "can call with no queue",v)
    for i in range(9):
        API._addCall()
    test(len(API._calls) == 9, "adding calls correctly",v)
    test(API._callCheck(True) == 0, "can call with an almost full queue",v)
    API._addCall()
    test(API._callCheck(True) != 0, "can't call with a full queue",v)


def test(test,text,v):
    if not test:
        print "{0} -- FAILURE".format(text)
        exit()
    elif test and v:
        print "{0} -- SUCCESS".format(text)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', dest='verbose', action='store_const', const=True, default=False)
    args = parser.parse_args()
    APITests(args.verbose)
