"""
File: backend_main.py
Author: Jason, Richard, Brandon
Description:
    This is the main program that acts as the entry point for executing our backend program. The backend program is a 
    batch processor that creates a master bank account file and a new current bank accounts file
"""
import sys
from backend_read import read_old_bank_accounts, read_merged_transactions
from backend_write import write_new_current_accounts, write_new_master_accounts
import backend_processor as backend_processor

def main():
    print("--- Starting Back End Batch Processing ---")
    
    # Read Old Master File
    print("Reading old master accounts...")
    accounts = read_old_bank_accounts("old_master_accounts.txt")

    # Check if accounts is empty
    if not accounts:
        print("ERROR: Could not load master accounts. Exiting.")
        sys.exit(1)
        
    # Read Merged Transactions 
    print("Reading merged transactions...")
    transactions = read_merged_transactions("merged_transactions.txt")
    
    # Process transactions from merged_transactions
    print("Processing transactions...")
    accounts = backend_processor.process_transactions(accounts, transactions)
    
    # Apply Daily Fees 
    print("Applying daily fees...")
    accounts = backend_processor.fee_application(accounts)
    
    # Output new Files
    print("Writing new account files...")
    write_new_master_accounts(accounts, "new_master_accounts.txt")
    write_new_current_accounts(accounts, "new_current_accounts.txt")
    
    print("--- Back End Processing Complete ---")

if __name__ == "__main__":
    main()
