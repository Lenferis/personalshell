from pathlib import Path
import json
from datetime import datetime
from typing import Dict, List, Any

class Session:
    """
    A class to create a session to store variables, env, etc.
    """
    def __init__(self, dir: str):
        self.dir = Path(dir)
        self.session_dir = self.dir / "session.json"

        #Переделать вид структуры данных с простых переменных на словарь
        # data = {
        #     vars:....
        #     env....
        # }
        self.variables = {}
        self.env = {}
        self.commands_raw = []
        self.start_time = datetime.now().isoformat()
        self.data = {
            "vars": self.variables,
            "env": self.env,
            "commands": self.commands_raw,
            'created_at': self.start_time,
            'updated_at': self.start_time
        }

        self.load()

    def add_variable(self, key: str, value: str) -> Any:
        """
        Adding a variable to a session file
        """
        self.data["vars"][key] = value
        self.save()
        return self.data["vars"][key]

    def add_env(self, key: str, value: str) -> Any:
        """
        Adding a env to a session file
        """
        self.data["env"][key] = value
        self.save()
        return self.data["env"][key]

    def add_commands(self, full_command: str) -> None:
        """
        Adding a command that was entered in the session file
        """
        self.data["commands"].append(full_command)
        self.save()
    
    def get_commands(self, index: int = None) -> Any:
        """
        Retrieving a previously entered command
        """
        return self.data["commands"][len(self.data["commands"]) - 1] if len(self.data["commands"]) < 10 else self.data["commands"][index]

    
    def get_variable(self, key: str, value: str) -> Any:
        """
        Retrieving a variable from a session file
        """
        return self.data["vars"].get(key)
    
    def get_env(self, key: str, value: str) -> Any:
        """
        Retrieving a variable env from a session file
        """
        return self.data["env"].get(key)
    

    def save(self) -> None:
        """
        Saving session variables in a separate file(json)
        """
        session = {
            "vars": self.data["vars"],
            "env": self.data["env"],
            "commands": self.data["commands"],
            'created_at': self.data["created_at"],
            'updated_at': datetime.now().isoformat()
        }
        with open(self.session_dir, "w", encoding='utf-8') as f:
            json.dump(session, f, indent=4)

    def load(self) -> Dict[str, Any]:
        """
        Loading session variables from a file
        """
        if not self.session_dir.exists():
            return self.save({},{},[])
        
        with open(self.session_dir, encoding='utf-8') as f:
            session = json.loads(f.read())

            self.data["vars"] = session["vars"]
            self.data["env"] = session["env"]
            self.data["commands"] = session["commands"]
            self.data["created_at"] = session["created_at"]
            self.data["updated_at"] = session["updated_at"]

        
        return session





        
