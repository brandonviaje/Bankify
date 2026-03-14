"""
File: write.py
Author: Jason, Brandon, Richard
Description:
    Handles the generation of updated account files for the Banking System:
        - write_new_current_accounts()
        - write_new_master_accounts()

    Outputs account data into two distinct fixed-length formats. 
    It ensures the 37-character file is for the Front End and the 
    42-character file is correctly formatted and sorted.
"""

def write_new_current_accounts(accounts, file_path):
    """
    Produces the file for the Front End (Phase #4/5 requirements).
    Length: 37 chars [cite: 252]
    """
    with open(file_path, 'w') as file:
        for acc in accounts:
            #Format: NNNNN AAAAAAAAAAAAAAAAAAAA S PPPPPPPP 
            acc_num = str(acc['account_number']).zfill(5)
            name = acc['name'].ljust(20)[:20]
            status = acc['status']
            balance = f"{acc['balance']:08.2f}"

            file.write(f"{acc_num} {name} {status} {balance}\n")
        
        #End with END_OF_FILE marker
        file.write("00000 END_OF_FILE          A 00000.00\n")

def write_new_master_accounts(accounts, file_path):
    """
    Produces the overnight Master file.
    Length: 42 chars 
    """
    # Requirement: Must be in ascending order by account number 
    sorted_accounts = sorted(accounts, key=lambda x: int(x['account_number']))

    with open(file_path, 'w') as file:
        for acc in sorted_accounts:
            # Format: NNNNN AAAAAAAAAAAAAAAAAAAA S PPPPPPPP TTTT 
            acc_num = str(acc['account_number']).zfill(5)
            name = acc['name'].ljust(20)[:20]
            status = acc['status']
            balance = f"{acc['balance']:08.2f}"
            tx_count = str(acc.get('transactions', 0)).zfill(4)

            file.write(f"{acc_num} {name} {status} {balance} {tx_count}\n")