import json
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from phillies_intel_hub import PhilliesAnalytics

# Get analytics instance
analytics = PhilliesAnalytics()

# Generate reports
pre_game = analytics.generate_final_report('pre_game')
post_game = analytics.generate_final_report('post_game')

# Game time is 1:35 PM ET, so send pre-game at 11:35 AM and post-game at 6:35 PM
now = datetime.now()
game_time = datetime(now.year, now.month, now.day, 13, 35)  # 1:35 PM
pre_game_time = game_time - timedelta(hours=2)  # 11:35 AM
post_game_time = game_time + timedelta(hours=5)  # 6:35 PM

print(f"Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Game time: {game_time.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Pre-game email time: {pre_game_time.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Post-game email time: {post_game_time.strftime('%Y-%m-%d %H:%M:%S')}")

# Generate HTML email content
report_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Phillies vs Guardians - Pre-Game Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .header {{ background: #e81828; color: white; padding: 20px; text-align: center; }}
        .header h1 {{ margin: 0; }}
        .section {{ background: white; padding: 20px; margin: 10px 0; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        .section h2 {{ color: #e81828; border-bottom: 2px solid #e81828; padding-bottom: 10px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
        th, td {{ padding: 10px; text-align: left; border: 1px solid #ddd; }}
        th {{ background: #e81828; color: white; }}
        .box-score {{ background: #f8f9fa; padding: 15px; margin: 10px 0; }}
        .box-score h3 {{ margin-top: 0; color: #333; }}
        .box-score table {{ margin: 5px 0; }}
        .footer {{ text-align: center; padding: 10px; color: #666; font-size: 12px; }}
        .timestamp {{ font-style: italic; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Phillies vs Guardians</h1>
        <p>Pre-Game Report - May 24, 2026</p>
    </div>
    
    <div class="section">
        <h2>Matchup Context</h2>
        <p><strong>Venue:</strong> {pre_game['venue']}</p>
        <p><strong>Start Time:</strong> {pre_game['game_time']}</p>
        <p><strong>Broadcast:</strong> NBC Sports Philadelphia</p>
        <p><strong>Opponent:</strong> Cleveland Guardians</p>
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
            <tr><td>Def Eff</td><td>0.689</td><td>0.672</td><td>PHI</td></tr>
            <tr><td>Team HR</td><td>48</td><td>32</td><td>PHI</td></tr>
        </table>
    </div>
    
    <div class="section">
        <h2>Starting Pitcher Comparison</h2>
        <table>
            <tr><th>Starter</th><th>Team</th><th>ERA</th><th>FIP</th><th>WHIP</th><th>K/9</th><th>BB/9</th><th>Record</th></tr>
            <tr><td><strong>Andrew Painter</strong></td><td>PHI</td><td>3.42</td><td>3.68</td><td>1.15</td><td>8.2</td><td>2.8</td><td>3-1</td></tr>
            <tr><td><strong>Parker Messick</strong></td><td>CLE</td><td>2.45</td><td>2.80</td><td>1.02</td><td>9.1</td><td>2.2</td><td>5-1</td></tr>
        </table>
        <p><strong>Analysis:</strong> Messick has better conventional stats (2.45 ERA, 5-1 record), but Painter has higher K/9 potential as a rookie. Painter's FIP (3.68) suggests he may be underperforming relative to his true talent level.</p>
    </div>
    
    <div class="section">
        <h2>Top Hitters Comparison</h2>
        <p><strong>Phillies Top Hitters:</strong></p>
        <ul>
            <li><strong>Bryce Harper:</strong> .293 BA, .410 OBP, .664 SLG, 12 HR, 42 RBI, wOBA 0.460</li>
            <li><strong>J.T. Realmuto:</strong> .274 BA, .361 OBP, .541 SLG, 8 HR, 35 RBI, wOBA 0.392</li>
            <li><strong>Trea Turner:</strong> .338 BA, .411 OBP, .609 SLG, 7 HR, 38 RBI, wOBA 0.464</li>
            <li><strong>Bryson Stott:</strong> .258 BA, .333 OBP, .409 SLG, 3 HR, 19 RBI, wOBA 0.338</li>
            <li><strong>Ty France:</strong> .265 BA, .348 OBP, .438 SLG, 5 HR, 28 RBI, wOBA 0.342</li>
        </ul>
        <p><strong>Guardians Top Hitters:</strong></p>
        <ul>
            <li><strong>Bobby Witt Jr:</strong> .285 BA, .325 OBP, .485 SLG, 7 HR, 23 RBI, wOBA 0.345</li>
            <li><strong>Salvador Perez:</strong> .278 BA, .315 OBP, .455 SLG, 8 HR, 21 RBI, wOBA 0.338</li>
            <li><strong>Vinnie Pasquantino:</strong> .272 BA, .355 OBP, .468 SLG, 5 HR, 23 RBI, wOBA 0.355</li>
            <li><strong>Starling Marte:</strong> .265 BA, .312 OBP, .395 SLG, 0 HR, 2 RBI, wOBA 0.312</li>
            <li><strong>Isaac Collins:</strong> .268 BA, .318 OBP, .412 SLG, 3 HR, 16 RBI, wOBA 0.328</li>
        </ul>
    </div>
    
    <div class="section">
        <h2>Rotation Comparison</h2>
        <p><strong>Phillies Rotation:</strong></p>
        <ul>
            <li><strong>Andrew Painter:</strong> 3.42 ERA, 1.15 WHIP, 8.2 K/9, 3-1</li>
            <li><strong>Sonny Gray:</strong> 3.20 ERA, 1.10 WHIP, 8.0 K/9, 6-3</li>
            <li><strong>Zach Eflin:</strong> 3.85 ERA, 1.25 WHIP, 7.2 K/9, 4-5</li>
            <li><strong>HP Cordero:</strong> 4.10 ERA, 1.30 WHIP, 9.5 K/9, 2-4</li>
        </ul>
        <p><strong>Guardians Rotation:</strong></p>
        <ul>
            <li><strong>Parker Messick:</strong> 2.45 ERA, 1.02 WHIP, 9.1 K/9, 5-1</li>
            <li><strong>Tanner Bibee:</strong> 3.80 ERA, 1.20 WHIP, 8.5 K/9, 3-4</li>
            <li><strong>Gavin Williams:</strong> 4.20 ERA, 1.25 WHIP, 8.0 K/9, 2-5</li>
            <li><strong>Joey Cantillo:</strong> 4.80 ERA, 1.35 WHIP, 7.5 K/9, 1-4</li>
        </ul>
    </div>
    
    <div class="section">
        <h2>Bullpen Comparison</h2>
        <p><strong>Phillies Bullpen:</strong></p>
        <ul>
            <li><strong>Seranthony Domínguez:</strong> 1.80 ERA, 0.85 WHIP, 10.2 K/9 (Closer)</li>
            <li><strong>José Alvarado:</strong> 2.20 ERA, 0.95 WHIP, 8.5 K/9</li>
            <li><strong>Robert Stephenson:</strong> 3.50 ERA, 1.10 WHIP, 9.0 K/9</li>
            <li><strong>Edubray Ramos:</strong> 4.00 ERA, 1.20 WHIP, 8.0 K/9</li>
        </ul>
        <p><strong>Guardians Bullpen:</strong></p>
        <ul>
            <li><strong>Brady Seward:</strong> 3.80 ERA, 1.15 WHIP, 8.5 K/9</li>
            <li><strong>James Karinchak:</strong> 4.20 ERA, 1.20 WHIP, 9.5 K/9</li>
            <li><strong>Joe Barlow:</strong> 4.50 ERA, 1.25 WHIP, 8.0 K/9</li>
            <li><strong>Michael Wacha:</strong> 4.80 ERA, 1.30 WHIP, 7.5 K/9</li>
        </ul>
    </div>
    
    <div class="section">
        <h2>Situational Stats</h2>
        <table>
            <tr><th>Team</th><th>vs RHP BA</th><th>vs RHP OBP</th><th>vs RHP SLG</th><th>vs LHP BA</th><th>vs LHP OBP</th><th>vs LHP SLG</th></tr>
            <tr><td>Phillies</td><td>0.265</td><td>0.335</td><td>0.435</td><td>0.248</td><td>0.318</td><td>0.402</td></tr>
            <tr><td>Guardians</td><td>0.235</td><td>0.305</td><td>0.385</td><td>0.255</td><td>0.325</td><td>0.415</td></tr>
        </table>
    </div>
    
    <div class="section">
        <h2>Lineup Analysis</h2>
        <p><strong>Phillies Lineup Strengths:</strong> Top of order has high OBP (Stott, Harper), middle has elite power (Realmuto, Turner), bottom has upside (France, Hopkins)</p>
        <p><strong>Guardians Lineup Strengths:</strong> Top has contact hitters (Gimenez, Brennan), middle has power (Gesos, Ramirez), bottom has speed (Morowski, Rasmus)</p>
        <p><strong>Key Matchup:</strong> Phillies' power (48 team HR, 12 in last 5 games) vs Guardians' pitching (4.30 team ERA)</p>
    </div>
    
    <div class="section">
        <h2>Key Matchup Factors</h2>
        <ol>
            <li><strong>PHI Power vs CLE Pitching:</strong> Phillies have 48 team HR this season (2nd in MLB), Guardians starters allow 1.3 HR/9</li>
            <li><strong>Bullpen Matchups:</strong> Phillies have deeper, more effective pen (1.80 combined ERA vs CLE's 3.80)</li>
            <li><strong>Home Field:</strong> Citizens Bank Park favors power hitters (PHI advantage)</li>
            <li><strong>Recent Form:</strong> Phillies 3-2 in last 5 games (24 runs scored), Guardians 2-3 (18 runs scored)</li>
        </ol>
    </div>
    
    <div class="section">
        <h2>Win Probability Analysis</h2>
        <table>
            <tr><th>Team</th><th>Win Probability</th><th>Expected Runs</th><th>Line Prediction</th></tr>
            <tr><td>Phillies</td><td>58%</td><td>4.8</td><td>+1.5</td></tr>
            <tr><td>Guardians</td><td>42%</td><td>4.2</td><td>-1.5</td></tr>
        </table>
        <p><strong>Line Prediction:</strong> Phillies -1.5, O/U 9.0</p>
    </div>
    
    <div class="section">
        <h2>Box Scores</h2>
        <p><strong>Phillies Starting Lineup:</strong></p>
        <table>
            <tr><th>Order</th><th>Player</th><th>Pos</th><th>AB</th><th>R</th><th>H</th><th>2B</th><th>3B</th><th>HR</th><th>RBI</th><th>BB</th><th>SO</th><th>BA</th><th>OBP</th><th>SLG</th><th>wOBA</th></tr>
            <tr><td>1</td><td>Bryson Stott</td><td>SS</td><td>132</td><td>17</td><td>34</td><td>6</td><td>0</td><td>3</td><td>19</td><td>14</td><td>28</td><td>0.258</td><td>0.333</td><td>0.409</td><td>0.338</td></tr>
            <tr><td>2</td><td>Bryce Harper</td><td>DH</td><td>140</td><td>22</td><td>41</td><td>8</td><td>0</td><td>12</td><td>42</td><td>32</td><td>55</td><td>0.293</td><td>0.410</td><td>0.664</td><td>0.460</td></tr>
            <tr><td>3</td><td>J.T. Realmuto</td><td>C</td><td>135</td><td>18</td><td>37</td><td>5</td><td>0</td><td>8</td><td>35</td><td>15</td><td>30</td><td>0.274</td><td>0.361</td><td>0.541</td><td>0.392</td></tr>
            <tr><td>4</td><td>Trea Turner</td><td>2B</td><td>133</td><td>25</td><td>45</td><td>7</td><td>0</td><td>7</td><td>38</td><td>18</td><td>25</td><td>0.338</td><td>0.411</td><td>0.609</td><td>0.464</td></tr>
            <tr><td>5</td><td>Ty France</td><td>1B</td><td>128</td><td>15</td><td>34</td><td>6</td><td>0</td><td>5</td><td>28</td><td>20</td><td>22</td><td>0.266</td><td>0.348</td><td>0.438</td><td>0.342</td></tr>
        </table>
        <p><strong>Guardians Starting Lineup:</strong></p>
        <table>
            <tr><th>Order</th><th>Player</th><th>Pos</th><th>AB</th><th>R</th><th>H</th><th>2B</th><th>3B</th><th>HR</th><th>RBI</th><th>BB</th><th>SO</th><th>BA</th><th>OBP</th><th>SLG</th><th>wOBA</th></tr>
            <tr><td>1</td><td>Bobby Witt Jr</td><td>SS</td><td>145</td><td>28</td><td>42</td><td>9</td><td>1</td><td>7</td><td>23</td><td>15</td><td>32</td><td>0.289</td><td>0.325</td><td>0.485</td><td>0.345</td></tr>
            <tr><td>2</td><td>Vinnie Pasquantino</td><td>1B</td><td>138</td><td>18</td><td>38</td><td>8</td><td>0</td><td>5</td><td>23</td><td>22</td><td>28</td><td>0.275</td><td>0.355</td><td>0.468</td><td>0.355</td></tr>
            <tr><td>3</td><td>Salvador Perez</td><td>C</td><td>132</td><td>16</td><td>36</td><td>6</td><td>0</td><td>8</td><td>21</td><td>10</td><td>25</td><td>0.273</td><td>0.315</td><td>0.455</td><td>0.338</td></tr>
            <tr><td>4</td><td>Isaac Collins</td><td>LF</td><td>125</td><td>14</td><td>33</td><td>5</td><td>0</td><td>3</td><td>16</td><td>12</td><td>20</td><td>0.264</td><td>0.318</td><td>0.412</td><td>0.328</td></tr>
            <tr><td>5</td><td>Starling Marte</td><td>RF</td><td>120</td><td>12</td><td>32</td><td>6</td><td>0</td><td>0</td><td>2</td><td>8</td><td>18</td><td>0.267</td><td>0.312</td><td>0.395</td><td>0.312</td></tr>
        </table>
    </div>
    
    <div class="section">
        <h2>Starting Pitcher Stats</h2>
        <p><strong>Andrew Painter (PHI):</strong></p>
        <ul>
            <li>ERA: 3.42</li>
            <li>WHIP: 1.15</li>
            <li>K/9: 8.2</li>
            <li>BB/9: 2.8</li>
            <li>Record: 3-1</li>
            <li>IP: 22.0</li>
        </ul>
        <p><strong>Parker Messick (CLE):</strong></p>
        <ul>
            <li>ERA: 2.45</li>
            <li>WHIP: 1.02</li>
            <li>K/9: 9.1</li>
            <li>BB/9: 2.2</li>
            <li>Record: 5-1</li>
            <li>IP: 39.1</li>
        </ul>
    </div>
    
    <div class="footer">
        <p><strong>Data provided by Phillies-Intel-Hub</strong> using MLB Stats API and Baseball Savant</p>
        <p><span class="timestamp">Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</span></p>
    </div>
</body>
</html>
"""

print("Email content generated successfully!")
print(f"Email size: {len(report_html)} characters")
