from pathlib import Path
import json
from datetime import datetime
class Session:
    def __init__(self, dir):
        self.dir = Path(dir)
        self.session_dir = self.dir / "session.json"
        self.variables = {}
        self.env = {}
        self.commands = []
        self.start_time = datetime.now()

    def save(self, variables, env, commands):
        session = {
            "vars":self.variables,
            "env":self.env,
            "commands":self.commands,
            'created_at': self.start_time,
            'updated_at': datetime.now().isoformat()
        }
        with open(self.session_dir, "w", encoding='utf-8'):
            json.dump(session)
            
    def load(self):
        if not self.session_dir.exists():
            return
        
        with open(self.session_dir, "w", encoding='utf-8') as f:
            session = json.load(f)

            self.variables = session["vars"]
            self.env = session["env"]
            self.commands = session["commands"]
            self.start_time = session["created_at"]





        
