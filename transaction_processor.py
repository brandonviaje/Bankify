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
    to the daily transaction output file (self.output_file).
"""

from __future__ import annotations
from typing import Optional
from accounts import BankAccount

# -------------------------
# Fixed-width formatting helpers (Front End transaction file)
# -------------------------
# Spec line form (40 chars + newline):
# CC(2) ' ' NAME(20) ' ' ACCT(5) ' ' AMOUNT(8) ' ' MISC(2)
# Example: "04 Brandon______________ 00001 00010.00   \n"

def fmt_code(code: str) -> str:
    return f"{str(code)[:2]:>2}"

def fmt_name(name: str) -> str:
    # left-justified, space-filled to 20
    return f"{name[:20]:20}"

def fmt_acct(acct_num: str) -> str:
    # keep only digits, format as 5 digits, zero-filled
    digits = "".join(ch for ch in str(acct_num) if ch.isdigit())
    if digits == "":
        digits = "0"
    return f"{int(digits):05d}"

def fmt_amount(amount: float) -> str:
    # 8 chars including decimal, zero-filled (e.g., 00010.00)
    return f"{amount:08.2f}"

def fmt_misc(misc: str) -> str:
    # 2 chars, left-justified
    return f"{misc[:2]:2}"

def write_txn_line(out_file: str, code: str, name: str, acct: str, amount: float, misc: str = "") -> None:
    line = (
        f"{fmt_code(code)} "
        f"{fmt_name(name)} "
        f"{fmt_acct(acct)} "
        f"{fmt_amount(amount)} "
        f"{fmt_misc(misc)}"
    )
    # should be exactly 40 characters before newline
    # (keep this check while debugging; you can remove later)
    if len(line) != 40:
        print(f"[DEBUG] txn line length={len(line)} expected=40 :: {repr(line)}")

    with open(out_file, "a") as f:
        f.write(line + "\n")


class TransactionProcessor:
    """
    TransactionProcessor writes accepted transactions to self.output_file
    in the required fixed-width format.

    Note: Front End should NOT permanently update bank_accounts.txt in Phase 3.
    That is handled by the Back End when it applies merged transaction files.
    """

    # standard-mode session caps
    STD_WITHDRAW_CAP = 500.00
    STD_TRANSFER_CAP = 1000.00
    STD_PAYBILL_CAP = 2000.00

    def __init__(self, accounts: dict[str, BankAccount], output_file: str, debug_log: bool = False):
        self.accounts = accounts
        self.output_file = output_file
        self.debug_log = debug_log

        # session running totals (reset these on login in main.py)
        self.standard_withdraw_total = 0.0
        self.standard_transfer_total = 0.0
        self.standard_paybill_total = 0.0

    # --------------------
    # optional debug logger
    # --------------------
    def _log_debug(self, msg: str) -> None:
        if not self.debug_log:
            return
        with open("transactions_file_log.txt", "a") as f:
            f.write(msg + "\n")

    # --------------------
    # common validation helpers
    # --------------------
    def _require_admin(self, session_type: str) -> bool:
        if session_type != "admin":
            print("Privileged transaction. You must be logged in as admin.")
            return False
        return True

    def _find_holder_name_for_admin(self) -> Optional[str]:
        holder = input("Enter account holder name: ").strip()
        if not holder:
            print("Account holder name cannot be empty.")
            return None
        # holder must exist (at least one account with this name)
        if not any(a.name.lower() == holder.lower() for a in self.accounts.values()):
            print("Account holder not found.")
            return None
        return holder

    def _resolve_account(self, session_type: str, current_user: str, prompt_acct: str = "Enter account number: ") -> Optional[BankAccount]:
        """
        Resolves and validates the account for the current action.
        - standard: must belong to current_user
        - admin: asks for holder name, and account must belong to that holder
        """
        if session_type == "admin":
            holder = self._find_holder_name_for_admin()
            if holder is None:
                return None
        else:
            holder = current_user

        acct_num = input(prompt_acct).strip()
        if acct_num not in self.accounts:
            print("Account not found.")
            return None

        acct = self.accounts[acct_num]
        if acct.name.lower() != holder.lower():
            print("Account number does not match the specified account holder.")
            return None

        return acct

    def _read_positive_amount(self, prompt: str) -> Optional[float]:
        raw = input(prompt).strip()
        try:
            amt = float(raw)
        except ValueError:
            print("Invalid amount. Please enter a numeric value.")
            return None
        if amt <= 0:
            print("Amount must be positive.")
            return None
        return amt

    # --------------------
    # deposit (04)
    # --------------------
    def process_deposit(self, session_type: str, current_user: str) -> bool:
        acct = self._resolve_account(session_type, current_user, prompt_acct="Enter account number to deposit into: ")
        if acct is None or not acct.is_active():
            print("Deposit rejected.")
            return False

        amount = self._read_positive_amount("Enter amount to deposit: ")
        if amount is None:
            return False

        # FE rule: deposit recorded; funds not available this session.
        # So we do NOT change acct.balance here.
        write_txn_line(self.output_file, "04", acct.name, acct.number, amount, "")
        self._log_debug(f"DEPOSIT accepted -> {acct.number} {amount:.2f}")
        print(f"Deposit accepted for account {acct.number}. (Funds available next session)")
        return True

    # --------------------
    # withdrawal (01) - standard: $500 TOTAL per session
    # --------------------
    def process_withdrawal(self, session_type: str, current_user: str) ->  bool:
        acct = self._resolve_account(session_type, current_user, prompt_acct="Enter account number to withdraw from: ")
        if acct is None:
            return False
 
        if not acct.is_active():
            print("Account is disabled. Cannot withdraw.")
            return False

        amount = self._read_positive_amount("Enter withdrawal amount: ")
        if amount is None:
            return False

        if session_type == "standard":
            remaining = self.STD_WITHDRAW_CAP - self.standard_withdraw_total
            if amount > remaining:
                print(f"Session withdrawal limit exceeded. You have ${remaining:.2f} remaining this session.")
                return False

        if acct.balance - amount < 0:
            print("Insufficient funds. Balance cannot go below $0.00")
            return False

        # withdrawals DO change in-session balance (so later checks are correct)
        acct.balance -= amount
        if session_type == "standard":
            self.standard_withdraw_total += amount

        write_txn_line(self.output_file, "01", acct.name, acct.number, amount, "")
        self._log_debug(f"WITHDRAW accepted -> {acct.number} {amount:.2f}")

        print(f"Withdraw accepted for account {acct.number}.")
        return True

    # --------------------
    # transfer (02) - standard: $1000 TOTAL per session
    # NOTE: spec for misc is 2 chars; transfer needs TO account (5 digits).
    # Many course versions allow transfer lines longer. If YOUR tests expect TO account,
    # we append it as an extra field (common in these projects).
    # --------------------
    def transfer(self, session_type: str, current_user: str) -> bool:
        from_acct = self._resolve_account(session_type, current_user, prompt_acct="Enter account number to transfer FROM: ")
        if from_acct is None:
            return False

        if not from_acct.is_active():
            print("Source account is disabled. Cannot transfer.")
            return False

        to_num = input("Enter account number to transfer TO: ").strip()
        if to_num not in self.accounts:
            print("Destination account not found.")
            return False

        if to_num == from_acct.number:
            print("Cannot transfer to the same account.")
            return False

        to_acct = self.accounts[to_num]
        if not to_acct.is_active():
            print("Destination account is disabled. Cannot transfer.")
            return False

        amount = self._read_positive_amount("Enter transfer amount: ")
        if amount is None:
            return False

        if session_type == "standard":
            remaining = self.STD_TRANSFER_CAP - self.standard_transfer_total
            if amount > remaining:
                print(f"Session transfer limit exceeded. You have ${remaining:.2f} remaining this session.")
                return False

        if from_acct.balance - amount < 0:
            print("Insufficient funds. Balance cannot go below $0.00")
            return False

        # apply in-session balances
        from_acct.balance -= amount
        to_acct.balance += amount

        if session_type == "standard":
            self.standard_transfer_total += amount

        # WRITE OUTPUT:
        # If your expected format includes TO account, write a “common” transfer line:
        # "02 NAME(20) FROM(5) AMOUNT(8) TO(5)\n"
        transfer_line = (
            f"{fmt_code('02')} "
            f"{fmt_name(from_acct.name)} "
            f"{fmt_acct(from_acct.number)} "
            f"{fmt_amount(amount)} "
            f"{fmt_acct(to_acct.number)}"
        )
        with open(self.output_file, "a") as f:
            f.write(transfer_line + "\n")

        self._log_debug(f"TRANSFER accepted -> {from_acct.number} -> {to_acct.number} {amount:.2f}")
        print(f"Transfer accepted from {from_acct.number} to {to_acct.number}.")
        return True

    # --------------------
    # paybill (03) - standard: $2000 TOTAL per session
    # --------------------
    COMPANIES = {
        "EC": "The Bright Light Electric Company",
        "CQ": "Credit Card Company Q",
        "FI": "Fast Internet, Inc.",
    }

    def paybill(self, session_type: str, current_user: str) -> bool:
        acct = self._resolve_account(session_type, current_user, prompt_acct="Enter account number to pay FROM: ")
        if acct is None:
            return False

        if not acct.is_active():
            print("Account is disabled. Cannot pay bill.")
            return False

        company_code = input("Enter company code (EC, CQ, FI): ").strip().upper()
        if company_code not in self.COMPANIES:
            print("Company not found.")
            return False

        amount = self._read_positive_amount("Enter bill payment amount: ")
        if amount is None:
            return False

        if session_type == "standard":
            remaining = self.STD_PAYBILL_CAP - self.standard_paybill_total
            if amount > remaining:
                print(f"Session paybill limit exceeded. You have ${remaining:.2f} remaining this session.")
                return False

        if acct.balance - amount < 0:
            print("Insufficient funds. Balance cannot go below $0.00")
            return False

        # apply in-session balance
        acct.balance -= amount
        if session_type == "standard":
            self.standard_paybill_total += amount

        # misc holds company code (2 chars)
        write_txn_line(self.output_file, "03", acct.name, acct.number, amount, company_code)
        self._log_debug(f"PAYBILL accepted -> {acct.number} {amount:.2f} {company_code}")

        print(f"Paybill accepted from {acct.number} to {self.COMPANIES[company_code]}.")
        return True

    # --------------------
    # create (05) - admin only
    # --------------------
    def process_create(self, session_type: str) -> bool:
        if not self._require_admin(session_type):
            return False

        name = input("Enter NEW account holder name: ").strip()
        if not name:
            print("Name cannot be empty.")
            return False
        if len(name) > 20:
            print("Name must be at most 20 characters.")
            return False

        bal_str = input("Enter initial balance (e.g., 1000 or 1000.00): ").strip()
        try:
            balance = float(bal_str)
        except ValueError:
            print("Invalid balance. Please enter a numeric value.")
            return False

        if balance < 0:
            print("Balance cannot be negative.")
            return False
        if balance > 99999.99:
            print("Balance can be at most 99999.99.")
            return False

        # Front End does NOT assign account number. Back End will.
        write_txn_line(self.output_file, "05", name, "00000", balance, "")
        self._log_debug(f"CREATE accepted -> {name} {balance:.2f}")

        print("Create accepted. (New account available next session)")
        return True

    # --------------------
    # delete (06) - admin only
    # --------------------
    def process_delete(self, session_type: str, current_user: str) -> bool:
        if not self._require_admin(session_type):
            return False

        acct = self._resolve_account(session_type, current_user, prompt_acct="Enter account number to DELETE: ")
        if acct is None:
            return False

        # record delete
        write_txn_line(self.output_file, "06", acct.name, acct.number, 0.0, "")
        self._log_debug(f"DELETE accepted -> {acct.number}")

        # prevent further transactions this session
        del self.accounts[acct.number]

        print(f"Delete accepted. Account {acct.number} removed for this session.")
        return True

    # --------------------
    # disable (07) - admin only
    # --------------------
    def process_disable(self, session_type: str, current_user: str) -> bool:
        if not self._require_admin(session_type):
            return False

        acct = self._resolve_account(session_type, current_user, prompt_acct="Enter account number to DISABLE: ")
        if acct is None:
            return False

        acct.status = "D"
        write_txn_line(self.output_file, "07", acct.name, acct.number, 0.0, "")
        self._log_debug(f"DISABLE accepted -> {acct.number}")

        print(f"Disable accepted. Account {acct.number} is now disabled for this session.")
        return True

    # --------------------
    # changeplan (08) - admin only
    # --------------------
    def process_changeplan(self, session_type: str, current_user: str) -> bool:
        if not self._require_admin(session_type):
            return False

        acct = self._resolve_account(session_type, current_user, prompt_acct="Enter account number to CHANGEPLAN: ")
        if acct is None:
            return False

        # Front End records it; Back End applies plan + transaction fees.
        write_txn_line(self.output_file, "08", acct.name, acct.number, 0.0, "")
        self._log_debug(f"CHANGEPLAN accepted -> {acct.number}")

        print(f"Changeplan accepted for account {acct.number} (SP -> NP).")
        return True
