import pandas as pd
import numpy as np

# Sample Phillies player data
PhilliesPlayers = pd.DataFrame({
    'player_id': [571364, 593075, 545361, 669261, 571619],
    'player_name': ['Bryson Stott', 'J.T. Realmuto', 'Bryce Harper', 'Trea Turner', 'Rhys Hopkins'],
    'position': ['SS', 'C', 'DH', '2B', 'RF'],
    'games': [38, 37, 38, 38, 37],
    'ab': [132, 135, 140, 133, 142],
    'runs': [17, 18, 22, 25, 15],
    'hits': [34, 37, 41, 45, 32],
    'doubles': [6, 5, 8, 7, 4],
    'triples': [0, 0, 1, 0, 0],
    'hr': [3, 8, 12, 7, 2],
    'rbi': [19, 35, 42, 38, 14],
    'bb': [14, 15, 32, 18, 8],
    'so': [28, 30, 55, 25, 22],
    'ba': [0.258, 0.274, 0.293, 0.338, 0.225],
    'obp': [0.333, 0.361, 0.410, 0.411, 0.278],
    'slg': [0.409, 0.541, 0.664, 0.609, 0.345],
    'woba': [0.338, 0.392, 0.460, 0.464, 0.305],
    'war': [1.2, 2.5, 3.8, 2.9, 0.8]
})

# Sample game data
Games = pd.DataFrame({
    'game_id': ['GID_2026_05_23_phimia_1', 'GID_2026_05_22_phimia_1', 'GID_2026_05_21_phimia_1'],
    'game_date': ['2026-05-23', '2026-05-22', '2026-05-21'],
    'home_team': ['PHI', 'PHI', 'PHI'],
    'away_team': ['MIA', 'MIA', 'MIA'],
    'home_score': [5, 7, 4],
    'away_score': [2, 3, 5],
    'venue': ['Citizens Bank Park', 'Citizens Bank Park', 'Citizens Bank Park'],
    'attendance': [43210, 42500, 41800],
    'winning_pitcher': ['Aaron Nola', 'Seranthony Domínguez', 'Zach Eflin'],
    'losing_pitcher': ['José Salas', 'A.J. Puk', 'Trey Mayes'],
    'save_pitcher': ['Seranthony Domínguez', 'José Alvarado', None]
})

# Sample Statcast data (simplified)
StatcastData = pd.DataFrame({
    'pitch_id': range(1, 11),
    'game_date': ['2026-05-23'] * 10,
    'pitch_type': ['FF', 'CU', 'FF', 'SL', 'FF', 'CU', 'FF', 'SL', 'FF', 'CU'],
    'start_speed': [94.2, 78.5, 95.1, 85.3, 94.8, 79.2, 95.5, 86.1, 94.6, 78.8],
    'end_speed': [88.5, 72.1, 89.2, 79.5, 88.9, 72.8, 89.8, 80.2, 88.7, 72.5],
    'spin_rate': [2350, 1800, 2400, 1950, 2380, 1820, 2420, 1980, 2360, 1810],
    'spin_dir': [220, 150, 225, 160, 218, 148, 228, 162, 222, 152],
    'break_angle': [15.2, 12.8, 16.1, 18.5, 15.8, 13.2, 16.5, 19.0, 15.5, 12.5],
    'break_length': [2.1, 3.5, 2.3, 4.2, 2.0, 3.8, 2.4, 4.5, 2.2, 3.2],
    'plate_x': [0.1, -0.3, 0.2, 0.4, 0.15, -0.2, 0.25, 0.5, 0.12, -0.25],
    'plate_z': [3.2, 1.8, 3.5, 2.8, 3.3, 1.9, 3.6, 2.9, 3.4, 1.7],
    'pitch_num': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'batter_id': [571364, 593075, 545361, 669261, 571364, 593075, 545361, 669261, 571364, 593075],
    'pitcher_id': [502711, 502711, 502711, 502711, 502711, 502711, 502711, 502711, 502711, 502711],
    'type': ['X', 'B', 'X', 'S', 'X', 'B', 'X', 'S', 'X', 'B'],
    'description': ['Single', 'Ball', 'Double', 'Strike', 'Home Run', 'Ball', 'Single', 'Strike', 'Single', 'Ball'],
    'events': ['single', None, 'double', None, 'home_run', None, 'single', None, 'single', None],
    'launch_speed': [102.3, None, 98.1, None, 112.5, None, 95.2, None, 97.8, None],
    'launch_angle': [25, None, 15, None, 30, None, 18, None, 12, None],
    'total_distance': [105, None, 85, None, 415, None, 75, None, 65, None],
    'batter': ['Bryson Stott', 'J.T. Realmuto', 'Bryce Harper', 'Trea Turner', 'Bryson Stott', 'J.T. Realmuto', 'Bryce Harper', 'Trea Turner', 'Bryson Stott', 'J.T. Realmuto'],
    'pitcher': ['Aaron Nola', 'Aaron Nola', 'Aaron Nola', 'Aaron Nola', 'Aaron Nola', 'Aaron Nola', 'Aaron Nola', 'Aaron Nola', 'Aaron Nola', 'Aaron Nola'],
    'team': ['PHI', 'PHI', 'PHI', 'PHI', 'PHI', 'PHI', 'PHI', 'PHI', 'PHI', 'PHI']
})

# Sabermetric metrics
Sabermetrics = pd.DataFrame({
    'metric': ['wOBA', 'wRAA', 'WAR', 'FIP', 'xFIP', 'BB%', 'K%', 'SB%', 'OBP', 'SLG'],
    'phillies': [0.345, 42.3, 15.2, 3.42, 3.68, 8.5, 22.1, 78.9, 0.333, 0.415],
    'league_avg': [0.320, 0.0, 0.0, 4.20, 4.30, 8.2, 23.5, 75.0, 0.318, 0.402]
})

# Win probability data (simplified)
WinProbData = pd.DataFrame({
    'game_id': ['GID_2026_05_23_phimia_1'] * 18,
    'inning': [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9],
    'top': [True, False] * 9,
    'out': [0, 0, 0, 0, 0, 0, 0, 0, 0],
    'home_score': [0, 0, 1, 1, 2, 2, 3, 3, 5],
    'away_score': [0, 0, 0, 0, 0, 0, 0, 0, 2],
    'win_prob': [0.50, 0.50, 0.52, 0.48, 0.55, 0.45, 0.60, 0.40, 0.62]
})
