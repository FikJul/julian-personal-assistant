"""
Schedule Manager Module
========================
Modul untuk manajemen jadwal dan kalender
"""
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import pytz
from sqlalchemy.orm import Session

from ..core.database import db, Schedule
from ..core.config import config


class ScheduleManager:
    """Manager untuk jadwal dan kalender"""
    
    def __init__(self, session: Optional[Session] = None):
        """Initialize schedule manager"""
        self.session = session or db.get_session()
        self.timezone = pytz.timezone(config.TIMEZONE)
    
    def create_schedule(
        self,
        title: str,
        start_time: datetime,
        description: Optional[str] = None,
        end_time: Optional[datetime] = None,
        location: Optional[str] = None,
        priority: str = "medium"
    ) -> Schedule:
        """
        Buat jadwal baru
        
        Args:
            title: Judul acara
            start_time: Waktu mulai
            description: Deskripsi acara
            end_time: Waktu selesai
            location: Lokasi
            priority: Prioritas (low, medium, high)
        
        Returns:
            Schedule object yang telah dibuat
        """
        schedule = Schedule(
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
            location=location,
            priority=priority
        )
        
        self.session.add(schedule)
        self.session.commit()
        self.session.refresh(schedule)
        
        return schedule
    
    def get_schedule(self, schedule_id: int) -> Optional[Schedule]:
        """Get schedule by ID"""
        return self.session.query(Schedule).filter(Schedule.id == schedule_id).first()
    
    def get_today_schedules(self) -> List[Schedule]:
        """Dapatkan jadwal hari ini"""
        today_start = datetime.now(self.timezone).replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)
        
        return self.session.query(Schedule).filter(
            Schedule.start_time >= today_start,
            Schedule.start_time < today_end,
            Schedule.status != "cancelled"
        ).order_by(Schedule.start_time).all()
    
    def get_upcoming_schedules(self, days: int = 7) -> List[Schedule]:
        """Dapatkan jadwal yang akan datang"""
        now = datetime.now(self.timezone)
        future = now + timedelta(days=days)
        
        return self.session.query(Schedule).filter(
            Schedule.start_time >= now,
            Schedule.start_time <= future,
            Schedule.status != "cancelled"
        ).order_by(Schedule.start_time).all()
    
    def update_schedule(
        self,
        schedule_id: int,
        **kwargs
    ) -> Optional[Schedule]:
        """Update jadwal"""
        schedule = self.get_schedule(schedule_id)
        if not schedule:
            return None
        
        for key, value in kwargs.items():
            if hasattr(schedule, key):
                setattr(schedule, key, value)
        
        schedule.updated_at = datetime.utcnow()
        self.session.commit()
        self.session.refresh(schedule)
        
        return schedule
    
    def delete_schedule(self, schedule_id: int) -> bool:
        """Hapus jadwal"""
        schedule = self.get_schedule(schedule_id)
        if not schedule:
            return False
        
        self.session.delete(schedule)
        self.session.commit()
        return True
    
    def mark_completed(self, schedule_id: int) -> Optional[Schedule]:
        """Tandai jadwal sebagai selesai"""
        return self.update_schedule(schedule_id, status="completed")
    
    def get_schedule_conflicts(self, start_time: datetime, end_time: datetime) -> List[Schedule]:
        """Cek konflik jadwal"""
        return self.session.query(Schedule).filter(
            Schedule.status != "cancelled",
            Schedule.start_time < end_time,
            Schedule.end_time > start_time
        ).all()
    
    def get_statistics(self) -> Dict[str, Any]:
        """Dapatkan statistik jadwal"""
        total = self.session.query(Schedule).count()
        completed = self.session.query(Schedule).filter(Schedule.status == "completed").count()
        pending = self.session.query(Schedule).filter(Schedule.status == "pending").count()
        
        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "completion_rate": (completed / total * 100) if total > 0 else 0
        }
