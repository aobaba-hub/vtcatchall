import random
import time

import mouse
import sys
from tkinter import *



class ScreenSize:
    maxX: int = 1920
    maxY: int = 1080
    xOrdinate: int = 100
    yOrdinate: int = 100

    def __init__(self):
        root = Tk()
        self.maxX = root.winfo_screenheight()
        self.maxY = root.winfo_screenwidth()
        print("width x height = %d x %d (pixels)" % (self.maxX, self.maxY))


screen = ScreenSize()


def moveMouse(moveReq):
    print("1 mouse move and click: ", moveReq)
    if len(moveReq) > 1:
        sleepTime = int(moveReq[1]) * 60
    else:
        sleepTime = 300
    while 1:
        generateXY()
        mouse.move(screen.xOrdinate, screen.yOrdinate)
        mouse.click()
        print("sleep for: ", sleepTime, " seconds")
        time.sleep(sleepTime)
    return 0


def generateXY():
    screen.xOrdinate = random.randint(1, screen.maxX)
    screen.yOrdinate = random.randint(1, screen.maxY)
    print("value of screenSize: ", screen.xOrdinate, screen.yOrdinate)
    return screen
