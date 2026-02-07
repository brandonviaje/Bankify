# admin.py
from accounts import BankAccount

class Admin:
    def __init__(self, accounts: dict[str, BankAccount]):
        self.accounts = accounts

    def _require_admin(self, session_type: str) -> bool:
        if session_type != "admin":
            print("Admin transaction. You must be logged in as admin.")
            return False
        return True

    def process_create(self, session_type: str) -> None:
        if not self._require_admin(session_type):
            return

        acct_num = input("Enter NEW account number (5 digits): ").strip()
        if not (acct_num.isdigit() and len(acct_num) == 5):
            print("Account number must be exactly 5 digits.")
            return

        if acct_num in self.accounts:
            print("Account number already exists.")
            return

        name = input("Enter account holder name: ").strip()
        if not name:
            print("Name cannot be empty.")
            return

        bal_str = input("Enter initial balance (0+ integer): ").strip()
        if not bal_str.isdigit():
            print("Invalid balance.")
            return

        balance = int(bal_str)
        self.accounts[acct_num] = BankAccount(acct_num, name, "A", float(balance))
        print(f"Created account {acct_num} for {name} with balance {balance}.")

    def process_delete(self, session_type: str) -> None:
        if not self._require_admin(session_type):
            return

        acct_num = input("Enter account number to DELETE: ").strip()
        if acct_num not in self.accounts:
            print("Account not found.")
            return

        acct = self.accounts[acct_num]

        # Common rule: only allow delete if balance is 0
        if int(acct.balance) != 0:
            print("Account balance must be 0 to delete.")
            return

        del self.accounts[acct_num]
        print(f"Deleted account {acct_num}.")

    def process_disable(self, session_type: str) -> None:
        if not self._require_admin(session_type):
            return

        acct_num = input("Enter account number to DISABLE: ").strip()
        if acct_num not in self.accounts:
            print("Account not found.")
            return

        acct = self.accounts[acct_num]
        acct.status = "D"
        print(f"Disabled account {acct_num}.")
