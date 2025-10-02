import unittest
from accounts import User

class TestAccount(unittest.TestCase):
    def setUp(self):
        # Create a new account for testing
        self.account = User.create_account('user123', 1000)

    def test_create_account(self):
        # Test if account is created with the correct initial balance
        self.assertEqual(self.account.user_id, 'user123')
        self.assertEqual(self.account.balance, 1000)
        self.assertEqual(self.account.initial_deposit, 1000)

    def test_deposit_funds(self):
        # Test depositing funds to the account
        result = self.account.deposit_funds(500)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 1500)

    def test_withdraw_funds(self):
        # Test withdrawing funds from the account
        result = self.account.withdraw_funds(300)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 700)

    def test_withdraw_funds_insufficient_balance(self):
        # Test withdrawing more funds than available in the account
        result = self.account.withdraw_funds(1100)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 1000)

    def test_deposit_negative_amount(self):
        # Test depositing a negative amount (edge case)
        result = self.account.deposit_funds(-100)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 1000)

    def test_withdraw_funds_negative_amount(self):
        # Test withdrawing a negative amount (edge case)
        result = self.account.withdraw_funds(-100)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 1000)

if __name__ == '__main__':
    unittest.main()