if __name__ == "__main__":
    print("This is a module that is imported by 'uGecko.py'. Don't run it directly.")
    exit()
else:
    pass

class NoIpEnteredException(Exception): pass
class InvalidIpAddressException(Exception): pass
class ConnectionIsAlreadyInProgressException(Exception): pass
class ConnectionIsNotInProgressException(Exception): pass
class ConnectionErrorException(Exception): pass
class InvalidMemoryAreaException(Exception): pass
class InvalidLengthException(Exception): pass
class ReadMemoryException(Exception): pass
class TooManyArgumentsException(Exception): pass
