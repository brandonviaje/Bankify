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

## Project Structure

```
Bankify/
│
├── accounts.txt          # Stores account information
├── transactions/         # Input .atf transaction files
├── expected/             # Expected output files
├── output/               # Program-generated outputs
├── bankify.py            # Main program
└── README.md
```

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
