'''
Author: Richard
Description:
    Handles the parsing of the merged transaction file (.atf) and 
    conversion of each fixed-width transaction line into a Transaction object.
'''

from transaction import Transaction

def read_merged_transactions(path) -> list[Transaction]:

    """
    Reads the merged transaction (.atf) file and converts each
    fixed-width transaction line into a Transaction object.

    Parameters:
        path (str): Path to the merged transaction file.

    Returns:
        list[Transaction]: A list of Transaction objects parsed
        from the file. Reading stops when the end transaction
        record (code "00") is encountered.
    """
    transactions = []
    with open(path) as file:
        for line in file:
            txn = parse_txn_line(line)
            if txn.code == "00":  # End transaction record
                break
            transactions.append(txn)

    return transactions
    

def parse_txn_line(line) -> Transaction:

    """
    Parses a fixed-width transaction line and returns a
    Transaction object.

    Transaction line format:
        CC AAAAAAAAAAAAAAAAAAAA NNNNN SSSSSSSS MM

        CC  : Transaction code (2 characters)
        name: Account holder name (20 characters)
        NNNNN: Account number (5 characters)
        amount: Transaction amount (8 characters)
        misc: Miscellaneous field (2 characters)

    Parameters:
        line (str): A single line from the merged transaction file.

    Returns:
        Transaction: A Transaction object containing the parsed data.
    """

    code = line[0:2]                 
    name = line[3:23].strip()        
    account_number = line[24:29]     
    amount = line[30:38]             
    misc = line[39:41]        

    txn = Transaction(code, name, account_number, amount, misc)     

    return txn   

