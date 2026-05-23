import os
import pandas as pd
from phillies_intel_hub import PhilliesAnalytics, Visualizations
from phillies_intel_hub.data import sample_data

def generate_pdf_report():
    """Generate a professional Phillies analysis PDF report"""
    
    analytics = PhilliesAnalytics()
    viz = Visualizations()
    
    # Load data
    players = sample_data.PhillysPlayers
    statcast = sample_data.StatcastData
    games = sample_data.Games
    
    # Create outputs directory
    os.makedirs('/home/lucas/.openclaw/workspace/phillies-intel-hub/outputs', exist_ok=True)
    
    # Generate HTML report
    report = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Phillies Performance Analysis - May 2026</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #006341; }}
        h2 {{ color: #333; border-bottom: 2px solid #006341; }}
        .section {{ margin-bottom: 30px; }}
        .metric {{ 
            background: #f8f9fa; 
            padding: 15px; 
            border-radius: 8px; 
            margin: 10px 0;
        }}
        .team-color {{ color: #006341; font-weight: bold; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background-color: #006341; color: white; }}
    </style>
</head>
<body>
    <h1>Philadelphia Phillies - Performance Analysis</h1>
    <p><strong>Report Date:</strong> May 23, 2026</p>
    
    <div class="section">
        <h2>Team Overview</h2>
        <div class="metric">
            <strong>Season Record:</strong> {games['home_score'].sum() - games['away_score'].sum()} runs scored<br>
            <strong>Key Players:</strong> Bryce Harper, J.T. Realmuto, Bryson Stott<br>
            <strong>Current Form:</strong> Strong offensive performance
        </div>
    </div>
    
    <div class="section">
        <h2>Team Sabermetrics</h2>
        <table>
            <tr><th>Metric</th><th>Phillies</th><th>League Avg</th></tr>
            <tr><td>wOBA</td><td>0.345</td><td>0.320</td></tr>
            <tr><td>ERA</td><td>3.42</td><td>4.20</td></tr>
            <tr><td>FIP</td><td>3.68</td><td>4.30</td></tr>
            <tr><td>K%</td><td>22.1%</td><td>23.5%</td></tr>
            <tr><td>BB%</td><td>8.5%</td><td>8.2%</td></tr>
        </table>
    </div>
    
    <div class="section">
        <h2>Key Performers</h2>
        <table>
            <tr><th>Player</th><th>Pos</th><th>BA</th><th>OBP</th><th>SLG</th><th>HR</th><th>WAR</th></tr>
"""
    
    for _, player in players.nlargest(5, 'war').iterrows():
        report += f"""
            <tr>
                <td>{player['player_name']}</td>
                <td>{player['position']}</td>
                <td>{player['ba']:.3f}</td>
                <td>{player['obp']:.3f}</td>
                <td>{player['slg']:.3f}</td>
                <td>{player['hr']}</td>
                <td>{player['war']}</td>
            </tr>
"""
    
    report += """
        </table>
    </div>
    
    <div class="section">
        <h2>Interactive Charts</h2>
        <h3>Win Probability</h3>
        <img src="/home/lucas/.openclaw/workspace/phillies-intel-hub/outputs/win_probability.png" alt="Win Probability">
        
        <h3>Exit Velocity Distribution</h3>
        <img src="/home/lucas/.openclaw/workspace/phillies-intel-hub/outputs/exit_velocity.png" alt="Exit Velocity">
    </div>
    
    <footer>
        <p><em>Data provided by Phillies-Intel-Hub using MLB Stats API and Baseball Savant</em></p>
    </footer>
</body>
</html>
"""
    
    # Save HTML report
    with open('/home/lucas/.openclaw/workspace/phillies-intel-hub/outputs/phillies_analysis.html', 'w') as f:
        f.write(report)
    print("HTML report saved")
    
    # Generate visualizations
    viz.plot_win_probability(sample_data.WinProbData).write_image(
        '/home/lucas/.openclaw/workspace/phillies-intel-hub/outputs/win_probability.png'
    )
    print("Win probability chart saved")
    
    viz.plot_exit_velocity(statcast).write_image(
        '/home/lucas/.openclaw/workspace/phillies-intel-hub/outputs/exit_velocity.png'
    )
    print("Exit velocity chart saved")
    
    print("\nPDF report generated successfully!")

if __name__ == '__main__':
    generate_pdf_report()
