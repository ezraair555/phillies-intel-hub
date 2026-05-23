import unittest
import pandas as pd
import numpy as np
from phillies_intel_hub import PhilliesAnalytics, Visualizations

class TestPhilliesAnalytics(unittest.TestCase):
    def test_init(self):
        analytics = PhilliesAnalytics()
        self.assertEqual(analytics.phillies_team_id, 143)
    
    def test_get_games(self):
        analytics = PhilliesAnalytics()
        games = analytics.get_games('2026-05-01', '2026-05-02')
        # Just verify it returns a DataFrame (may be empty if API fails)
        self.assertIsInstance(games, pd.DataFrame)
    
    def test_statcast_data_structure(self):
        analytics = PhilliesAnalytics()
        statcast = analytics.get_statcast_data('2026-05-23')
        self.assertIsInstance(statcast, pd.DataFrame)

class TestVisualizations(unittest.TestCase):
    def test_init(self):
        viz = Visualizations()
        self.assertEqual(viz.phillies_color, '#006341')
    
    def test_plot_creation(self):
        viz = Visualizations()
        # Create a sample DataFrame
        data = pd.DataFrame({
            'inning': [1, 2, 3],
            'team': ['PHI', 'PHI', 'PHI'],
            'win_prob': [0.5, 0.55, 0.6]
        })
        fig = viz.plot_win_probability(data)
        self.assertIsNotNone(fig)

if __name__ == '__main__':
    unittest.main()
