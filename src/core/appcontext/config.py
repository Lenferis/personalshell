import yaml
from pathlib import Path

class Config:
    def __init__(self):
        self.config_path = {
            'base': Path(f"src/config/config_base.yaml"),
            'user': Path(f"config/config_user.yaml")
            
        }
            
        self.data = self._load_config()
    
    def _load_config(self):
        def deep_merge(base_dict, user_dict):
            result = base_dict.copy()
            for key, value in user_dict.items():
                if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = deep_merge(result[key], value)
                else:
                    result[key] = value
            return result

        base = yaml.safe_load(self.config_path['base'].read_text(encoding="utf-8"))
        user = yaml.safe_load(self.config_path['user'].read_text(encoding="utf-8"))
        return deep_merge(base, user)
    
    def get_version(self):
        return self.data["app"]["version"]
    def get_session_path(self):
        return self.data["paths"]["session"]
    
    def get_modulescore_path(self):
        return self.data["modules"]["core"]
    
    def get_modulesplugin_path(self):
        path_list = []
        if self.data["modules"]["plugins"]:
            for plugin in self.data["modules"]["plugins"]:
                for plugin_name, plugin_data in plugin.items():
                    if 'path' in plugin_data:
                        path_list.append(plugin_data['path'])
        return path_list
    
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