from accounts import BankAccount
import re

r"""
Regex Account Pattern:
(\d{5})     : account number
_           : underscore padding before  name
(.+?)       : account holder name
_+          : underscore padding before status
([AD])      : account status
_           : underscore padding before balance
(\d{8})     : account balance
"""
account_pattern = r"(\d{5})_(.+?)_+([AD])_(\d{8})"

def read_bank_accounts(file_path):
    accounts = {}
    try:
        # open file
        with open(file_path, "r") as file:
            # read accounts line by line
            for line in file:          
                line = line.rstrip()    # remove whitespaces            

                # if we reached EOF stop reading
                if line == "END_OF_FILE": 
                    break                        

                match = re.match(account_pattern, line)                       # check if line matches regex pattern
                
                if not match:                                                 # skip misformatted lines
                    continue                                        

                number, name, status, balance = match.groups()                # get account attributes
                balance = float(balance)                                      # cast balance to float type
                accounts[number] = BankAccount(number, name, status, balance) # set account number to bank account object
    except FileNotFoundError:
        print(f"File {file_path} not found")
    except Exception as e:
        print(f"ERROR: {e}")
        
    return accounts # return accounts
