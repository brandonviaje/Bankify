from account_reader import read_bank_accounts
from account_writer import format_account_line, write_bank_accounts


class TransactionProcessor:
    def __init__(self, accounts):
        # shared accounts dict loaded from the accounts file
        self.accounts = accounts


    # helpers

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


    # deposit

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

        # deposits get recorded, but aren't available until next session (FE_22)
        with open("transactions_file_log.txt", "a") as f:
            f.write(f"DEPOSIT {acct_num} {amount:.2f} {acct.name}\n")

        print(f"Deposit accepted for account {acct_num}. (Funds available next session)")


    # privileged: create
 
    def process_create(self, session_type: str) -> None:
        if not self._require_admin(session_type):
            return

        # ask for holder name (max 20 chars)
        name = input("Enter account holder name: ").strip()
        if not name:
            print("Name cannot be empty.")
            return
        if len(name) > 20:
            print("Name must be at most 20 characters.")
            return

        # ask for initial balance (<= 99999.99)
        bal_str = input("Enter initial balance (e.g., 1000 or 1000.00): ").strip()
        try:
            balance = float(bal_str)
        except ValueError:
            print("Invalid balance.")
            return

        if balance < 0:
            print("Balance cannot be negative.")
            return
        if balance > 99999.99:
            print("Balance can be at most 99999.99.")
            return

        # front end records create, but doesnt add it to self.accounts in this session
        # account number uniqueness and creation happens when back end processes file
        with open("transactions_file_log.txt", "a") as f:
            f.write(f"CREATE {name} {balance:.2f}\n")

        print("Create accepted. (New account available next session)")

  
    # privileged: delete
   
    def process_delete(self, session_type: str) -> None:
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

        # account number must match the specified account holder
        if acct.name.lower() != holder_name.lower():
            print("Account number does not match the specified account holder.")
            return

        # record transaction first
        with open("transactions_file_log.txt", "a") as f:
            f.write(f"DELETE {holder_name} {acct_num}\n")

        # no further transactions should be accepted on a deleted account in this session
        del self.accounts[acct_num]

        print(f"Delete accepted. Account {acct_num} removed for this session.")


    # privileged: disable

    def process_disable(self, session_type: str) -> None:
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

        # account number must match the specified account holder
        if acct.name.lower() != holder_name.lower():
            print("Account number does not match the specified account holder.")
            return

        # change account from active to disabled in this session
        acct.status = "D"

        # record transaction
        with open("transactions_file_log.txt", "a") as f:
            f.write(f"DISABLE {holder_name} {acct_num}\n")

        print(f"Disable accepted. Account {acct_num} is now disabled for this session.")

  
    # privileged: changeplan

    def process_changeplan(self, session_type: str) -> None:
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

        # account number must match the specified account holder
        if acct.name.lower() != holder_name.lower():
            print("Account number does not match the specified account holder.")
            return

        # your BankAccount doesn't store plan yet, so just record it for the back end
        with open("transactions_file_log.txt", "a") as f:
            f.write(f"CHANGEPLAN {holder_name} {acct_num}\n")

        print(f"Changeplan accepted for account {acct_num} (SP -> NP).")


    # transfer

    def transfer(self, session_type, current_user):

        accounts = self.accounts

        # checks if user is admin, if so ask for account holder name to transfer from
        if session_type == "admin":
            account_holder_name = input("Enter account holder name: ").strip()

            matching_accounts = [
                acct_num for acct_num, acct in accounts.items()
                if acct.name.lower() == account_holder_name.lower()
            ]
            if not matching_accounts:
                print("Account holder not found.")
                return

        account_number_from = input("Enter account number to transfer from: ").strip()
        if account_number_from not in accounts:
            print("Source account not found.")
            return
        account_from = accounts[account_number_from]

        # standard user can only transfer from their own account
        if session_type != "admin" and account_from.name != current_user:
            print("You can only transfer from your own account.")
            return

        account_number_to = input("Enter account number to transfer to: ").strip()

        if account_number_to not in accounts:
            print("Destination account not found.")
            return

        if account_number_from == account_number_to:
            print("Cannot transfer to the same account.")
            return

        account_to = accounts[account_number_to]

        # try to read and validate amount to transfer
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

    # list of given companies to pay bills to
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

        # checks if user is admin, if so ask for account holder name to pay bill from
        if session_type == "admin":
            account_holder_name = input("Enter account holder name: ").strip()

            # your accounts dict is keyed by account number, so check via values()
            if not any(acct.name.lower() == account_holder_name.lower() for acct in accounts.values()):
                print("Account holder not found.")
                return

        account_number_from = input("Enter account number to transfer from: ").strip()

        if account_number_from not in accounts:
            print("Source account not found.")
            return

        account_from = accounts[account_number_from]

        if session_type != "admin" and account_from.name != current_user:
            print("You can only transfer from your own account.")
            return

        company_code = input("Enter company to transfer to: ").strip().upper()

        if company_code not in companies:
            print("Company not found.")
            return

        company_data = companies[company_code]

        try:
            amount = float(input("Enter amount to transfer: "))
        except ValueError:
            print("Invalid amount. Please enter a numeric value.")
            return

        try:
            if amount <= 0 or amount > 1000:
                print("Amount must be positive and less than or equal to $1000.")
                return
            if account_from.balance - amount < 0:
                print("Account balance cannot go below $0.")
                return

            account_from.balance -= amount
            company_data["balance"] += amount

            print(f"\nTransferred {amount} from {account_number_from} to {company_data['name']}.")

            with open("transactions_file_log.txt", "a") as f:
                f.write(f"Bill paid ${amount} from {account_number_from} to {company_data['name']}\n")

            with open("bank_accounts.txt", "w") as f:
                for acct_num in sorted(accounts.keys()):
                    f.write(format_account_line(accounts[acct_num]) + "\n")
                f.write("END_OF_FILE\n")

        except ValueError:
            print("Invalid amount. Please enter a numeric value.")
            return

    def process_withdrawal(self, session_type, current_user):
        # constraints for withdrawing
        max_withdraw = 500.00

        # ask for account holder's name if logged in as admin
        if session_type == "admin":
            account_holder_name = input("Enter account holder name: ").strip()
        else:
            account_holder_name = current_user

        # ask for account number
        account_number = input("Enter account number: ").strip()
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

        withdraw_amount = input("Enter withdrawal amount: ").strip()
        try:
            amount = float(withdraw_amount)
        except ValueError:
            print("Invalid amount")
            return

        if amount <= 0:
            print("Withdraw amount has to be positive")
            return

        if session_type == "standard" and amount > max_withdraw:
            print("Cannot exceed 500 withdrawal limit")
            return

        if account.balance - amount < 0:
            print("Insufficient funds in account. Balance cannot go below $0.00")
            return

        # withdrawals are recorded in transaction files
        with open("transactions_file_log.txt", "a") as f:
            f.write(f"WITHDRAW {account_number} {amount:.2f} {account.name}\n")

        print(f"Withdraw accepted for account: {account_number}")
