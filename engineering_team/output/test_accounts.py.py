import unittest

# Assuming the following basic implementation of Account class
class Account:
    def __init__(self, user_id, initial_deposit):
        self.account_id = 0  # Simulating autoincrement
        self.user_id = user_id
        self.initial_deposit = initial_deposit
        self.balance = initial_deposit

    def deposit(self, amount):
        if amount <= 0:
            return False
        self.balance += amount
        return True

    def withdraw(self, amount):
        if amount <= 0 or amount > self.balance:
            return False
        self.balance -= amount
        return True

    def calculate_profit_loss(self):
        return self.balance - self.initial_deposit


class TestAccount(unittest.TestCase):
    def test_initialization(self):
        account = Account(user_id=1, initial_deposit=100.0)
        self.assertEqual(account.balance, 100.0)
        self.assertEqual(account.initial_deposit, 100.0)

    def test_deposit_positive_amount(self):
        """Test depositing a positive amount"""
        account = Account(user_id=1, initial_deposit=100.0)
        result = account.deposit(50.0)
        self.assertTrue(result)
        self.assertEqual(account.balance, 150.0)

    def test_deposit_negative_amount(self):
        """Test depositing a negative amount"""
        account = Account(user_id=1, initial_deposit=100.0)
        result = account.deposit(-50.0)
        self.assertFalse(result)
        self.assertEqual(account.balance, 100.0)

    def test_withdraw_valid_amount(self):
        """Test withdrawing a valid amount"""
        account = Account(user_id=1, initial_deposit=100.0)
        result = account.withdraw(50.0)
        self.assertTrue(result)
        self.assertEqual(account.balance, 50.0)

    def test_withdraw_overdraft(self):
        """Test withdrawing more than balance"""
        account = Account(user_id=1, initial_deposit=100.0)
        result = account.withdraw(150.0)
        self.assertFalse(result)
        self.assertEqual(account.balance, 100.0)

    def test_withdraw_negative_amount(self):
        """Test withdrawing a negative amount"""
        account = Account(user_id=1, initial_deposit=100.0)
        result = account.withdraw(-50.0)
        self.assertFalse(result)
        self.assertEqual(account.balance, 100.0)

    def test_calculate_profit_loss(self):
        account = Account(user_id=1, initial_deposit=100.0)
        account.deposit(50.0)
        account.withdraw(70.0)
        self.assertEqual(account.calculate_profit_loss(), -20.0)


unittest.main(argv=[''], verbosity=2, exit=False)