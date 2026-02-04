class BankAccount:
    # constructor
    def __init__(self, number : str, name : str, status : str, balance : float):
        self.number = number      
        self.name = name
        self.status = status      
        self.balance = balance    

    # checks if account is active
    def is_active(self) -> bool:
        return self.status == "A"
    
    # string representation of obj
    def __repr__(self) -> str:
        return f"{self.number} | {self.name} | {self.status} | {self.balance}"
