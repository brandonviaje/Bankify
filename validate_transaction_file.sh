#!/bin/bash

echo "  VALIDATING TRANSACTION FILES (.atf)   "

# loop through all expected transaction files
for expected_file in expected/*.etf; do

    # get the base name (e.g., FE_09)
    filename=$(basename -- "$expected_file")
    base="${filename%.*}"
    
    echo "Checking $base..."
    
    # validate if our actual output aligns with expected output
    if diff -q -Z "outputs/$base.atf" "expected/$base.etf" > /dev/null; then
        echo "  -> PASS"
    else
        echo "  -> FAIL (Differences found)"
        diff "outputs/$base.atf" "expected/$base.etf"
    fi
done
