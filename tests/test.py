import os, sys      # This boilerplate is just for the tests, since the script is placed in a parent directory
sys.path.insert(1, os.path.dirname(os.getcwd()))

import bashr

bashr.init()

bashr.clear()
bashr.echo("Terminal was just cleared")

bashr.echo(bashr.Echo.FgGreen + bashr.Echo.Underline + "Hello " + bashr.Echo.FgYellow + bashr.Echo.BgGray + "World!")
bashr.echo("Another", no_newline=True)
bashr.echo(" " + bashr.Echo.Strike + "test")
bashr.echo("Bold: " + bashr.Echo.Bold + "test")
bashr.echo("Dim: " + bashr.Echo.Dim + "test")
bashr.echo("Underline: " + bashr.Echo.Underline + "test")
bashr.echo("Italic: " + bashr.Echo.Italic + "test")
bashr.echo("Invert: " + bashr.Echo.Bold + "test")
bashr.echo("Hidden: " + bashr.Echo.Hidden + "test")
bashr.echo("Strike: " + bashr.Echo.Strike + "test")
bashr.echo("This is a \"Quote\" test")

file = "out/test.txt"
bashr.echo()
bashr.echo(f"Touching {file}...")
bashr.touch(file)
bashr.echo(f"Done")

bashr.close()