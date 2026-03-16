"""
File: backend_processor.py
Author: Jason, Richard, Brandon, Moksh
Description:
    Handles core Back End business logic and account updates:
        - process_transactions()
        - process_withdrawal()
        - process_transfer()
        - process_paybill()
        - process_deposit()
        - process_create()
        - process_delete()
        - process_disable()
        - process_change_plan()
        - fee_application()

    Each method modifies the account data based on validated transaction 
    entries from the transaction summary file. The fee_application method 
    specifically handles daily deductions and resets transaction counters.
"""

from print_error import log_constraint_error

def process_transactions(accounts, transactions):
    """
    Iterates through the merged transaction list and routes each 
    action to the appropriate handler function.
    """
    for txn in transactions:
        code = txn['code']
        acc_num = txn['account_number']
        amount = txn['amount']
        name = txn['name']
        misc = txn['misc']
        
        # Skip end of session codes
        if code == '00':
            continue
            
        # Ensure the account exists for most transactions (except create)
        if code != '05' and acc_num not in accounts:
            log_constraint_error(f"Account {acc_num} does not exist", str(txn))
            continue
            
        # Route to the correct helper function
        if code == '01':   # Withdrawal
            accounts = process_withdrawal(accounts, acc_num, amount, str(txn))
        elif code == '02': # Transfer
            dest_acc = misc # For transfer, the misc field holds the destination account
            accounts = process_transfer(accounts, acc_num, dest_acc, amount, str(txn))
        elif code == '03': # Paybill
            accounts = process_paybill(accounts, acc_num, amount, str(txn))
        elif code == '04': # Deposit
            accounts = process_deposit(accounts, acc_num, amount, str(txn))
        elif code == '05': # Create Account
            accounts = process_create(accounts, acc_num, name, amount, str(txn))
        elif code == '06': # Delete Account
            accounts = process_delete(accounts, acc_num, name, str(txn))
        elif code == '07': # Disable Account
            accounts = process_disable(accounts, acc_num, str(txn))
        elif code == '08': # Change Plan
            accounts = process_change_plan(accounts, acc_num, str(txn))
        else:
            log_constraint_error(f"Invalid transaction code {code}", str(txn))
            
    return accounts

def process_withdrawal(accounts, acc_num, amount, txn_context):
    """
    Handles 01 Withdrawal Math.
    Subtracts amount from balance and increments transaction count.
    Ensures balance does not drop below zero.
    """
    if accounts[acc_num]['balance'] < amount:
        log_constraint_error(f"Insufficient funds for withdrawal. Balance: {accounts[acc_num]['balance']}, Attempted: {amount}", txn_context)
    else:
        accounts[acc_num]['balance'] -= amount
        accounts[acc_num]['total_transactions'] += 1
    return accounts

def process_transfer(accounts, acc_num, dest_acc, amount, txn_context):
    """
    Handles 02 Transfer Math.
    Subtracts from source account, adds to destination account.
    Increments transaction count for BOTH accounts.
    """
    if dest_acc not in accounts:
        log_constraint_error(f"Destination account {dest_acc} does not exist for transfer", txn_context)
        return accounts
        
    if accounts[acc_num]['balance'] < amount:
        log_constraint_error(f"Insufficient funds for transfer. Balance: {accounts[acc_num]['balance']}, Attempted: {amount}", txn_context)
    else:
        # deduct from sender
        accounts[acc_num]['balance'] -= amount
        accounts[acc_num]['total_transactions'] += 1
        
        # add to receiver
        accounts[dest_acc]['balance'] += amount
        accounts[dest_acc]['total_transactions'] += 1
        
    return accounts

def process_paybill(accounts, acc_num, amount, txn_context):
    """
    Handles 03 Paybill Math.
    Subtracts amount from balance and increments transaction count.
    (Money leaves the system to the company).
    """
    if accounts[acc_num]['balance'] < amount:
        log_constraint_error(f"Insufficient funds to pay bill. Balance: {accounts[acc_num]['balance']}, Attempted: {amount}", txn_context)
    else:
        accounts[acc_num]['balance'] -= amount
        accounts[acc_num]['total_transactions'] += 1
    return accounts

def process_deposit(accounts, acc_num, amount, txn_context):
    """
    Handles 04 Deposit Math.
    Adds amount to balance and increments transaction count.
    """
    accounts[acc_num]['balance'] += amount
    accounts[acc_num]['total_transactions'] += 1
    return accounts

def process_create(accounts, acc_num, name, amount, txn_context):
    """
    Handles 05 Create Account.
    The Front End sends '00000' as the account number. 
    The Back End must generate a new, unique 5-digit account number.
    """
    # Find the highest existing account number and add 1
    if not accounts:
        new_acc_num_int = 1
    else:
        new_acc_num_int = max(int(k) for k in accounts.keys()) + 1
        
    # format back to a 5-digit string (e.g., '00042')
    new_acc_num = f"{new_acc_num_int:05d}"
    
    # create the new account entry in the hashmap
    accounts[new_acc_num] = {
        'account_number': new_acc_num,
        'name': name,
        'status': 'A',          # new accounts are always Active
        'balance': amount,      # initial deposit amount
        'total_transactions': 0, 
        'plan': 'NP'            # default to Non-Student Plan
    }
    return accounts

def process_delete(accounts, acc_num, name, txn_context):
    """
    Handles 06 Delete Account.
    Ensures the name matches before removing it from the system.
    """
    if accounts[acc_num]['name'] != name:
        log_constraint_error(f"Name mismatch for deletion. Expected {accounts[acc_num]['name']}, got {name}", txn_context)
        return accounts
        
    # in many banking systems, balance must be 0 to delete, but i just pop it from the hashmap
    accounts.pop(acc_num, None)
    return accounts

def process_disable(accounts, acc_num, txn_context):
    """
    Handles 07 Disable Account.
    Changes the account status from 'A' to 'D'.
    """
    # Note: don't need to check if it's already disabled, setting it to 'D' again doesn't hurt.
    accounts[acc_num]['status'] = 'D'
    return accounts

def process_change_plan(accounts, acc_num, txn_context):
    """
    Handles 08 Change Plan.
    Toggles the account plan between 'SP' (Student) and 'NP' (Non-Student).
    """
    current_plan = accounts[acc_num]['plan']
    
    if current_plan == 'SP':
        accounts[acc_num]['plan'] = 'NP'
    else:
        accounts[acc_num]['plan'] = 'SP'
        
    return accounts

def fee_application(accounts):
    '''
    Calculates and applies transaction fees based on account payment plans.
    
    This method processes daily service charges:
        - Student plans (SP) are charged $0.05 per transaction.
        - Non-student plans (NP) are charged $0.10 per transaction.
    
    Method resets the total_transactions counter to zero and ensures the account balance 
    has not dropped below $0.00.
    '''
    fee_rates = {'SP': 0.05, 'NP': 0.10}

    # iterate through accounts
    for acc in accounts.values():
        rate = fee_rates.get(acc.get('plan'), 0.10)

        # calculate exact fee amount for this account
        total_fee = acc['total_transactions'] * rate
        
        # deduct the fee from the balance
        acc['balance'] -= total_fee

        # reset transaction counter
        # acc['total_transactions'] = 0
        
        # error handling: check for negative balances
        if acc['balance'] < 0:
            log_constraint_error(f"Account {acc['account_number']} has a negative balance after fees.", 
                                 "backend_processor", fatal=True)
            
    return accounts
