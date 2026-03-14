"""
File: backend_main.py
Author: Jason, Richard, Brandon
Description:
    Handles all functions for the Back End :
        - read_old_bank_accounts()
        - process_transaction_summary()
        - fee_application()
        - write_new_master_accounts()
        - write_new_current_accounts()

    The program reads the Old Master Bank Accounts file, processing the daily transaction summary, applying 
    fees, and generating updated account files
"""

import sys
from read import read_old_bank_accounts
from write import write_new_current_accounts, write_new_master_accounts
import backend_processor

def main():
    #Input
    accounts = read_old_bank_accounts("old_master.txt")
    if not accounts:
        sys.exit(1)
    
    #Call function
    backend_processor.fee_application(accounts)

    # 4. Outputs
    write_new_master_accounts(accounts, "new_master.txt")
    write_new_current_accounts(accounts, "new_current.txt")

if __name__ == "__main__":
    main()