import unittest
from accounts import Account

class TestAccount(unittest.TestCase):

    def test_initial_deposit(self):
        account = Account(initial_deposit=1000)
        self.assertEqual(account.balance, 1000)

    def test_deposit(self):
        account = Account(initial_deposit=1000)
        account.deposit(500)
        self.assertEqual(account.balance, 1500)

    def test_withdraw(self):
        account = Account(initial_deposit=1000)
        result = account.withdraw(500)
        self.assertTrue(result)
        self.assertEqual(account.balance, 500)
        result = account.withdraw(600)
        self.assertFalse(result)
        self.assertEqual(account.balance, 500)

    def test_buy_shares(self):
        account = Account(initial_deposit=1500)
        result = account.buy_shares('AAPL', 10)
        self.assertTrue(result)
        self.assertEqual(account.balance, 0)
        self.assertEqual(account.holdings['AAPL'], 10)
        result = account.buy_shares('AAPL', 1)
        self.assertFalse(result)
        self.assertEqual(account.balance, 0)

    def test_sell_shares(self):
        account = Account(initial_deposit=1500)
        account.buy_shares('AAPL', 10)
        result = account.sell_shares('AAPL', 5)
        self.assertTrue(result)
        self.assertEqual(account.balance, 750)
        self.assertEqual(account.holdings['AAPL'], 5)
        result = account.sell_shares('AAPL', 10)
        self.assertFalse(result)
        self.assertEqual(account.balance, 750)

    def test_get_portfolio_value(self):
        account = Account(initial_deposit=1500)
        account.buy_shares('AAPL', 10)
        value = account.get_portfolio_value()
        self.assertEqual(value, 1500)

    def test_get_profit_or_loss(self):
        account = Account(initial_deposit=1500)
        account.buy_shares('AAPL', 10)
        profit_or_loss = account.get_profit_or_loss()
        self.assertEqual(profit_or_loss, 0)

    def test_get_holdings(self):
        account = Account(initial_deposit=1500)
        account.buy_shares('AAPL', 10)
        holdings = account.get_holdings()
        self.assertEqual(holdings, {'AAPL': 10})

    def test_get_transaction_history(self):
        account = Account(initial_deposit=1500)
        account.deposit(500)
        account.buy_shares('AAPL', 10)
        account.sell_shares('AAPL', 5)
        expected_history = [
            'Deposit: $500',
            'Buy: 10 AAPL shares at $150.0 each',
            'Sell: 5 AAPL shares at $150.0 each'
        ]
        self.assertEqual(account.get_transaction_history(), expected_history)

if __name__ == '__main__':
    unittest.main()