#  Testing the Program

##  Run All Tests

To execute the full test suite, run:

```bash
./run_tests.sh
```

This will:
- Run the program against all test cases
- Generate transaction files
- Simulate the full terminal session (user interaction flow)

---

## About Terminal Logs

The terminal logs represent the **full ATM simulation**, including prompts and system responses.
The terminal logs **do NOT capture user input**. They only capture what the program **prints to terminal**.

Example output:

```
Please login to continue.

Available transaction codes:
login, logout, deposit, transfer, withdrawal, paybill, create, delete, disable, changeplan, exit

Enter transaction code: You must login first.

Please login to continue.

Available transaction codes:
login, logout, deposit, transfer, withdrawal, paybill, create, delete, disable, changeplan, exit

Enter transaction code: [DEBUG] txn line length=41 expected=40 :: '00                      00000 00000.00   '
```

The validation script compares this entire output exactly to the expected output including:
- Prompts  
- Error messages  
- Debug messages  
- Spacing  
- Line breaks  

---

## Validate the Transaction File Output

To compare the generated transaction file with the expected output:

```bash
./validate_transaction_file.sh
```

This checks:
- The produced `.atf` file  
- Against the expected transaction file  
- Reports any differences  

---

## Validate the Terminal Logs

To compare the actual console simulation with the expected log:

```bash
./validate_terminal_logs.sh
```

This checks:
- Printed terminal output against the expected terminal log  
- Reports mismatches 

---

## Recommended Workflow

```bash
./run_tests.sh
./validate_transaction_file.sh
./validate_terminal_logs.sh
```
