# Quick Start Guide - Julian Personal Assistant

## Instalasi Cepat

```bash
# 1. Clone repository
git clone https://github.com/FikJul/julian-personal-assistant.git
cd julian-personal-assistant

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Opsional) Setup environment
cp .env.example .env
# Edit .env jika ingin mengkustomisasi

# 4. Install package
pip install -e .

# 5. Jalankan!
python main.py
```

## Penggunaan Dasar

### 1. Mode Interaktif (CLI)

```bash
python main.py
```

Setelah aplikasi berjalan, coba perintah berikut:

```
You> jadwal hari ini
Julian> 📅 Tidak ada jadwal untuk hari ini.

You> saldo
Julian> 💰 Saldo Anda: IDR 0.00

You> tips data
Julian> 💡 Tips Data & Statistik:
        Mean (rata-rata) adalah jumlah total dibagi dengan jumlah data

You> bantuan
Julian> [Menampilkan semua fitur yang tersedia]
```

### 2. Jalankan Example Script

```bash
python examples/basic_usage.py
```

Script ini akan:
- Membuat contoh jadwal
- Menambah transaksi keuangan
- Menampilkan berbagai statistik
- Memberikan tips data

### 3. Gunakan sebagai Library Python

```python
from julian_assistant import JulianAssistant
from datetime import datetime, timedelta

# Buat assistant
with JulianAssistant() as assistant:
    # Tambah jadwal
    tomorrow = datetime.now() + timedelta(days=1)
    assistant.schedule_manager.create_schedule(
        title="Meeting Penting",
        start_time=tomorrow.replace(hour=14, minute=0),
        priority="high"
    )
    
    # Tambah transaksi
    assistant.finance_manager.add_income(
        amount=5000000,
        category="Gaji"
    )
    
    # Dapatkan tips
    tip = assistant.data_advisor.get_random_tip()
    print(tip)
```

## Perintah yang Sering Digunakan

### Jadwal
```
jadwal hari ini          # Lihat jadwal hari ini
jadwal minggu ini        # Lihat jadwal 7 hari ke depan
statistik jadwal         # Statistik penyelesaian jadwal
```

### Keuangan
```
saldo                    # Cek saldo total
ringkasan bulan ini      # Ringkasan keuangan bulanan
statistik keuangan       # Statistik 30 hari terakhir
```

### Data & Statistik
```
tips data                # Tips acak
kategori tips            # Lihat kategori tips
saran visualisasi        # Saran visualisasi data
```

## Menambahkan Data

### Cara 1: Melalui Code

```python
from julian_assistant import JulianAssistant

with JulianAssistant() as assistant:
    # Tambah jadwal
    from datetime import datetime
    assistant.schedule_manager.create_schedule(
        title="Rapat Tim",
        start_time=datetime(2026, 1, 15, 10, 0),
        end_time=datetime(2026, 1, 15, 11, 0),
        location="Zoom",
        priority="high"
    )
    
    # Tambah pemasukan
    assistant.finance_manager.add_income(
        amount=5000000,
        category="Gaji",
        description="Gaji Januari 2026"
    )
    
    # Tambah pengeluaran
    assistant.finance_manager.add_expense(
        amount=500000,
        category="Makanan",
        description="Groceries bulan ini"
    )
```

### Cara 2: Menggunakan Database Langsung

Data disimpan di SQLite database `julian_assistant.db`. Anda bisa mengaksesnya dengan tools seperti:
- DB Browser for SQLite
- DBeaver
- SQLite CLI

## Tips & Trik

### 1. Gunakan dengan Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

### 2. Backup Database

```bash
cp julian_assistant.db julian_assistant.db.backup
```

### 3. Reset Database

```bash
rm julian_assistant.db
# Database akan otomatis dibuat ulang saat aplikasi dijalankan
```

### 4. Custom Configuration

Edit `.env` untuk mengubah:
- Nama asisten
- Bahasa (id/en)
- Timezone
- Currency

```env
AGENT_NAME=MyAssistant
LANGUAGE=en
TIMEZONE=Asia/Jakarta
DEFAULT_CURRENCY=USD
```

## Troubleshooting

### Error: ModuleNotFoundError

```bash
# Pastikan dependencies terinstall
pip install -r requirements.txt

# Atau install package dalam mode development
pip install -e .
```

### Error: Database locked

```bash
# Tutup semua koneksi aktif
# Restart aplikasi
```

### Ingin menghapus semua data

```bash
# Hapus database
rm julian_assistant.db

# Atau reset tables via Python
from julian_assistant.core.database import db, Base
Base.metadata.drop_all(db.engine)
Base.metadata.create_all(db.engine)
```

## Next Steps

1. ✅ Baca [README.md](README.md) untuk dokumentasi lengkap
2. ✅ Baca [ARCHITECTURE.md](ARCHITECTURE.md) untuk memahami arsitektur
3. ✅ Jalankan tests: `python -m unittest discover tests/`
4. ✅ Customize sesuai kebutuhan Anda!

## Pengembangan Lebih Lanjut

Jika ingin menambah fitur:
1. Buat module baru di `julian_assistant/modules/`
2. Tambahkan handler di `julian_assistant/core/agent.py`
3. Buat tests di `tests/`
4. Update dokumentasi

Lihat [ARCHITECTURE.md](ARCHITECTURE.md) untuk panduan pengembangan detail.

## Support

Jika menemukan bug atau punya ide fitur:
1. Buka issue di GitHub
2. Atau buat Pull Request

---

Happy organizing! 🚀
