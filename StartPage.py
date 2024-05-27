# -*- coding: utf-8 -*-

import tkinter
import Color
import Util
from tkinter import *
from SettingPage import SettingPage
from SnakeAndApple import SnakeAndApple


class StartPage:
    def __init__(self):
        self.canvas = None
        self.window = Tk()
        self.window.title("Snake-and-Apple")
        self.setBackground()
        self.speed = 150  # Base Speed
        self.size = 10  # Base Board Size
        self.setTitle()
        self.setStartButton()
        self.window.bind("<Return>", lambda event: self.startGame())
        self.window.bind("<space>", lambda event: self.startGame())
        self.setSettingPageButton()

    def setBackground(self):
        self.canvas = Canvas(self.window, width=Util.SIZE_BOARD, height=Util.SIZE_BOARD, bg="White")
        self.canvas.pack()

    def setTitle(self):
        self.canvas.create_text(
            Util.SIZE_BOARD / 2,
            3 * Util.SIZE_BOARD / 8,
            font="cmr 30 bold",
            fill=Color.GREEN_COLOR,
            text="Welcome SnakeAndApple Game 😄",
        )

    def setStartButton(self):
        startBtn = tkinter.Button(
            self.window,
            text="시작하기 🐍",
            width=10,
            padx=20,
            pady=5,
            borderwidth=0.2,
            font="cmr 14 bold",
            command=self.startGame
        )
        startBtn.pack(side="bottom", anchor="se", padx=5)

    def setSettingPageButton(self):
        settingPageBtn = tkinter.Button(
            self.window,
            text="게임설정 ⚙️",
            width=10,
            padx=20,
            pady=5,
            borderwidth=0.2,
            font="cmr 14 bold",
            command=self.moveSettingPage
        )
        settingPageBtn.pack(side="bottom", anchor="se", padx=5)

    def setSpeed(self, speed):
        self.speed = speed

    def setBoardSize(self, size):
        self.size = size

    def startGame(self):
        self.window.withdraw()
        SnakeAndApple(speed=self.speed, size=self.size).mainloop()

    def moveSettingPage(self):
        self.window.withdraw()
        SettingPage(self)


game_instance = StartPage()
game_instance.window.mainloop()
