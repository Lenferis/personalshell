import yaml
from pathlib import Path

class Config:
    def __init__(self):
        self.config_path = Path(f"config/config.yaml")
        self.data = self._load_config()
    
    def _load_config(self):
        return yaml.safe_load(self.config_path.read_text(encoding="utf-8"))
    
    def get_version(self):
        return self.data["app"]["version"]
    def get_session_path(self):
        return self.data["paths"]["session"]
    
    def get_modulescore_path(self):
        return self.data["modules"]["core"]
    
    def commands_paths(self):
        return [Path(p) for p in self.data["paths"]["commands"]]

    def get_integration_config(self, name):
        return self.data["integrations"].get(name, {})
    
    def change_config(self, keys, value):
        with open(self.config_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        current = data

        for key in keys[:-1]:
            if key not in current:
                return  # Прерываем если ключ не существует
            current = current[key]

        current[keys[-1]] = value

        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False)