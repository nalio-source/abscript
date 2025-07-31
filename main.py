PROGRAM         = "ABScript"  # abs in short
MADE_BY         = "NALIo"
VERSION         = "0.1.0-dev"
LATEST_UPDATE   = "31/07/2025"
FIRST_UPDATE    = "29/07/2025"

CHANGELOG = """
- Created main.py
- Added basic string "compilation" into commands
- Added basic Script class with basic operations
- Added special_split, to account for parenthesis
- Added special_contains, to account for parenthesis
- Modified many operators
- Added sub operator (:)
- Now you can run script inside scripts
- Added comments
"""



def cmd_get(script, arguments):
    print(f"OUTPUT> {script.value(arguments[0])}")
    return "void"

def cmd_set(script, arguments):
    if len(arguments) == 1:
        return script.value(arguments[0])
    else: script.variables[arguments[0]] = script.value(arguments[1])
    return "void"

def cmd_increase(script, arguments):
    script.variables[arguments[0]] += script.value(arguments[1])
    return "void"

def cmd_mark(script, arguments):
    return "Error: mark not implemented yet"

def cmd_if(script, arguments):
    return "Error: if not implemented yet"

def cmd_repeat(script, arguments):
    return "Error: repeat not implemented yet"

def cmd_nothing(script, arguments):
    return "void"


COMMANDS = {
    ">": cmd_get,
    "<": cmd_set,
    "+": cmd_increase,
    ".": cmd_mark,
    "?": cmd_if,
    "*": cmd_repeat,
    "#": cmd_nothing,
}


def special_split(string, separator, openers="[(", closers="])"):
    split = [""]
    cont = 0
    for l in string:
        if (l in openers):
            cont += 1 
        if (l in closers):
            cont -= 1
        if (l == separator) and (cont == 0):
            split.append("")
            continue 
        split[-1] += l
    return split

def special_contains(string, wanted, openers="[(", closers="])"):
    cont = 0
    for l in string:
        if (l in openers):
            cont += 1 
        if (l in closers):
            cont -= 1
        if (l == wanted) and (cont == 0):
            return True
    return False


def from_string_to_line(string):
    string = string.replace("\n",";")
    string = string.replace("\t","")
    return string


def from_line_to_lines(line):
    return list(filter(lambda l: l != "", special_split(line, ";")))


def from_lines_to_commands(lines):
    commands = []
    for line in lines:
        line = special_split(line, " ")
        line = list(filter(lambda l: l != "", line))
        commands.append(line[:])
    return commands


class Script:
    def __init__(self, string):
        self.string = string
        self.line = from_string_to_line(self.string)
        self.lines = from_line_to_lines(self.line)
        self.commands = from_lines_to_commands(self.lines)
        self.variables = {}

    def value(self, argument):
        if argument in self.variables.keys():
            return self.variables[argument]
        
        if len(argument) >= 2:
            if argument[0] == "[" and argument[-1] == "]":
                return argument[1:-1]
            if argument[0] == "(" and argument[-1] == ")":
                return self.value(argument[1:-1])

        for operation in ["+", "-", "*", "/", "^", ":"]:
            if not (special_contains(argument, operation)):
                continue
            a_list = special_split(argument, operation)
            a_list = [self.value(a_list[0]), self.value(a_list[1])]
            both_numbers = (type(a_list[0]) in [float, int]) and (type(a_list[1]) in [float, int])

            if operation == "+":
                if both_numbers:
                    return a_list[0] + a_list[1]
                return str(a_list[0]) + str(a_list[1])
            
            elif operation == "-":
                if both_numbers:
                    return a_list[0] - a_list[1]
                if type(a_list[1]) in [float, int]:
                    if a_list[1] == 0:
                        return a_list[0]
                    return a_list[0][:-(a_list[1])]
                return str(a_list[0])+"-"+str(a_list[1])
            
            elif operation == "*":
                if type(a_list[0]) != str or type(a_list[1]) != str:
                    return a_list[0] * a_list[1]
                return a_list[0]+"*"+a_list[1]
            
            elif operation == "/":
                if both_numbers:
                    return a_list[0] / a_list[1]
                if type(a_list[0]) == str and type(a_list[1]) != str:
                    return special_split(a_list[0], a_list[1])
                return str(a_list[0])+"/"+a_list[1]
            
            elif operation == "^":
                if both_numbers:
                    return a_list[0] ** a_list[1]
                if special_contains(str(a_list[0]), str(a_list[1])):
                    return "true"
                else: return "false"
            
            elif operation == ":":
                if a_list[0] == "run":
                    return execute_script(a_list[1], self.variables)
                return str(a_list[0])+":"+str(a_list[1])
        try:
            return eval(argument)
        except: return argument

    def execute_command(self, command):
        cmd = command[0]
        arguments = command[1:]

        if cmd in COMMANDS.keys():
            return COMMANDS[cmd](self, arguments)
        else: return cmd_nothing(self, arguments)

    def execute(self, variables):
        self.variables = variables
        for command in self.commands:
            execution = self.execute_command(command) 
            if execution != "void":
                return execution
        return "void"


def execute_script(script_string, parameters):
    script = Script(script_string)
    return script.execute(parameters)


script_txt = """
< word [Hello s]
< word word-1
+ word   world!
< word word+[ ]
< word word*3
> word

< run:script_2
# < run:[< 1+1]   <----  the result of this line is equal to the one above
"""
values = {"word": "test", "number": 0, "script_2": "< number number+2;< number"}

print(f"\nRETURNED: {execute_script(script_txt, values)}")
