# Julian Personal Assistant - AI Agent

🤖 Asisten pribadi AI yang membantu Anda dalam manajemen jadwal, keuangan, dan memberikan saran literasi data & statistik.

> **📚 Dokumentasi Lengkap**:
> - 📖 [SUMMARY.md](SUMMARY.md) - **Jawaban lengkap untuk problem statement**
> - 🏗️ [SYSTEMATICS.md](SYSTEMATICS.md) - Penjelasan detail sistematika AI Agent
> - 📐 [ARCHITECTURE.md](ARCHITECTURE.md) - Arsitektur sistem dan design patterns
> - 📋 [API.md](API.md) - Referensi API lengkap
> - ⚡ [QUICKSTART.md](QUICKSTART.md) - Panduan cepat memulai

## 📋 Fitur Utama

### 1. 📅 Manajemen Jadwal
- Membuat dan mengelola jadwal/kalender
- Melihat jadwal harian dan mingguan
- Cek konflik jadwal
- Statistik penyelesaian tugas

### 2. 💰 Manajemen Keuangan
- Catat pemasukan (income)
- Catat pengeluaran (expense)
- Lihat saldo total
- Ringkasan keuangan bulanan
- Statistik keuangan dengan kategori

### 3. 📊 Literasi Data & Statistik
- Tips dan saran tentang data science
- Panduan visualisasi data
- Analisis DataFrame pandas
- Statistik deskriptif
- Rekomendasi best practices

### 4. 💼 Bantuan Pekerjaan
- Manajemen tugas kerja
- Tracking produktivitas
- Integrasi dengan semua modul

## 🏗️ Arsitektur Sistem

```
julian-personal-assistant/
├── julian_assistant/           # Package utama
│   ├── core/                  # Core components
│   │   ├── agent.py          # Main AI Agent
│   │   ├── config.py         # Configuration
│   │   └── database.py       # Database models
│   ├── modules/              # Feature modules
│   │   ├── schedule_manager.py   # Schedule management
│   │   ├── finance_manager.py    # Finance management
│   │   └── data_advisor.py       # Data literacy advisor
│   └── utils/                # Utilities
│       └── helpers.py        # Helper functions
├── examples/                 # Usage examples
│   └── basic_usage.py
├── tests/                    # Unit tests
├── main.py                   # CLI interface
├── requirements.txt          # Dependencies
└── README.md                # Documentation
```

## 🚀 Instalasi

### 1. Clone Repository

```bash
git clone https://github.com/FikJul/julian-personal-assistant.git
cd julian-personal-assistant
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Konfigurasi

Copy file `.env.example` ke `.env` dan sesuaikan konfigurasi:

```bash
cp .env.example .env
```

Edit file `.env`:

```env
# OpenAI API Configuration (opsional, untuk fitur AI lanjutan)
OPENAI_API_KEY=your_api_key_here

# Database Configuration
DATABASE_URL=sqlite:///julian_assistant.db

# Agent Configuration
AGENT_NAME=Julian
LANGUAGE=id  # id untuk Indonesian, en untuk English
TIMEZONE=Asia/Jakarta
DEFAULT_CURRENCY=IDR
```

## 💻 Penggunaan

### Cara 1: Interactive CLI

Jalankan aplikasi dalam mode interaktif:

```bash
python main.py
```

Kemudian gunakan perintah seperti:
- `jadwal hari ini` - Lihat jadwal hari ini
- `saldo` - Cek saldo keuangan
- `tips data` - Dapatkan tips data & statistik
- `bantuan` - Lihat semua perintah
- `exit` - Keluar

### Cara 2: Run Example

```bash
python examples/basic_usage.py
```

### Cara 3: Import sebagai Library

```python
from julian_assistant import JulianAssistant

# Buat instance assistant
with JulianAssistant() as assistant:
    # Sapa pengguna
    print(assistant.greet())
    
    # Proses perintah
    response = assistant.process_command("jadwal hari ini")
    print(response)
```

## 📚 Contoh Penggunaan Detail

### Manajemen Jadwal

```python
from julian_assistant import JulianAssistant
from datetime import datetime, timedelta

with JulianAssistant() as assistant:
    # Buat jadwal baru
    tomorrow = datetime.now() + timedelta(days=1)
    schedule = assistant.schedule_manager.create_schedule(
        title="Meeting dengan Tim",
        start_time=tomorrow.replace(hour=10, minute=0),
        end_time=tomorrow.replace(hour=11, minute=0),
        description="Diskusi progress proyek",
        location="Ruang Meeting A",
        priority="high"
    )
    
    # Lihat jadwal hari ini
    today_schedules = assistant.schedule_manager.get_today_schedules()
    
    # Update jadwal
    assistant.schedule_manager.update_schedule(
        schedule.id,
        status="completed"
    )
```

### Manajemen Keuangan

```python
from julian_assistant import JulianAssistant

with JulianAssistant() as assistant:
    # Tambah pemasukan
    income = assistant.finance_manager.add_income(
        amount=5000000,
        category="Gaji",
        description="Gaji bulan Januari",
        payment_method="bank_transfer"
    )
    
    # Tambah pengeluaran
    expense = assistant.finance_manager.add_expense(
        amount=500000,
        category="Makanan",
        description="Belanja bulanan",
        payment_method="cash"
    )
    
    # Cek saldo
    balance = assistant.finance_manager.get_balance()
    print(f"Saldo: IDR {balance:,.2f}")
    
    # Ringkasan bulanan
    summary = assistant.finance_manager.get_monthly_summary(2025, 1)
    print(summary)
```

### Literasi Data

```python
from julian_assistant import JulianAssistant
import pandas as pd

with JulianAssistant() as assistant:
    # Dapatkan tips acak
    tip = assistant.data_advisor.get_random_tip()
    print(tip)
    
    # Dapatkan tips spesifik kategori
    tips = assistant.data_advisor.get_tips_by_category("python_pandas")
    
    # Analisis DataFrame
    df = pd.DataFrame({
        'A': [1, 2, 3, 4, 5],
        'B': [10, 20, 30, 40, 50]
    })
    analysis = assistant.data_advisor.analyze_dataframe(df)
    print(analysis)
    
    # Saran visualisasi
    suggestion = assistant.data_advisor.suggest_visualization("time_series")
    print(suggestion)
```

## 🎯 Perintah yang Tersedia

### Jadwal
- `jadwal hari ini` - Lihat jadwal hari ini
- `jadwal minggu ini` - Lihat jadwal 7 hari ke depan
- `statistik jadwal` - Lihat statistik jadwal

### Keuangan
- `saldo` - Cek saldo total
- `ringkasan bulan ini` - Ringkasan keuangan bulan berjalan
- `statistik keuangan` - Statistik 30 hari terakhir

### Data & Statistik
- `tips data` - Dapatkan tips acak
- `kategori tips` - Lihat semua kategori tips
- `saran visualisasi` - Saran untuk visualisasi data

### Umum
- `bantuan` / `help` - Lihat bantuan
- `exit` / `quit` - Keluar dari aplikasi

## 🗄️ Database Schema

Aplikasi menggunakan SQLite dengan schema berikut:

### Schedules
- id, title, description, start_time, end_time, location, priority, status, reminder_sent

### FinanceTransactions
- id, transaction_type, category, amount, currency, description, date, payment_method, tags

### WorkTasks
- id, title, description, priority, status, due_date, estimated_hours, actual_hours, tags

### ConversationHistory
- id, session_id, role, content, timestamp

## 🛠️ Teknologi yang Digunakan

- **Python 3.8+** - Bahasa pemrograman utama
- **SQLAlchemy** - ORM untuk database
- **Pandas & NumPy** - Analisis data dan statistik
- **Rich** - CLI interface yang cantik
- **Python-dotenv** - Manajemen environment variables
- **PyTZ** - Timezone handling

## 🔮 Pengembangan Masa Depan

- [ ] Integrasi dengan LLM (GPT-4) untuk pemrosesan natural language
- [ ] Notifikasi otomatis untuk jadwal
- [ ] Export data ke Excel/CSV
- [ ] Visualisasi grafik keuangan
- [ ] Mobile app integration
- [ ] Cloud sync
- [ ] Voice assistant integration
- [ ] Task automation dengan AI

## 🤝 Kontribusi

Kontribusi sangat diterima! Silakan:

1. Fork repository ini
2. Buat branch fitur (`git checkout -b fitur-baru`)
3. Commit perubahan (`git commit -m 'Tambah fitur baru'`)
4. Push ke branch (`git push origin fitur-baru`)
5. Buat Pull Request

## 📝 Lisensi

MIT License - Lihat file LICENSE untuk detail

## 👨‍💻 Author

**FikJul**

---

Made with ❤️ using Python