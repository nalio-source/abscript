PROGRAM         = "ABScript"  # abs in short
MADE_BY         = "NALIo"
VERSION         = "0.1.0-dev"
LATEST_UPDATE   = "29/07/2025"
FIRST_UPDATE    = "29/07/2025"

CHANGELOG = """
- Created main.py
- Added basic string "compilation" into commands
- Added basic Script class with basic operations
"""



def cmd_get(script, arguments):
    var_name = arguments[0]
    if var_name in script.variables.keys():
        return script.variables[var_name]
    else: return f"Error 1: variable {var_name} was not declared"

def cmd_set(script, arguments):
    script.variables[arguments[0]] = arguments[1]
    return f"set {arguments}"

def cmd_increase(script, arguments):
    script.variables[arguments[0]] += arguments[1]
    return f"increase {arguments}"

def cmd_mark(script, arguments):
    return f"mark {arguments}"

def cmd_if(script, arguments):
    return f"if {arguments}"

def cmd_repeat(script, arguments):
    return f"repeat {arguments}"

def cmd_nothing(script, arguments):
    return "void"


COMMANDS = {
    ">": cmd_get,
    "<": cmd_set,
    "+": cmd_increase,
    ".": cmd_mark,
    "?": cmd_if,
    "*": cmd_repeat,
}



def from_string_to_line(string):
    string = string.replace("\n",";")
    string = string.replace("\t","")
    return string


def from_line_to_lines(line):
    return list(filter(lambda l: l != "", line.split(";")))


def from_lines_to_commands(lines):
    commands = []
    for line in lines:
        line = line.split(" ")
        line = list(filter(lambda l: l != "", line))
        commands.append(line[:])
    return commands


class Script:
    def __init__(self, string):
        self.string = string
        self.line = from_string_to_line(self.string)
        self.lines = from_line_to_lines(self.line)
        self.commands = from_lines_to_commands(self.lines)
        print("PHASE 1:", self.string)
        print("PHASE 2:", self.line)
        print("PHASE 3:", self.lines)
        print("PHASE 4:", self.commands)
        self.variables = {}

    def value(self, argument):
        for operation in ["+", "-", "*", "/", "^"]:
            if not (operation in argument):
                continue
            a_list = argument.split(operation)

            if operation == "+":
                return a_list[0] + a_list[1]
            elif operation == "-":
                return a_list[0] - a_list[1]
            elif operation == "*":
                return a_list[0] * a_list[1]
            elif operation == "/":
                return a_list[0] / a_list[1]
            elif operation == "^":
                return a_list[0] ** a_list[1]
        return argument

    def execute_command(self, command):
        cmd = command[0]
        arguments = command[1:]
        for i in range(len(arguments)):
            arguments[i] = self.value(arguments[i])

        if cmd in COMMANDS.keys():
            print(COMMANDS[cmd](self, arguments))
        else:
            print(cmd_nothing(self, arguments))

    def execute(self, variables):
        self.variables = variables
        for command in self.commands:
            self.execute_command(command)
        return "Executed"


def execute_script(script_string, parameters):
    script = Script(script_string)
    return script.execute(parameters)


script_txt = """> word

+ word   world!
> word
"""
values = {"word": "Hello "}

print(f"\n{execute_script(script_txt, values)}")
