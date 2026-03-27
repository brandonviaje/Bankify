# Bankify 🏦

**Bankify** is a banking system simulator that allows users to manage accounts, process transactions, and validate transaction files. It demonstrates core programming concepts such as file I/O, state management, and transaction processing.

---

## Features

- Create and manage user accounts  
- Deposit and withdraw funds  
- Transfer between accounts  
- Process `.atf` (Automated Transaction File) files  
- Validate transaction outputs against expected results  
- Maintain persistent account records  

---

## Tech Stack

- Python 3  
- File-based storage system  
- Command-line interface (CLI)  

---

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Bankify.git
   cd Bankify
   ```

2. Run the program:
   ```bash
   python3 main.py bank_accounts.txt daily_transaction_file.txt
   ```

---
## Backend
The backend of Bankify is a batch processor that reads the previous day's master bank account file and a merged transaction file, applies all transactions in order, logs constraint violations, and generates:

- A new master bank accounts file 
- A new current bank accounts file for the next day’s frontend runs
—
## Features 
Process merged transactions from the frontend
Prevents invalid states such as negative balances 
Updates account balances, status, and transaction counts
Supports:
  - withdrawal and deposit  
  - create, delete, transfer, and disable 
  - transfer
  - paybill
  - changeplan

- Applies daily transaction fees:
	- **Student Plan:** $0.05 per transaction
   - **Non-Student Plan:** $0.10 per transaction

---

## Example Transaction Record Format

```
TT Name                 AccNo Balance
```

Where:
- `TT` → Transaction type  
- `Name` → Account holder name  
- `AccNo` → Account number  
- `Balance` → Account balance  

## Testing

To run our tests, please see [TESTING.md](./TESTING.md).
