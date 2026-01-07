"""
Unit tests for Julian Assistant main agent
"""
import unittest
from julian_assistant import JulianAssistant
from julian_assistant.core.database import Database


class TestJulianAssistant(unittest.TestCase):
    """Test cases for JulianAssistant"""
    
    def setUp(self):
        """Set up test assistant"""
        # Use in-memory database for testing
        self.db = Database("sqlite:///:memory:")
        # Create assistant but use test database
        self.assistant = JulianAssistant(session_id="test_session")
        # Replace with test session
        if self.assistant.db_session:
            self.assistant.db_session.close()
        self.assistant.db_session = self.db.get_session()
        # Reinitialize managers with test session
        from julian_assistant.modules.schedule_manager import ScheduleManager
        from julian_assistant.modules.finance_manager import FinanceManager
        self.assistant.schedule_manager = ScheduleManager(self.assistant.db_session)
        self.assistant.finance_manager = FinanceManager(self.assistant.db_session)
    
    def tearDown(self):
        """Clean up after tests"""
        self.assistant.close()
        self.db.close()
    
    def test_initialization(self):
        """Test assistant initialization"""
        self.assertIsNotNone(self.assistant)
        self.assertEqual(self.assistant.session_id, "test_session")
        self.assertIsNotNone(self.assistant.schedule_manager)
        self.assertIsNotNone(self.assistant.finance_manager)
        self.assertIsNotNone(self.assistant.data_advisor)
    
    def test_greet(self):
        """Test greeting message"""
        greeting = self.assistant.greet()
        self.assertIsNotNone(greeting)
        self.assertIn("Julian", greeting)
        self.assertIn("asisten", greeting.lower())
    
    def test_process_schedule_command(self):
        """Test processing schedule command"""
        response = self.assistant.process_command("jadwal hari ini")
        self.assertIsNotNone(response)
        self.assertIn("jadwal", response.lower())
    
    def test_process_finance_command(self):
        """Test processing finance command"""
        response = self.assistant.process_command("saldo")
        self.assertIsNotNone(response)
        self.assertIn("saldo", response.lower())
    
    def test_process_data_command(self):
        """Test processing data tips command"""
        response = self.assistant.process_command("tips data")
        self.assertIsNotNone(response)
        # Should contain a tip
        self.assertGreater(len(response), 10)
    
    def test_process_help_command(self):
        """Test help command"""
        response = self.assistant.process_command("bantuan")
        self.assertIsNotNone(response)
        self.assertIn("jadwal", response.lower())
        self.assertIn("keuangan", response.lower())
    
    def test_conversation_history(self):
        """Test conversation history tracking"""
        self.assistant.process_command("jadwal hari ini")
        self.assistant.process_command("saldo")
        
        history = self.assistant.get_conversation_history()
        # Should have at least user messages and responses
        self.assertGreater(len(history), 0)
    
    def test_context_manager(self):
        """Test context manager usage"""
        with JulianAssistant() as assistant:
            self.assertIsNotNone(assistant)
            greeting = assistant.greet()
            self.assertIn("Julian", greeting)
        # Should close properly


if __name__ == '__main__':
    unittest.main()
