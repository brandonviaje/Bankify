from backend_processor import process_change_plan

def create_account(plan):
    return {
        "12345": {
            "account_number": "12345",
            "name": "Test",
            "status": "A",
            "balance": 1000,
            "plan": plan,
            "total_transactions": 0
        }
    }

def test_change_plan_sp_to_np():
    accounts = create_account("SP")
    updated = process_change_plan(accounts, "12345", "test_txn")
    assert updated["12345"]["plan"] == "NP"

def test_change_plan_np_to_sp():
    accounts = create_account("NP")
    updated = process_change_plan(accounts, "12345", "test_txn")
    assert updated["12345"]["plan"] == "SP"