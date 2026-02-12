# admin.py
from accounts import BankAccount

class Admin:
    def __init__(self, accounts: dict[str, BankAccount]):
        # keep a reference to the shared accounts dictionary
        # so changes here show up everywhere.
        self.accounts = accounts

    def _require_admin(self, session_type: str) -> bool:
        # small helper to block admin-only actions in standard mode.
        if session_type != "admin":
            print("Admin transaction. You must be logged in as admin.")
            return False
        return True

    def process_create(self, session_type: str) -> None:
        # only admins can create accounts.
        if not self._require_admin(session_type):
            return

        # get a new account number (must be exactly 5 digits).
        acct_num = input("Enter NEW account number (5 digits): ").strip()
        if not (acct_num.isdigit() and len(acct_num) == 5):
            print("Account number must be exactly 5 digits.")
            return

        # can't create an account with a number that already exists.
        if acct_num in self.accounts:
            print("Account number already exists.")
            return

        # get the account holder name.
        name = input("Enter account holder name: ").strip()
        if not name:
            print("Name cannot be empty.")
            return

        # initial balance is expected to be a non-negative integer here.
        bal_str = input("Enter initial balance (0+ integer): ").strip()
        if not bal_str.isdigit():
            print("Invalid balance.")
            return

        balance = int(bal_str)

        # create the new account as active ("A") and store it in the dict.
        self.accounts[acct_num] = BankAccount(acct_num, name, "A", float(balance))
        print(f"Created account {acct_num} for {name} with balance {balance}.")

    def process_delete(self, session_type: str) -> None:
        # only admins can delete accounts.
        if not self._require_admin(session_type):
            return

        # ask which account to delete.
        acct_num = input("Enter account number to DELETE: ").strip()
        if acct_num not in self.accounts:
            print("Account not found.")
            return

        acct = self.accounts[acct_num]

        # usually the rule is: only delete if the balance is 0
        # (prevents "losing" money by deleting accounts with funds).
        if int(acct.balance) != 0:
            print("Account balance must be 0 to delete.")
            return

        # remove the account completely.
        del self.accounts[acct_num]
        print(f"Deleted account {acct_num}.")

    def process_disable(self, session_type: str) -> None:
        # only admins can disable accounts.
        if not self._require_admin(session_type):
            return

        # ask which account to disable.
        acct_num = input("Enter account number to DISABLE: ").strip()
        if acct_num not in self.accounts:
            print("Account not found.")
            return

        # flip the status to disabled ("D").
        acct = self.accounts[acct_num]
        acct.status = "D"
        print(f"Disabled account {acct_num}.")
