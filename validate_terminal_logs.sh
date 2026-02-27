#!/bin/bash
echo "VALIDATING TERMINAL LOGS (.out)"

# loop through expected logs
for expected_log in expected/*.ecf; do

    # get the base name (e.g., FE_09)
    filename=$(basename -- "$expected_log")
    base="${filename%.*}"
    
    echo "Checking log for $base..."
    
    # validate if our actual output log aligns with expected output log
    if diff -q -Z "outputs/$base.out" "expected/$base.ecf" > /dev/null; then
        echo "  -> PASS"
    else
        echo "  -> FAIL (Differences found)"
        diff "outputs/$base.out" "expected/$base.ecf"
    fi
done
