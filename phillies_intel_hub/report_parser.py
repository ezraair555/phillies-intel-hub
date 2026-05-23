import os
import re
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
import json
from io import StringIO


class PhilliesAnalyticsParser:
    """Parse Phillies Intelligence reports from Google Drive HTML/PDF files"""
    
    def __init__(self, reports_dir: str = '/home/lucas/.openclaw/workspace/phillies-intel-hub/data/google_drive_pdfs'):
        self.reports_dir = reports_dir
        self.parsed_reports = []
        
    def parse_html_file(self, filepath: str) -> Dict:
        """Parse a Phillies Intelligence HTML report"""
        
        with open(filepath, 'r') as f:
            content = f.read()
            
        soup = BeautifulSoup(content, 'html.parser')
        
        # Extract report metadata
        report = {
            'filepath': filepath,
            'filename': os.path.basename(filepath),
            'content': content,
            'soup': soup
        }
        
        # Extract title and date from header
        header = soup.find('div', class_='header')
        if header:
            h1 = header.find('h1')
            if h1:
                report['title'] = h1.get_text(strip=True)
            
            # Extract date from the paragraph with date info
            date_p = header.find('p')
            if date_p:
                report['date_range'] = date_p.get_text(strip=True)
        
        # Extract executive narrative
        narrative_div = soup.find('div', class_='narrative')
        if narrative_div:
            narrative_h2 = narrative_div.find('h2')
            if narrative_h2:
                report['narrative_section'] = narrative_h2.get_text(strip=True)
            # Get narrative text
            paragraphs = narrative_div.find_all('p')
            if paragraphs:
                report['narrative_text'] = ' '.join([p.get_text(strip=True) for p in paragraphs[:3]])
        
        # Extract benchmark boxes
        benchmark_boxes = soup.find_all('div', class_='benchmark-box')
        if benchmark_boxes:
            benchmarks = []
            for box in benchmark_boxes:
                text = box.get_text(strip=True)
                # Parse key metrics from benchmark text
                match = re.search(r'(Phillies|Team) Benchmark:\s*(.+?)\s+(leads|is|has)', text)
                if match:
                    benchmarks.append({
                        'type': 'benchmark',
                        'text': text,
                        'entity': match.group(2).strip()
                    })
            report['benchmarks'] = benchmarks
        
        # Extract tables if present
        tables = soup.find_all('table')
        if tables:
            table_data = []
            for i, table in enumerate(tables):
                try:
                    # Convert table to string and parse using StringIO
                    table_str = str(table)
                    df = pd.read_html(StringIO(table_str))[0] if table.find('tr') else pd.DataFrame()
                    table_data.append({
                        'index': i,
                        'columns': list(df.columns) if not df.empty else [],
                        'rows': len(df) if not df.empty else 0
                    })
                except Exception as e:
                    # Skip problematic tables
                    print(f"Warning: Could not parse table {i}: {e}")
                    table_data.append({'index': i, 'error': str(e)})
            report['tables'] = table_data
        
        # Extract charts
        chart_boxes = soup.find_all('div', class_='chart-box')
        if chart_boxes:
            charts = []
            for box in chart_boxes:
                img = box.find('img')
                if img and img.get('src'):
                    charts.append({
                        'type': 'chart',
                        'src': img.get('src')[:50] + '...' if len(img.get('src', '')) > 50 else img.get('src', '')
                    })
            report['charts'] = charts
        
        # Extract Sabermetric sections
        sabermetric_div = soup.find('div', string=re.compile(r'Sabermetric|EB Shrinkage'))
        if sabermetric_div:
            report['has_sabermetrics'] = True
            # Find related text
            parent = sabermetric_div.find_parent()
            if parent:
                report['sabermetrics_section'] = parent.get_text(strip=True)[:200]
        
        # Extract player tables
        player_tables = []
        for table in tables:
            try:
                table_str = str(table)
                df = pd.read_html(StringIO(table_str))[0] if table.find('tr') else pd.DataFrame()
                if not df.empty:
                    # Check if it looks like a player stat table
                    cols = [str(c).lower() for c in df.columns]
                    if any('ba' in c or 'obp' in c or 'slg' in c or 'war' in c for c in cols):
                        player_tables.append(df)
            except:
                pass
        
        if player_tables:
            report['player_tables'] = player_tables
        
        self.parsed_reports.append(report)
        return report
    
    def parse_all_reports(self) -> List[Dict]:
        """Parse all reports in the directory"""
        if not os.path.exists(self.reports_dir):
            print(f"Directory not found: {self.reports_dir}")
            return []
        
        reports = []
        for filename in sorted(os.listdir(self.reports_dir)):
            if filename.endswith('.html'):
                filepath = os.path.join(self.reports_dir, filename)
                report = self.parse_html_file(filepath)
                reports.append(report)
                print(f"Parsed: {filename}")
        
        return reports
    
    def extract_key_metrics(self, report: Dict) -> Dict:
        """Extract key metrics from a parsed report"""
        metrics = {
            'phillies_team_id': 'PHI',
            'report_date': None,
            'player_stats': [],
            'team_stats': {},
            'benchmarks': []
        }
        
        # Extract benchmarks from report
        if 'benchmarks' in report:
            for bench in report['benchmarks']:
                metrics['benchmarks'].append(bench['entity'])
        
        # Extract player tables
        if 'player_tables' in report:
            for df in report['player_tables']:
                # Convert to list of dictionaries
                players = df.to_dict('records')
                metrics['player_stats'].extend(players)
        
        # Extract team stats from Sabermetrics section
        if 'sabermetrics_section' in report:
            sabermetrics_text = report['sabermetrics_section']
            # Extract key sabermetric values
            patterns = {
                'woba': r'wOBA[:\s]+([0-9.]+)',
                'era': r'ERA[:\s]+([0-9.]+)',
                'fip': r'FIP[:\s]+([0-9.]+)',
                'xbat': r'xBA[:\s]+([0-9.]+)',
                'xslg': r'xSLG[:\s]+([0-9.]+)',
            }
            
            for key, pattern in patterns.items():
                match = re.search(pattern, sabermetrics_text, re.IGNORECASE)
                if match:
                    metrics['team_stats'][key] = float(match.group(1))
        
        return metrics
    
    def get_player_stats_summary(self, reports: List[Dict]) -> pd.DataFrame:
        """Combine player stats from multiple reports"""
        all_players = []
        
        for report in reports:
            if 'player_tables' in report:
                for df in report['player_tables']:
                    if not df.empty:
                        # Add source info
                        df['source_file'] = report['filename']
                        df['parsed_date'] = pd.Timestamp.now().strftime('%Y-%m-%d')
                        all_players.append(df)
        
        if all_players:
            return pd.concat(all_players, ignore_index=True)
        return pd.DataFrame()
    
    def save_parsed_data(self, output_dir: str = '/home/lucas/.openclaw/workspace/phillies-intel-hub/data/parsed'):
        """Save parsed data to JSON and CSV"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Save all parsed reports
        for report in self.parsed_reports:
            output_file = os.path.join(output_dir, f"{os.path.splitext(report['filename'])[0]}_parsed.json")
            # Convert BeautifulSoup to string for JSON serialization
            report_copy = report.copy()
            report_copy['soup'] = str(report_copy['soup'])[:1000]  # Truncate for JSON
            
            with open(output_file, 'w') as f:
                json.dump(report_copy, f, indent=2)
        
        # Save combined player stats
        combined_df = self.get_player_stats_summary(self.parsed_reports)
        if not combined_df.empty:
            combined_df.to_csv(os.path.join(output_dir, 'combined_player_stats.csv'), index=False)
        
        print(f"Saved parsed data to {output_dir}")


def main():
    """Main function to parse Phillies Intelligence reports"""
    
    parser = PhilliesAnalyticsParser()
    
    print("Parsing Phillies Intelligence reports...")
    reports = parser.parse_all_reports()
    
    print(f"\nParsed {len(reports)} reports")
    
    if reports:
        # Extract key metrics from first report
        print("\n" + "="*50)
        print("Key Metrics from Latest Report:")
        print("="*50)
        
        metrics = parser.extract_key_metrics(reports[-1])
        print(f"Benchmarks: {metrics['benchmarks'][:3]}...")
        print(f"Team Stats: {metrics['team_stats']}")
        
        if metrics['player_stats']:
            print(f"\nPlayer Stats (first 3):")
            for player in metrics['player_stats'][:3]:
                print(f"  {player.get('Player', 'Unknown')}: "
                      f"BA {player.get('BA', 'N/A')}, OBP {player.get('OBP', 'N/A')}, "
                      f"SLG {player.get('SLG', 'N/A')}, HR {player.get('HR', 'N/A')}")
        
        # Save parsed data
        print("\nSaving parsed data...")
        parser.save_parsed_data()
        
        # Summary
        print("\n" + "="*50)
        print("Parsing Complete!")
        print("="*50)
        print(f"Total reports parsed: {len(reports)}")
        print(f"Reports saved to: /home/lucas/.openclaw/workspace/phillies-intel-hub/data/parsed")
    else:
        print("No reports found to parse.")


if __name__ == '__main__':
    main()
