"""
User activity processing logic.
"""

from collections import defaultdict, Counter
from datetime import datetime
from typing import Dict, List

from .models import DomainStats, PcStats, UserStats, DailyReport
from .exclusion import ExclusionManager


class UserActivityProcessor:
    """Processes logs to build user activity data."""
    
    def __init__(self, exclusion_manager: ExclusionManager):
        self.exclusion_manager = exclusion_manager
        self.users = defaultdict(
            lambda: {
                "pcs": defaultdict(list),
                "timeline": [],
                "domain_counter": Counter(),
            }
        )
    
    @staticmethod
    def extract_domain(url: str) -> str:
        """Extract main domain from URL."""
        parts = url.split(".")
        if len(parts) >= 2:
            if len(parts) >= 3 and len(parts[-1]) == 2:
                return ".".join(parts[-3:])
            return ".".join(parts[-2:])
        return url
    
    def process_logs(self, logs: List) -> Dict:
        """Process logs to build user activity data."""
        self.users.clear()
        
        for entry in logs:
            user = entry.user or "unknown"
            ip = entry.ip
            url = entry.url
            status = entry.status
            
            # Skip unwanted status codes
            if status in [407, 403, 503]:
                continue
            
            # Skip invalid users
            if not user or user == "-" or user == "unknown" or user.startswith("SEMINARY"):
                continue
            
            # Extract and check domain
            domain = self.extract_domain(url)
            if self.exclusion_manager.is_excluded(domain):
                continue
            
            # Add to user data
            self.users[user]["pcs"][ip].append(entry)
            self.users[user]["timeline"].append(
                {"time": entry.timestamp, "pc": ip, "url": url}
            )
            self.users[user]["domain_counter"][domain] += 1
        
        return self.users
    
    def generate_report(self, date: datetime) -> DailyReport:
        """Generate report from processed user data."""
        report = DailyReport(date=date.strftime("%Y-%m-%d"), users=[])
        
        for user, data in self.users.items():
            if not data["pcs"]:
                continue
            
            user_pcs = []
            total_count = 0
            
            for ip, entries in data["pcs"].items():
                pc_domains = Counter()
                for entry in entries:
                    domain = self.extract_domain(entry.url)
                    pc_domains[domain] += 1
                
                domains_list = [DomainStats(name=d, count=c) for d, c in pc_domains.items()]
                domains_list.sort(key=lambda x: x.count, reverse=True)
                
                pc_stats = PcStats(
                    ip=ip,
                    domains=domains_list,
                    count=len(entries)
                )
                user_pcs.append(pc_stats)
                total_count += len(entries)
            
            user_pcs.sort(key=lambda x: x.count, reverse=True)
            
            user_stats = UserStats(
                username=user,
                pcs=user_pcs,
                total_count=total_count
            )
            report.users.append(user_stats)
        
        report.users.sort(key=lambda x: x.total_count, reverse=True)
        return report