# transaction_processor.py
from accounts import BankAccount

class TransactionProcessor:
    def __init__(self, accounts: dict[str, BankAccount]):
        self.accounts = accounts

    def process_deposit(self, session_type: str, current_user: str) -> None:
        """
        - Standard user: can only deposit to their own account (name must match current_user)
        - Admin: can deposit to any account
        - Account must exist and be active
        - Amount must be positive integer
        """
        acct_num = input("Enter account number to deposit into (5 digits): ").strip()

        if acct_num not in self.accounts:
            print("Account not found.")
            return

        acct = self.accounts[acct_num]

        if not acct.is_active():
            print("Account is disabled. Cannot deposit.")
            return

        # Standard users can only deposit to their own named account
        if session_type == "standard" and acct.name != current_user:
            print("You can only deposit into your own account.")
            return

        amount_str = input("Enter deposit amount (positive integer): ").strip()

        if not amount_str.isdigit():
            print("Invalid amount.")
            return

        amount = int(amount_str)
        if amount <= 0:
            print("Amount must be positive.")
            return

        acct.balance += amount
        print(f"Deposit successful. New balance for {acct.number}: {int(acct.balance)}")
