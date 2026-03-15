'''
Author: Richard
Description:
    Defines the Transaction class, which represents a single transaction
    parsed from the merged transaction file (.atf). This class serves as
    a structured data container for transaction details, facilitating
    easier processing and manipulation of transaction data in the backend.
'''
class Transaction:

    def __init__(self, code, name, account_number, amount, misc):
        self.code = code
        self.name = name
        self.account_number = account_number
        self.amount = amount
        self.misc = misc

    