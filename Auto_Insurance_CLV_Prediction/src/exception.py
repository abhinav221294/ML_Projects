# Importing required modules
import sys        # Used to get detailed exception information (traceback, file name, line number)
import logging    # Used for logging events (instead of print in production systems)


# Function to extract detailed error information
def error_message_details(error, error_detail: sys):
    """
    This function extracts detailed information about an exception:
    - File name where error occurred
    - Line number of error
    - Actual error message
    """

    # exc_info() returns a tuple:
    # (exception_type, exception_value, traceback_object)
    # We only need the traceback object, so ignore first two using _
    _, _, exec_tb = error_detail.exc_info()

    # Extracting the file name where the exception occurred
    file_name = exec_tb.tb_frame.f_code.co_filename

    # Creating a formatted error message including:
    # - File name
    # - Line number
    # - Original error message
    error_message = "Error occured in python script name [{0}] line number [{1}] message[{2}]".format(
        file_name,          # File in which error occurred
        exec_tb.tb_lineno,  # Line number where error occurred
        str(error)          # Original error message converted to string
    )

    # Returning the formatted error message
    return error_message


# Creating a custom exception class by inheriting from built-in Exception class
class CustomException(Exception):

    # Constructor method
    def __init__(self, error_message, error_detail: sys):

        # Calling parent class constructor to store original error
        super().__init__(error_message)

        # Storing the detailed formatted error message
        # This calls the function defined above
        self.error_message = error_message_details(
            error_message,
            error_detail=error_detail
        )

    # Overriding __str__ method so that when exception is printed,
    # it shows our custom detailed error message
    def __str__(self):
        return self.error_message


# This block runs only when this script is executed directly
if __name__ == "__main__":

    try:
        # Intentionally creating an error (division by zero)
        # This will raise ZeroDivisionError
        a = 1 / 0

    except Exception as e:
        # Logging that an error has occurred
        logging.info("logging has started!!")

        # Raising our custom exception instead of default Python exception
        # Passing:
        # - Original error (e)
        # - sys module to extract traceback details
        raise CustomException(e, sys)