"""
Test Suite: process_change_plan
Author: Moksh Patel and Richard Wu
This module contains unit tests for the `process_change_plan` function,
which handles transaction code 08 (Change Plan).

Purpose:
- Verify correct toggling between Student Plan (SP) and Non-Student Plan (NP)
- Ensure account data is updated accurately after processing a change plan transaction

"""

from backend_processor import process_change_plan
# helper function to create a sample account dictionary
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
    """
    TC1: Test change plan from SP to NP.

    Expectation:
    - Account plan should change from 'SP' to 'NP'
    """
    accounts = create_account("SP")  # Initial condition plan = SP
    
    updated = process_change_plan(accounts, "12345", "test_txn")
    
    # plan  toggle to NP
    assert updated["12345"]["plan"] == "NP"


def test_change_plan_np_to_sp():
    """
    TC2: Test change plan from NP to SP.

    Expectation:
    - Account plan should change from 'NP' to 'SP'
    """
    accounts = create_account("NP")  # Initial condition plan = NP
    
   
    updated = process_change_plan(accounts, "12345", "test_txn")
    
    # plan should toggle to SP
    assert updated["12345"]["plan"] == "SP"


def test_change_plan_other_value_to_sp():
    """
    TC3: Test change plan with invalid/unknown value.

    Expectation:
    - Any plan not equal to 'SP' should be set to 'SP'
    """
    accounts = create_account("XX")
    
    
    updated = process_change_plan(accounts, "12345", "test_txn")
    
    # plan should default to SP
    assert updated["12345"]["plan"] == "SP"