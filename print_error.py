"""
File: print_error.py
Author: Jason, Brandon, Richard
Description:
    Provides error handling and logging for the Back End:
        - log_constraint_error()

    The system ensures all system errors are reported in "ERROR: <msg>" format. 
    It distinguishes between non-fatal transaction 
    errors and fatal system errors
"""

import sys 

def log_constraint_error(description, context, fatal=False):
    """
    Logs errors in the required format and exits if fatal.
    
    Args:
        message: The main error message/type
        description: Detailed error description
        context: File name (if fatal) or constraint type (if non-fatal)
        fatal: If True, treats as fatal error and exits program
    """
    if fatal:
        print(f"ERROR: Fatal error - File {context} - {description}")
        #exit system code here
        sys.exit(1)
    else:
        print(f"ERROR: {context}: {description}")
