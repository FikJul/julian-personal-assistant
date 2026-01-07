"""
Unit tests for Data Advisor
"""
import unittest
import pandas as pd
import numpy as np
from julian_assistant.modules.data_advisor import DataAdvisor


class TestDataAdvisor(unittest.TestCase):
    """Test cases for DataAdvisor"""
    
    def setUp(self):
        """Set up test advisor"""
        self.advisor = DataAdvisor()
    
    def test_get_random_tip(self):
        """Test getting random tip"""
        tip = self.advisor.get_random_tip()
        self.assertIsNotNone(tip)
        self.assertIsInstance(tip, str)
        self.assertGreater(len(tip), 0)
    
    def test_get_random_tip_by_category(self):
        """Test getting random tip from specific category"""
        tip = self.advisor.get_random_tip(category="python_pandas")
        self.assertIsNotNone(tip)
        self.assertIn("df.", tip)  # Should be pandas-related
    
    def test_get_tips_by_category(self):
        """Test getting all tips from category"""
        tips = self.advisor.get_tips_by_category("statistik_dasar")
        self.assertIsInstance(tips, list)
        self.assertGreater(len(tips), 0)
    
    def test_get_all_categories(self):
        """Test getting all categories"""
        categories = self.advisor.get_all_categories()
        self.assertIsInstance(categories, list)
        self.assertIn("statistik_dasar", categories)
        self.assertIn("visualisasi_data", categories)
        self.assertIn("python_pandas", categories)
    
    def test_analyze_dataframe(self):
        """Test DataFrame analysis"""
        # Create test DataFrame
        df = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': [10, 20, 30, 40, 50],
            'C': ['a', 'b', 'c', 'd', 'e']
        })
        
        analysis = self.advisor.analyze_dataframe(df)
        
        self.assertEqual(analysis['shape'], (5, 3))
        self.assertIn('A', analysis['columns'])
        self.assertIn('B', analysis['columns'])
        self.assertIn('numeric_summary', analysis)
        self.assertIn('recommendations', analysis)
    
    def test_analyze_dataframe_with_missing_values(self):
        """Test DataFrame analysis with missing values"""
        df = pd.DataFrame({
            'A': [1, 2, None, 4, 5],
            'B': [10, None, 30, 40, 50]
        })
        
        analysis = self.advisor.analyze_dataframe(df)
        
        self.assertGreater(len(analysis['recommendations']), 0)
        # Should recommend handling missing values
        any_missing_recommendation = any(
            'missing' in rec.lower() 
            for rec in analysis['recommendations']
        )
        self.assertTrue(any_missing_recommendation)
    
    def test_suggest_visualization_numeric(self):
        """Test visualization suggestion for numeric data"""
        suggestion = self.advisor.suggest_visualization("numeric")
        
        self.assertIn('chart_type', suggestion)
        self.assertIn('reason', suggestion)
        self.assertIn('library', suggestion)
        self.assertIn('Histogram', suggestion['chart_type'])
    
    def test_suggest_visualization_categorical(self):
        """Test visualization suggestion for categorical data"""
        suggestion = self.advisor.suggest_visualization("categorical", num_categories=5)
        
        self.assertIn('chart_type', suggestion)
        self.assertIn('Chart', suggestion['chart_type'])
    
    def test_suggest_visualization_time_series(self):
        """Test visualization suggestion for time series"""
        suggestion = self.advisor.suggest_visualization("time_series")
        
        self.assertIn('chart_type', suggestion)
        self.assertIn('Line Chart', suggestion['chart_type'])
    
    def test_calculate_basic_stats(self):
        """Test basic statistics calculation"""
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        stats = self.advisor.calculate_basic_stats(data)
        
        self.assertEqual(stats['count'], 10)
        self.assertEqual(stats['mean'], 5.5)
        self.assertEqual(stats['median'], 5.5)
        self.assertEqual(stats['min'], 1.0)
        self.assertEqual(stats['max'], 10.0)
    
    def test_calculate_basic_stats_empty(self):
        """Test basic statistics with empty list"""
        stats = self.advisor.calculate_basic_stats([])
        self.assertEqual(stats, {})


if __name__ == '__main__':
    unittest.main()
