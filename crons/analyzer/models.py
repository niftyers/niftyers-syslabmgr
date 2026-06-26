"""
Data models and enums for the proxy log analyzer.
"""

from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


class RunMode(Enum):
    """Available run modes for the analyzer."""
    DAILY = "daily"
    DATE = "date"
    RANGE = "range"


@dataclass
class DateRange:
    """Represents a date range for analysis."""
    start: datetime
    end: datetime
    
    def __post_init__(self):
        if self.start > self.end:
            raise ValueError("Start date must be before end date")


@dataclass
class LogEntry:
    """Represents a parsed log entry."""
    timestamp: datetime
    timestamp_raw: float
    user: Optional[str]
    ip: Optional[str]
    method: Optional[str]
    url: str
    status: Optional[int]
    raw_line: str


@dataclass
class DomainStats:
    """Statistics for a domain."""
    name: str
    count: int


@dataclass
class PcStats:
    """Statistics for a PC/IP."""
    ip: str
    domains: List[DomainStats]
    count: int


@dataclass
class UserStats:
    """Statistics for a user."""
    username: str
    pcs: List[PcStats]
    total_count: int


@dataclass
class DailyReport:
    """Daily report structure."""
    date: str
    users: List[UserStats]
    created_at: Optional[datetime] = None