import pandas as pd
import numpy as np
from phillies_intel_hub import PhilliesAnalytics, Visualizations
from phillies_intel_hub.data import sample_data

def main():
    analytics = PhilliesAnalytics()
    viz = Visualizations()
    
    # Load data
    players = sample_data.PhillysPlayers
    statcast = sample_data.StatcastData
    win_prob = sample_data.WinProbData
    
    # Player Analysis
    print("=== Phillies Player Analysis ===\n")
    
    # Hitters
    print("--- Hitters ---")
    hitters = players[players['position'].isin(['SS', '2B', 'RF', '1B', 'LF', 'CF'])].sort_values('war', ascending=False)
    for _, player in hitters.head(10).iterrows():
        print(f"{player['player_name']:15} {player['position']} "
              f"BA: {player['ba']:.3f} | OBP: {player['obp']:.3f} | SLG: {player['slg']:.3f} | "
              f"HR: {player['hr']} | RBI: {player['rbi']} | WAR: {player['war']}")
    
    # Pitchers
    print("\n--- Pitchers ---")
    pitchers = players[players['position'].isin(['SP', 'RP', 'CP'])].sort_values('war', ascending=False)
    for _, player in pitchers.head(10).iterrows():
        print(f"{player['player_name']:15} {player['position']} | WAR: {player['war']}")
    
    # Sabermetric Analysis
    print("\n=== Sabermetric Insights ===\n")
    
    # Calculate team Sabermetrics
    team_woba = players['woba'].mean()
    team_war = players['war'].sum()
    team_hr = players['hr'].sum()
    team_rbi = players['rbi'].sum()
    
    print(f"Team wOBA: {team_woba:.3f}")
    print(f"Team WAR: {team_war:.1f}")
    print(f"Team HR: {team_hr}")
    print(f"Team RBI: {team_rbi}")
    
    # High leverage situations
    high_leverage = statcast[statcast['events'].isin(['home_run', 'double'])]
    print(f"\nHigh-leverage HR: {len(high_leverage[high_leverage['events'] == 'home_run'])}")
    print(f"High-leverage 2B: {len(high_leverage[high_leverage['events'] == 'double'])}")
    
    # Interactive Visualizations
    print("\n=== Interactive Visualizations ===")
    
    # Win probability chart
    fig = viz.plot_win_probability(win_prob, 'Game 1')
    fig.write_html('/home/lucas/.openclaw/workspace/phillies-intel-hub/outputs/win_probability.html')
    print("  ✓ Win probability chart saved")
    
    # Exit velocity histogram
    fig = viz.plot_exit_velocity(statcast)
    fig.write_html('/home/lucas/.openclaw/workspace/phillies-intel-hub/outputs/exit_velocity.html')
    print("  ✓ Exit velocity histogram saved")
    
    # Launch angle histogram
    fig = viz.plot_launch_angle(statcast)
    fig.write_html('/home/lucas/.openclaw/workspace/phillies-intel-hub/outputs/launch_angle.html')
    print("  ✓ Launch angle histogram saved")
    
    # Player trend
    fig = viz.plot_player_trend(players, 'war')
    fig.write_html('/home/lucas/.openclaw/workspace/phillies-intel-hub/outputs/player_trend.html')
    print("  ✓ Player trend chart saved")
    
    print("\nAll visualizations saved to outputs/ directory")

if __name__ == '__main__':
    main()
