import main
import colorama;
import time
from colorama import Fore, Back, Style

colorama.init()


class Object:
    def __init__(self, name):
        print(name)

    @staticmethod
    def new(_, name):
        o = Object(name)

def call(name):
    # Use correct dictionary access for files
    main.runFile(main.json_object["files"][name])

def info(text):
    print(f"{Style.BRIGHT}{Fore.CYAN}Info:{Style.RESET_ALL} {text}")

def warn(text):
    print(f"{Style.BRIGHT}{Fore.YELLOW}Warn:{Style.RESET_ALL} {text}")

def error(text):
    print(f"{Style.BRIGHT}{Fore.RED}Error:{Style.RESET_ALL}{Fore.RED} {text}{Fore.RESET}")

def wait(length):
    time.sleep(length)