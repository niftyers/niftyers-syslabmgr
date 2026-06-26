"""
MongoDB storage for reports.
"""

import os
from datetime import datetime
from pymongo.synchronous.mongo_client import MongoClient
from typing import Dict


class ReportStorage:
    def __init__(self):
        self.client = MongoClient(os.getenv("DATABASE_LOG"))
        self.db = self.client.get_database()
        self.collection = self.db["logs"]
    
    def save_report(self, report: Dict):
        report["created_at"] = datetime.now()
        
        self.collection.update_one(
            {"date": report["date"]},
            {"$set": report},
            upsert=True
        )
        print(f"✅ Report saved to MongoDB for {report['date']}")
    
    def close(self):
        self.client.close()