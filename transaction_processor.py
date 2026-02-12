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
