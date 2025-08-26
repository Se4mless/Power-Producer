from lupa import LuaRuntime
import webview
import os
import commands
import luaglobals
import json
import threading


lua = LuaRuntime()
# Init Lua 
lua.globals().Object = luaglobals.Object
lua.globals().call = luaglobals.call
lua.globals().logInfo = luaglobals.info
lua.globals().logWarn = luaglobals.warn
lua.globals().logError = luaglobals.error
lua.globals().wait = luaglobals.wait
lua.globals().Window = luaglobals.Window



path = os.path.join(os.path.abspath( os.getcwd()),"access.json")

json_object = None  # Will be set in run()

def run():
    global json_object
    with open(path, "r") as file:
        json_object = json.load(file)
        root_path = json_object["root"]
        runFile(root_path)


def getPath(file_path):
    # Use os.path for robust path handling
    import os
    base = os.path.dirname(path)
    return os.path.join(base, file_path)


def runFile(file_path):
    with open(getPath(file_path), "r") as file:
        code = file.read()
    # Run Lua code in main thread for simplicity
    lua.execute(code)
     
    



def main():


    current_input = ""
    while True:
        current_input = input("Type Command : \n\t- ")
        commands.check(current_input)
        print("\n\n")
    

if __name__ == "__main__":
    main()


