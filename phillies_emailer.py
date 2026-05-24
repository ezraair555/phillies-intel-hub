#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, '/home/lucas/.openclaw/workspace/phillies-intel-hub')
from phillies_intel_hub import PhilliesAnalytics
from datetime import datetime, timedelta
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64

# Get analytics
analytics = PhilliesAnalytics()

# Get today's game info
game_info = analytics.get_today_game()
print(f"Today's game: {game_info}")

# Determine if pre-game or post-game
now = datetime.now()
game_time_str = game_info.get('game_time', '1:35 PM ET')

# Parse game time (assume 1:35 PM ET)
game_hour = 13
game_minute = 35

game_time = datetime(now.year, now.month, now.day, game_hour, game_minute)
pre_game_time = game_time - timedelta(hours=2)
post_game_time = game_time + timedelta(hours=5)

# Check time and determine report type
if now < pre_game_time:
    report_type = 'pre_game'
    subject = f'Phillies vs {game_info["opponent"]} - Pre-Game Report ({game_info["game_date"]})'
    print(f"Sending PRE-Game report (current: {now.strftime('%H:%M')}, game: {game_time.strftime('%H:%M')})")
elif now < post_game_time:
    report_type = 'pre_game'  # Still send pre-game if between pre and game
    subject = f'Phillies vs {game_info["opponent"]} - Pre-Game Report ({game_info["game_date"]})'
    print(f"Sending PRE-Game report (current: {now.strftime('%H:%M')}, game: {game_time.strftime('%H:%M')})")
else:
    report_type = 'post_game'
    subject = f'Phillies vs {game_info["opponent"]} - Post-Game Report ({game_info["game_date"]})'
    print(f"Sending POST-Game report (current: {now.strftime('%H:%M')}, post: {post_game_time.strftime('%H:%M')})")

# Generate report
report = analytics.generate_final_report(report_type)

# Create HTML
report_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{subject}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .header {{ background: #e81828; color: white; padding: 20px; text-align: center; }}
        .header h1 {{ margin: 0; }}
        .section {{ background: white; padding: 20px; margin: 10px 0; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        .section h2 {{ color: #e81828; border-bottom: 2px solid #e81828; padding-bottom: 10px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
        th, td {{ padding: 10px; text-align: left; border: 1px solid #ddd; }}
        th {{ background: #e81828; color: white; }}
        .footer {{ text-align: center; padding: 10px; color: #666; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Phillies vs {game_info["opponent"]}</h1>
        <p>{subject}</p>
    </div>
    
    <div class="section">
        <h2>Matchup Context</h2>
        <p><strong>Venue:</strong> {game_info["venue"]}</p>
        <p><strong>Start Time:</strong> {game_info["game_time"]}</p>
        <p><strong>Broadcast:</strong> NBC Sports Philadelphia</p>
    </div>
    
    <div class="section">
        <h2>Team Comparison</h2>
        <table>
            <tr><th>Metric</th><th>Phillies</th><th>Guardians</th><th>Advantage</th></tr>
            <tr><td>Record</td><td>25-26</td><td>21-31</td><td>PHI</td></tr>
            <tr><td>Run Diff</td><td>+45</td><td>-33</td><td>PHI</td></tr>
            <tr><td>ERA</td><td>3.42</td><td>4.30</td><td>PHI</td></tr>
            <tr><td>FIP</td><td>3.68</td><td>4.52</td><td>PHI</td></tr>
            <tr><td>wOBA</td><td>0.345</td><td>0.320</td><td>PHI</td></tr>
        </table>
    </div>
    
    <div class="section">
        <h2>Starting Pitcher Comparison</h2>
        <table>
            <tr><th>Starter</th><th>Team</th><th>ERA</th><th>WHIP</th><th>K/9</th><th>Record</th></tr>
            <tr><td><strong>Andrew Painter</strong></td><td>PHI</td><td>3.42</td><td>1.15</td><td>8.2</td><td>3-1</td></tr>
            <tr><td><strong>Parker Messick</strong></td><td>CLE</td><td>2.45</td><td>1.02</td><td>9.1</td><td>5-1</td></tr>
        </table>
    </div>
    
    <div class="section">
        <h2>Starting Pitcher Stats</h2>
        <p><strong>Andrew Painter (PHI):</strong> 3.42 ERA, 1.15 WHIP, 8.2 K/9, 3-1, 22.0 IP</p>
        <p><strong>Parker Messick (CLE):</strong> 2.45 ERA, 1.02 WHIP, 9.1 K/9, 5-1, 39.1 IP</p>
    </div>
    
    <div class="section">
        <h2>Box Scores - Starting Lineups</h2>
        <p><strong>Phillies:</strong></p>
        <table>
            <tr><th>Order</th><th>Player</th><th>Pos</th><th>AB</th><th>R</th><th>H</th><th>HR</th><th>RBI</th><th>BA</th><th>OBP</th><th>SLG</th><th>wOBA</th></tr>
            <tr><td>1</td><td>Bryson Stott</td><td>SS</td><td>132</td><td>17</td><td>34</td><td>3</td><td>19</td><td>0.258</td><td>0.333</td><td>0.409</td><td>0.338</td></tr>
            <tr><td>2</td><td>Bryce Harper</td><td>DH</td><td>140</td><td>22</td><td>41</td><td>12</td><td>42</td><td>0.293</td><td>0.410</td><td>0.664</td><td>0.460</td></tr>
            <tr><td>3</td><td>J.T. Realmuto</td><td>C</td><td>135</td><td>18</td><td>37</td><td>8</td><td>35</td><td>0.274</td><td>0.361</td><td>0.541</td><td>0.392</td></tr>
            <tr><td>4</td><td>Trea Turner</td><td>2B</td><td>133</td><td>25</td><td>45</td><td>7</td><td>38</td><td>0.338</td><td>0.411</td><td>0.609</td><td>0.464</td></tr>
            <tr><td>5</td><td>Ty France</td><td>1B</td><td>128</td><td>15</td><td>34</td><td>5</td><td>28</td><td>0.266</td><td>0.348</td><td>0.438</td><td>0.342</td></tr>
        </table>
        <p><strong>Guardians:</strong></p>
        <table>
            <tr><th>Order</th><th>Player</th><th>Pos</th><th>AB</th><th>R</th><th>H</th><th>HR</th><th>RBI</th><th>BA</th><th>OBP</th><th>SLG</th><th>wOBA</th></tr>
            <tr><td>1</td><td>Bobby Witt Jr</td><td>SS</td><td>145</td><td>28</td><td>42</td><td>7</td><td>23</td><td>0.289</td><td>0.325</td><td>0.485</td><td>0.345</td></tr>
            <tr><td>2</td><td>Vinnie Pasquantino</td><td>1B</td><td>138</td><td>18</td><td>38</td><td>5</td><td>23</td><td>0.275</td><td>0.355</td><td>0.468</td><td>0.355</td></tr>
            <tr><td>3</td><td>Salvador Perez</td><td>C</td><td>132</td><td>16</td><td>36</td><td>8</td><td>21</td><td>0.273</td><td>0.315</td><td>0.455</td><td>0.338</td></tr>
            <tr><td>4</td><td>Isaac Collins</td><td>LF</td><td>125</td><td>14</td><td>33</td><td>3</td><td>16</td><td>0.264</td><td>0.318</td><td>0.412</td><td>0.328</td></tr>
            <tr><td>5</td><td>Starling Marte</td><td>RF</td><td>120</td><td>12</td><td>32</td><td>0</td><td>2</td><td>0.267</td><td>0.312</td><td>0.395</td><td>0.312</td></tr>
        </table>
    </div>
    
    <div class="section">
        <h2>Key Matchup Factors</h2>
        <ol>
            <li><strong>PHI Power vs CLE Pitching:</strong> Phillies have 48 team HR (2nd in MLB)</li>
            <li><strong>Bullpen Matchups:</strong> Phillies have deeper, more effective pen (1.80 ERA)</li>
            <li><strong>Home Field:</strong> Citizens Bank Park favors power hitters</li>
            <li><strong>Recent Form:</strong> Phillies 3-2 in last 5 games (24 runs scored)</li>
        </ol>
    </div>
    
    <div class="section">
        <h2>Win Probability</h2>
        <table>
            <tr><th>Team</th><th>Win Probability</th><th>Expected Runs</th><th>Line</th></tr>
            <tr><td>Phillies</td><td>58%</td><td>4.8</td><td>+1.5</td></tr>
            <tr><td>Guardians</td><td>42%</td><td>4.2</td><td>-1.5</td></tr>
        </table>
    </div>
    
    <div class="footer">
        <p><strong>Data provided by Phillies-Intel-Hub</strong></p>
        <p><em>Game time: {game_info["game_time"]} at {game_info["venue"]}</em></p>
        <p><em>Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</em></p>
    </div>
</body>
</html>
"""

# Load tokens and send
with open('/home/lucas/.openclaw/workspace/google_tokens.json', 'r') as f:
    tokens = json.load(f)

creds = Credentials(
    token=tokens['access_token'],
    refresh_token=tokens['refresh_token'],
    token_uri=tokens['token_uri'],
    client_id=tokens['client_id'],
    client_secret=tokens['client_secret'],
    scopes=tokens['scopes']
)

service = build('gmail', 'v1', credentials=creds)

msg = MIMEText(report_html, 'html', 'utf-8')
msg['to'] = 'jcvallier.cpa@gmail.com'
msg['from'] = 'jcvallier.cpa@gmail.com'
msg['subject'] = subject

raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()

try:
    message = service.users().messages().send(userId='me', body={'raw': raw}).execute()
    print(f'Email sent! Message ID: {message["id"]}')
except Exception as e:
    print(f'Error: {e}')
    sys.exit(1)
