"""
File: backend_processor.py
Author: Jason, Richard, Brandon
Description:
    Handles core Back End business logic and account updates:
        - process_transaction_summary()
        - fee_application()
        - create_account()
        - delete_account()
        - deposit()
        - withdraw()
        - transfer()
        - paybill()
        - change_plan()
        - enable_disable()

    Each method modifies the account data based on validated transaction 
    entries from the transaction summary file. The fee_application method 
    specifically handles daily deductions and resets transaction counters.
"""

from print_error import log_constraint_error

def fee_application(accounts):
    '''
    Calculates and applies transaction fees based on account payment plans.
    
    This method processes daily service charges:
        - Student plans (SP) are charged $0.05 per transaction.
        - Non-student plans (NP) are charged $0.10 per transaction.
    
    Method resets the total_transaction counter to zero and ensures the account balance 
    has not dropped below $0.00.
    '''
    fee_rates = {'SP': 0.05, 'NP': 0.10}

    for acc in accounts:
        rate = fee_rates.get(acc.get('plan'), 0.10)

        #Fee calculation
        total_fee -= acc['total_transaction']*rate
        acc['balance'] -= total_fee

        acc['total_transaction'] = 0
        
        #Error handling 
        if acc['balance'] < 0:
            log_constraint_error(f"Account {acc['account_number']} has a negative balance", 
                                 "backend_processor", fatal = True)