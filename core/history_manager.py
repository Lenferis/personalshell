from pathlib import Path
import logging

class HistoryManager:
    def __init__(self, dir):
        self.log_dir = Path(dir)
        self.file_log_dir = self.log_dir / "pccl.log"
        self.setup_logger()

    def setup_logger(self):
        logger = logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s | %(levelname)s | %(message)s',
            handlers=[
                logging.FileHandler(self.file_log_dir),
                logging.StreamHandler()
            ])
    def log_command_brief(self, command):
        logging.info(f"The command was executed {command}")
    def log_command_json(self, command, args, kwargs, flags, success):

        log_json = {
            "command":command,
            "args":args,
            "kwargs":kwargs,
            "flags":flags,
            "success":success
        }
        if success:
            logging.info(log_json)
        else:
            logging.error(log_json)
    def log_app(self):
        pass

