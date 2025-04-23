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
        self.variables = {}
        self.env = {}
        self.commands_raw = []
        self.start_time = datetime.now().isoformat()
        self.load()

    def add_variable(self, key: str, value: str) -> Any:
        """
        Adding a variable to a session file
        """
        self.variables[key] = value
        self.save()
        return self.variables[key]

    def add_env(self, key: str, value: str) -> Any:
        """
        Adding a env to a session file
        """
        self.env[key] = value
        self.save()
        return self.env[key]

    def add_commands(self, full_command: str) -> None:
        """
        Adding a command that was entered in the session file
        """
        self.commands_raw.append(full_command)
    
    def get_commands(self, index: int = None, slice: int = None) -> Any:
        """
        Retrieving a previously entered command
        """
        if index:
            return self.commands_raw[index]
        elif slice:
            return self.commands_raw[slice]
        else:
            return self.commands_raw
    
    def get_variable(self, key: str, value: str) -> Any:
        """
        Retrieving a variable from a session file
        """
        return self.variables.get(key)
    
    def get_env(self, key: str, value: str) -> Any:
        """
        Retrieving a variable env from a session file
        """
        return self.env.get(key)
    

    def save(self, variables: Dict[str, Any], env: Dict[str, Any], commands:List[str]) -> None:
        """
        Saving session variables in a separate file(json)
        """
        session = {
            "vars":self.variables,
            "env":self.env,
            "commands":self.commands_raw,
            'created_at': self.start_time,
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

            self.variables = session["vars"]
            self.env = session["env"]
            self.commands = session["commands"]
            self.start_time = session["created_at"]
        
        return session





        
