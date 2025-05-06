from command import Command, ArgumentType
from typing import Any, Dict, List
from pathlib import Path
import shutil
from os import chmod, remove, stat
import json

class FileCommand(Command):
    """
    Command for working with files
    """
    def __init__(self):
        super().__init__()
        self.name = "file"
        self.description: str = "Command for working with files"
        self.aliases = ["f"]
        self.register_argument()
        self.add_subcommand(FileCopyCommand())

    def register_argument(self):
        self.add_argument(
            name="source",
            arg_type=ArgumentType.POSITIONAL,
            required=True,
            default=False,
            help="Path to the object we are going to work with"
        )
    def execute_main(self, parse, context):
        source = Path(parse['args'][0])
        if not source.exists():
            source = Path(context['args']['current_dir']) / Path(parse['args'][0])
        with open(source, "r") as file1:
            read_content = file1.read()
            return read_content

class FileReadCommand(Command):
    def __init__(self):
        super().__init__()
        self.name = "read"
        self.description: str = "Reading text from a file"
        self.aliases = ["r", "cat", "show"]
        self.subcommands = False
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
            name="lines",
            arg_type=ArgumentType.NAMED,
            required=True,
            default=False,
            help="Number of rows to output"
        )
        self.add_argument(
            name="endcoding",
            arg_type=ArgumentType.NAMED,
            required=False,
            default="utf-8",
            help="File encoding, default utf-8"
        )
        self.add_argument(
            name="numbers",
            arg_type=ArgumentType.FLAGS,
            required=False,
            default=False,
            help="Show line numbers (-n)"
        )
    def execute_main(self, parse, context):
        path = Path(parse['parse']['args'][0])
        endcoding = parse['parse']['kwargs'].get('endcoding', 'utf-8')
        show_numbers = 'n' in parse['parse']['flags'][0]
        try:
            with open(path, 'r', encoding=endcoding) as f:
                lines = f.readlines()
                
                if 'lines' in parse['parse']['kwargs']:
                    lines = lines[:int(parse['parse']['kwargs']['lines'])]
                
                if show_numbers:
                    lines = [f"{i+1}: {line}" for i, line in enumerate(lines)]
                
                return ''.join(lines)
        except Exception as e:
            return f"Error: {str(e)}"

class FileWriteCommand(Command):
    def __init__(self):
            super().__init__()    
            self.name = "write"
            self.description: str = "Write text to a file"
            self.aliases = ["w", "echo"]
            self.subcommands = False
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
    def execute_main(self, parse, context):
        path = Path(parse['parse']['args'][1])
        encoding = parse['parse']['kwargs'].get('encoding', 'utf-8')
        mode = parse['parse']['args'][0]  if 'a' in parse['parse']['flags'] else 'w'
        newline = parse['parse']['args'][1]
        if not Path(path).is_dir() or not Path(path).parent.exists():
            return f"Error: This path does not exist {path}"
        
        if newline:
            text += '\n'

        try:
            with open(path, mode, encoding=encoding) as f:
                f.write(text)
        except Exception as e:
            return f"Error: {str(e)}"
       
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
            default='644',
            help="Overwrite an existing file (-o)"
        )
    def execute_main(self, parse, context):
        path = Path(parse['parse']['args'][0]) if Path(parse['args'][0]).parents.exists() else (Path(context['current_dir']) / Path(parse['parse']['args'][0])).parents.exists()
        mode = int(parse['parse']['kwargs'].get(mode, "644"))
        overwrite = "o" in parse['parse']['args']

        if Path(path) and not overwrite:
            return f"Error: The file '{path}' already exists. Use -f to overwrite it."
        try:
            with open(path, 'w'):
                chmod(path, mode)
                return f"The file '{path}' was created with the permissions {oct(mode)[2:]}."
        except Exception as e:
            return f"Error: {str(e)}"

class FileDeleteCommand(Command):
    def __init__(self):
        super().__init__()
        self.name = "delete"
        self.description = "Delete file"
        self.aliases = ["d","rm", "del"]
        self.register_argument()
    def register_argument(self):
        self.add_argument(
            name="path",
            arg_type=ArgumentType.POSITIONAL,
            required=True,
            default=False,
            help="File path"
        )
    def execute_main(self, parse, context):
        path = Path(parse['parse']['args'][0]) if Path(parse['args'][0]).parents.exists() else (Path(context['current_dir']) / Path(parse['parse']['args'][0])).parents.exists()
        try:
            remove(path)
            return f'File {path} has been deleted'
        except Exception as e:
            return f"Error: {str(e)}"
        
class FileCopyCommand(Command):
    """
    Subcommand of the file command to copy files
    """
    def __init__(self):
        super().__init__()
        self.name = "copy"
        self.description: str = "Copying files to the correct directory"
        self.aliases = ["cp", "dup"]
        self.register_argument()

    def register_argument(self):
        self.add_argument(
            name="source",
            arg_type=ArgumentType.POSITIONAL,
            required=True,
            default=False,
            help="Source file"
        )
        self.add_argument(
            name="destination",
            arg_type=ArgumentType.POSITIONAL,
            required=True,
            default=False,
            help="Destination path"
        )
        self.add_argument(
            name="overwrite",
            arg_type=ArgumentType.FLAGS,
            required=False,
            default=False,
            help="Overwrite existing file (-f)"
        )
        self.add_argument(
            name="preserve",
            arg_type=ArgumentType.FLAGS,
            required=False,
            default=False,
            help="Preserve metadata (-p)"
        )
    def execute_main(self, parse, context):
        src = Path(parse['parse']['args'][0]) if Path(parse['args'][0]).parents.exists() else (Path(context['current_dir']) / Path(parse['parse']['args'][0])).parents.exists()
        dest = Path(parse['parse']['args'][1]) if Path(src).exists() else (Path(context['current_dir']) / Path(src)).exists()
        overwrite = 'o' or 'overwrite' in parse['parse']['flags']
        preserve = 'p' or 'preserve' in parse['parse']['flags']
        if not Path(src).exists():
            return f"Error: Source file '{src}' does not exist."
        if not Path(dest).is_dir() or not Path(dest).exists():
            return f"Error: There is no destination {dest}"
        if (Path(dest) / Path(src).name).exists():
            return f"Error: File '{dest}' already exists. Use -f to overwrite."
        if preserve:
            shutil.copy2(src, dest)
        else:
            shutil.copy(src, dest)
        return f"File {src.name} is copied to {dest}"
    
class FileMoveCommand(Command):
    def __init__(self):
        super().__init__()
        self.name = "move"
        self.description = "Переместить или переименовать файл"
        self.aliases = ["m", "mv"]
        self.register_argument()
    def register_argument(self):
        self.add_argument(
            name="source",
            arg_type=ArgumentType.POSITIONAL,
            required=True,
            default=False,
            help="Source file"
        )
        self.add_argument(
            name="destination",
            arg_type=ArgumentType.POSITIONAL,
            required=True,
            default=False,
            help="Destination path"
        )
        self.add_argument(
            name="overwrite",
            arg_type=ArgumentType.FLAGS,
            required=False,
            default=False,
            help="Overwrite existing file (-f)"
        )
    def execute_main(self, parse, context):
        src = Path(parse['parse']['args'][0]) if Path(parse['args'][0]).exists() else (Path(context['current_dir']) / Path(parse['parse']['args'][0])).exists()
        dest = Path(parse['parse']['args'][0]) if Path(parse['args'][0]).parents.exists() else (Path(context['current_dir']) / Path(parse['parse']['args'][0])).parents.exists()
        overwrite = 'o' or 'overwrite' in parse['parse']['flags'] 
        if not Path(src).exists():
            return f"Error: Source file '{src}' does not exist."
        if not Path(dest).is_dir() or not Path(dest).exists():
            return f"Error: There is no destination {dest}"
        if (Path(dest) / Path(src).name).exists():
            return f"Error: File '{dest}' already exists. Use -f to overwrite."
        try:
            shutil.move(src, dest)
            return f"File moved from {src} to {dest}."
        except Exception as e:
            return f"Erroe: {str(e)}"

class FileInfoCommand(Command):
    def __init__(self):
        super().__init__()
        self.name = "info"
        self.description = "Show file information"
        self.aliases = ["stat", "details"]
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
            name="human",
            arg_type=ArgumentType.FLAGS,
            required=False,
            default=False,
            help="Human-readable format (-h)"
        )
        self.add_argument(
            name="json",
            arg_type=ArgumentType.FLAGS,
            required=False,
            default=False,
            help="Output in JSON format (-j)"
        )
    def execute_main(self, parse, context):
        path = Path(parse['parse']['args'][0]) if Path(parse['args'][0]).exists() else (Path(context['current_dir']) / Path(parse['parse']['args'][0])).exists()
        human = "h" in parse['parse']['args']
        as_json = "j" in parse['parse']['args']
        if not Path(path).exists():
            return f"Error: Source file '{path}' does not exist."

        try:
            stat = stat(path)
            info = {
                'path': Path(path).absolute,
                'size': stat.st_size,
                'created': stat.st_ctime,
                'modified': stat.st_mtime,
                'access': stat.st_atime,
                'mode': stat.st_mode,
                'owner': stat.st_uid,
                'group': stat.st_gid
            }
            
            if human:
                from humanize import naturalsize, naturaltime
                info['size'] = naturalsize(info['size'])
                info['created'] = naturaltime(info['created'])
                info['modified'] = naturaltime(info['modified'])
                info['access'] = naturaltime(info['access'])
                info['mode'] = oct(info['mode'])[-3:]
            
            if as_json:
                return json.dumps(info, indent=2, default=str)
            else:
                result = [
                    f"Информация о файле: {info['path']}",
                    f"Size: {info['size']}",
                    f"Created: {info['created']}",
                    f"Modified: {info['modified']}",
                    f"Last accessed: {info['access']}",
                    f"Permissions: {info['mode']}",
                    f"Owner: {info['owner']}",
                    f"Group: {info['group']}"
                ]
                return '\n'.join(result)
                
        except Exception as e:
            return f"Erroe: {str(e)}"



# print(FileCopyCommand().execute_main({'args':[fr'D:\Projects\pccl - Python custom comand line\ui\components\сonsoleInput.py','adad']}, {'args':{'current_dir': 'D:\Projects\pccl - Python custom comand line\commands'}}))
# s = 'D:\Projects\pccl - Python custom comand line\ui\components\сonsoleInput.py'
print(FileCommand().help())
        