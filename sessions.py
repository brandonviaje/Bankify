from account_reader import read_bank_accounts

class Session:
    # Constructor
    def __init__(self):
        self.session_active = False     # session state
        self.session_type = None        # "standard" or "admin"
        self.current_user = None        # account holder name
        self.transactions_done = False  # track if a transaction happened

    def mark_transaction(self):
        """true whenever a transaction is successfully performed."""
        self.transactions_done = True

    # Handle User Login
    def handle_login(self, file_path):

        if self.session_active:
            print("Already logged in.")
            return None

        while True:
            try:
                self.session_type = input("Enter session type (standard/admin): ").strip().lower()
            except EOFError:
                return None            
            if self.session_type in {"standard", "admin"}:
                break
            print("Invalid session type. Retry")

        if self.session_type == "standard":
            self.current_user = input("Enter account holder name: ").strip()
        else:
            self.current_user = "ADMIN"

        accounts = read_bank_accounts(file_path)


        if self.session_type == "standard":
            if not any(acc.name.lower() == self.current_user.lower() for acc in accounts.values()):
                print("Account holder not found.")
                self.session_type = None
                self.current_user = None
                return None

        self.session_active = True
        print(f"Logged in as {self.current_user} ({self.session_type})")
        return accounts

    # Handle User Logout
    def handle_logout(self, accounts, output_file_path):

        # Check if logged in
        if not self.session_active:
            print("No active session. Please login first.")
            return

        # End login session
        self.session_active = False
        self.session_type = None
        self.current_user = None

        print("Logged out successfully. No transactions can be processed until login.")
