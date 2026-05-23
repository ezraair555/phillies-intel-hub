# Phillies-Intel-Hub

Baseball analytics hub for Philadelphia Phillies performance tracking, powered by **Baseball Savant/MLB Statcast data**.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

The Phillies-Intel-Hub provides:

- **Real-time game tracking** - Phillies game logs, box scores, and play-by-play data
- **Player performance analysis** - Batting/pitching stats, WAR, wOBA, exit velocity, launch angle
- **Sabermetric insights** - WPA, leverage index, FIP, xwOBA, defensive metrics
- **Interactive visualizations** - Interactive charts for win probability, pitch tracking, player trends
- **Game-day briefings** - Automated pre-game reports with matchups and projections

## Data Sources

| Source | Description |
|--------|-------------|
| **MLB Stats API** | Official MLB game schedules, rosters, box scores |
| **Baseball Savant (Statcast)** | Pitch-level data, exit velocity, launch angle, expected metrics |
| **FanGraphs** | Advanced sabermetrics, WAR, league context |

## Installation

```bash
pip install phillies-intel-hub
```

## Quick Start

```python
import pandas as pd
from phillies_intel_hub import PhilliesAnalytics

# Initialize analytics
analytics = PhilliesAnalytics()

# Get Phillies games for current season
games = analytics.get_games(start_date='2026-03-01', end_date='2026-05-23')

# Get player statistics
player_stats = analytics.get_player_stats(player_type='batter', qualified=True)

# Get Statcast data for a specific game
statcast_data = analytics.get_statcast_data(game_date='2026-05-23')

# Generate game-day briefing
briefing = analytics.generate_briefing(opponent='NY Mets', game_date='2026-05-24')
```

## Key Features

### 1. Phillies Game Tracker
- Daily game updates with real-time scores
- Box score analysis with advanced metrics
- Win probability graphs

### 2. Player Performance Dashboard
- **Hitters**: Batting average, OBP, SLG, wOBA, WAR, exit velocity, launch angle
- **Pitchers**: ERA, FIP, xFIP, WAR, strikeout rate, walk rate
- **Defensive metrics**: Outs above average, framing metrics

### 3. Sabermetric Analytics
- **Win Probability Added (WPA)** - Contextual impact of plays
- **Leverage Index** - High-pressure situation tracking
- **Expected Metrics** - xwOBA, xBA, xSLG (based on exit velocity/angle)
- **Pitch metrics**: Spin rate, velocity, movement, zone rates

### 4. Interactive Visualizations
- Win probability charts
- Exit velocity/launch angle histograms
- Pitch tracking visualizations
- Player trend analysis graphs

### 5. Automated Reports
- Pre-game briefings (PDF/HTML)
- Post-game analysis
- Weekly performance summaries

## API Documentation

### Core Classes

#### `PhilliesAnalytics`
Main analytics engine with methods for:
- `get_games()` - Phillies game schedule and results
- `get_player_stats()` - Player batting/pitching statistics
- `get_statcast_data()` - Pitch-level Statcast data
- `generate_briefing()` - Automated pre-game reports
- `plot_win_probability()` - Interactive win probability charts
- `plot_pitch_tracking()` - Interactive pitch visualizations

### Data Models

```python
# Game object structure
{
    'game_id': 'GID_2026_05_23_phimia_1',
    'game_date': '2026-05-23',
    'home_team': 'PHI',
    'away_team': 'MIA',
    'home_score': 5,
    'away_score': 2,
    'venue': ' Citizens Bank Park',
    'attendance': 43210,
    'winning_pitcher': ' Aaron Nola',
    'losing_pitcher': ' Jose Salas'
}

# Player stat object structure
{
    'player_id': 571364,
    'player_name': 'Bryson Stott',
    'position': 'SS',
    'games': 38,
    'ab': 132,
    'runs': 17,
    'hits': 34,
    'doubles': 6,
    'triples': 0,
    'hr': 3,
    'rbi': 19,
    'bb': 14,
    'so': 28,
    'ba': 0.258,
    'obp': 0.333,
    'slg': 0.409,
    'woba': 0.338,
    'war': 1.2
}
```

## Examples

See `examples/` directory:
- `examples/game_tracker.py` - Phillies game tracking
- `examples/player_analysis.py` - Player performance analysis
- `examples/statcast_visualizations.py` - Interactive pitch charts
- `examples/game_briefing.py` - Automated pre-game reports

## Architecture

```
phillies-intel-hub/
├── phillies_intel_hub/
│   ├── __init__.py
│   ├── analytics.py          # Main analytics engine
│   ├── data_sources.py       # Data fetching from MLB API + Baseball Savant
│   ├── visualizations.py     # Interactive charts (Plotly)
│   └── reporting.py          # Automated report generation
├── examples/                 # Usage examples
├── docs/                     # Detailed documentation
└── tests/                    # Test suite
```

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- **MLB Advanced Media** - For Statcast data and official APIs
- **Baseball Savant** - For pitch-level analytics and visualization inspiration
- **pybaseball** - For Python wrapper around Baseball Savant data
