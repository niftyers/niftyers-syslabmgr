import os

from ast import Tuple
from datetime import datetime
from pymongo.synchronous.mongo_client import MongoClient
from typing import Dict, List, Optional, Tuple


class ReportStorage:
    def __init__(self):
        self.client = MongoClient(os.getenv("DATABASE_LOG"))
        self.db = self.client.get_database()
        self.logs = self.db["logs"]
        self.excludes = self.db["excludes"]

    def close(self):
        self.client.close()
    
    def save_report(self, report: Dict):
        report["created_at"] = datetime.now()
        
        self.logs.update_one(
            {"date": report["date"]},
            {"$set": report},
            upsert=True
        )

    def get_exclusions(self) -> Optional[List[Tuple[str, str]]]:
        exclusions = []
        try:
            for doc in self.excludes.find({}):
                if "domain" in doc:
                    exclusions.append(
                        (doc["domain"].lower(), doc.get("type", "exact").lower())
                    )
            
            return exclusions
        
        except Exception as e:
            print(f"Error fetching exclusions from MongoDB: {e}")
            return []