import tkinter
from tkinter import *
from PIL import ImageTk, Image

size_board = 600


class SettingPage:
    def __init__(self):
        self.canvas = None
        self.window = Tk()
        self.window.title("Snake-and-Apple")
        self.setBackground()
        self.setTitle()
        self.setSpeed()

    def setBackground(self):
        self.canvas = Canvas(self.window, width=size_board, height=size_board, bg="White")
        self.canvas.pack()

    def setTitle(self):
        self.canvas.create_text(
            size_board / 2,
            50,
            font="cmr 30 bold",
            fill="Green",
            text="게임 설정",
        )

    def setSpeed(self):
        self.canvas.create_text(
            45,
            100,
            font="cmr 20 bold",
            fill="Black",
            text="난이도"
        )
        self.setSpeedRadioButton()

    def setSpeedRadioButton(self):
        self.createRadioButton("매우 쉬움", value=500, x=140, y=100)
        self.createRadioButton("쉬움", value=300, x=200, y=100)

    def createRadioButton(self, text, value, x, y):
        difficulty = IntVar()

        button = Radiobutton(
            self.window,
            text=text,
            variable=difficulty,
            value=value
        )
        self.canvas.create_window(x,y,window=button)


SettingPage().window.mainloop()
