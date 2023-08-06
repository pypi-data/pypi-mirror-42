class BrokerHelpersException(Exception):

    def __init__(self, msg = "Unexpected error in BrokerHelpers", innerException:Exception = None):
        self.msg = msg
        self.innerException = innerException

    def __str__(self):
        return "BrokerHelpers exception: {msg}, inner exception: {innerException}".format(msg = self.msg, innerException = str(self.innerException))