"""
File: read.py
Author: Jason, Brandon, Richard
Description:
    Handles the parsing and validation of the Master Bank Accounts File:
        - read_old_bank_accounts()
        - read_merged_transactions()

    Reads the fixed-length 42-character Master file and parses 
    it into a dictionary-based data structure. It validates 
    account numbers, names, statuses, balances, 
"""

def read_old_bank_accounts(file_path):
    """
    Reads and validates the Master Bank Accounts file format with plan type (SP/NP)
    and transaction counts. Returns a dictionary of accounts.
    """
    accounts = {}
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, 1):
            clean_line = line.rstrip('\n')
            
            # catch EOF marker before doing length checks
            if "END_OF_FILE" in clean_line:
                break
            
            # validate line length (45 characters for the new Master format)
            if len(clean_line) != 45:
                print(f"ERROR: Fatal error - Line {line_num}: Invalid length ({len(clean_line)} chars).")
                continue

            try:
                # extract fields 
                account_number = clean_line[0:5]
                name = clean_line[6:26].replace('_', ' ').strip()  
                status = clean_line[27]
                balance_str = clean_line[29:37] 
                transactions_str = clean_line[38:42]
                plan_type = clean_line[43:45]

                # validate account number
                if not account_number.isdigit():
                    print(f"ERROR: Fatal error - Line {line_num}: Account number must be 5 digits")
                    continue

                # validate status
                if status not in ('A', 'D'):
                    print(f"ERROR: Fatal error - Line {line_num}: Invalid status '{status}'")
                    continue

                # validate balance format
                if not balance_str.isdigit():
                    print(f"ERROR: Fatal error - Line {line_num}: Invalid balance format, must be numeric.")
                    continue

                # validate transaction count
                if not transactions_str.isdigit():
                    print(f"ERROR: Fatal error - Line {line_num}: Transaction count must be 4 digits")
                    continue

                # validate plan type
                if plan_type not in ('SP', 'NP'):
                    print(f"ERROR: Fatal error - Line {line_num}: Invalid plan type '{plan_type}'")
                    continue

                # convert values
                balance = float(balance_str)
                transactions = int(transactions_str)

                # save using account num as key
                accounts[account_number] = {
                    'account_number': account_number, 
                    'name': name,
                    'status': status,
                    'balance': balance,
                    'total_transactions': transactions,
                    'plan': plan_type
                }

            except Exception as e:
                print(f"ERROR: Fatal error - Line {line_num}: Unexpected error - {str(e)}")
                continue

    return accounts

def read_merged_transactions(file_path):
    """
    Reads the merged transaction file output by the Front End.
    Adjusts parsing for code 02 to capture the full destination account.
    """
    transactions = []
    
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, 1):
            clean_line = line.strip('\n') 
            
            if not clean_line.strip():
                continue
                
            # If it's a transfer, we need to ensure the line is long enough to hold the TO account
            # Transfer lines are usually longer (approx 45 chars) than standard lines (40 chars)
            clean_line = clean_line.ljust(45)
            
            try:
                code = clean_line[0:2]
                name = clean_line[3:23].strip() 
                account_number = clean_line[24:29].strip()

                amount_str = clean_line[30:38].replace('.', '')
                amount = float(amount_str) / 100 if amount_str.isdigit() else 0.0
                
                # parse account number if transfer
                if code == '02':
                    # get 5-digit destination account number 
                    misc = clean_line[39:44].strip()
                else:
                    # grab the 2-character company or misc code (
                    misc = clean_line[39:41].strip()
                
                transactions.append({
                    'code': code,
                    'name': name,
                    'account_number': account_number,
                    'amount': amount,
                    'misc': misc
                })
                
            except Exception as e:
                print(f"ERROR: Constraint Failure - Bad transaction format on line {line_num}")
                continue
                
    return transactions
