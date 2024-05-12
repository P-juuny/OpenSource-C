import tkinter
from tkinter import *
from SnakeAndApple import SnakeAndApple


class StartPage:
    def __init__(self):
        self.canvas = None
        self.window = Tk()
        self.window.title("Snake-and-Apple")
        self.setBackground()
        self.setTitle()
        self.setStartButton()

    def setBackground(self):
        self.window.geometry('600x600')
        self.window.configure(bg="white")

    def setTitle(self):
        label = tkinter.Label(
            self.window,
            text="Welcome SnakeAndApple Game 😄",
            font=("Arial", 24, "bold"),
            fg="green",
            bg="white",
        )
        label.pack(pady=200)

    def setStartButton(self):
        startBtn = tkinter.Button(
            self.window,
            text="시작하기 🐍",
            width=10,
            pady=5,
            padx=20,
            borderwidth=0.2,
            font=("Arial", 12, "bold"),
            command=self.startGame
        )
        startBtn.pack(side="right", padx=10, pady=10)

    def startGame(self):
        self.window.withdraw()
        SnakeAndApple().mainloop()
        self.window.destroy()


exam = StartPage()
exam.window.mainloop()
