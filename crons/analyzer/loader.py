from datetime import datetime
from pathlib import Path
from typing import List

from .models import LogEntry
from .parsers import LogParser


class LogLoader:
    def __init__(self, base_log_dir: Path):
        self.base_log_dir = base_log_dir
 
    def get_log_file_path(self, date: datetime) -> Path:
        year = date.strftime("%Y")
        month = date.strftime("%m")
        day_month_year = date.strftime("%d-%m-%y")
        
        return self.base_log_dir / year / month / day_month_year / "access.log.1"
    
    def load_logs_for_date(self, date: datetime) -> List[LogEntry]:
        log_file = self.get_log_file_path(date)
        logs = []
        
        if not log_file.exists():
            print(f"⚠️  Log file not found: {log_file}")
            return logs
        
        with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                entry = LogParser.parse_line(line)
                if entry:
                    logs.append(entry)
        return logs