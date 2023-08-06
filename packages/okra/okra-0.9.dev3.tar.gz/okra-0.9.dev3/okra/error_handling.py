""" Custom errors we can expect. 

References:
  https://docs.python.org/3/tutorial/errors.html
"""

class Error(Exception):
    """ Base class for exceptions in okra """
    pass

class NetworkError(Error):
    """ Exception raised for errors related to network requests

    :param expression: input expression in which the error occurred
    :param message: explanation of error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


    
