"""
Log parsing utilities.
"""

import re
from datetime import datetime
from typing import List, Optional, Tuple
from .models import LogEntry


class LogParser:
    """Handles parsing of individual log lines."""
    
    @staticmethod
    def parse_line(line: str) -> Optional[LogEntry]:
        """Parse a single log line into structured data."""
        line = line.strip()
        if not line:
            return None

        try:
            parts = line.split(" ")
            
            # Extract timestamp
            timestamp_str = parts[0]
            timestamp = float(timestamp_str)
            dt = datetime.fromtimestamp(timestamp)
            
            # Extract user
            user = LogParser._extract_user(parts)
            
            # Extract IP
            ip = LogParser._extract_ip(parts)
            
            # Extract method and URL
            method, url = LogParser._extract_method_url(parts)
            
            # Extract status
            status = LogParser._extract_status(parts)
            
            if url and ip:
                url = url.split("/")[0] if "/" in url else url
                if url.endswith(":"):
                    url = url[:-1]
                
                return LogEntry(
                    timestamp=dt,
                    timestamp_raw=timestamp,
                    user=user,
                    ip=ip,
                    method=method,
                    url=url.lower(),
                    status=status,
                    raw_line=line,
                )
        except Exception:
            pass
        return None
    
    @staticmethod
    def _extract_user(parts: List[str]) -> Optional[str]:
        """Extract username from log parts."""
        user_part = None
        for part in parts:
            if "@" in part and not part.startswith("-"):
                user_part = part
                break
            elif "-" in part and len(part) <= 2:
                continue
        
        if user_part and "@" in user_part:
            user = user_part.split("@")[0]
            if user.endswith("$"):
                user = user[:-1] + "-MACHINE"
            return user
        return None
    
    @staticmethod
    def _extract_ip(parts: List[str]) -> Optional[str]:
        """Extract IP address from log parts."""
        for part in parts:
            if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", part):
                return part
        return None
    
    @staticmethod
    def _extract_method_url(parts: List[str]) -> Tuple[Optional[str], Optional[str]]:
        """Extract HTTP method and URL from log parts."""
        methods = ["CONNECT", "GET", "POST", "HEAD", "PUT", "DELETE"]
        
        for i, part in enumerate(parts):
            if part in methods:
                method = part
                url = None
                if i + 1 < len(parts):
                    url = parts[i + 1]
                    if url.startswith("http://") or url.startswith("https://"):
                        url = url.split("://")[1]
                    if ":" in url and not url.startswith("["):
                        url_parts = url.split(":")
                        if len(url_parts) > 1 and re.match(r"^[a-zA-Z0-9\-\.]+$", url_parts[0]):
                            url = url_parts[0]
                return method, url
        return None, None
    
    @staticmethod
    def _extract_status(parts: List[str]) -> Optional[int]:
        """Extract HTTP status code from log parts."""
        for part in parts:
            if part.isdigit() and len(part) == 3:
                return int(part)
        return None