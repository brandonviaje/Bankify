"""
File: admin.py
Author: Brandon 
Description:
    This class handles administrator-only account properties within the banking system

    The admin class:
        - Validates admin session permission
        - Creates new bank accounts 
        - Deletes existing accounts if balance is 0 
        - Disables accounts 
        - Changes account plans 
        - Updates the shared accounts dictionary 
    
    The admin actions directly modify the in-memory accounts dictionary and may log certain changes 
    to the transaction file
"""

# admin.py
from accounts import BankAccount

class Admin:
    def __init__(self, accounts: dict[str, BankAccount]):
        # keep a reference to the shared accounts dictionary
        # so changes here show up everywhere.
        self.accounts = accounts

    def _require_admin(self, session_type: str) -> bool:
        """
        Ensures the current session has admin privileges
        """

        # small helper to block admin-only actions in standard mode.
        if session_type != "admin":
            print("Admin transaction. You must be logged in as admin.")
            return False
        return True

    def process_create(self, session_type: str) -> None:
        """
        Creates a new bank account (admin only)

        This method:
            - Verifies the current session has admin privileges.
            - Prompts for a new 5-digit account number and ensures it is unique.
            - Prompts for a non-empty account holder name.
            - Prompts for a non-negative integer initial balance.
            - Creates a new active ("A") BankAccount object.
            - Adds the account to the shared accounts dictionary.

        Parameters:
            session_type (str): The type of session ("admin" or "standard").

        Returns:
            None
        """

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
        """
        Deletes an existing bank account (admin only).

        This method:  
            - Verifies the current session has admin privileges.
            - Prompts for the account number to delete.
            - Confirms the account exists.
            - Ensures the account balance is zero before deletion.
            - Removes the account from the shared accounts dictionary.

        Parameters:
            session_type (str): The type of session ("admin" or "standard").

        Returns:
            None
        """
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
        """
        Deletes an existing bank account (admin only).

        This method:
            - Verifies the current session has admin privileges.
            - Prompts for the account number to delete.
            - Confirms the account exists.
            - Ensures the account balance is zero before deletion.
            - Removes the account from the shared accounts dictionary.

        Parameters:
            session_type (str): The type of session ("admin" or "standard").

        Returns:
            None
        """

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

    def process_change_plan(self, session_type):
        """
        Changes an account's plan from Student Plan (SP) to
        Non-Student Plan (NP) (admin-only operation).

        This method:
            - Verifies the current session has admin privileges.
            - Prompts for the account number and confirms it exists.
            - Prompts for the account holder name and verifies it matches.
            - Ensures the current plan is "SP".
            - Updates the account plan to "NP".
            - Logs the plan change in "transactions_file_log.txt".

        Parameters:
            session_type (str): The type of session ("admin" or "standard").

        Returns:
            None

        """
        #Only admins are able to change plans
        if not self._require_admin(session_type):
            return
        
        account_number = input("Enter account number:")

        #Check if the account exists
        if account_number not in self.accounts:
            print("Account not found.")
            return 
        
        account = self.accounts[account_number]

        account_name = input("Enter account holder name:")

        #Check if the name matches account holder 
        if account.name != account_name:
            print("Account holder name does not match.")
            return 
        
        #Check current plan 
        if account.plan != "SP":
            print("Account is not a student plan.")
            return 
        
        #Update plan
        account.plan = "NP"

        #Log the transaction 
        with open("transactions_file_log.txt", "a") as f:
            f.write(f"Changed plan: Account name:{account_name}, Account number:{account_number} to NP\n")

        print(f"User plan for account {account_number} changed to NP")