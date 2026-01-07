"""
Julian Personal Assistant - AI Agent System
============================================

Sistem AI Agent untuk asisten pribadi yang membantu dalam:
- Manajemen jadwal dan tugas
- Saran literasi data dan statistik
- Bantuan pekerjaan
- Manajemen keuangan (pemasukan dan pengeluaran)
"""

__version__ = "1.0.0"
__author__ = "FikJul"

from .core.agent import JulianAssistant
from .modules.schedule_manager import ScheduleManager
from .modules.finance_manager import FinanceManager
from .modules.data_advisor import DataAdvisor

__all__ = [
    "JulianAssistant",
    "ScheduleManager",
    "FinanceManager",
    "DataAdvisor",
]
