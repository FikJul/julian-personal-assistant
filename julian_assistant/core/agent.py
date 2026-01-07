"""
Main AI Agent - Julian Personal Assistant
==========================================
Agen AI utama yang mengorkestra semua modul
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session

from ..core.config import config
from ..core.database import db, ConversationHistory
from ..modules.schedule_manager import ScheduleManager
from ..modules.finance_manager import FinanceManager
from ..modules.data_advisor import DataAdvisor


class JulianAssistant:
    """
    Julian Personal Assistant - AI Agent
    
    Asisten pribadi AI yang membantu dalam:
    - Manajemen jadwal dan tugas
    - Manajemen keuangan (pemasukan dan pengeluaran)
    - Saran literasi data dan statistik
    - Bantuan pekerjaan umum
    """
    
    def __init__(self, session_id: Optional[str] = None):
        """
        Initialize Julian Assistant
        
        Args:
            session_id: ID sesi untuk tracking percakapan
        """
        self.name = config.AGENT_NAME
        self.language = config.LANGUAGE
        self.session_id = session_id or f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Initialize modules
        self.db_session = db.get_session()
        self.schedule_manager = ScheduleManager(self.db_session)
        self.finance_manager = FinanceManager(self.db_session)
        self.data_advisor = DataAdvisor()
        
        # Conversation history
        self.conversation_history: List[Dict[str, str]] = []
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
    
    def close(self):
        """Close database session"""
        if self.db_session:
            self.db_session.close()
    
    def _save_message(self, role: str, content: str):
        """Save message to conversation history"""
        message = ConversationHistory(
            session_id=self.session_id,
            role=role,
            content=content
        )
        self.db_session.add(message)
        self.db_session.commit()
        
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
    
    def greet(self) -> str:
        """Sapa pengguna"""
        if self.language == "id":
            greeting = f"""
Halo! Saya {self.name}, asisten pribadi AI Anda.

Saya dapat membantu Anda dengan:
1. 📅 Manajemen Jadwal - Atur dan kelola jadwal Anda
2. 💰 Manajemen Keuangan - Catat pemasukan dan pengeluaran
3. 📊 Literasi Data - Tips dan saran tentang data & statistik
4. 💼 Bantuan Pekerjaan - Kelola tugas dan produktivitas

Bagaimana saya bisa membantu Anda hari ini?
"""
        else:
            greeting = f"""
Hello! I'm {self.name}, your AI personal assistant.

I can help you with:
1. 📅 Schedule Management - Organize and manage your calendar
2. 💰 Finance Management - Track income and expenses
3. 📊 Data Literacy - Tips and advice on data & statistics
4. 💼 Work Assistant - Manage tasks and productivity

How can I help you today?
"""
        
        self._save_message("assistant", greeting)
        return greeting
    
    def process_command(self, user_input: str) -> str:
        """
        Proses perintah dari pengguna
        
        Args:
            user_input: Input dari pengguna
        
        Returns:
            Response dari assistant
        """
        self._save_message("user", user_input)
        
        # Simple command processing (dapat diperluas dengan NLP/LLM)
        user_input_lower = user_input.lower()
        
        # Schedule commands
        if any(word in user_input_lower for word in ["jadwal", "schedule", "kalender", "calendar"]):
            response = self._handle_schedule_query(user_input)
        
        # Finance commands
        elif any(word in user_input_lower for word in ["keuangan", "finance", "uang", "money", "pemasukan", "pengeluaran", "income", "expense", "saldo", "balance", "ringkasan", "summary"]):
            response = self._handle_finance_query(user_input)
        
        # Data/Statistics commands
        elif any(word in user_input_lower for word in ["data", "statistik", "statistics", "analisis", "analysis", "visualisasi", "visualization", "tips"]):
            response = self._handle_data_query(user_input)
        
        # Help command
        elif any(word in user_input_lower for word in ["help", "bantuan", "apa yang bisa", "what can"]):
            response = self.greet()
        
        else:
            response = self._default_response()
        
        self._save_message("assistant", response)
        return response
    
    def _handle_schedule_query(self, query: str) -> str:
        """Handle schedule-related queries"""
        query_lower = query.lower()
        
        if "hari ini" in query_lower or "today" in query_lower:
            schedules = self.schedule_manager.get_today_schedules()
            if not schedules:
                return "📅 Tidak ada jadwal untuk hari ini." if self.language == "id" else "📅 No schedule for today."
            
            response = "📅 Jadwal Hari Ini:\n\n" if self.language == "id" else "📅 Today's Schedule:\n\n"
            for schedule in schedules:
                response += f"• {schedule.start_time.strftime('%H:%M')} - {schedule.title}"
                if schedule.location:
                    response += f" ({schedule.location})"
                response += "\n"
            return response
        
        elif "minggu ini" in query_lower or "upcoming" in query_lower or "yang akan datang" in query_lower:
            schedules = self.schedule_manager.get_upcoming_schedules(days=7)
            if not schedules:
                return "📅 Tidak ada jadwal minggu ini." if self.language == "id" else "📅 No upcoming schedule this week."
            
            response = "📅 Jadwal Minggu Ini:\n\n" if self.language == "id" else "📅 This Week's Schedule:\n\n"
            for schedule in schedules:
                response += f"• {schedule.start_time.strftime('%d/%m %H:%M')} - {schedule.title}\n"
            return response
        
        elif "statistik" in query_lower or "stats" in query_lower:
            stats = self.schedule_manager.get_statistics()
            return f"""
📊 Statistik Jadwal:
• Total jadwal: {stats['total']}
• Selesai: {stats['completed']}
• Pending: {stats['pending']}
• Tingkat penyelesaian: {stats['completion_rate']:.1f}%
"""
        
        else:
            return "📅 Untuk melihat jadwal, coba:\n- 'jadwal hari ini'\n- 'jadwal minggu ini'\n- 'statistik jadwal'"
    
    def _handle_finance_query(self, query: str) -> str:
        """Handle finance-related queries"""
        query_lower = query.lower()
        
        if "saldo" in query_lower or "balance" in query_lower:
            balance = self.finance_manager.get_balance()
            currency = self.finance_manager.currency
            return f"💰 Saldo Anda: {currency} {balance:,.2f}"
        
        elif "ringkasan" in query_lower or "summary" in query_lower or "bulan ini" in query_lower:
            now = datetime.now()
            summary = self.finance_manager.get_monthly_summary(now.year, now.month)
            
            response = f"""
💰 Ringkasan Keuangan {summary['period']}:

📈 Pemasukan: {self.finance_manager.currency} {summary['total_income']:,.2f}
📉 Pengeluaran: {self.finance_manager.currency} {summary['total_expense']:,.2f}
💵 Saldo: {self.finance_manager.currency} {summary['balance']:,.2f}

Pengeluaran per Kategori:
"""
            for category, amount in summary['expense_by_category'].items():
                response += f"  • {category}: {self.finance_manager.currency} {amount:,.2f}\n"
            
            return response
        
        elif "statistik" in query_lower or "stats" in query_lower:
            stats = self.finance_manager.get_statistics(days=30)
            return f"""
📊 Statistik Keuangan (30 hari terakhir):

• Total pemasukan: {stats['income_count']} transaksi
• Total pengeluaran: {stats['expense_count']} transaksi
• Rata-rata pemasukan: {self.finance_manager.currency} {stats['avg_income']:,.2f}
• Rata-rata pengeluaran: {self.finance_manager.currency} {stats['avg_expense']:,.2f}
• Saldo: {self.finance_manager.currency} {stats['balance']:,.2f}
"""
        
        else:
            return "💰 Untuk melihat keuangan, coba:\n- 'saldo'\n- 'ringkasan bulan ini'\n- 'statistik keuangan'"
    
    def _handle_data_query(self, query: str) -> str:
        """Handle data/statistics queries"""
        query_lower = query.lower()
        
        # Check more specific queries first
        if "visualisasi" in query_lower or "visualization" in query_lower:
            suggestion = self.data_advisor.suggest_visualization("numeric")
            return f"""
📊 Saran Visualisasi Data:

Tipe Chart: {suggestion['chart_type']}
Alasan: {suggestion['reason']}
Library: {suggestion['library']}
"""
        
        elif "kategori" in query_lower or "categories" in query_lower:
            categories = self.data_advisor.get_all_categories()
            response = "📚 Kategori Tips yang Tersedia:\n\n"
            for i, cat in enumerate(categories, 1):
                response += f"{i}. {cat.replace('_', ' ').title()}\n"
            return response
        
        elif "tips" in query_lower or "saran" in query_lower:
            tip = self.data_advisor.get_random_tip()
            return f"💡 Tips Data & Statistik:\n\n{tip}"
        
        else:
            return "📊 Untuk tips data & statistik, coba:\n- 'tips data'\n- 'kategori tips'\n- 'saran visualisasi'"
    
    def _default_response(self) -> str:
        """Default response when command is not recognized"""
        if self.language == "id":
            return """
Maaf, saya belum memahami perintah tersebut. 

Coba gunakan perintah seperti:
• 'jadwal hari ini' - Lihat jadwal
• 'saldo' - Cek saldo keuangan
• 'tips data' - Dapatkan tips data & statistik
• 'bantuan' - Lihat semua fitur
"""
        else:
            return """
Sorry, I don't understand that command yet.

Try commands like:
• 'today's schedule' - View schedule
• 'balance' - Check financial balance
• 'data tips' - Get data & statistics tips
• 'help' - View all features
"""
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get conversation history for current session"""
        return self.conversation_history
