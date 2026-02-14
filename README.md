# Bankify

🏦 **Banking System — Front End (Phase 2)**

## Overview

This project implements the **Front End** of a simplified banking system as part of a **Software Quality Assurance** assignment.

The Front End:

- Accepts transaction commands via **standard input**
- Validates user actions based on **session type** (standard/admin)
- Reads account data from a **Current Bank Accounts** file
- Writes accepted transactions to a **Daily Transaction File**
- Produces responses via **standard output**

This version represents the **first working implementation (Phase 2)** and is **not fully tested or finalized**.

---

## 📂 File Structure

```txt
bank_accounts.txt              # Current Bank Accounts file (input)
daily_transaction_file.txt     # Daily Transaction File (output)
main.py                        # Program entry point
transaction_processor.py       # Core transaction logic
sessions.py                    # Login/logout management
account_reader.py              # Reads accounts file
account_writer.py              # Formats account records
accounts.py                    # BankAccount class
```

▶️ How to Run

Make sure Python 3 is installed.

Ensure bank_accounts.txt exists in the same directory.

Run:
```bash
python main.py
```

If needed, use:
```bash
python3 main.py
```
🧾 Input File Format

bank_accounts.txt must follow this format:
```markdown

00001_Brandon_____________A_00001101
00002_Hello_______________A_00010160
00003_John_Doe____________D_00010069
END_OF_FILE
```

Format:
```php-template
<5-digit account number>_<name padded to 20 chars>_<status>_<8-digit balance>
```

Where

A = Active

D = Disabled

# 🔐 Session Types
## Standard Session

Can only perform transactions on their own account

Cannot perform privileged operations

Admin Session

Can perform privileged operations:

create

delete

disable

changeplan

# ✅ Currently Implemented Features
## Login / Logout

Loads accounts from bank_accounts.txt

Tracks session type (standard/admin)

## Deposit

Validates account exists and is active

Standard users can only deposit into their own account

Records transaction in the Daily Transaction File

Funds are not available until next session (per specification)

## Withdrawal

Validates ownership and active status

Standard users limited to $500 per transaction

Prevents negative balances

Records transaction in the Daily Transaction File

## Transfer

Validates source and destination accounts

Standard users limited to $1000 per transaction

Prevents negative balances

Records transaction

## Pay Bill

Validates allowed company codes (EC, CQ, FI)

Prevents negative balances

Records transaction

# 🔒 Privileged Features (Admin Only)
## Create

Validates name (≤ 20 characters)

Validates balance (≤ 99999.99)

Records create request

Account becomes available after back end processing

## Delete

Validates account holder name and number match

Removes account from session memory

Records delete request

## Disable

Changes account status from A → D in session

Records disable request

## Change Plan

Records changeplan request (SP → NP)

Applied during back end processing

# ⚠️ Not Fully Implemented Yet (Phase 2 Limitations)

## This version is a rapid first implementation. The following behaviors are not yet complete:

❌ No full automated test validation

❌ No full transaction file formatting (fixed-width records not finalized)

❌ Back End processing not implemented

❌ Create/delete/disable effects persist only after back end is built

❌ No full enforcement of all edge-case constraints

❌ No full session-end transaction file finalization

In Phase 3, the Front End will be fully tested against the Phase 1 Requirements Tests.

# 🧠 Design Intent
## Front End reads:

Standard input

Current Bank Accounts file

Front End writes:

Standard output

Daily Transaction File

Back End (future phase) will:

Read the Daily Transaction File

Apply changes

Produce a new Current Bank Accounts file

# 🛠 Development Notes

Code is structured around a TransactionProcessor class

Privileged transactions require admin login

Account validation is centralized through a shared account dictionary

Daily transactions are appended to daily_transaction_file.txt
