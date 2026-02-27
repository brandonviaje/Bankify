"""
File: transaction_processor.py
Author: Jason, Richard, Moksh
Description:
    Handles all front-end banking transactions:
        - process_deposit()
        - process_withdrawal()
        - transfer()
        - paybill()
        - process_create()      (admin)
        - process_delete()      (admin)
        - process_disable()     (admin)
        - process_changeplan()  (admin)

    Each method validates the session + inputs, then records accepted transactions
    to the daily transaction output file.
"""

from account_reader import read_bank_accounts
from account_writer import format_account_line, write_bank_accounts
from accounts import BankAccount

# -------------------------
# Transaction formatting helpers
# -------------------------

def fmt_name(name: str) -> str:
    return f"{name[:20]:20}"  # left justified 20 chars

def fmt_acct(acct_num: str) -> str:
    digits = "".join(ch for ch in acct_num if ch.isdigit())
    return f"{int(digits):05d}"

def fmt_amount(amount: float) -> str:
    return f"{amount:08.2f}"  # zero-filled 8 chars including decimal

def fmt_misc(misc: str, width: int = 2) -> str:
    return f"{misc[:width]:{width}}"

def write_txn_line(out_file: str, code: str, name: str, acct: str, amount: float, misc: str = "", misc_width: int = 2):
    line = (
        f"{code:>2} "
        f"{fmt_name(name)} "
        f"{fmt_acct(acct)} "
        f"{fmt_amount(amount)} "
        f"{fmt_misc(misc, misc_width)}"
        "\n"
    )
    with open(out_file, "a") as f:
        f.write(line)

class TransactionProcessor:
    def __init__(self, accounts, transaction_file):
        self.accounts = accounts
        self.output_file = transaction_file

        self.standard_withdraw_total = 0
        self.standard_transfer_total = 0
        self.standard_paybill_total = 0

    # helpers
    # --------------------
    def _require_admin(self, session_type: str) -> bool:
        # privileged transactions only work in admin mode
        if session_type != "admin":
            print("Privileged transaction. You must be logged in as admin.")
            return False
        return True

    def _name_exists(self, name: str) -> bool:
        # checks if there is at least one account with this holder name
        return any(acct.name.lower() == name.lower() for acct in self.accounts.values())

    def _account_matches_holder(self, acct_num: str, holder_name: str) -> bool:
        # checks acct exists and belongs to holder name
        if acct_num not in self.accounts:
            return False
        return self.accounts[acct_num].name.lower() == holder_name.lower()


    def _resolve_account(self, session_type: str, current_user: str) -> 'BankAccount | None':
        """Prompt for and validate account, with admin name check. Returns account or None."""
        if session_type == "admin":
            holder_name = input("Enter account holder name: ").strip()
            if not self._name_exists(holder_name):
                print("Account holder not found.")
                return None
        else:
            holder_name = current_user

        acct_num = input("Enter account number: ").strip()
        if acct_num not in self.accounts:
            print("Account not found.")
            return None

        acct = self.accounts[acct_num]
        if acct.name.lower() != holder_name.lower():
            print("Account number does not match the specified account holder.")
            return None

        return acct
    
    def _log_transaction(self, message: str):
        """Append a transaction message to the transaction log file."""
        with open("transactions_file_log.txt", "a") as f:
            f.write(message + "\n")

    def _save_accounts(self):
        """Rewrite the accounts file with updated balances."""
        with open("bank_accounts.txt", "w") as f:
            for acct_num in sorted(self.accounts.keys()):
                f.write(format_account_line(self.accounts[acct_num]) + "\n")
            f.write("END_OF_FILE\n")

    # --------------------
    # deposit
    # --------------------

    def process_deposit(self, session_type: str, current_user: str) -> None:
        # ask which account the user wants to deposit into
        # acct_num = input("Enter account number to deposit into (5 digits): ").strip()

        # # account must exist
        # if acct_num not in self.accounts:
        #     print("Account not found.")
        #     return

        # acct = self.accounts[acct_num]

        acct = self._resolve_account(session_type, current_user)
        if acct is None:
            return

        if not acct.is_active():
            print("Account is disabled. Cannot deposit.")
            return


        # read and validate amount
        amount_str = input("Enter amount to deposit: ").strip()
        try:
            amount = float(amount_str)
        except ValueError:
            print("Invalid amount. Please enter a numeric value.")
            return

        if amount <= 0:
            print("Amount must be positive.")
            return

        # deposits get recorded, but aren't available until next session (FE_22)
        with open("transactions_file_log.txt", "a") as f:
            f.write(f"DEPOSIT {acct.number} {amount:.2f} {acct.name}\n")

        print(f"Deposit accepted for account {acct.number}. (Funds available next session)")

    # --------------------
    # privileged: create
    # --------------------

    def process_create(self, session_type: str) -> None:
        # privileged transaction: admin only
        if not self._require_admin(session_type):
            return

        # ask for holder name (<= 20 chars)
        name = input("Enter account holder name: ").strip()
        if not name:
            print("Name cannot be empty.")
            return
        if len(name) > 20:
            print("Name must be at most 20 characters.")
            return

        # ask for initial balance (0 <= balance <= 99999.99)
        bal_str = input("Enter initial balance (e.g., 1000 or 1000.00): ").strip()
        try:
            balance = float(bal_str)
        except ValueError:
            print("Invalid balance. Please enter a numeric value.")
            return

        if balance < 0:
            print("Balance cannot be negative.")
            return
        if balance > 99999.99:
            print("Balance can be at most 99999.99.")
            return

        #Do not create the account in self.accounts during this session.
        # Just record it so the Back End can assign a unique account number later
        with open(self.output_file, "a") as f:
            write_txn_line(self.output_file, "05", name, "00000", balance)

        print("Create accepted. (New account available next session)")


    # --------------------
    # privileged: delete
   
    def process_delete(self, session_type: str, current_user: str) -> None:
        if not self._require_admin(session_type):
            return

        # holder_name = input("Enter account holder name: ").strip()
        # if not self._name_exists(holder_name):
        #     print("Account holder not found.")
        #     return

        # acct_num = input("Enter account number: ").strip()
        # if acct_num not in self.accounts:
        #     print("Account not found.")
        #     return

        # acct = self.accounts[acct_num]

        acct = self._resolve_account(session_type, current_user)

        if acct is None:
            return
        # record transaction first
        with open("transactions_file_log.txt", "a") as f:
            f.write(f"DELETE {acct.name} {acct.number}\n")

        # no further transactions should be accepted on a deleted account in this session
        del self.accounts[acct.number]

        print(f"Delete accepted. Account {acct.number} removed for this session.")


    # --------------------
    # privileged: disable
    # --------------------

    def process_disable(self, session_type: str, current_user: str) -> None:
        if not self._require_admin(session_type):
            return

        holder_name = input("Enter account holder name: ").strip()
        if not self._name_exists(holder_name):
            print("Account holder not found.")
            return

        acct_num = input("Enter account number: ").strip()
        if acct_num not in self.accounts:
            print("Account not found.")
            return

        acct = self.accounts[acct_num]

        # acct = self._resolve_account(session_type, current_user)

        #account number must match the specified account holder
        if acct.name.lower() != holder_name.lower():
            print("Account number does not match the specified account holder.")
            return

        acct.status = "D" # Disable status

        # record transaction
        with open("transactions_file_log.txt", "a") as f:
            f.write(f"DISABLE {acct.name} {acct.number}\n")

        print(f"Disable accepted. Account {acct.number} is now disabled for this session.")

  
    # --------------------
    # privileged: changeplan
    # --------------------

    def process_changeplan(self, session_type: str,current_user: str) -> None:
        if not self._require_admin(session_type):
            return

        # holder_name = input("Enter account holder name: ").strip()
        # if not self._name_exists(holder_name):
        #     print("Account holder not found.")
        #     return

        # acct_num = input("Enter account number: ").strip()
        # if acct_num not in self.accounts:
        #     print("Account not found.")
        #     return

        # acct = self.accounts[acct_num]

        # # account number must match the specified account holder
        # if acct.name.lower() != holder_name.lower():
        #     print("Account number does not match the specified account holder.")
        #     return

        acct = self._resolve_account(session_type, current_user)
        if acct is None:
            return

        # your BankAccount doesn't store plan yet, so just record it for the back end
        with open("transactions_file_log.txt", "a") as f:
            f.write(f"CHANGEPLAN {acct.name} {acct.number}\n")

        print(f"Changeplan accepted for account {acct.number} (SP -> NP).")


    # --------------------
    # transfer
    # --------------------

    def transfer(self, session_type, current_user):

        session_limit = 1000.00

        account_from = self._resolve_account(session_type, current_user)
        if account_from is None:
            return

        if not account_from.is_active():
            print("Account is disabled. Cannot transfer.")
            return

        # Get destination account
        dest_number = input("Enter destination account number: ").strip()

        account_to = self.accounts.get(dest_number)
        if account_to is None:
            print("Destination account not found.")
            return

        try:
            amount = float(input("Enter transfer amount: ").strip())
        except ValueError:
            print("Invalid amount.")
            return

        if amount <= 0:
            print("Transfer amount must be positive.")
            return

        # Standard user session transfer limit
        if session_type == "standard":
            remaining = session_limit - self.standard_transfer_total

            if amount > remaining:
                print(f"Session transfer limit exceeded. You have ${remaining:.2f} remaining this session.")
                return

            self.standard_transfer_total += amount

        # Balance validation
        if account_from.balance - amount < 0:
            print("Insufficient funds. Balance cannot go below $0.00")
            return

        # Perform transfer
        account_from.balance -= amount
        account_to.balance += amount

        # Log transaction
        with open("transactions_file_log.txt", "a") as f:
            f.write(
                f"TRANSFER {account_from.number} {account_to.number} {amount:.2f} {account_from.name}\n"
            )

        self._save_accounts()

        print(f"Transfer accepted from account {account_from.number} to {account_to.number}")
            

    # list of given companies to pay bills to
    companies = {
    "EC": {"name": "The Bright Light Electric Company", "account_number": "99901", "balance": 1000000},
    "CQ": {"name": "Credit Card Company Q", "account_number": "99902", "balance": 30000},
    "FI": {"name": "Fast Internet, Inc.", "account_number": "99903", "balance": 40000},
    }

    def paybill(self, session_type, current_user):

        account_from = self._resolve_account(session_type, current_user)
        if account_from is None:
            return

        session_limit = 2000.00

        # ownership rules
        if session_type == "standard":
            if account_from.name.lower() != current_user.lower():
                print("You can only pay bills from your own account.")
                return

        company_code = input("Enter company code (EC, CQ, FI): ").strip().upper()

        if company_code not in self.companies:
            print("Company not found.")
            return

        company_data = self.companies[company_code]

        try:
            amount = float(input("Enter amount to pay: ").strip())
        except ValueError:
            print("Invalid amount. Please enter a numeric value.")
            return

        if amount <= 0:
            print("Amount must be positive.")
            return

        # standard session paybill limit
        if session_type == "standard":
            remaining = session_limit - self.standard_paybill_total

            if amount > remaining:
                print(f"Session paybill limit exceeded. You have ${remaining:.2f} remaining this session.")
                return

            self.standard_paybill_total += amount

        # update balances
        account_from.balance -= amount
        self.accounts[company_data["account_number"]].balance += amount

        # log transaction
        with open("transactions_file_log.txt", "a") as f:
            f.write(
                f"PAYBILL {account_from.number} {amount:.2f} {company_data['account_number']}\n"
            )

        self._save_accounts()

        print(f"Paybill accepted from account {account_from.number}")

    def process_withdrawal(self, session_type, current_user):
        # constraints for withdrawing
        session_limit = 500.00


        # ask for account holder's name if logged in as admin
        # if session_type == "admin":
        #     account_holder_name = input("Enter account holder name: ").strip()
        # else:
        #     account_holder_name = current_user

        # # ask for account number
        # account_number = input("Enter account number: ").strip()
        # if account_number not in self.accounts:
        #     print("Account holder not found")
        #     return

        account = self._resolve_account(session_type, current_user)

        if account is None:
            return

        if not account.is_active():
            print("Account is disabled. Cannot withdraw")
            return

        withdraw_amount = input("Enter withdrawal amount: ").strip() # read as string first to validate numeric input
        try:
            amount = float(withdraw_amount)
        except ValueError:
            print("Invalid amount.")
            return

        if amount <= 0: # amount must be positive
            print("Withdraw amount has to be positive.")
            return

        # standard users: total across session <= 500
        if session_type == "standard":
            remaining = session_limit - self.standard_withdraw_total
            if amount > remaining:
                print(f"Session withdrawal limit exceeded. You have ${remaining:.2f} remaining this session.")
                return

        if account.balance - amount < 0:
            print("Insufficient funds. Balance cannot go below $0.00")
            return

        # withdrawals are recorded in transaction files
        with open("transactions_file_log.txt", "a") as f:
            f.write(f"WITHDRAW {account.number} {amount:.2f} {account.name}\n")

        print(f"Withdraw accepted for account: {account.number}")
