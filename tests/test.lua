
script = ""

function init()
    print("init")
end

function echo(str)
    script = script .. str .. "\n"
end

function silence_output()
    script = script .. " s"
end

function close()
    print("close")
    print(script)
end

init()

test = "Hello" | "World"
print(test)

echo("Hello World!")
echo("Hello World!")silence_output()

close()