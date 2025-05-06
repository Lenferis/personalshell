from typing import Dict, Any
from dataclasses import dataclass
from .session import Session
from .config import Config

@dataclass
class AppContext:
    session: Session
    config: Config
    console: Any
    command_registry: Any
