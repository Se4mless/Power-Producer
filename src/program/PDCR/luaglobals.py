import main
import colorama
import time
import sys
import os
from colorama import Fore, Back, Style
sys.stdout = open(os.devnull,'w')
import pygame
sys.stdout = sys.__stdout__
colorama.init()

global keyDownThisFrame
keyDownThisFrame = ""



class Object:
    def __init__(self, name, window, idx,startFrame, icon=None, x=None, y=None):
        self.idx = idx
        self.window = window
        self.startFrame = startFrame
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

    

    def update(self,frame):

        for feature in self.features:feature(self,"Update",frame)

            

    def check_frame(self,frame,x):
        return (frame - self.startFrame) % x == 0


def call(name):
    # Use correct dictionary access for files
    main.runFile(main.json_object["files"][name])

def info(text):
    print(f"{Style.BRIGHT}{Fore.CYAN}Info:{Style.RESET_ALL} {text}")

def warn(text):
    print(f"{Style.BRIGHT}{Fore.YELLOW}Warn:{Style.RESET_ALL} {text}")

def error(text):
    print(f"{Style.BRIGHT}{Fore.RED}Error:{Style.RESET_ALL}{Fore.RED} {text}{Fore.RESET}")




    
class Window:
    def __init__(self, name, width=500, height=500):
        self.name = name
        self.width = width
        self.height = height
        self.objects = []
        self.parents = []
        self.screen = None
        self.clock = pygame.time.Clock()
        self.running = False 


    def add(self, name, icon=None, x=0, y=0):
        idx = len(self.objects)
        obj = Object(name, self, idx,self.clock.get_time(), icon=icon, x=x, y=y)
        self.objects.append(obj)
        self.parents.append(-1)
        return obj

    def add_child(self, name, parent, icon=None, x=0, y=0):
        idx = len(self.objects)
        obj = Object(name, self, idx,self.clock.get_time(), icon=icon, x=x, y=y)
        self.objects.append(obj)
        self.parents.append(parent)
        return obj

    def set_size(self,w,h):
        self.width = w
        self.height = h

    def start(self):


        pygame.init()

        # Try to set window icon, but ignore if missing
        try:
            pygame.display.set_icon(pygame.image.load("D:/.Projects/python/TermiPPTXGame/pie(3).png"))
        except Exception as e:
            print(f"Warning: Could not set window icon: {e}")
        self.screen = pygame.display.set_mode((self.width, self.height),vsync=1)
        self.running = True
        while self.running:
            global keyDownThisFrame   

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.end()
                    break
                if event.type == pygame.KEYDOWN:
                    keyDownThisFrame = pygame.key.name(event.key)

            if not self.running:
                break
            # Update Objects
            time = self.clock.get_time()
            
            for obj in self.objects:
                obj.update(time)
            



            self.screen.fill((30, 30, 30))  # dark background


            # Render Objects
            for obj in self.objects:
                pos = obj.get_pos()
                img = pygame.image.load(obj.get_icon())
                rect = img.get_rect()
                draw_x = (self.screen.get_size()[0] // 2) + pos["x"] - rect.width // 2
                draw_y = (self.screen.get_size()[1] // 2) + pos["y"] - rect.height // 2
                self.screen.blit(img,(draw_x,draw_y))

            

            keyDownThisFrame = ""
            pygame.display.flip()
            self.clock.tick(60)

    def end(self):
        self.running = False
        pygame.quit()
    
def isKeyDown(key):
    return pygame.key.get_pressed()[pygame.key.key_code(key)] == 1
def isKeyDownThisFrame(key):
    return keyDownThisFrame == key

            
