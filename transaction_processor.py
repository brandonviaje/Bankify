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

        
    def transfer(accounts, session_type, current_user):
        
        if session_type == "admin":
            account_holder_name = input("Enter account holder name: ")

            if account_holder_name not in accounts:
                print("Account holder not found.")
                return

        account_number_from = input("Enter account number to transfer from: ")

        if account_number_from not in accounts:
            print("Source account not found.")
            return


        account_from = accounts[account_number_from]

        account_number_to = input("Enter account number to transfer to: ")

        if account_number_to not in accounts:
            print("Destination account not found.")
            return


        account_to = accounts[account_number_to]

        try:
            amount = float(input("Enter amount to transfer: "))
        except ValueError:
            print("Invalid amount. Please enter a numeric value.")
            return
        

        if session_type != "admin" and account_from.name != current_user:
            print("You can only transfer from your own account.")
            return
        
        try:
            if amount <= 0 or amount > 1000:
                print("Amount must be positive and less than or equal to $1000.")
                return
            if account_from.balance - amount < 0 or account_to.balance + amount < 0:
                print("Account balance cannot go below $0.")
                return
            
            account_from.balance -= amount
            account_to.balance += amount
            print(f"Transferred {amount} from {account_number_from} to {account_number_to}.")
            with open("transactions_file_log.txt", "a") as f:
                f.write(f"Transferred ${amount} from {account_number_from} to {account_number_to}\n")

            

        except ValueError:
            print("Invalid amount. Please enter a numeric value.")
            return

    



