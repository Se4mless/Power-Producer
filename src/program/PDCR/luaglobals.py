import main
import colorama
import time

from colorama import Fore, Back, Style
import pygame

colorama.init()






class Object:
    def __init__(self, name, window, idx, icon=None, x=None, y=None):
        self.idx = idx
        self.window = window
        # Default to center of window if not specified
        self.x = x if x is not None else window.width // 2
        self.y = y if y is not None else window.height // 2
        self.icon = icon
        self.features = []
        print(name)

    def set_icon(self, icon_path):
        self.icon = main.path.removesuffix("access.json") + icon_path



    def add(self,name):
        return self.window.add_child(name,self.idx)
    
    def get_icon(self):
        return self.icon
    
    def get_pos(self):
        return {"x":self.x,"y":self.y}
    
    def set_pos(self,x,y):
        self.x = x 
        self.y = y 
    
    def add_feature(self,func):
        self.features.append(func)

    def update(self):
        for feature in self.features:feature(self,"Update")


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



    
class Window:
    def __init__(self, name, width=500, height=500):
        self.name = name
        self.width = width
        self.height = height
        self.objects = []
        self.parents = []
        self.screen = None
        self.clock = None
        self.running = False 

    def add(self, name, icon=None, x=0, y=0):
        idx = len(self.objects)
        obj = Object(name, self, idx, icon=icon, x=x, y=y)
        self.objects.append(obj)
        self.parents.append(-1)
        return obj

    def add_child(self, name, parent, icon=None, x=0, y=0):
        idx = len(self.objects)
        obj = Object(name, self, idx, icon=icon, x=x, y=y)
        self.objects.append(obj)
        self.parents.append(parent)
        return obj

    def set_size(self,w,h):
        self.width = w
        self.height = h

    def start(self):
        import os
        pygame.init()
        # Try to set window icon, but ignore if missing
        try:
            pygame.display.set_icon(pygame.image.load("D:\.Projects\python\TermiPPTXGame\pie(3).png"))
        except Exception as e:
            print(f"Warning: Could not set window icon: {e}")
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.running = True
        self.clock = pygame.time.Clock()
        while self.running:
            # Update Objects
            for obj in self.objects:
                obj.update()
            




            self.screen.fill((30, 30, 30))  # dark background
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.end()
                    break
            if not self.running:
                break

            # Render Objects
            for obj in self.objects:
                pos = obj.get_pos()
                self.screen.blit(pygame.image.load(obj.get_icon()),(pos["x"],pos["y"]))



            
            pygame.display.flip()
            self.clock.tick(60)

    def end(self):
        self.running = False
        pygame.quit()
