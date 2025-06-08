from src.modules.command import Command, ArgumentType
from pathlib import Path
from os import chmod, remove, stat
import re
class FileCommand(Command):
    """Main file operations command."""
    
    def __init__(self):
        super().__init__()
        self.name = "file"
        self.description = "File system operations"
        
        self.add_subcommand(FileCreateCommand())
        self.add_subcommand(FileWriteCommand())
        self.add_subcommand(FileReadCommand())
        self.add_subcommand(FileDeleteCommand())
        
        
    
    def execute_main(self, parse, appcontext):
        return "Available subcommands: create, read, delete, rename"

class FileCreateCommand(Command):
    def __init__(self):
        super().__init__()
        self.name = "create"
        self.description: str = "Create a new file"
        self.aliases = ["touch", "new"]
        self.register_argument()
    def register_argument(self):
        self.add_argument(
            name="path",
            arg_type=ArgumentType.POSITIONAL,
            required=True,
            default=False,
            help="File path"
        )
        self.add_argument(
            name="mode",
            arg_type=ArgumentType.NAMED,
            required=False,
            default='644',
            help="Access rights (e.g. 644)"
        )
        self.add_argument(
            name="overwrite",
            arg_type=ArgumentType.NAMED,
            required=False,
            default=False,
            help="Overwrite an existing file (-o)"
        )
    def execute_main(self, parse, context):
        path = Path(parse['parse']['args'][0])
        content = ''
        if ">" in parse['input_string']:
            content = re.search(r'>(.*)', parse['input_string']).group(1).lstrip()
        mode = int(parse['parse']['kwargs'].get('mode', "644"))
        overwrite = "o" in parse['parse']['flags']

        if Path(path).exists() and not overwrite:
            return f"Error: The file '{path}' already exists. Use -o to overwrite it."
        try:
            with open(path, 'w') as f:
                f.write(content)
                chmod(path, mode)
                return f"The file '{path}' was created with the permissions {oct(mode)[2:]}."
        except Exception as e:
            return f"Error: {str(e)}"


class FileWriteCommand(Command):
    def __init__(self):
            super().__init__()    
            self.name = "write"
            self.description: str = "Write text to a file"
            self.aliases = ["w", "echo"]
            self.register_argument()
    def register_argument(self):
        self.add_argument(
            name="path",
            arg_type=ArgumentType.POSITIONAL,
            required=True,
            default=False,
            help="File path"
        )
        self.add_argument(
            name="text",
            arg_type=ArgumentType.POSITIONAL,
            required=True,
            default=False,
            help="Text for recording"
        )
        self.add_argument(
            name="encoding",
            arg_type=ArgumentType.NAMED,
            required=False,
            default="utf-8",
            help="File encoding, default utf-8"
        )
        self.add_argument(
            name="append",
            arg_type=ArgumentType.FLAGS,
            required=False,
            default=False,
            help="Add to the end of the file (-a)"
        )
        self.add_argument(
            name="newline",
            arg_type=ArgumentType.FLAGS,
            required=False,
            default=False,
            help="Start the record on a new line (-n)"
        )
    def execute_main(self, parse, appcontext):
        path = Path(parse['parse']['args'][0])
        text = parse['parse']['args'][1]
        encoding = parse['parse']['kwargs'].get('encoding', 'utf-8')
        mode = 'a' if 'a' in parse['parse']['flags'] else 'w'
        newline = 'n' if 'n' in parse['parse']['flags'] else None
        
        if newline:
            text = fr"\n{text}"

        try:
            with open(path, mode, encoding=encoding) as f:
                f.write(text)
        except Exception as e:
            return f"Error: {str(e)}"
        
class FileReadCommand(Command):
    """Read file contents"""
    
    def __init__(self):
        super().__init__()
        self.name = "read"
        self.description = "Read file contents"
        self.register_arguments()
        self.is_subcommand = True

    def register_arguments(self):
        self.add_argument(
            name="path",
            arg_type=ArgumentType.POSITIONAL,
            required=True,
            help="File path to read"
        )
        
    def execute_main(self, parse, appcontext):
        path = parse['parse']['args'][0]
        
        try:
            with open(path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return f"File not found: {path}"
        except Exception as e:
            return f"Error reading file: {str(e)}"
        




class FileDeleteCommand(Command):
    """Delete specified file"""
    
    def __init__(self):
        super().__init__()
        self.name = "delete"
        self.description = "Delete a file"
        self.register_arguments()
        self.is_subcommand = True

    def register_arguments(self):
        self.add_argument(
            name="path",
            arg_type=ArgumentType.POSITIONAL,
            required=True,
            help="File path to delete"
        )
        
    def execute_main(self, parse, appcontext):
        path = parse['parse']['args'][0]
        
        try:
            import os
            os.remove(path)
            return f"Deleted file: {path}"
        except FileNotFoundError:
            return f"File not found: {path}"
        except Exception as e:
            return f"Error deleting file: {str(e)}"
