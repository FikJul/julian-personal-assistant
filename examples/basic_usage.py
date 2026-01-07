"""
Example usage of Julian Personal Assistant
"""
from datetime import datetime, timedelta
from julian_assistant import JulianAssistant


def main():
    """Main example function"""
    
    print("=" * 60)
    print("Julian Personal Assistant - Example Usage")
    print("=" * 60)
    print()
    
    # Create assistant instance
    with JulianAssistant() as assistant:
        # Greet user
        print(assistant.greet())
        print("\n" + "=" * 60 + "\n")
        
        # Example 1: Check today's schedule
        print("Example 1: Checking today's schedule")
        response = assistant.process_command("jadwal hari ini")
        print(response)
        print("\n" + "=" * 60 + "\n")
        
        # Example 2: Check financial balance
        print("Example 2: Checking financial balance")
        response = assistant.process_command("saldo")
        print(response)
        print("\n" + "=" * 60 + "\n")
        
        # Example 3: Get data tips
        print("Example 3: Getting data & statistics tips")
        response = assistant.process_command("tips data")
        print(response)
        print("\n" + "=" * 60 + "\n")
        
        # Example 4: Add sample schedule
        print("Example 4: Adding sample schedule data")
        tomorrow = datetime.now() + timedelta(days=1)
        schedule = assistant.schedule_manager.create_schedule(
            title="Meeting dengan Tim",
            start_time=tomorrow.replace(hour=10, minute=0, second=0),
            end_time=tomorrow.replace(hour=11, minute=0, second=0),
            description="Diskusi progress proyek",
            location="Ruang Meeting A",
            priority="high"
        )
        print(f"✅ Jadwal berhasil ditambahkan: {schedule.title}")
        print("\n" + "=" * 60 + "\n")
        
        # Example 5: Add sample finance transactions
        print("Example 5: Adding sample financial transactions")
        
        # Add income
        income = assistant.finance_manager.add_income(
            amount=5000000,
            category="Gaji",
            description="Gaji bulan ini",
            payment_method="bank_transfer"
        )
        print(f"✅ Pemasukan ditambahkan: {income.category} - IDR {income.amount:,.2f}")
        
        # Add expenses
        expense1 = assistant.finance_manager.add_expense(
            amount=500000,
            category="Makanan",
            description="Groceries",
            payment_method="cash"
        )
        print(f"✅ Pengeluaran ditambahkan: {expense1.category} - IDR {expense1.amount:,.2f}")
        
        expense2 = assistant.finance_manager.add_expense(
            amount=200000,
            category="Transportasi",
            description="Bensin dan parkir",
            payment_method="cash"
        )
        print(f"✅ Pengeluaran ditambahkan: {expense2.category} - IDR {expense2.amount:,.2f}")
        
        print("\n" + "=" * 60 + "\n")
        
        # Example 6: Check updated balance
        print("Example 6: Checking updated balance")
        response = assistant.process_command("saldo")
        print(response)
        print("\n" + "=" * 60 + "\n")
        
        # Example 7: Get monthly summary
        print("Example 7: Getting monthly financial summary")
        response = assistant.process_command("ringkasan bulan ini")
        print(response)
        print("\n" + "=" * 60 + "\n")
        
        # Example 8: Get schedule statistics
        print("Example 8: Getting schedule statistics")
        response = assistant.process_command("statistik jadwal")
        print(response)
        print("\n" + "=" * 60 + "\n")
        
        # Example 9: Get data visualization suggestions
        print("Example 9: Getting data visualization suggestions")
        response = assistant.process_command("saran visualisasi")
        print(response)
        print("\n" + "=" * 60 + "\n")
        
        print("✅ Example completed successfully!")


if __name__ == "__main__":
    main()
