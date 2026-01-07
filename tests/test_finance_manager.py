"""
Unit tests for Finance Manager
"""
import unittest
from datetime import datetime
from julian_assistant.modules.finance_manager import FinanceManager
from julian_assistant.core.database import Database


class TestFinanceManager(unittest.TestCase):
    """Test cases for FinanceManager"""
    
    def setUp(self):
        """Set up test database and manager"""
        # Use in-memory database for testing
        self.db = Database("sqlite:///:memory:")
        self.session = self.db.get_session()
        self.manager = FinanceManager(self.session)
    
    def tearDown(self):
        """Clean up after tests"""
        self.session.close()
        self.db.close()
    
    def test_add_income(self):
        """Test adding income transaction"""
        transaction = self.manager.add_income(
            amount=5000000,
            category="Gaji",
            description="Salary for January"
        )
        
        self.assertIsNotNone(transaction)
        self.assertEqual(transaction.transaction_type, "income")
        self.assertEqual(transaction.amount, 5000000)
        self.assertEqual(transaction.category, "Gaji")
    
    def test_add_expense(self):
        """Test adding expense transaction"""
        transaction = self.manager.add_expense(
            amount=500000,
            category="Makanan",
            description="Groceries"
        )
        
        self.assertIsNotNone(transaction)
        self.assertEqual(transaction.transaction_type, "expense")
        self.assertEqual(transaction.amount, 500000)
        self.assertEqual(transaction.category, "Makanan")
    
    def test_get_balance(self):
        """Test calculating balance"""
        # Add income
        self.manager.add_income(amount=5000000, category="Gaji")
        
        # Add expenses
        self.manager.add_expense(amount=500000, category="Makanan")
        self.manager.add_expense(amount=200000, category="Transport")
        
        balance = self.manager.get_balance()
        expected_balance = 5000000 - 500000 - 200000
        
        self.assertEqual(balance, expected_balance)
    
    def test_get_transactions(self):
        """Test getting transactions with filters"""
        # Add transactions
        self.manager.add_income(amount=1000000, category="Gaji")
        self.manager.add_expense(amount=500000, category="Makanan")
        self.manager.add_expense(amount=200000, category="Transport")
        
        # Get all transactions
        all_transactions = self.manager.get_transactions()
        self.assertEqual(len(all_transactions), 3)
        
        # Get only expenses
        expenses = self.manager.get_transactions(transaction_type="expense")
        self.assertEqual(len(expenses), 2)
        
        # Get by category
        food_expenses = self.manager.get_transactions(category="Makanan")
        self.assertEqual(len(food_expenses), 1)
        self.assertEqual(food_expenses[0].category, "Makanan")
    
    def test_monthly_summary(self):
        """Test getting monthly summary"""
        now = datetime.now()
        
        # Add transactions for current month
        self.manager.add_income(amount=5000000, category="Gaji", date=now)
        self.manager.add_expense(amount=500000, category="Makanan", date=now)
        self.manager.add_expense(amount=300000, category="Transport", date=now)
        
        summary = self.manager.get_monthly_summary(now.year, now.month)
        
        self.assertEqual(summary['total_income'], 5000000)
        self.assertEqual(summary['total_expense'], 800000)
        self.assertEqual(summary['balance'], 4200000)
        self.assertIn("Makanan", summary['expense_by_category'])
        self.assertIn("Transport", summary['expense_by_category'])
    
    def test_delete_transaction(self):
        """Test deleting a transaction"""
        transaction = self.manager.add_income(amount=1000000, category="Gaji")
        
        result = self.manager.delete_transaction(transaction.id)
        self.assertTrue(result)
        
        deleted = self.manager.get_transaction(transaction.id)
        self.assertIsNone(deleted)
    
    def test_statistics(self):
        """Test getting financial statistics"""
        # Add transactions
        self.manager.add_income(amount=5000000, category="Gaji")
        self.manager.add_income(amount=1000000, category="Bonus")
        self.manager.add_expense(amount=500000, category="Makanan")
        self.manager.add_expense(amount=200000, category="Transport")
        
        stats = self.manager.get_statistics(days=30)
        
        self.assertEqual(stats['income_count'], 2)
        self.assertEqual(stats['expense_count'], 2)
        self.assertEqual(stats['total_income'], 6000000)
        self.assertEqual(stats['total_expense'], 700000)
        self.assertEqual(stats['balance'], 5300000)


if __name__ == '__main__':
    unittest.main()
