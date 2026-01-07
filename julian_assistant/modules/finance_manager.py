"""
Finance Manager Module
=======================
Modul untuk manajemen keuangan (pemasukan dan pengeluaran)
"""
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..core.database import db, FinanceTransaction
from ..core.config import config


class FinanceManager:
    """Manager untuk keuangan"""
    
    def __init__(self, session: Optional[Session] = None):
        """Initialize finance manager"""
        self.session = session or db.get_session()
        self.currency = config.DEFAULT_CURRENCY
    
    def add_income(
        self,
        amount: float,
        category: str,
        description: Optional[str] = None,
        date: Optional[datetime] = None,
        payment_method: Optional[str] = None,
        tags: Optional[str] = None
    ) -> FinanceTransaction:
        """
        Tambah pemasukan
        
        Args:
            amount: Jumlah uang
            category: Kategori (gaji, bonus, investasi, dll)
            description: Deskripsi
            date: Tanggal transaksi
            payment_method: Metode pembayaran
            tags: Tag (comma-separated)
        
        Returns:
            FinanceTransaction object
        """
        transaction = FinanceTransaction(
            transaction_type="income",
            amount=amount,
            category=category,
            description=description,
            date=date or datetime.now(),
            payment_method=payment_method,
            tags=tags,
            currency=self.currency
        )
        
        self.session.add(transaction)
        self.session.commit()
        self.session.refresh(transaction)
        
        return transaction
    
    def add_expense(
        self,
        amount: float,
        category: str,
        description: Optional[str] = None,
        date: Optional[datetime] = None,
        payment_method: Optional[str] = None,
        tags: Optional[str] = None
    ) -> FinanceTransaction:
        """
        Tambah pengeluaran
        
        Args:
            amount: Jumlah uang
            category: Kategori (makanan, transportasi, hiburan, dll)
            description: Deskripsi
            date: Tanggal transaksi
            payment_method: Metode pembayaran
            tags: Tag (comma-separated)
        
        Returns:
            FinanceTransaction object
        """
        transaction = FinanceTransaction(
            transaction_type="expense",
            amount=amount,
            category=category,
            description=description,
            date=date or datetime.now(),
            payment_method=payment_method,
            tags=tags,
            currency=self.currency
        )
        
        self.session.add(transaction)
        self.session.commit()
        self.session.refresh(transaction)
        
        return transaction
    
    def get_transaction(self, transaction_id: int) -> Optional[FinanceTransaction]:
        """Get transaction by ID"""
        return self.session.query(FinanceTransaction).filter(
            FinanceTransaction.id == transaction_id
        ).first()
    
    def get_transactions(
        self,
        transaction_type: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        category: Optional[str] = None
    ) -> List[FinanceTransaction]:
        """Dapatkan daftar transaksi dengan filter"""
        query = self.session.query(FinanceTransaction)
        
        if transaction_type:
            query = query.filter(FinanceTransaction.transaction_type == transaction_type)
        if start_date:
            query = query.filter(FinanceTransaction.date >= start_date)
        if end_date:
            query = query.filter(FinanceTransaction.date <= end_date)
        if category:
            query = query.filter(FinanceTransaction.category == category)
        
        return query.order_by(FinanceTransaction.date.desc()).all()
    
    def get_monthly_summary(self, year: int, month: int) -> Dict[str, Any]:
        """Dapatkan ringkasan keuangan bulanan"""
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)
        
        # Total income
        total_income = self.session.query(func.sum(FinanceTransaction.amount)).filter(
            FinanceTransaction.transaction_type == "income",
            FinanceTransaction.date >= start_date,
            FinanceTransaction.date < end_date
        ).scalar() or 0
        
        # Total expense
        total_expense = self.session.query(func.sum(FinanceTransaction.amount)).filter(
            FinanceTransaction.transaction_type == "expense",
            FinanceTransaction.date >= start_date,
            FinanceTransaction.date < end_date
        ).scalar() or 0
        
        # Balance
        balance = total_income - total_expense
        
        # Expense by category
        expense_by_category = self.session.query(
            FinanceTransaction.category,
            func.sum(FinanceTransaction.amount).label("total")
        ).filter(
            FinanceTransaction.transaction_type == "expense",
            FinanceTransaction.date >= start_date,
            FinanceTransaction.date < end_date
        ).group_by(FinanceTransaction.category).all()
        
        return {
            "period": f"{year}-{month:02d}",
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": balance,
            "expense_by_category": {cat: float(total) for cat, total in expense_by_category}
        }
    
    def get_balance(self) -> float:
        """Dapatkan saldo total (total pemasukan - total pengeluaran)"""
        total_income = self.session.query(func.sum(FinanceTransaction.amount)).filter(
            FinanceTransaction.transaction_type == "income"
        ).scalar() or 0
        
        total_expense = self.session.query(func.sum(FinanceTransaction.amount)).filter(
            FinanceTransaction.transaction_type == "expense"
        ).scalar() or 0
        
        return total_income - total_expense
    
    def delete_transaction(self, transaction_id: int) -> bool:
        """Hapus transaksi"""
        transaction = self.get_transaction(transaction_id)
        if not transaction:
            return False
        
        self.session.delete(transaction)
        self.session.commit()
        return True
    
    def get_statistics(self, days: int = 30) -> Dict[str, Any]:
        """Dapatkan statistik keuangan"""
        start_date = datetime.now() - timedelta(days=days)
        
        transactions = self.get_transactions(start_date=start_date)
        
        income_count = sum(1 for t in transactions if t.transaction_type == "income")
        expense_count = sum(1 for t in transactions if t.transaction_type == "expense")
        
        total_income = sum(t.amount for t in transactions if t.transaction_type == "income")
        total_expense = sum(t.amount for t in transactions if t.transaction_type == "expense")
        
        avg_income = total_income / income_count if income_count > 0 else 0
        avg_expense = total_expense / expense_count if expense_count > 0 else 0
        
        return {
            "period_days": days,
            "income_count": income_count,
            "expense_count": expense_count,
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": total_income - total_expense,
            "avg_income": avg_income,
            "avg_expense": avg_expense
        }
