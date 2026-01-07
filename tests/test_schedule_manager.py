"""
Unit tests for Schedule Manager
"""
import unittest
from datetime import datetime, timedelta
from julian_assistant.modules.schedule_manager import ScheduleManager
from julian_assistant.core.database import Database


class TestScheduleManager(unittest.TestCase):
    """Test cases for ScheduleManager"""
    
    def setUp(self):
        """Set up test database and manager"""
        # Use in-memory database for testing
        self.db = Database("sqlite:///:memory:")
        self.session = self.db.get_session()
        self.manager = ScheduleManager(self.session)
    
    def tearDown(self):
        """Clean up after tests"""
        self.session.close()
        self.db.close()
    
    def test_create_schedule(self):
        """Test creating a new schedule"""
        start_time = datetime.now() + timedelta(days=1)
        end_time = start_time + timedelta(hours=1)
        
        schedule = self.manager.create_schedule(
            title="Test Meeting",
            start_time=start_time,
            end_time=end_time,
            description="Test description",
            priority="high"
        )
        
        self.assertIsNotNone(schedule)
        self.assertEqual(schedule.title, "Test Meeting")
        self.assertEqual(schedule.priority, "high")
        self.assertEqual(schedule.status, "pending")
    
    def test_get_schedule(self):
        """Test retrieving a schedule"""
        start_time = datetime.now() + timedelta(days=1)
        created = self.manager.create_schedule(
            title="Test Meeting",
            start_time=start_time
        )
        
        retrieved = self.manager.get_schedule(created.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.title, created.title)
    
    def test_update_schedule(self):
        """Test updating a schedule"""
        start_time = datetime.now() + timedelta(days=1)
        schedule = self.manager.create_schedule(
            title="Original Title",
            start_time=start_time
        )
        
        updated = self.manager.update_schedule(
            schedule.id,
            title="Updated Title",
            status="completed"
        )
        
        self.assertEqual(updated.title, "Updated Title")
        self.assertEqual(updated.status, "completed")
    
    def test_delete_schedule(self):
        """Test deleting a schedule"""
        start_time = datetime.now() + timedelta(days=1)
        schedule = self.manager.create_schedule(
            title="To Delete",
            start_time=start_time
        )
        
        result = self.manager.delete_schedule(schedule.id)
        self.assertTrue(result)
        
        deleted = self.manager.get_schedule(schedule.id)
        self.assertIsNone(deleted)
    
    def test_get_today_schedules(self):
        """Test getting today's schedules"""
        today = datetime.now()
        tomorrow = today + timedelta(days=1)
        
        # Create schedule for today
        self.manager.create_schedule(
            title="Today's Meeting",
            start_time=today.replace(hour=10, minute=0)
        )
        
        # Create schedule for tomorrow
        self.manager.create_schedule(
            title="Tomorrow's Meeting",
            start_time=tomorrow.replace(hour=10, minute=0)
        )
        
        today_schedules = self.manager.get_today_schedules()
        self.assertEqual(len(today_schedules), 1)
        self.assertEqual(today_schedules[0].title, "Today's Meeting")
    
    def test_mark_completed(self):
        """Test marking schedule as completed"""
        start_time = datetime.now() + timedelta(days=1)
        schedule = self.manager.create_schedule(
            title="Task",
            start_time=start_time
        )
        
        completed = self.manager.mark_completed(schedule.id)
        self.assertEqual(completed.status, "completed")


if __name__ == '__main__':
    unittest.main()
