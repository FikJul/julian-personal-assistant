"""
Data Advisor Module
===================
Modul untuk memberikan saran literasi data dan statistik
"""
from typing import List, Dict, Any, Optional
import random
import pandas as pd
import numpy as np


class DataAdvisor:
    """Advisor untuk literasi data dan statistik"""
    
    def __init__(self):
        """Initialize data advisor"""
        self.tips_library = self._load_tips_library()
    
    def _load_tips_library(self) -> Dict[str, List[str]]:
        """Load library of data literacy tips"""
        return {
            "statistik_dasar": [
                "Mean (rata-rata) adalah jumlah total dibagi dengan jumlah data",
                "Median adalah nilai tengah ketika data diurutkan",
                "Modus adalah nilai yang paling sering muncul",
                "Standard deviation mengukur seberapa tersebar data dari rata-rata",
                "Variance adalah kuadrat dari standard deviation"
            ],
            "visualisasi_data": [
                "Gunakan bar chart untuk membandingkan kategori",
                "Line chart cocok untuk menunjukkan tren waktu",
                "Pie chart baik untuk menampilkan proporsi, tapi terbatas untuk <7 kategori",
                "Scatter plot berguna untuk melihat korelasi antar variabel",
                "Histogram menunjukkan distribusi data numerik"
            ],
            "analisis_data": [
                "Selalu cek missing values sebelum analisis",
                "Normalisasi data penting untuk algoritma machine learning",
                "Correlation tidak selalu berarti causation",
                "Outlier bisa mempengaruhi hasil analisis secara signifikan",
                "Cross-validation penting untuk menghindari overfitting"
            ],
            "data_cleaning": [
                "Hapus atau imputasi missing values dengan bijak",
                "Deteksi dan handle outliers dengan metode statistik",
                "Standardisasi format data (tanggal, angka, teks)",
                "Validasi konsistensi data antar kolom",
                "Hapus duplikasi data yang tidak diperlukan"
            ],
            "python_pandas": [
                "df.describe() memberikan statistik deskriptif cepat",
                "df.info() menampilkan tipe data dan missing values",
                "df.groupby() sangat powerful untuk agregasi data",
                "df.merge() untuk menggabungkan DataFrame",
                "df.apply() untuk custom transformations"
            ]
        }
    
    def get_random_tip(self, category: Optional[str] = None) -> str:
        """
        Dapatkan tips acak tentang data dan statistik
        
        Args:
            category: Kategori tips (optional)
        
        Returns:
            String berisi tip
        """
        if category and category in self.tips_library:
            tips = self.tips_library[category]
        else:
            # Get random category
            all_tips = []
            for tips_list in self.tips_library.values():
                all_tips.extend(tips_list)
            tips = all_tips
        
        return random.choice(tips)
    
    def get_tips_by_category(self, category: str) -> List[str]:
        """Dapatkan semua tips dari kategori tertentu"""
        return self.tips_library.get(category, [])
    
    def get_all_categories(self) -> List[str]:
        """Dapatkan daftar semua kategori tips"""
        return list(self.tips_library.keys())
    
    def analyze_dataframe(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analisis DataFrame dan berikan insight
        
        Args:
            df: Pandas DataFrame
        
        Returns:
            Dictionary berisi analisis dan saran
        """
        analysis = {
            "shape": df.shape,
            "columns": list(df.columns),
            "dtypes": df.dtypes.to_dict(),
            "missing_values": df.isnull().sum().to_dict(),
            "numeric_summary": {},
            "recommendations": []
        }
        
        # Numeric columns analysis
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            analysis["numeric_summary"] = df[numeric_cols].describe().to_dict()
        
        # Generate recommendations
        missing_count = df.isnull().sum().sum()
        if missing_count > 0:
            analysis["recommendations"].append(
                f"Terdapat {missing_count} missing values. Pertimbangkan untuk imputasi atau hapus baris."
            )
        
        # Check for duplicates
        duplicate_count = df.duplicated().sum()
        if duplicate_count > 0:
            analysis["recommendations"].append(
                f"Terdapat {duplicate_count} baris duplikat. Pertimbangkan untuk menghapusnya."
            )
        
        # Check for potential outliers in numeric columns
        for col in numeric_cols:
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            outliers = df[(df[col] < q1 - 1.5 * iqr) | (df[col] > q3 + 1.5 * iqr)]
            if len(outliers) > 0:
                analysis["recommendations"].append(
                    f"Kolom '{col}' memiliki {len(outliers)} potential outliers."
                )
        
        return analysis
    
    def suggest_visualization(self, data_type: str, num_categories: int = 1) -> Dict[str, str]:
        """
        Sarankan jenis visualisasi berdasarkan tipe data
        
        Args:
            data_type: Tipe data (numeric, categorical, time_series, bivariate)
            num_categories: Jumlah kategori (untuk categorical data)
        
        Returns:
            Dictionary dengan saran visualisasi
        """
        suggestions = {
            "numeric": {
                "chart_type": "Histogram atau Box Plot",
                "reason": "Untuk melihat distribusi dan outliers data numerik",
                "library": "matplotlib, seaborn, atau plotly"
            },
            "categorical": {
                "chart_type": "Bar Chart" if num_categories > 7 else "Pie Chart atau Bar Chart",
                "reason": "Untuk membandingkan kategori atau melihat proporsi",
                "library": "matplotlib, seaborn, atau plotly"
            },
            "time_series": {
                "chart_type": "Line Chart",
                "reason": "Untuk melihat tren dan pola temporal",
                "library": "matplotlib, seaborn, atau plotly"
            },
            "bivariate": {
                "chart_type": "Scatter Plot",
                "reason": "Untuk melihat korelasi antar dua variabel",
                "library": "matplotlib, seaborn, atau plotly"
            }
        }
        
        return suggestions.get(data_type, {
            "chart_type": "Tergantung pada data",
            "reason": "Analisis lebih lanjut diperlukan",
            "library": "matplotlib, seaborn, atau plotly"
        })
    
    def calculate_basic_stats(self, data: List[float]) -> Dict[str, float]:
        """
        Hitung statistik dasar dari list angka
        
        Args:
            data: List of numbers
        
        Returns:
            Dictionary dengan statistik dasar
        """
        if not data:
            return {}
        
        arr = np.array(data)
        
        return {
            "count": len(arr),
            "mean": float(np.mean(arr)),
            "median": float(np.median(arr)),
            "std": float(np.std(arr)),
            "min": float(np.min(arr)),
            "max": float(np.max(arr)),
            "q25": float(np.percentile(arr, 25)),
            "q75": float(np.percentile(arr, 75))
        }
