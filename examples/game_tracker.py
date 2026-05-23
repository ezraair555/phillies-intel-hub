import pandas as pd
import numpy as np
from phillies_intel_hub import PhilliesAnalytics

def main():
    analytics = PhilliesAnalytics()
    
    # Get Phillies games for current season
    games = analytics.get_games('2026-03-01', '2026-05-23')
    
    if not games.empty:
        print(f"Found {len(games)} Phillies games in 2026")
        print(f"Record: {games['home_score'].sum() - games['away_score'].sum()} runs")
        
        # Get last 5 games
        last_5 = games.tail(5)
        print("\nLast 5 Games:")
        for _, game in last_5.iterrows():
            result = "W" if game['home_score'] > game['away_score'] else "L"
            print(f"  {game['game_date']}: {result} {game['home_score']}-{game['away_score']}")
    
    # Get Phillies team stats
    phillies_stats = analytics.get_team_stats()
    print(f"\nPhillies Record: {phillies_stats.get('wins', 0)}-{phillies_stats.get('losses', 0)}")
    
    # Generate game-day briefing
    briefing = analytics.generate_briefing('NY Mets', '2026-05-24')
    print("\n" + briefing)

if __name__ == '__main__':
    main()
