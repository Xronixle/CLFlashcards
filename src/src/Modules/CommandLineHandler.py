import os


def ClearCLI(msg):
    clearCommand = "clear"

    if (os.name == "nt"):
        clearCommand = "cls"

    os.system(clearCommand)

    if (msg != None):
        print(msg)


def Prettify(msg):
    if (type(msg) != str):
        return msg
    
    LongestLine = 0

    for line in msg.split("\n"):
        LongestLine = max(LongestLine, len(line))
    
    Buffer = ("-" * LongestLine)
    Prettied = f"{msg}\n{Buffer}"
    
    return Prettied, LongestLine


def GetInput(msg):
    Prompt, LineCount = Prettify(msg)
    Data = input("\n" + Prompt + "\n")

    return Data