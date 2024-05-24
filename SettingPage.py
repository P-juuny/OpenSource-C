# -*- coding: utf-8 -*-

import tkinter
from tkinter import *

import Color
from Color import *
from PIL import ImageTk, Image

size_board = 600


class SettingPage:
    def __init__(self, parent):
        self.canvas = None
        self.parent = parent
        self.speed = 150
        self.variable = IntVar(value=150)
        self.window = Tk()
        self.window.title("Snake-and-Apple")
        self.setBackground()
        self.setTitle()
        self.setSpeedTitle()
        self.setApplyButton()

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

    def setSpeedTitle(self):
        self.canvas.create_text(
            45,
            100,
            font="cmr 20 bold",
            fill="Black",
            text="난이도"
        )
        self.setSpeedRadioButton()

    def setSpeedRadioButton(self):
        self.createRadioButton("매우 쉬움", speed=270, x=140, y=100, color=Color.LIGHT_GREEN_1)
        self.createRadioButton("쉬움", speed=210, x=220, y=100, color=Color.HARD_GREEN_1)
        self.createRadioButton("보통", speed=150, x=290, y=100, color=Color.MIDDLE_ORANGE_1)
        self.createRadioButton("어려움", speed=90, x=360, y=100, color=Color.MIDDLE_RED_1)
        self.createRadioButton("매우 어려움", speed=30, x=460, y=100, color=Color.HARD_RED_1)

    def createRadioButton(self, text, speed, x, y, color):
        button = Radiobutton(
            self.window,
            text=text,
            variable=self.variable,
            value=speed,
            font="cmr 18 bold",
            fg=color,
            bg="White",
        )
        button.configure(command=lambda: self.setSpeed(speed))
        self.canvas.create_window(x, y, window=button)

    def setSpeed(self, speed):
        self.speed = speed

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
        speed = self.speed
        self.parent.setSpeed(speed)
        self.parent.window.deiconify()
        self.window.destroy()
