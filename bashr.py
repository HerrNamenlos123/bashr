import argparse
import os
    
mode = "powershell"
script_content = ""

parser = argparse.ArgumentParser(description='Bashr: A tool to auto-generate powershell and shell scripts')
parser.add_argument('--output-folder', dest='output_folder', type=str, help='Output folder to place the generated scripts into', required=False, default="out")
args = parser.parse_args()

class Echo:
    Bold = "\e[1m"
    Dim = "\e[2m"
    Italic = "\e[3m"
    Underline = "\e[4m"
    Invert = "\e[7m"
    Hidden = "\e[8m"
    Strike = "\e[9m"

    FgBlack = "\e[30m"
    FgRed = "\e[31m"
    FgGreen = "\e[32m"
    FgYellow = "\e[33m"
    FgBlue = "\e[34m"
    FgMagenta = "\e[35m"
    FgCyan = "\e[36m"
    FgLightGray = "\e[37m"
    FgGray = "\e[90m"
    FgLightRed = "\e[91m"
    FgLightGreen = "\e[92m"
    FgLightYellow = "\e[93m"
    FgLightBlue = "\e[94m"
    FgLightMagenta = "\e[95m"
    FgLightCyan = "\e[96m"
    FgWhite = "\e[97m"

    BgBlack = "\e[40m"
    BgRed = "\e[41m"
    BgGreen = "\e[42m"
    BgYellow = "\e[43m"
    BgBlue = "\e[44m"
    BgMagenta = "\e[45m"
    BgCyan = "\e[46m"
    BgLightGray = "\e[47m"
    BgGray = "\e[100m"
    BgLightRed = "\e[101m"
    BgLightGreen = "\e[102m"
    BgLightYellow = "\e[103m"
    BgLightBlue = "\e[104m"
    BgLightMagenta = "\e[105m"
    BgLightCyan = "\e[106m"
    BgWhite = "\e[107m"

def generate(script):
    global script_content
    global mode
    mode = "powershell"
    script_content = "Set-StrictMode -Version Latest\n"
    script_content += "$ErrorActionPreference = \"Stop\"\n"
    script_content += "function if_inline($condition, $then, $otherwise) {if ($condition) {$then} else {$otherwise}}\n"
    script()
    script_powershell = script_content

    mode = "shellscript"
    script_content = "#!/bin/bash\n"
    script_content += "set -e\n"
    script()
    script_shellscript = script_content

    os.makedirs(args.output_folder, exist_ok=True)
    with open(f'{args.output_folder}/run.ps1', "w") as f:
        f.write(script_powershell)
    with open(f'{args.output_folder}/run.sh', "w") as f:
        f.write(script_shellscript)

class BashrBuilder:
    sh_esc = "\e["
    ps_esc = "["

    def __init__(self, content=""):
        self.content = content

    def __del__(self):
        global script_content
        if self.content != "":
            script_content += self.content + "\n"

    def __eq__(self, other):
        raise Exception("BashrBuilder objects cannot be compared like this. Please use bashr.eq(..., ...) instead.")
    
    def __ne__(self, other):
        raise Exception("BashrBuilder objects cannot be compared like this. Please use bashr.ne(..., ...) instead.")

    def __lt__(self, other):
        raise Exception("BashrBuilder objects cannot be compared like this. Please use bashr.lt(..., ...) instead.")
        
    def __le__(self, other):
        raise Exception("BashrBuilder objects cannot be compared like this. Please use bashr.le(..., ...) instead.")
    
    def __ge__(self, other):
        raise Exception("BashrBuilder objects cannot be compared like this. Please use bashr.ge(..., ...) instead.")

    def __or__(self, other):
        if isinstance(other, BashrBuilder):
            self.content += " | " + other.content
            other.content = ""
        elif isinstance(other, str):
            self.content += " | " + other
        else:
            raise Exception("Only BashrBuilder objects can be piped together")
        return self
    
    def __gt__(self, other):
        if isinstance(other, BashrBuilder):
            self.content += " > " + other.content
            other.content = ""
        elif isinstance(other, str):
            self.content += " > " + other
        else:
            raise Exception("Only BashrBuilder objects can be piped together")
        return self
    
    def __str__(self):
        str = self.content
        self.content = ""
        return str
    
    def custom(self, ps, sh):
        if not self.powershell == "":
            self.powershell += " "
        if not self.shellscript == "":
            self.shellscript += " "

        self.powershell += ps
        self.shellscript += sh
    
    # def nullify_output(self):
    #     self.custom(ps=" | Out-Null", sh=" > /dev/null")
    #     return self
    
    def ignore_errors(self):
        self.custom(ps=" -ErrorAction SilentlyContinue", sh=" || true")
        return self
    
    def equals(self, expression):
        self.custom(ps=f" -eq {expression.powershell}", sh=f" == {expression.shellscript}")
        return self

    def touch(self, file, suppress_output=True, ignore_errors=False):
        # powershell_suppress = " | Out-Null" if suppress_output else ""
        # powershell_errors = " -ErrorAction SilentlyContinue" if ignore_errors else ""
        # self.prepare_powershell += f"if (Test-Path {file}) {{\n"
        # self.prepare_powershell += f"    (Get-Item {file}{powershell_errors}).LastWriteTime = Get-Date\n"
        # self.prepare_powershell += "} else {\n"
        # self.prepare_powershell += f"    New-Item -ItemType File{powershell_errors} -Path {file}{powershell_suppress}\n"
        # self.prepare_powershell += "}\n"
        
        # shellscript_suppress = " > /dev/null" if suppress_output else ""
        # shellscript_errors = " || true" if ignore_errors else ""
        # self.prepare_shellscript += f"touch {file}{shellscript_suppress}{shellscript_errors}\n"
        

        return self

def echo(message=""):
    contains_colors = message.find('\e[') != -1

    message = message.replace('"', '\\"')
    if mode == "powershell":
        msg = message.replace(BashrBuilder.sh_esc, BashrBuilder.ps_esc).replace('\\', '`')
        return BashrBuilder(f'(Write-Output ("{msg}{BashrBuilder.ps_esc + "0m" if contains_colors else ""}"))')
    else:
        return BashrBuilder(f'(echo -e "{message}{BashrBuilder.sh_esc + "0m" if contains_colors else ""}")')

def set_var(name, value):
    if mode == "powershell":
        return BashrBuilder(f"${name} = {value}")
    else:
        return BashrBuilder(f"{name}={value}")

def get_var(name):
    if mode == "powershell":
        return BashrBuilder(f"${name}")
    else:
        return BashrBuilder(f"${name}")
    
def null_sink():
    if mode == "powershell":
        return BashrBuilder("$null")
    else:
        return BashrBuilder("/dev/null")
    
def clear():
    if mode == "powershell":
        return BashrBuilder("(Clear-Host)")
    else:
        return BashrBuilder("(clear)")
    
def eq(first, second):
    if not isinstance(first, BashrBuilder):
        raise Exception("First argument must be a BashrBuilder object")
    if not isinstance(second, BashrBuilder):
        raise Exception("Second argument must be a BashrBuilder object")
    str = f'{first} -eq {second}' if mode == "powershell" else f'{first} == {second}'
    first.content = ""
    second.content = ""
    return BashrBuilder(str)

def ne(first, second):
    if not isinstance(first, BashrBuilder):
        raise Exception("First argument must be a BashrBuilder object")
    if not isinstance(second, BashrBuilder):
        raise Exception("Second argument must be a BashrBuilder object")
    str = f'{first} -ne {second}' if mode == "powershell" else f'{first} != {second}'
    first.content = ""
    second.content = ""
    return BashrBuilder(str)

def gt(first, second):
    if not isinstance(first, BashrBuilder):
        raise Exception("First argument must be a BashrBuilder object")
    if not isinstance(second, BashrBuilder):
        raise Exception("Second argument must be a BashrBuilder object")
    str = f'{first} -gt {second}' if mode == "powershell" else f'{first} > {second}'
    first.content = ""
    second.content = ""
    return BashrBuilder(str)

def lt(first, second):
    if not isinstance(first, BashrBuilder):
        raise Exception("First argument must be a BashrBuilder object")
    if not isinstance(second, BashrBuilder):
        raise Exception("Second argument must be a BashrBuilder object")
    str = f'{first} -lt {second}' if mode == "powershell" else f'{first} < {second}'
    first.content = ""
    second.content = ""
    return BashrBuilder(str)

def ge(first, second):
    if not isinstance(first, BashrBuilder):
        raise Exception("First argument must be a BashrBuilder object")
    if not isinstance(second, BashrBuilder):
        raise Exception("Second argument must be a BashrBuilder object")
    str = f'{first} -ge {second}' if mode == "powershell" else f'{first} >= {second}'
    first.content = ""
    second.content = ""
    return BashrBuilder(str)

def le(first, second):
    if not isinstance(first, BashrBuilder):
        raise Exception("First argument must be a BashrBuilder object")
    if not isinstance(second, BashrBuilder):
        raise Exception("Second argument must be a BashrBuilder object")
    str = f'{first} -le {second}' if mode == "powershell" else f'{first} <= {second}'
    first.content = ""
    second.content = ""
    return BashrBuilder(str)
    
def if_block(condition, then=None, otherwise=None):
    if not isinstance(condition, BashrBuilder):
        raise Exception("Condition must be a BashrBuilder object")
    
    if then and not isinstance(then, BashrBuilder):
        raise Exception("Then-branch must be a BashrBuilder object")
    
    if otherwise and not isinstance(otherwise, BashrBuilder):
        raise Exception("Else-branch must be a BashrBuilder object")

    str = f"if ({condition.content}) {{\n" if mode == "powershell" else "if [ " + condition.content + " ]\n"
    condition.content = ""
    str += f'{then.content}\n' if then else ""
    if then:
        then.content = ""
    str += "} else {\n" if mode == "powershell" else "else\n"
    str += f'{otherwise.content}\n' if otherwise else ""
    if otherwise:
        otherwise.content = ""
    str += "}\n" if mode == "powershell" else "fi\n"
    return BashrBuilder(str)
    
def if_inline(condition, then, otherwise):
    if not isinstance(condition, BashrBuilder):
        raise Exception("Condition must be a BashrBuilder object")
    if then and not isinstance(then, BashrBuilder):
        raise Exception("Then-branch must be a BashrBuilder object")
    if otherwise and not isinstance(otherwise, BashrBuilder):
        raise Exception("Else-branch must be a BashrBuilder object")

    str = f"(if_inline ({condition.content})" if mode == "powershell" else "$(( (" + condition.content
    str += ")" if mode == "powershell" else ") ? "
    str += f'({then.content})' + ("" if mode == "powershell" else " : ")
    str += f'({otherwise.content}' + ("))" if mode == "powershell" else ") ))")
    condition.content = ""
    then.content = ""
    otherwise.content = ""
    return BashrBuilder(str)

def boolean(value):
    if not isinstance(value, bool):
        raise Exception("Value must be a boolean")
    if mode == "powershell":
        return BashrBuilder("$true" if value else "$false")
    else:
        return BashrBuilder("true" if value else "false")