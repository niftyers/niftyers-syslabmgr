"""
Proxy Log Analyzer - Main orchestrator.
"""

from analyzer import (
    RunMode, LogLoader, ReportStorage, 
    ExclusionManager, UserActivityProcessor
)

import os
import sys

from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, List, Dict
from dotenv import load_dotenv

load_dotenv()

class LogAnalyzer:
    """Main analyzer class supporting different run modes."""
    
    def __init__(self):

        log_dir = os.getenv("LOG_SOURCE")
        if not log_dir:
            print("❌ ERROR: LOG_SOURCE not set in .env file")
            sys.exit(1)
        
        self.base_log_dir = Path(log_dir)
        if not self.base_log_dir.exists():
            print(f"❌ ERROR: Log directory does not exist: {self.base_log_dir}")
            sys.exit(1)
        
        self.script_dir = Path(__file__).parent
        self.exclusion_manager = ExclusionManager(self.script_dir)
        self.log_loader = LogLoader(self.base_log_dir)
        self.report_storage = ReportStorage()
        
    def analyze_daily(self) -> Optional[Dict]:
        today = datetime.now()
        return self.analyze_date(today)
    
    def analyze_date(self, date: datetime) -> Optional[Dict]:
        print(f"\n🔍 Analyzing logs for {date.strftime('%Y-%m-%d')}")
        print("-" * 80)

        logs = self.log_loader.load_logs_for_date(date)
        if not logs:
            print("❌ No valid logs found for this date!")
            return None
        
        processor = UserActivityProcessor(self.exclusion_manager)
        processor.process_logs(logs)
        report = processor.generate_report(date)
        
        report_dict = {
            "date": report.date,
            "users": [
                {
                    "username": user.username,
                    "pcs": [
                        {
                            "ip": pc.ip,
                            "domains": [
                                {"name": d.name, "count": d.count} 
                                for d in pc.domains
                            ],
                            "count": pc.count
                        }
                        for pc in user.pcs
                    ],
                    "total_count": user.total_count
                }
                for user in report.users
            ]
        }
        
        self.report_storage.save_report(report_dict)
        return report_dict
    
    def analyze_date_range(self, start_date: datetime, end_date: datetime) -> List[Dict]:
        print(f"\n🔍 Analyzing logs from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
        print("-" * 80)
        
        reports = []
        current_date = start_date
        
        while current_date <= end_date:
            try:
                report = self.analyze_date(current_date)
                if report:
                    reports.append(report)
            except Exception as e:
                print(f"❌ Error processing {current_date.strftime('%Y-%m-%d')}: {e}")
            
            current_date += timedelta(days=1)
        
        return reports
    
    def run(self, mode: RunMode = RunMode.DAILY, 
            start_date: Optional[datetime] = None,
            end_date: Optional[datetime] = None):
        print("🚀 Starting Log Analyzer...")
        print("=" * 80)
        
        if mode == RunMode.DAILY:
            self.analyze_daily()
        elif mode == RunMode.DATE:
            if not start_date:
                raise ValueError("start_date is required for DATE mode")
            self.analyze_date(start_date)
        elif mode == RunMode.RANGE:
            if not start_date or not end_date:
                raise ValueError("start_date and end_date are required for RANGE mode")
            self.analyze_date_range(start_date, end_date)
        else:
            raise ValueError(f"Invalid mode: {mode}")
        
        self.report_storage.close()
        print("\n✅ Analysis complete!")


def parse_date(date_str: str) -> datetime:
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Invalid date format: {date_str}. Use YYYY-MM-DD")


def main():
    if len(sys.argv) == 1:
        analyzer = LogAnalyzer()
        analyzer.run(mode=RunMode.DAILY)
    
    elif len(sys.argv) == 2:
        try:
            date = parse_date(sys.argv[1])
            analyzer = LogAnalyzer()
            analyzer.run(mode=RunMode.DATE, start_date=date)
        except ValueError as e:
            print(f"❌ Error: {e}")
            sys.exit(1)
    
    elif len(sys.argv) == 3:
        try:
            start_date = parse_date(sys.argv[1])
            end_date = parse_date(sys.argv[2])
            if start_date > end_date:
                print("❌ Error: Start date must be before end date")
                sys.exit(1)
            
            analyzer = LogAnalyzer()
            analyzer.run(mode=RunMode.RANGE, start_date=start_date, end_date=end_date)
        except ValueError as e:
            print(f"❌ Error: {e}")
            sys.exit(1)
    
    else:
        print("Usage:")
        print("  python analyzer.py               # Run for today")
        print("  python analyzer.py YYYY-MM-DD    # Run for specific date")
        print("  python analyzer.py YYYY-MM-DD YYYY-MM-DD # Run for date range")
        sys.exit(1)


if __name__ == "__main__":
    main()