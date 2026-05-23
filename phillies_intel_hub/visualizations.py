import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Optional, List, Dict, Any
import numpy as np

class Visualizations:
    """ Interactive visualizations for Phillies analytics """
    
    def __init__(self):
        self.phillies_color = '#006341'  # Phillies green
        self.opponent_color = '#CC0033'  # Default opponent red
        
    def plot_win_probability(self, win_probs: pd.DataFrame, 
                            game_id: str = None) -> go.Figure:
        """
        Plot win probability over game time
        
        Args:
            win_probs: DataFrame with 'inning', 'top', 'win_prob'
            game_id: Optional game identifier
            
        Returns:
            Plotly figure
        """
        fig = go.Figure()
        
        # Phillies win probability (top of inning)
        phillies_wp = win_probs[win_probs['team'] == 'PHI']['win_prob']
        
        # Opponent win probability
        opp_wp = win_probs[win_probs['team'] != 'PHI']['win_prob']
        
        fig.add_trace(go.Scatter(
            x=win_probs[win_probs['team'] == 'PHI']['inning'],
            y=phillies_wp,
            mode='lines+markers',
            name='Phillies Win Prob',
            line=dict(color=self.phillies_color, width=3),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title=f"Win Probability - Game {game_id}" if game_id else "Win Probability",
            xaxis_title="Inning",
            yaxis_title="Win Probability",
            yaxis=dict(range=[0, 1], tickformat='.0%'),
            height=600,
            width=1000,
            plot_bgcolor='white',
            hovermode='x unified'
        )
        
        return fig
    
    def plot_pitch_tracking(self, statcast_data: pd.DataFrame,
                           pitch_type: str = None) -> go.Figure:
        """
        Plot pitch tracking visualization
        
        Args:
            statcast_data: DataFrame with Statcast data
            pitch_type: Filter by pitch type (e.g., 'FF', 'CU')
            
        Returns:
            Plotly figure
        """
        if pitch_type:
            statcast_data = statcast_data[statcast_data['pitch_type'] == pitch_type]
        
        fig = go.Figure()
        
        # Create scatter plot of pitch locations
        fig.add_trace(go.Scatter(
            x=statcast_data['plate_x'],
            y=statcast_data['plate_z'],
            mode='markers',
            marker=dict(
                size=8,
                color=statcast_data['spin_rate'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Spin Rate")
            ),
            text=statcast_data['description'],
            hovertemplate=(
                "Pitch Type: %{customdata[0]}<br>"
                "Speed: %{customdata[1]} mph<br>"
                "Spin: %{customdata[2]} RPM<br>"
                "Result: %{text}<br>"
            ),
            customdata=np.column_stack([
                statcast_data['pitch_type'],
                statcast_data['start_speed'],
                statcast_data['spin_rate']
            ])
        ))
        
        # Add strike zone outline
        fig.add_shape(
            type="rect",
            x0=-1, y0=2.5, x1=1, y1=3.5,
            line=dict(color="red", width=2),
            fillcolor="rgba(255,0,0,0.1)"
        )
        
        fig.update_layout(
            title="Pitch Tracking - Phillies Games",
            xaxis_title="Horizontal Location (feet)",
            yaxis_title="Vertical Location (feet)",
            height=600,
            width=800,
            xaxis=dict(range=[-2, 2]),
            yaxis=dict(range=[0, 5]),
            plot_bgcolor='white'
        )
        
        return fig
    
    def plot_exit_velocity(self, statcast_data: pd.DataFrame) -> go.Figure:
        """
        Plot exit velocity distribution
        
        Args:
            statcast_data: DataFrame with Statcast data
            
        Returns:
            Plotly figure
        """
        # Filter for balls in play
        bip = statcast_data[statcast_data['type'] == 'X'].copy()
        
        # Calculate barrel rate
        barrel = bip[(bip['exit_velocity'] >= 95) & 
                    (bip['launch_angle'].between(10, 50))]
        
        fig = go.Figure()
        
        # Exit velocity histogram
        fig.add_trace(go.Histogram(
            x=bip['exit_velocity'],
            nbinsx=40,
            name='Exit Velocity',
            marker_color=self.phillies_color,
            opacity=0.7
        ))
        
        fig.add_vline(
            x=95, line=dict(color='red', width=2, dash='dash'),
            annotation_text='Barrel Threshold (95 mph)'
        )
        
        fig.update_layout(
            title="Exit Velocity Distribution - Phillies Batters",
            xaxis_title="Exit Velocity (mph)",
            yaxis_title="Count",
            height=600,
            width=1000,
            plot_bgcolor='white'
        )
        
        return fig
    
    def plot_launch_angle(self, statcast_data: pd.DataFrame) -> go.Figure:
        """
        Plot launch angle distribution
        
        Args:
            statcast_data: DataFrame with Statcast data
            
        Returns:
            Plotly figure
        """
        bip = statcast_data[statcast_data['type'] == 'X'].copy()
        
        fig = go.Figure()
        
        fig.add_trace(go.Histogram(
            x=bip['launch_angle'],
            nbinsx=40,
            name='Launch Angle',
            marker_color='#006341',
            opacity=0.7
        ))
        
        # Add optimal zones
        fig.add_vrect(
            x0=10, x1=50, fillcolor="green", opacity=0.2,
            annotation_text="Hard Hit Zone (10-50°)",
            annotation_position="top left"
        )
        
        fig.update_layout(
            title="Launch Angle Distribution - Phillies Batters",
            xaxis_title="Launch Angle (degrees)",
            yaxis_title="Count",
            height=600,
            width=1000,
            plot_bgcolor='white'
        )
        
        return fig
    
    def plot_player_trend(self, player_data: pd.DataFrame,
                         metric: str = 'wOBA') -> go.Figure:
        """
        Plot player performance trend
        
        Args:
            player_data: DataFrame with date and metric columns
            metric: Metric to plot
            
        Returns:
            Plotly figure
        """
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=player_data['date'],
            y=player_data[metric],
            mode='lines+markers',
            name=metric,
            line=dict(color=self.phillies_color, width=2),
            marker=dict(size=8),
            text=player_data.get('game_context', ''),
            hovertemplate=(
                "Date: %{x}<br>"
                f"{metric}: %{{y:.3f}}<br>"
                "Context: %{text}<br>"
            )
        ))
        
        # Add 30-day moving average
        if len(player_data) >= 30:
            fig.add_trace(go.Scatter(
                x=player_data['date'],
                y=player_data[metric].rolling(30).mean(),
                mode='lines',
                name='30-Day MA',
                line=dict(color='red', width=2, dash='dash')
            ))
        
        fig.update_layout(
            title=f"{metric} Trend - Phillies Player",
            xaxis_title="Date",
            yaxis_title=metric,
            height=600,
            width=1000,
            plot_bgcolor='white'
        )
        
        return fig
    
    def plot_league_comparison(self, player_stats: pd.DataFrame,
                             metric: str = 'wOBA') -> go.Figure:
        """
        Plot league comparison for a metric
        
        Args:
            player_stats: DataFrame with player and league stats
            metric: Metric to compare
            
        Returns:
            Plotly figure
        """
        # Top Phillies players
        phillies_players = player_stats[player_stats['team'] == 'PHI'].nlargest(10, metric)
        
        # League average
        league_avg = player_stats[metric].mean()
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=phillies_players['player_name'],
            y=phillies_players[metric],
            name='Phillies',
            marker_color=self.phillies_color
        ))
        
        fig.add_hline(
            y=league_avg, line=dict(color='red', width=2, dash='dash'),
            annotation_text=f"League Avg: {league_avg:.3f}",
            annotation_position="right"
        )
        
        fig.update_layout(
            title=f"{metric} Comparison - Phillies vs League",
            xaxis_title="Player",
            yaxis_title=metric,
            height=600,
            width=1000,
            plot_bgcolor='white'
        )
        
        return fig
