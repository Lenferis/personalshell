import yaml
from pathlib import Path

class Config:
    def __init__(self):
        self.data = self._load_config()
    
    def _load_config(self):
        config_path = Path(f"config/config.yaml")
        return yaml.safe_load(config_path.read_text(encoding="utf-8"))
    
    def get_session_path(self):
        return self.data["paths"]["session"]
    
    def get_modulescore_path(self):
        return self.data["modules"]["core"]
    
    def commands_paths(self):
        return [Path(p) for p in self.data["paths"]["commands"]]

    def get_integration_config(self, name):
        return self.data["integrations"].get(name, {})