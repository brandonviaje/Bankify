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
    Produces the Current Bank Accounts file for tomorrow's Front End.
    Length: 40 chars (Includes SP/NP plan)
    """
    with open(file_path, 'w') as file:
        for acc in accounts.values():
            # Format: NNNNN_AAAAAAAAAAAAAAAAAAAA_S_PPPPPPPP_PL
            acc_num = str(acc['account_number']).zfill(5)
            
            # Pad the name with underscores to exactly 20 characters
            name = acc['name'].ljust(20, '_')[:20]
            status = acc['status']
            
            # Format balance as 8 digits, no decimals (e.g. 00002000)
            balance = f"{int(acc['balance']):08d}"
            plan = acc['plan']

            file.write(f"{acc_num}_{name}_{status}_{balance}_{plan}\n")
        
        # add END_OF_FILE marker
        file.write("END_OF_FILE\n")


def write_new_master_accounts(accounts, file_path):
    """
    Produces the overnight Master Bank Accounts file.
    Length: 45 chars (Includes TTTT and SP/NP plan)
    """
    # sort in ascending order by account number 
    sorted_accounts = sorted(accounts.values(), key=lambda x: int(x['account_number']))

    with open(file_path, 'w') as file:
        for acc in sorted_accounts:
            # Format: NNNNN_AAAAAAAAAAAAAAAAAAAA_S_PPPPPPPP_TTTT_PL
            acc_num = str(acc['account_number']).zfill(5)
            name = acc['name'].ljust(20, '_')[:20]
            status = acc['status']
            balance = f"{int(acc['balance']):08d}"
            
            tx_count = str(acc.get('total_transactions', 0)).zfill(4)
            plan = acc['plan']

            file.write(f"{acc_num}_{name}_{status}_{balance}_{tx_count}_{plan}\n")
            
        # add END_OF_FILE marker
        file.write("END_OF_FILE\n")
