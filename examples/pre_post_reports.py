import os
import pandas as pd
from phillies_intel_hub import PhilliesAnalytics

def main():
    analytics = PhilliesAnalytics()
    
    # Generate Pre-Game Report
    print("=== Pre-Game Report ===")
    pre_game = analytics.generate_pre_game_report('Mets', '2026-05-24')
    
    print(f"\nGame: Phillies vs {pre_game['opponent']} on {pre_game['game_date']}")
    print(f"\nRecent Record: {pre_game['sections'].get('recent_record', 'N/A')}")
    
    print(f"\nPhillies Team Stats:")
    print(f"  Record: {pre_game['sections']['phillies_team_stats'].get('wins', 0)}-{pre_game['sections']['phillies_team_stats'].get('losses', 0)}")
    print(f"  ERA: {pre_game['sections']['phillies_team_stats'].get('era', 'N/A')}")
    
    print(f"\nMatchup Analysis:")
    print(f"  Phillies Starter: {pre_game['sections']['matchup_analysis'].get('phillies_starter', 'N/A')}")
    print(f"  Opponent Starter: {pre_game['sections']['matchup_analysis'].get('opponent_starter', 'N/A')}")
    print(f"  Win Probability: {pre_game['sections']['matchup_analysis'].get('win_probability', 'N/A')}")
    
    print(f"\nSabermetric Insights:")
    print(f"  Phillies wOBA: {pre_game['sections']['sabermetrics'].get('phillies_woba', 'N/A')}")
    print(f"  Phillies FIP: {pre_game['sections']['sabermetrics'].get('phillies_fip', 'N/A')}")
    
    # Generate Post-Game Report
    print("\n" + "="*60)
    print("=== Post-Game Report ===")
    post_game = analytics.generate_post_game_report('GID_2026_05_23_phimia_1', '2026-05-23')
    
    print(f"\nGame: {post_game['game_id']}")
    print(f"  Score: {post_game['sections'].get('final_score', 'N/A')}")
    print(f"  Winner: {post_game['sections'].get('winner', 'N/A')}")
    
    print(f"\nKey Metrics:")
    print(f"  Runs Scored: {post_game['sections']['key_metrics'].get('runs_scored', 'N/A')}")
    print(f"  Runs Allowed: {post_game['sections']['key_metrics'].get('runs_allowed', 'N/A')}")
    print(f"  Hits: {post_game['sections']['key_metrics'].get('hits', 'N/A')}")
    print(f"  Errors: {post_game['sections']['key_metrics'].get('errors', 'N/A')}")
    
    print(f"\nPerformance Analysis:")
    print(f"  Offense: {post_game['sections']['performance_analysis'].get('offense', 'N/A')}")
    print(f"  Pitching: {post_game['sections']['performance_analysis'].get('pitching', 'N/A')}")
    print(f"  Defense: {post_game['sections']['performance_analysis'].get('defense', 'N/A')}")
    
    print(f"\nKey Plays:")
    for play in post_game['sections']['performance_analysis'].get('key_plays', []):
        print(f"  - {play}")
    
    print("\n" + "="*60)
    print("Reports Generated Successfully!")

if __name__ == '__main__':
    main()
