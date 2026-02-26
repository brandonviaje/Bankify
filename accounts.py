"""
File: accounts.py
Author: Brandon 
Description:
    This class handles defines the individual banks accounts within the banking system

    The BankAccount class stores:
        - Account number
        - Account holder name 
        - Account status
        - Account balance 
        - Account plan type

    The class has methods to check if an account is active and string representation for displaying details
    
    This file creates a bankaccount object to read account data from file and used throughout
    the system to perform transactions
"""

class BankAccount:
    # constructor
    def __init__(self, number : str, name : str, status : str, balance : float, plan = "SP"):
        self.number = number      
        self.name = name
        self.status = status      
        self.balance = balance 
        self.plan = plan   

    # checks if account is active
    def is_active(self) -> bool:
        return self.status == "A"
    
    # string representation of obj
    def __repr__(self) -> str:
        return f"{self.number} | {self.name} | {self.status} | {self.balance}"
