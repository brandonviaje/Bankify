"""
File: read.py
Author: Jason, Brandon, Richard
Description:
    Handles the parsing and validation of the Master Bank Accounts File:
        - read_old_bank_accounts()

    Reads the fixed-length 42-character Master file and parses 
    it into a dictionary-based data structure. It validates 
    account numbers, names, statuses, balances, 
"""

def read_old_bank_accounts(file_path):
    """
    Reads and validates the bank account file format with plan type (SP/NP)
    Returns list of accounts and prints fatal errors for invalid format
    """
    accounts = []
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, 1):
            clean_line = line.rstrip('\n')
            
            # Validate line length (now 42 chars to include plan type)
            if len(clean_line) != 42:
                print(f"ERROR: Fatal error - Line {line_num}: Invalid length ({len(clean_line)} chars, expected 45)")
                continue

            try:
                #Fixed updated slices for 42-char format
                # Extract fields with positional validation
                account_number = clean_line[0:5]
                name = clean_line[6:26].strip()  # 20 characters
                status = clean_line[27]
                balance_str = clean_line[29:37]  # 8 characters
                transactions_str = clean_line[38:42]  # 4 characters
                plan_type = 'NP'  # 2 characters (SP/NP)

                # Validate account number
                if not account_number.isdigit():
                    print(f"ERROR: Fatal error - Line {line_num}: Account number must be 5 digits")
                    continue

                # Validate status
                if status not in ('A', 'D'):
                    print(f"ERROR: Fatal error - Line {line_num}: Invalid status '{status}'. Must be 'A' or 'D'")
                    continue

                # Validate balance format with explicit negative check
                if balance_str[0] == '-':
                    print(f"ERROR: Fatal error - Line {line_num}: Negative balance detected: {balance_str}")
                    continue
                
                if (len(balance_str) != 8 or 
                    balance_str[5] != '.' or 
                    not balance_str[:5].isdigit() or 
                    not balance_str[6:].isdigit()):
                    print(f"ERROR: Fatal error - Line {line_num}: Invalid balance format. Expected XXXXX.XX, got {balance_str}")
                    continue

                # Validate transaction count
                if not transactions_str.isdigit():
                    print(f"ERROR: Fatal error - Line {line_num}: Transaction count must be 4 digits")
                    continue

                # Validate plan type
                if plan_type not in ('SP', 'NP'):
                    print(f"ERROR: Fatal error - Line {line_num}: Invalid plan type '{plan_type}'. Must be SP or NP")
                    continue

                # Convert values
                balance = float(balance_str)
                transactions = int(transactions_str)

                # Business rule validation
                if balance < 0:
                    print(f"ERROR: Fatal error - Line {line_num}: Negative balance detected")
                    continue
                if transactions < 0:
                    print(f"ERROR: Fatal error - Line {line_num}: Negative transaction not allowed")
                    continue

                accounts.append({
                    'account_number': account_number.lstrip('0') or '0',
                    'name': name.strip(),
                    'status': status,
                    'balance': balance,
                    'total_transactions': transactions,
                    'plan': plan_type
                })

            except Exception as e:
                print(f"ERROR: Fatal error - Line {line_num}: Unexpected error - {str(e)}")
                continue

    return accounts