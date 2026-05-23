import pandas as pd
import numpy as np
from phillies_intel_hub import PhilliesAnalytics, Visualizations
from phillies_intel_hub.data import sample_data

# Initialize analytics and visualizations
analytics = PhilliesAnalytics()
viz = Visualizations()

# Load sample data
games = sample_data.Games
players = sample_data.PhilliesPlayers
statcast = sample_data.StatcastData
win_prob = sample_data.WinProbData

# Example 1: Game Tracking
print("=== Phillies Game Tracking ===")
print(f"Games loaded: {len(games)}")
for _, game in games.iterrows():
    print(f"  {game['game_date']}: {game['home_team']} {game['home_score']} vs {game['away_team']} {game['away_score']}")

# Example 2: Player Statistics
print("\n=== Top Phillies Players ===")
for _, player in players.iterrows():
    print(f"  {player['player_name']} ({player['position']}): "
          f"BA {player['ba']:.3f}, OBP {player['obp']:.3f}, SLG {player['slg']:.3f}, "
          f"HR {player['hr']}, WAR {player['war']}")

# Example 3: Sabermetric Analysis
print("\n=== Sabermetric Insights ===")
for _, metric in sample_data.Sabermetrics.iterrows():
    phillies_val = metric['phillies']
    league_val = metric['league_avg']
    diff = phillies_val - league_val
    print(f"  {metric['metric']}: PHI {phillies_val:.2f} (League: {league_val:.2f}) {'+' if diff > 0 else ''}{diff:.2f}")

# Example 4: Win Probability
print("\n=== Win Probability Analysis ===")
for _, wp in win_prob.iterrows():
    team = 'PHI' if wp['top'] else 'OPP'
    print(f"  Inning {wp['inning']}, {'Top' if wp['top'] else 'Bottom'}: "
          f"Score {win_prob.iloc[int((wp.name+1)/2)]['home_score'] if not wp['top'] else win_prob.iloc[int(wp.name/2)]['away_score']}-"
          f"{win_prob.iloc[int((wp.name+1)/2)]['away_score'] if not wp['top'] else win_prob.iloc[int(wp.name/2)]['home_score']} - "
          f"Win Prob: {wp['win_prob']:.2%}")

# Example 5: Interactive Visualizations
print("\n=== Interactive Visualizations ===")

# Win probability chart
fig_wp = viz.plot_win_probability(win_prob, 'GID_2026_05_23_phimia_1')
print("  - Win probability chart created")

# Exit velocity histogram
fig_ev = viz.plot_exit_velocity(statcast)
print("  - Exit velocity distribution created")

# Launch angle histogram
fig_la = viz.plot_launch_angle(statcast)
print("  - Launch angle distribution created")

# Pitch tracking
fig_pitch = viz.plot_pitch_tracking(statcast)
print("  - Pitch tracking visualization created")

# Player trend
fig_trend = viz.plot_player_trend(players, 'war')
print("  - Player trend analysis created")

# League comparison
fig_comp = viz.plot_league_comparison(players, 'woba')
print("  - League comparison chart created")

print("\n=== Analytics Complete ===")
print("All visualizations can be saved with fig.write_html() or fig.write_image()")
