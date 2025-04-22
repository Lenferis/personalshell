import re
class CommandParser:
    
    def __init__(self):
        self.arg_pattern = re.compile(r'--(\w+)=(.*)') 
        self.flag_pattern = re.compile(r'-(\w+)')

    def parse(self, input_string: str):
        """
        {
            "command": str,          
            "args": List[str],        
            "kwargs": Dict[str, str], 
            "flags": List[str]        
        }
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
        return {"command": command, "args": args, "kwargs": kwargs, "flags": flags}
    


    def _split_input(self, input_string: str):
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

test = CommandParser()
print(test.parse("download 334 wewewe --565='d aqw eqe qe'  -v -d -r"))