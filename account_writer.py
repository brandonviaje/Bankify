# account_writer.py
from accounts import BankAccount

NAME_WIDTH = 20  # fixed padding width for names (underscores)

def format_account_line(acct: BankAccount) -> str:
    """
    Output format must match:
    (\d{5})_(.+?)_+([AD])_(\d{8})
    We'll write: 12345_Name___________A_00001000
    """
    number = acct.number
    name_padded = acct.name.ljust(NAME_WIDTH, "_")
    status = acct.status  # "A" or "D"

    # Balance in file is 8 digits. We'll store as integer-like amount.
    balance_int = int(round(acct.balance))
    balance_str = f"{balance_int:08d}"

    return f"{number}_{name_padded}{status}_{balance_str}"

def write_bank_accounts(file_path: str, accounts: dict[str, BankAccount]) -> None:
    with open(file_path, "w") as f:
        for acct_num in sorted(accounts.keys()):
            f.write(format_account_line(accounts[acct_num]) + "\n")
        f.write("END_OF_FILE\n")
