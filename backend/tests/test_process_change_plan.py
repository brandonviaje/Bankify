# import the function under test from the backend processor module
from backend_processor import process_change_plan

# helper function to create a sample account dictionary
def create_account(plan):
    return {
        "12345": {
            "account_number": "12345",
            "name": "Test",
            "status": "A",
            "balance": 1000,
            "plan": plan,                 # plan is parameterized for testing both cases
            "total_transactions": 0
        }
    }


# Test Case 1:
# verifies that an account with a Student Plan (SP)
# is correctly changed to a Non-Student Plan (NP)
def test_change_plan_sp_to_np():
    accounts = create_account("SP")  # Initial condition: plan = SP
    
    # execute function under test
    updated = process_change_plan(accounts, "12345", "test_txn")
    
    # plan should toggle to NP
    assert updated["12345"]["plan"] == "NP"


# Test Case 2:
# verifies that an account with a Non-Student Plan (NP)
# is correctly changed to a Student Plan (SP)
def test_change_plan_np_to_sp():
    accounts = create_account("NP")  # Initial condition: plan = NP
    
    # Execute function under test
    updated = process_change_plan(accounts, "12345", "test_txn")
    
    # plan should toggle to SP
    assert updated["12345"]["plan"] == "SP"