
from analyzer.storage import ReportStorage
import json

from pathlib import Path
from typing import List, Tuple



class ExclusionManager:
    def __init__(self, script_dir: Path):
        self.script_dir = script_dir
        self.exclusion_file = script_dir / "exclude.json"
        
        self._sync_from_mongodb()
        self.exclusions = self._load_exclusions()

    def _load_exclusions(self) -> List[Tuple[str, str]]:
        if not self.exclusion_file.exists():
            print("exclude.json not found. No exclusions loaded.")
            return []
        
        try:
            with open(self.exclusion_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            return [(item["domain"].lower(), item["type"].lower()) for item in data]
        except Exception as e:
            print(f"Error loading exclude.json: {e}")
            return []
    
    def _save_exclusions(self, exclusions: List[Tuple[str, str]]) -> bool:
        try:
            data = [{"domain": d, "type": t} for d, t in exclusions]
            with open(self.exclusion_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            print(f"Saved {len(exclusions)} exclusions to {self.exclusion_file}")
            return True
        except Exception as e:
            print(f"Error saving exclude.json: {e}")
            return False
    
    def _sync_from_mongodb(self) -> bool:
        try:
            storage = ReportStorage()
            exclusions = storage.get_exclusions()
            storage.close()
            self._save_exclusions(exclusions)
            return True
        except Exception as e:
            print(f"Could not sync exclusions from MongoDB: {e}")
            return False

    @staticmethod
    def _is_numeric_domain(domain: str) -> bool:
        parts = domain.split('.')
        return all(part.isdigit() for part in parts)
    
    def is_excluded(self, domain: str) -> bool:
        domain = domain.lower()
        
        if self._is_numeric_domain(domain):
            return True
        
        for pattern, ptype in self.exclusions:
            if ptype == "exact":
                if domain == pattern or domain.endswith("." + pattern):
                    return True
            elif ptype == "prefix":
                if domain.startswith(pattern):
                    return True
            elif ptype == "suffix":
                if domain.endswith(pattern):
                    return True
        
        return False