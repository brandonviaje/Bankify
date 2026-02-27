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
    def __init__(self, accounts, output_file: str):
        # shared accounts dict loaded from the accounts file
        self.accounts = accounts
        self.output_file = output_file

        # track standard withdrawals across a single session resets on login in main.py
        self.standard_withdraw_total = 0.0

    # --------------------
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

    # --------------------
    # deposit
    # --------------------

    def process_deposit(self, session_type: str, current_user: str) -> None:
        # admin must specify which customers account they are acting on
        admin_holder = None
        if session_type == "admin":
            admin_holder = input("Enter account holder name: ").strip()
            if not any(acct.name.lower() == admin_holder.lower() for acct in self.accounts.values()):
                print("Account holder not found.")
                return

        acct_num = input("Enter account number to deposit into (5 digits): ").strip()

        # account must exist
        if acct_num not in self.accounts:
            print("Account not found.")
            return

        acct = self.accounts[acct_num]

        # cant deposit into disabled accounts 
        if not acct.is_active():
            print("Account is disabled. Cannot deposit.")
            return

        # ownership rules
        if session_type == "standard":
            if acct.name.lower() != current_user.lower():
                print("You can only deposit into your own account.")
                return
        else:
            # admin: account must belong to the holder name they typed
            if acct.name.lower() != admin_holder.lower():
                print("Account does not belong to the specified account holder.")
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

        # deposit is recorded only NOT applied this session
        with open(self.output_file, "a") as f:
            write_txn_line(self.output_file, "04", acct.name, acct_num, amount)

        print(f"Deposit accepted for account {acct_num}. (Funds available next session)")

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
    # --------------------

    def process_delete(self, session_type: str) -> None:
        """
        Admin-only. Records a delete transaction and removes the account from this session.
        """
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
        if acct.name.lower() != holder_name.lower():
            print("Account number does not match the specified account holder.")
            return

        with open(self.output_file, "a") as f:
            write_txn_line(self.output_file, "06", holder_name, acct_num, 0.0)

        # prevent future transactions on this account for the rest of the session
        del self.accounts[acct_num]

        print(f"Delete accepted. Account {acct_num} removed for this session.")

    # --------------------
    # privileged: disable
    # --------------------

    def process_disable(self, session_type: str) -> None:
        """
        Admin-only. Disables the account immediately (for this session) and records it.
        """
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
        if acct.name.lower() != holder_name.lower():
            print("Account number does not match the specified account holder.")
            return

        acct.status = "D" # Disable status

        with open(self.output_file, "a") as f:
            write_txn_line(self.output_file, "07", holder_name, acct_num, 0.0)

        print(f"Disable accepted. Account {acct_num} is now disabled for this session.")

    # --------------------
    # privileged: changeplan
    # --------------------

    def process_changeplan(self, session_type: str) -> None:
        # privileged transaction: admin only
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

        # account number must match the specified holder
        if acct.name.lower() != holder_name.lower():
            print("Account number does not match the specified account holder.")
            return

        # switch SP -> NP (only if currently SP)
        if getattr(acct, "plan", "SP") != "SP":
            print("Account is not on a student plan.")
            return

        acct.plan = "NP"  # update in-memory for this session

        # record the change for the back end
        with open(self.output_file, "a") as f:
            write_txn_line(self.output_file, "08", holder_name, acct_num, 0.0)

        print(f"Changeplan accepted. Account {acct_num} is now NP for this session.")

    # --------------------
    # transfer
    # --------------------

    def transfer(self, session_type: str, current_user: str) -> None:
        # track session total for standard transfers
        if not hasattr(self, "standard_transfer_total"):
            self.standard_transfer_total = 0.0

        session_limit = 1000.00
        accounts = self.accounts

        # admin chooses which customer's account they are acting on
        admin_holder = None
        if session_type == "admin":
            admin_holder = input("Enter account holder name: ").strip()
            if not any(acct.name.lower() == admin_holder.lower() for acct in accounts.values()):
                print("Account holder not found.")
                return

        from_acct_num = input("Enter account number to transfer from: ").strip()
        if from_acct_num not in accounts:
            print("Source account not found.")
            return

        from_acct = accounts[from_acct_num]

        # ownership rules
        if session_type == "standard":
            if from_acct.name != current_user:
                print("You can only transfer from your own account.")
                return
        else:
            # admin: from account must belong to the specified holder name
            if from_acct.name.lower() != admin_holder.lower():
                print("Source account does not belong to the specified account holder.")
                return

        if not from_acct.is_active():
            print("Source account is disabled.")
            return

        to_acct_num = input("Enter account number to transfer to: ").strip()
        if to_acct_num not in accounts:
            print("Destination account not found.")
            return

        if from_acct_num == to_acct_num: # prevent transferring to the same account
            print("Cannot transfer to the same account.")
            return

        to_acct = accounts[to_acct_num]

        if not to_acct.is_active(): # prevent transferring into disabled accounts 
            print("Destination account is disabled.")
            return

        try:
            amount = float(input("Enter amount to transfer: ").strip())
        except ValueError:
            print("Invalid amount. Please enter a numeric value.")
            return

        if amount <= 0:
            print("Amount must be positive.")
            return

        # standard: enforce $1000 per session TOTAL
        if session_type == "standard":
            remaining = session_limit - self.standard_transfer_total
            if amount > remaining:
                print(f"Session transfer limit exceeded. You have ${remaining:.2f} remaining this session.")
                return

        # balances must stay >= 0 after transfer
        if from_acct.balance - amount < 0:
            print("Account balance cannot go below $0.")
            return

        # apply in memory
        from_acct.balance -= amount
        to_acct.balance += amount

        # update session total
        if session_type == "standard":
            self.standard_transfer_total += amount

        # record transaction
        with open(self.output_file, "a") as f:
            write_txn_line(self.output_file, "02", from_acct.name, from_acct_num, amount, to_acct_num, 5)

        print(f"Transferred {amount:.2f} from {from_acct_num} to {to_acct_num}.")

    # --------------------
    # paybill
    # --------------------

    companies = {
    "EC": {"name": "The Bright Light Electric Company", "account_number": "99901", "balance": 1000000},
    "CQ": {"name": "Credit Card Company Q", "account_number": "99902", "balance": 30000},
    "FI": {"name": "Fast Internet, Inc.", "account_number": "99903", "balance": 40000},
    }

    def paybill(self, session_type: str, current_user: str) -> None:
        # track session total for standard paybills
        if not hasattr(self, "standard_paybill_total"):
            self.standard_paybill_total = 0.0

        session_limit = 2000.00
        accounts = self.accounts

        # admin chooses which customer's account they're paying from
        admin_holder = None
        if session_type == "admin":
            admin_holder = input("Enter account holder name: ").strip()
            if not any(acct.name.lower() == admin_holder.lower() for acct in accounts.values()):
                print("Account holder not found.")
                return

        acct_num = input("Enter account number to pay from: ").strip()
        if acct_num not in accounts:
            print("Source account not found.")
            return

        acct = accounts[acct_num]

        # must be active
        if not acct.is_active():
            print("Account is disabled. Cannot pay bill.")
            return

        # ownership rules
        if session_type == "standard":
            if acct.name.lower() != current_user.lower():
                print("You can only pay bills from your own account.")
                return
        else:
            # admin: account must belong to the specified holder
            if acct.name.lower() != admin_holder.lower():
                print("Account does not belong to the specified account holder.")
                return

        company_code = input("Enter company code (EC, CQ, FI): ").strip().upper()
        if company_code not in self.companies:
            print("Company not found.")
            return

        try:
            amount = float(input("Enter amount to pay: ").strip())
        except ValueError:
            print("Invalid amount. Please enter a numeric value.")
            return

        if amount <= 0:
            print("Amount must be positive.")
            return

        # standard: enforce $2000 per session TOTAL
        if session_type == "standard":
            remaining = session_limit - self.standard_paybill_total
            if amount > remaining:
                print(f"Session paybill limit exceeded. You have ${remaining:.2f} remaining this session.")
                return

        # balance must stay >= 0 after payment
        if acct.balance - amount < 0:
            print("Account balance cannot go below $0.")
            return

        # apply in memory
        acct.balance -= amount

        # update standard session total
        if session_type == "standard":
            self.standard_paybill_total += amount

        # record transaction
        with open(self.output_file, "a") as f:
            write_txn_line(self.output_file, "03", acct.name, acct_num, amount, company_code, 2)

        print(f"Paid {amount:.2f} to {self.companies[company_code]['name']} from account {acct_num}.")

    # --------------------
    # withdrawal (500 per session in standard mode)
    # --------------------

    def process_withdrawal(self, session_type: str, current_user: str) -> None:
        session_limit = 500.00

        if session_type == "admin":
            account_holder_name = input("Enter account holder name: ").strip()
        else:
            account_holder_name = current_user

        account_number = input("Enter account number: ").strip()
        if account_number not in self.accounts:
            print("Account not found.")
            return

        account = self.accounts[account_number]

        if account.name.lower() != account_holder_name.lower(): # ownership check
            print("Account number does not match the specified account holder.")
            return

        if not account.is_active(): # account must be active
            print("Account is disabled. Cannot withdraw.")
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

        # apply in memory
        account.balance -= amount

        if session_type == "standard":
            self.standard_withdraw_total += amount

        with open(self.output_file, "a") as f:
            write_txn_line(self.output_file, "01", account.name, account_number, amount)

        print(f"Withdraw accepted for account: {account_number}")