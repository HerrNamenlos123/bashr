import argparse
import os

args = None
initialized = False

powershell = ""
shellscript = ""

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

def powershell_append(command):
    global powershell
    initted()
    powershell += command

def shellscript_append(command):
    global shellscript
    initted()
    shellscript += command

def init():
    global args
    global initialized
    global powershell
    global shell

    parser = argparse.ArgumentParser(description='Bashr: A tool to auto-generate powershell and shell scripts')
    parser.add_argument('--output-folder', dest='output_folder', type=str, help='Output folder to place the generated scripts into', required=False, default="out")
    args = parser.parse_args()
    initialized = True

    powershell = ""
    shell = ""
    
    powershell_append("Set-StrictMode -Version Latest\n")
    powershell_append("$ErrorActionPreference = \"Stop\"\n")

def initted():
    if not initialized:
        raise Exception("Bashr was not initialized. Did you forget to call bashr.init()?")

def echo(message="", no_newline=False):
    initted()

    contains_colors = message.find('\e[') != -1

    message = message.replace('"', '\\"')
    powershell_msg = message.replace('\e[', '[').replace('\\', '`')

    if contains_colors:
        message += "\e[0m"
        powershell_msg += "[0m"

    if no_newline:
        powershell_append(f'Write-Host "{powershell_msg}" -NoNewline\n')
        shellscript_append(f'echo -n -e "{message}"\n')
    else:
        powershell_append(f'Write-Host "{powershell_msg}"\n')
        shellscript_append(f'echo -e "{message}"\n')

def clear():
    initted()
    powershell_append("Clear-Host\n")
    shellscript_append("clear\n")

def touch(file, suppress_output=True, ignore_errors=False):
    initted()
    
    powershell_suppress = " | Out-Null" if suppress_output else ""
    powershell_errors = " -ErrorAction SilentlyContinue" if ignore_errors else ""
    powershell_append(f"if (Test-Path {file}) {{\n")
    powershell_append(f"    (Get-Item {file}{powershell_errors}).LastWriteTime = Get-Date\n")
    powershell_append("} else {\n")
    powershell_append(f"    New-Item -ItemType File{powershell_errors} -Path {'/'}{powershell_suppress}\n")
    powershell_append("}\n")
    
    shellscript_suppress = " > /dev/null" if suppress_output else ""
    shellscript_append(f"touch {file}{shellscript_suppress}\n")

def close():
    initted()
    os.makedirs(args.output_folder, exist_ok=True)
    with open(f'{args.output_folder}/run.ps1', "w") as f:
        f.write(powershell)
    with open(f'{args.output_folder}/run.sh', "w") as f:
        f.write(shellscript)