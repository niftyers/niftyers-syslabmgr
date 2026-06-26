import json
from pathlib import Path
from typing import List, Tuple


class ExclusionManager:
    def __init__(self, script_dir: Path):
        self.exclusions = self._load_exclusions(script_dir)
    
    @staticmethod
    def _load_exclusions(script_dir: Path) -> List[Tuple[str, str]]:
        exclusion_file = script_dir / "exclude.json"
        
        if not exclusion_file.exists():
            print("📂 exclude.json not found. No exclusions loaded.")
            return []
        
        with open(exclusion_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        return [(item["domain"].lower(), item["type"].lower()) for item in data]
    
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