# Import the sys module to access exception information
import sys

# Function to create a detailed error message
def error_message_detail(error, error_details: sys):
    """
    Returns a formatted error message with file name, line number, and exception info.

    Parameters:
    error : Exception object
        The actual exception that was caught.
    error_details : sys module
        The sys module is used to get current exception info.

    Returns:
    str : Formatted error message
    """
    
    # sys.exc_info() returns a tuple of (type, value, traceback) of the last exception
    # We only need the traceback object, so unpack it as (_, _, exc_tb)
    _, _, exc_tb = error_details.exc_info()
    
    # Get the file name where the exception occurred from the traceback
    file_name = exc_tb.tb_frame.f_code.co_filename
    
    # Format the error message with filename, line number, and original error message
    error_message = "Error occured in python script name [{0}] line number [{1}] error message[{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)
    )

    # Return the formatted message
    return error_message


# Custom exception class to provide detailed exception messages
class CustomException(Exception):
    """
    Custom Exception class that extends Python's built-in Exception.
    Stores detailed information about the exception including file name and line number.
    """
    
    def __init__(self, error_message, error_detail: sys):
        """
        Initializes the CustomException instance.

        Parameters:
        error_message : str
            The original exception message.
        error_detail : sys module
            The sys module, used to get traceback information.
        """
        # Call the parent Exception class constructor
        super().__init__(error_message)
        
        # Generate and store the detailed error message
        self.error_message = error_message_detail(error=error_message, error_details=error_detail)

    def __str__(self):
        """
        Overrides the default string representation of the exception.
        Returns the detailed error message when the exception is printed.
        """
        return self.error_message
