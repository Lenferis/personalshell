import re
from typing import Dict, List, Any, TypedDict
class CommandParser:
    
    def __init__(self):
        self.arg_pattern = re.compile(r'--(\w+)=(.*)') 
        self.flag_pattern = re.compile(r'-(\w+)')

    def parse(self, input_string: str) -> Dict[str, Any]:
        """
        A function that parses a string and selects a command and arguments(positional, named and flags) from it.
        Main function of the command parser
        """
        if not input_string:
            return {"command": "", "args": [], "kwargs": {}, "flags": []}
        parts = self._split_input(input_string)
        if not parts:
            return {"command": "", "args": [], "kwargs": {}, "flags": []}

        command = parts[0]
        args = []
        kwargs = {}
        flags = []

        for part in parts[1:]:
            arg_match = self.arg_pattern.match(part)
            if arg_match:
                key, value = arg_match.groups()
                kwargs[key] = value
                continue

            flag_match = self.flag_pattern.match(part)
            if flag_match:
                flags.extend(flag_match.group(1))
                continue

            args.append(part)
        return {
            "input_string": input_string,
                "parse": {
                    "command": command,
                    "args": args,
                    "kwargs": kwargs,
                    "flags": flags
                    }
                }
    


    def _split_input(self, input_string: str) -> List[str]:
        """
        A function that splits a string into parts that can be a command, argument, etc., but we don't know what is what
        """
        parts = []
        current = []
        in_quotes = False
        quote_char = None

        for char in input_string.strip():
            if char in ('"', "'"):
                in_quotes = not in_quotes
                if in_quotes:
                    quote_char = char
                continue
                
            if char.isspace() and not in_quotes:
                if current:
                    parts.append(''.join(current))
                    current = []
                continue

            current.append(char)

        if current:
            parts.append(''.join(current))

        return parts 
