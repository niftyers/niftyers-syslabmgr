import json
from pathlib import Path
from typing import Dict, Optional


class PCManager:
    
    def __init__(self, script_dir: Path):
        self.script_dir = script_dir
        self.pc_file = script_dir / "pc.json"
        self.mappings = self._load_mappings()
    
    def _load_mappings(self) -> Dict[str, str]:
        if not self.pc_file.exists():
            return {}
        
        try:
            with open(self.pc_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            mappings = {}
            for item in data:
                if "ip" in item and "name" in item:
                    mappings[item["ip"]] = item["name"]
            
            return mappings
        except Exception as e:
            return {}
    
    def get_pc_name(self, ip: str) -> str:
        return self.mappings.get(ip, ip)
    
    def reload(self) -> bool:
        self.mappings = self._load_mappings()
        return bool(self.mappings)