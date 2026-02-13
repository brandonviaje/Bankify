from account_reader import read_bank_accounts
from account_writer import format_account_line, write_bank_accounts


class TransactionProcessor:
    def __init__(self, accounts):
        # shared accounts dict loaded from the accounts file
        self.accounts = accounts

    def process_deposit(self, session_type: str, current_user: str) -> None:
        # ask which account the user wants to deposit into
        acct_num = input("Enter account number to deposit into (5 digits): ").strip()

        # account must exist
        if acct_num not in self.accounts:
            print("Account not found.")
            return

        acct = self.accounts[acct_num]

        # can't deposit into disabled accounts
        if not acct.is_active():
            print("Account is disabled. Cannot deposit.")
            return

        # standard users can only deposit into accounts they own
        if session_type == "standard" and acct.name != current_user:
            print("You can only deposit into your own account.")
            return

        # read and validate amount
        amount_str = input("Enter deposit amount (e.g., 200 or 200.00): ").strip()
        try:
            amount = float(amount_str)
        except ValueError:
            print("Invalid amount.")
            return

        if amount <= 0:
            print("Amount must be positive.")
            return

        # for this project, deposits are recorded but not available in the same session
        # (the back end applies deposits when it processes the transaction file)
        with open("transactions_file_log.txt", "a") as f:
            f.write(f"DEPOSIT {acct_num} {amount:.2f} {acct.name}\n")

        print(f"Deposit accepted for account {acct_num}. (Funds available next session)")

        
    def transfer(self, session_type, current_user):

        accounts = self.accounts

        #checks if user is admin, if so ask for account holder name to transfer from, otherwise use current user
        if session_type == "admin":
            account_holder_name = input("Enter account holder name: ").strip()

            matching_accounts = [acct_num for acct_num, acct in accounts.items()
                         if acct.name.lower() == account_holder_name.lower()]
            if not matching_accounts:
                print("Account holder not found.")
                return

        account_number_from = input("Enter account number to transfer from: ").strip()
        if account_number_from not in accounts:
            print("Source account not found.")
            return
        account_from = accounts[account_number_from]
         # check to see if standard user and can only transfer from their own account, but can transfer to any account
        if session_type != "admin" and account_from.name != current_user:
            print("You can only transfer from your own account.")
            return

        account_number_to = input("Enter account number to transfer to: ")

        if account_number_to not in accounts:
            print("Destination account not found.")
            return
        
        if account_number_from == account_number_to:
            print("Cannot transfer to the same account.")
            return


        account_to = accounts[account_number_to]
        #try to read and validate amount to transfer
        try:
            amount = float(input("Enter amount to transfer: "))
        except ValueError:
            print("Invalid amount. Please enter a numeric value.")
            return
        

        

        try:
            if session_type != "admin":
                if amount <= 0 or amount > 1000:
                    print("Amount must be positive and less than or equal to $1000.")
                    return
            if account_from.balance - amount < 0 or account_to.balance + amount < 0:
                print("Account balance cannot go below $0.")
                return
            
            account_from.balance -= amount
            account_to.balance += amount
            print(f"Transferred {amount} from {account_number_from} to {account_number_to}.")

            # record transaction in transaction log
            with open("transactions_file_log.txt", "a") as f:
                f.write(f"Transferred ${amount} from {account_number_from} to {account_number_to}\n")

            # update accounts file with new balances
            with open("bank_accounts.txt", "w") as f:
                for acct_num in sorted(accounts.keys()):
                    f.write(format_account_line(accounts[acct_num]) + "\n")

                f.write("END_OF_FILE\n")


        except ValueError:
            print("Invalid amount. Please enter a numeric value.")
            return

    #list of given companies to pay bills to, with account numbers and balances for each company
    companies = {
        "EC": {
            "name": "The Bright Light Electric Company",
            "account_number": "99901",
            "balance": 1000000,
        },
        "CQ": {
            "name": "Credit Card Company Q",
            "account_number": "99902",
            "balance": 30000,
        },
        "FI": {
            "name": "Fast Internet, Inc.",
            "account_number": "99903",
            "balance": 40000,
        }
    }


    def paybill(self, session_type, current_user, companies=companies):

        accounts = self.accounts


        #checks if user is admin, if so ask for account holder name to pay bill from, otherwise use current user
        if session_type == "admin":
            account_holder_name = input("Enter account holder name: ")

            if account_holder_name not in accounts:
                print("Account holder not found.")
                return

        account_number_from = input("Enter account number to transfer from: ")

        if account_number_from not in accounts:
            print("Source account not found.")
            return

        #find account object for account number
        account_from = accounts[account_number_from]

        company_code = input("Enter company to transfer to: ").strip().upper()

        if company_code not in companies:
            print("Company not found.")
            return

        company_data= companies[company_code]


        #ask for amount to transfer and validate it is a number
        try:
            amount = float(input("Enter amount to transfer: "))
        except ValueError:
            print("Invalid amount. Please enter a numeric value.")
            return
        

        #check to see if user is standard and if so, validate they are transferring from their own account
        if session_type != "admin" and account_from.name != current_user:
            print("You can only transfer from your own account.")
            return
        
        #amount must be positive and less than or equal to 1000, and account balance cannot go below 0 after transfer
        try:
            if amount <= 0 or amount > 1000:
                print("Amount must be positive and less than or equal to $1000.")
                return
            if account_from.balance - amount < 0:
                print("Account balance cannot go below $0.")
                return
            
            account_from.balance -= amount
            company_data["balance"] += amount

            print(f"Transferred {amount} from {account_number_from} to {company_data['name']}.")

            # record transaction in transaction log
            with open("transactions_file_log.txt", "a") as f:
                f.write(f"Bill paid ${amount} from {account_number_from} to {company_data['name']}\n")

            # update accounts file with new balances
            with open("bank_accounts.txt", "w") as f:
                for acct_num in sorted(accounts.keys()):
                    f.write(format_account_line(accounts[acct_num]) + "\n")

                f.write("END_OF_FILE\n")


        #error handling for invalid amount input
        except ValueError:
            print("Invalid amount. Please enter a numeric value.")
            return

    
    def process_withdrawal(self, session_type, current_user):
        #Constraints for withdrawing
        max_withdraw = 500.00
        
        #Ask for account holder's name if logged in as admin
        if session_type == "admin":
            account_holder_name = input("Enter account holder name")
        else:
            account_holder_name = current_user
        
        #Ask for account number 
        account_number = input("Enter account number")
        if account_number not in self.accounts:
            print("Account holder not found")
            return 
        
        account = self.accounts[account_number]
        
        if account.name != account_holder_name:
            print("Account is invalid")
            return 
        if not account.is_active():
            print("Account is disabled. Cannot withdraw")
            return 
        
        withdraw_amount = input("Enter withdrawal amount")
        try:
            amount = float(withdraw_amount)
        except ValueError:
            print("Invalid ammount")
            return 
        
        #Users can only withdraw positive numbers
        if amount <= 0:
            print("Withdraw amount has to be positive")
            return 
        
        #Standard users cannot withdraw more than 500
        if session_type == "standard" and amount > max_withdraw:
            print("Cannot exceed 500 withdrawal limit")
            return 
        
        #User balance cannot drop below 0 
        if account.balance - amount < 0:
            print("Insufficient funds in account. Balance cannot go below $0.00")
            return 
        
        #Withdrawals are recorded in transaction files
        with open("transaction_file_log.txt", "a") as f:
            f.write(f"Withdraw{account_number}{amount:.2f}{account.name}\n")

        print(f"Withdraw accepted for account: {account_number}")

