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
        self.initialize_board()
        self.initialize_title()
        self.speed = 150  # Default Snake Speed
        self.color = Color.BLUE_COLOR  # Default Snake Color
        self.poison = False  # Default poison value
        self.size = Util.SIZE_BOARD  # Default Board Size
        self.variable_speed = IntVar(value=150)
        self.variable_color = StringVar(value=Color.BLUE_COLOR)
        self.variable_poison = BooleanVar(value=False)
        self.variable_size = IntVar(value=Util.SIZE_BOARD)
        self.display_speed()
        self.display_color()
        self.display_size()
        self.display_poison()
        self.display_apply()

    def initialize_board(self):
        self.canvas = Canvas(self.window, width=Util.SIZE_BOARD, height=Util.SIZE_BOARD, bg="White")
        self.canvas.pack()

    def initialize_title(self):
        self.canvas.create_text(
            Util.SIZE_BOARD / 2,
            50,
            font="cmr 30 bold",
            fill="Green",
            text="게임 설정",
        )

    def display_speed(self):
        self.canvas.create_text(
            45,
            100,
            font="cmr 20 bold",
            fill="Black",
            text="난이도"
        )
        self.display_speed_buttons()

    def display_color(self):
        self.canvas.create_text(
            45,
            150,
            font="cmr 20 bold",
            fill="Black",
            text="뱀 색상"
        )
        self.display_color_buttons()

    def display_poison(self):
        self.canvas.create_text(
            45,
            200,
            font="cmr 20 bold",
            fill="Black",
            text="독사과"
        )
        self.display_poison_buttons()

    def display_size(self):
        self.canvas.create_text(
            60,
            250,
            font="cmr 20 bold",
            fill="Black",
            text="게임판 크기"
        )
        self.display_size_buttons()

    def display_speed_buttons(self):
        self.create_speed_button(x=140, y=100, text="매우 쉬움", speed=270, color=Color.LIGHT_GREEN_1)
        self.create_speed_button(x=220, y=100, text="쉬움", speed=210, color=Color.HARD_GREEN_1)
        self.create_speed_button(x=290, y=100, text="보통", speed=150, color=Color.MIDDLE_ORANGE_1)
        self.create_speed_button(x=360, y=100, text="어려움", speed=90, color=Color.MIDDLE_RED_1)
        self.create_speed_button(x=460, y=100, text="매우 어려움", speed=30, color=Color.HARD_RED_1)

    def display_color_buttons(self):
        self.create_color_button(x=140, y=150, text="연두", color=Color.LIGHT_GREEN_1)
        self.create_color_button(x=220, y=150, text="파랑", color=Color.BLUE_COLOR)
        self.create_color_button(x=290, y=150, text="빨강", color=Color.RED_COLOR)
        self.create_color_button(x=360, y=150, text="주황", color=Color.MIDDLE_ORANGE_1)
        self.create_color_button(x=460, y=150, text="노랑", color=Color.YELLOW_COLOR)

    def display_poison_buttons(self):
        self.create_poison_button(x=140, y=200, text="포함", value=True, color=Color.PURPLE_COLOR)
        self.create_poison_button(x=220, y=200, text="미포함", value=False, color=Color.GREEN_COLOR)

    def display_size_buttons(self):
        self.create_size_button(x=160, y=250, text="소(기본)", size=10)
        self.create_size_button(x=240, y=250, text="중", size=15)
        self.create_size_button(x=300, y=250, text="대", size=20)

    def create_speed_button(self, x, y, text, speed, color):
        button = Radiobutton(
            self.window,
            text=text,
            variable=self.variable_speed,
            value=speed,
            font="cmr 18 bold",
            fg=color,
            bg="White",
        )
        button.configure(command=lambda: self.setting_speed(speed))
        self.canvas.create_window(x, y, window=button)

    def create_color_button(self, x, y, text, color):
        button = Radiobutton(
            self.window,
            text=text,
            variable=self.variable_color,
            value=color,
            font="cmr 18 bold",
            fg=color,
            bg="White",
        )
        button.configure(command=lambda: self.setting_color(color))
        self.canvas.create_window(x, y, window=button)

    def create_poison_button(self, x, y, text, value, color):
        button = Radiobutton(
            self.window,
            text=text,
            variable=self.variable_poison,
            value=value,
            font="cmr 18 bold",
            fg=color,
            bg="White"
        )
        button.configure(command=lambda: self.setting_poison(value))
        self.canvas.create_window(x, y, window=button)

    def create_size_button(self, x, y, text, size):
        button = Radiobutton(
            self.window,
            text=text,
            variable=self.variable_size,
            value=size,
            font="cmr 18 bold",
            fg="Black",
            bg="White"
        )
        button.configure(command=lambda: self.setting_size(size))
        self.canvas.create_window(x, y, window=button)

    def setting_speed(self, speed):
        self.speed = speed

    def setting_color(self, color):
        self.color = color

    def setting_poison(self, value):
        self.poison = value

    def setting_size(self, size):
        self.size = size

    def display_apply(self):
        button = tkinter.Button(
            self.window,
            text="완료 ✅",
            width=10,
            padx=20,
            pady=5,
            borderwidth=0,
            font="cmr 16 bold",
            command=self.applySettings
        )
        self.canvas.create_window(500, 550, window=button)

    def applySettings(self):
        self.parent.setting_color(self.color)
        self.parent.setting_poison(self.poison)
        self.parent.setting_speed(self.speed)
        self.parent.setting_size(self.size)
        self.parent.window.deiconify()
        self.window.destroy()
