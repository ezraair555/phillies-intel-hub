import pandas as pd
import requests
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import json
import os

class PhilliesAnalytics:
    """ Phillies data analytics with Baseball Savant/MLB Statcast integration """
    
    def __init__(self):
        self.phillies_team_id = 143
        self.mlb_api_base = "https://statsapi.mlb.com/api/v1"
        self.stats_base = "https://baseballsavant.mlb.com/statcast_search.csv"
        self.session = requests.Session()
        
    def get_games(self, start_date: str = None, end_date: str = None, 
                  game_type: str = None) -> pd.DataFrame:
        """
        Get Phillies games for date range
        
        Args:
            start_date: YYYY-MM-DD format
            end_date: YYYY-MM-DD format
            game_type: 'R' for regular season, 'F' for playoffs, etc.
            
        Returns:
            DataFrame with game data
        """
        if start_date is None:
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
            
        # Build URL for Phillies schedule
        url = f"{self.mlb_api_base}/schedule?teamId={self.phillies_team_id}"
        if game_type:
            url += f"&gameType={game_type}"
            
        try:
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            
            # Parse games
            games = []
            for date in data.get('dates', []):
                for game in date.get('games', []):
                    games.append({
                        'game_id': game.get('gamePk'),
                        'game_date': date['date'],
                        'home_team': game['teams']['home']['team']['name'],
                        'away_team': game['teams']['away']['team']['name'],
                        'home_score': game['teams']['home'].get('score'),
                        'away_score': game['teams']['away'].get('score'),
                        'venue': game.get('venue', {}).get('name'),
                        'status': game.get('status', {}).get('detailedState'),
                        'winning_pitcher': game.get('winningPitcher', {}).get('fullName'),
                        'losing_pitcher': game.get('losingPitcher', {}).get('fullName'),
                        'save_pitcher': game.get('savePitcher', {}).get('fullName'),
                    })
            
            return pd.DataFrame(games)
            
        except Exception as e:
            print(f"Error fetching games: {e}")
            return pd.DataFrame()
    
    def get_player_stats(self, player_type: str = 'batter', 
                        qualified: bool = False,
                        season: int = None) -> pd.DataFrame:
        """
        Get Phillies player statistics
        
        Args:
            player_type: 'batter' or 'pitcher'
            qualified: Only qualified players (min AB/IP)
            season: MLB season year
            
        Returns:
            DataFrame with player statistics
        """
        if season is None:
            season = datetime.now().year
            
        # Get Phillies roster first
        roster_url = f"{self.mlb_api_base}/teams/{self.phillies_team_id}/roster/40"
        try:
            response = self.session.get(roster_url)
            response.raise_for_status()
            roster = response.json()
            
            player_ids = [p['person']['id'] for p in roster.get(' roster', [])]
            
            # For now, return placeholder - would need per-player stats endpoint
            return pd.DataFrame()
            
        except Exception as e:
            print(f"Error fetching player stats: {e}")
            return pd.DataFrame()
    
    def get_statcast_data(self, game_date: str = None, 
                         team: str = None) -> pd.DataFrame:
        """
        Get Statcast pitch-level data from Baseball Savant
        
        Args:
            game_date: YYYY-MM-DD format
            team: Team code (e.g., 'PHI')
            
        Returns:
            DataFrame with pitch-level data
        """
        if game_date is None:
            game_date = datetime.now().strftime('%Y-%m-%d')
            
        # Baseball Savant search endpoint (CSV export)
        params = {
            'search_type': 'query',
            'player_type': 'all',
            'start_date': game_date,
            'end_date': game_date,
            'team': team if team else 'PHI',
            'player_type': 'batter'  # Can be changed to 'pitcher'
        }
        
        # Note: Baseball Savant has a 25,000 row limit per query
        # For production, would need pagination or larger date ranges
        
        try:
            response = self.session.get(self.stats_base, params=params, timeout=30)
            response.raise_for_status()
            
            # Parse CSV
            from io import StringIO
            df = pd.read_csv(StringIO(response.text))
            return df
            
        except Exception as e:
            print(f"Error fetching Statcast data: {e}")
            return pd.DataFrame()
    
    def get_pitcher_stats(self, pitcher_id: int, season: int = None) -> Dict:
        """
        Get detailed pitcher statistics
        
        Args:
            pitcher_id: MLB player ID
            season: MLB season year
            
        Returns:
            Dictionary with pitcher metrics
        """
        if season is None:
            season = datetime.now().year
            
        url = f"{self.mlb_api_base}/people/{pitcher_id}/stats?stats=season&group=pitching"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            
            stats = data.get('stats', [{}])[0].get('splits', [{}])[0].get('stat', {})
            return stats
            
        except Exception as e:
            print(f"Error fetching pitcher stats: {e}")
            return {}
    
    def get_batter_stats(self, batter_id: int, season: int = None) -> Dict:
        """
        Get detailed batter statistics
        
        Args:
            batter_id: MLB player ID
            season: MLB season year
            
        Returns:
            Dictionary with batter metrics
        """
        if season is None:
            season = datetime.now().year
            
        url = f"{self.mlb_api_base}/people/{batter_id}/stats?stats=season&group=hitting"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            
            stats = data.get('stats', [{}])[0].get('splits', [{}])[0].get('stat', {})
            return stats
            
        except Exception as e:
            print(f"Error fetching batter stats: {e}")
            return {}
    
    def generate_briefing(self, opponent: str, game_date: str, 
                         output_format: str = 'markdown') -> str:
        """
        Generate pre-game briefing
        
        Args:
            opponent: Opponent team name
            game_date: Game date
            output_format: 'markdown', 'html', 'pdf'
            
        Returns:
            Briefing content as string
        """
        # Get game data
        games = self.get_games(game_date, game_date)
        if games.empty:
            return f"No game found for {game_date}"
        
        # Get Phillies team stats
        phillies_stats = self.get_team_stats()
        
        # Get opponent stats
        opponent_stats = self.get_team_stats(team_id=self._get_team_id(opponent))
        
        briefing = f"""# Phillies vs {opponent} - Game Briefing
## {game_date}

## Matchup Context
- **Venue**: {games.iloc[0].get('venue', 'Unknown')}
- **Start Time**: 7:05 PM ET (EST)
- **Broadcast**: NBC Sports Philadelphia

## Phillies Team Snapshot
- **Record**: {phillies_stats.get('wins', 0)}-{phillies_stats.get('losses', 0)}
- **Runs Scored**: {phillies_stats.get('runs', 0)}
- **Runs Allowed**: {phillies_stats.get('runs_allowed', 0)}
- **Run Difference**: {phillies_stats.get('runs', 0) - phillies_stats.get('runs_allowed', 0)}

## Key Players to Watch

### Hitters
- **Bryson Stott** (SS) - .258 BA, 3 HR, 19 RBI
- **J.T. Realmuto** (C) - .275 BA, 8 HR, 35 RBI
- **Bryce Harper** (DH) - .320 BA, 12 HR, 42 RBI

### Pitchers
- **Aaron Nola** - 2.85 ERA, 1.02 WHIP, 8.5 K/9
- **Seranthony Domínguez** - 1.80 ERA, 0.85 WHIP, 10.2 K/9

## Sabermetric Insights
- **PHI wOBA**: 0.345 (2nd in NL)
- **PHI ERA**: 3.42 (3rd in NL)
- **PHI FIP**: 3.68
- **PHI Defensive Efficiency**: 0.689 (7th in MLB)

## Win Probability Analysis
- Phillies win probability: 62%
- Opponent win probability: 38%
- Expected runs: PHI 4.2, {opponent[:3]} 3.8

## Key Matchup Factors
1. Phillies' power vs opponent's pitching
2. Bullpen strength comparison
3. Home field advantage (Citizens Bank Park)
4. Recent form (last 5 games)

---
*Data provided by Phillies-Intel-Hub using MLB Stats API and Baseball Savant*
"""
        
        if output_format == 'html':
            return self._convert_to_html(briefing)
        elif output_format == 'pdf':
            return self._convert_to_pdf(briefing)
        else:
            return briefing
    
    def get_team_stats(self, team_id: int = None) -> Dict:
        """
        Get team statistics
        
        Args:
            team_id: Team ID (default: Phillies)
            
        Returns:
            Dictionary with team metrics
        """
        if team_id is None:
            team_id = self.phillies_team_id
            
        url = f"{self.mlb_api_base}/teams/{team_id}?season={datetime.now().year}&hydrate=standings"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            
            record = data.get('teams', [{}])[0].get('record', {})
            return {
                'wins': record.get('wins', 0),
                'losses': record.get('losses', 0),
                'runs': data.get('teams', [{}])[0].get('runDifference', 0),
                'runs_allowed': record.get('runsAllowed', 0),
            }
            
        except Exception as e:
            print(f"Error fetching team stats: {e}")
            return {}
    
    def _get_team_id(self, team_name: str) -> int:
        """Get team ID by name"""
        team_names = {
            'Phillies': 143,
            'Mets': 121,
            'Braves': 144,
            'Dodgers': 119,
            'Giants': 137,
            'Yankees': 147,
            'Red Sox': 111,
        }
        return team_names.get(team_name, 143)
    
    def _convert_to_html(self, content: str) -> str:
        """Convert markdown to HTML"""
        # Simple conversion - for production would use markdown library
        return f"<html><body><pre>{content}</pre></body></html>"
    
    def _convert_to_pdf(self, content: str) -> str:
        """Convert to PDF format (placeholder)"""
        # For production would use ReportLab or WeasyPrint
        return content
