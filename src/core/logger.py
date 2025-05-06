from pathlib import Path
from typing import Dict, Any
import logging

class Logger:
    """
    A class for saving and logging the necessary objects and data (execution of commands, launching applications and their operation).
    """
    def __init__(self, dir: str):
        self.log_dir = Path(dir)
        self.file_log_dir = self.log_dir / "pccl.log"
        self.setup_logger()

    def setup_logger(self) -> None:
        """
        Setting up the logger
        """
        logger = logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s | %(levelname)s | %(message)s',
            handlers=[
                logging.FileHandler(self.file_log_dir),
                logging.StreamHandler()
            ])
    def log_command_brief(self, name: str, Exception = None) -> None:
        """
        Simple logging, records only the command name and the error if there is one.
        """
        if not Exception:
            logging.info(f"The command was executed {name}")
        else:
            logging.error(f"Failed to execute the command {name}, {Exception}")
    def log_command_json(self, parse: Dict[str, Any], context: Dict[str, Any], success: bool, result: Any) -> None:
        """
        Logging with json, records all command parameters
        """
        log_json = {
            "command":parse['parse']['command'],
            "args":parse['parse']['args'],
            "kwargs":parse['parse']['kwargs'],
            "flags":parse['parse']['flags'],
            "success":success,
            "context":context,
            "result":result
        }
        if success:
            logging.info(log_json)
        else:
            logging.error(log_json)


