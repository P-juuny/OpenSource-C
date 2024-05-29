# -*- coding: utf-8 -*-

import tkinter
import Color
import Util
from tkinter import *


class SettingPage:
    def __init__(self, parent):
        self.canvas = None
        self.parent = parent  # Parent is StartPage.py
        self.window = Tk()
        self.window.title("Snake-and-Apple")
        self.setBackground()
        self.setTitle()
        self.speed = 150  # Default Snake Speed
        self.color = Color.BLUE_COLOR  # Default Snake Color
        self.poison = False  # Default poison value
        self.size = Util.SIZE_BOARD  # Default Board Size
        self.speedVariable = IntVar(value=150)
        self.colorVariable = StringVar(value=Color.BLUE_COLOR)
        self.poisonVariable = BooleanVar(value=False)
        self.sizeVariable = IntVar(value=Util.SIZE_BOARD)
        self.setSpeedSetting()
        self.setSnakeColorSetting()
        self.setBoardSizeSetting()
        self.setPoisonSetting()
        self.setApplyButton()

    def setBackground(self):
        self.canvas = Canvas(self.window, width=Util.SIZE_BOARD, height=Util.SIZE_BOARD, bg="White")
        self.canvas.pack()

    def setTitle(self):
        self.canvas.create_text(
            Util.SIZE_BOARD / 2,
            50,
            font="cmr 30 bold",
            fill="Green",
            text="게임 설정",
        )

    def setSpeedSetting(self):
        self.canvas.create_text(
            45,
            100,
            font="cmr 20 bold",
            fill="Black",
            text="난이도"
        )
        self.setSpeedRadioButton()

    def setSnakeColorSetting(self):
        self.canvas.create_text(
            45,
            150,
            font="cmr 20 bold",
            fill="Black",
            text="뱀 색상"
        )
        self.setSnakeColorRadioButton()

    def setPoisonSetting(self):
        self.canvas.create_text(
            45,
            200,
            font="cmr 20 bold",
            fill="Black",
            text="독사과"
        )
        self.setPoisonSettingRadioButton()

    def setBoardSizeSetting(self):
        self.canvas.create_text(
            60,
            250,
            font="cmr 20 bold",
            fill="Black",
            text="게임판 크기"
        )
        self.setBoardSizeSettingRadioButton()

    def setSpeedRadioButton(self):
        self.createSpeedRadioButton(x=140, y=100, text="매우 쉬움", speed=270, color=Color.LIGHT_GREEN_1)
        self.createSpeedRadioButton(x=220, y=100, text="쉬움", speed=210, color=Color.HARD_GREEN_1)
        self.createSpeedRadioButton(x=290, y=100, text="보통", speed=150, color=Color.MIDDLE_ORANGE_1)
        self.createSpeedRadioButton(x=360, y=100, text="어려움", speed=90, color=Color.MIDDLE_RED_1)
        self.createSpeedRadioButton(x=460, y=100, text="매우 어려움", speed=30, color=Color.HARD_RED_1)

    def setSnakeColorRadioButton(self):
        self.createSnakeColorRadioButton(x=140, y=150, text="연두", color=Color.LIGHT_GREEN_1)
        self.createSnakeColorRadioButton(x=220, y=150, text="파랑", color=Color.BLUE_COLOR)
        self.createSnakeColorRadioButton(x=290, y=150, text="빨강", color=Color.RED_COLOR)
        self.createSnakeColorRadioButton(x=360, y=150, text="주황", color=Color.MIDDLE_ORANGE_1)
        self.createSnakeColorRadioButton(x=460, y=150, text="노랑", color=Color.YELLOW_COLOR)

    def setPoisonSettingRadioButton(self):
        self.createPoisonRadioButton(x=140, y=200, text="포함", value=True, color=Color.PURPLE_COLOR)
        self.createPoisonRadioButton(x=220, y=200, text="미포함", value=False, color=Color.GREEN_COLOR)

    def setBoardSizeSettingRadioButton(self):
        self.createBoardSizeRadioButton(x=160, y=250, text="소(기본)", size=10)
        self.createBoardSizeRadioButton(x=240, y=250, text="중", size=15)
        self.createBoardSizeRadioButton(x=300, y=250, text="대", size=20)

    def createSpeedRadioButton(self, x, y, text, speed, color):
        button = Radiobutton(
            self.window,
            text=text,
            variable=self.speedVariable,
            value=speed,
            font="cmr 18 bold",
            fg=color,
            bg="White",
        )
        button.configure(command=lambda: self.setSpeed(speed))
        self.canvas.create_window(x, y, window=button)

    def createSnakeColorRadioButton(self, x, y, text, color):
        button = Radiobutton(
            self.window,
            text=text,
            variable=self.colorVariable,
            value=color,
            font="cmr 18 bold",
            fg=color,
            bg="White",
        )
        button.configure(command=lambda: self.setColor(color))
        self.canvas.create_window(x, y, window=button)

    def createPoisonRadioButton(self, x, y, text, value, color):
        button = Radiobutton(
            self.window,
            text=text,
            variable=self.poisonVariable,
            value=value,
            font="cmr 18 bold",
            fg=color,
            bg="White"
        )
        button.configure(command=lambda: self.setPoison(value))
        self.canvas.create_window(x, y, window=button)

    def createBoardSizeRadioButton(self, x, y, text, size):
        button = Radiobutton(
            self.window,
            text=text,
            variable=self.sizeVariable,
            value=size,
            font="cmr 18 bold",
            fg="Black",
            bg="White"
        )
        button.configure(command=lambda: self.setBoardSize(size))
        self.canvas.create_window(x, y, window=button)

    def setSpeed(self, speed):
        self.speed = speed

    def setColor(self, color):
        self.color = color

    def setPoison(self, value):
        self.poison = value

    def setBoardSize(self, size):
        self.size = size

    def setApplyButton(self):
        exitBtn = tkinter.Button(
            self.window,
            text="완료 ✅",
            width=10,
            padx=20,
            pady=5,
            borderwidth=0,
            font="cmr 16 bold",
            command=self.applySettings
        )
        self.canvas.create_window(500, 550, window=exitBtn)

    def applySettings(self):
        self.parent.setColor(self.color)
        self.parent.setPoison(self.poison)
        self.parent.setSpeed(self.speed)
        self.parent.setBoardSize(self.size)
        self.parent.window.deiconify()
        self.window.destroy()