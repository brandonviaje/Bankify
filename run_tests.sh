#!/bin/bash

# remove old outputs directory completely
rm -rf outputs/

# create the outputs directory again
mkdir -p outputs

# loop through every .txt file in the inputs folder
for filepath in inputs/FE_*.txt; do
    
    # extract the filename (e.g., "FE_01.txt")
    filename=$(basename "$filepath")
    
    # strip the .txt extension so we have "FE_01"
    basename="${filename%.*}"
    
    echo "Running test $basename..."
    
    # execute Python program
    # - arg 1: bank_accounts.txt (The master accounts file)
    # - arg 2: outputs/FE_01.atf (The transaction file you pass into TransactionProcessor)
    # - < "$filepath": Feed input file into program 
    # - > "outputs/${basename}.out": Saves all your print() statements to a log file
    python3 main.py bank_accounts.txt "outputs/${basename}.atf" < "$filepath" > "outputs/${basename}.out"

done

echo "All tests complete!"
