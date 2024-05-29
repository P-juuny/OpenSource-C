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
        self.initialize_board()
        self.speed = 150  # Base Speed
        self.color = Color.BLUE_COLOR  # default color
        self.poison = False
        self.size = 10  # Base Board Size
        self.initialize_title()
        self.display_start()
        self.window.bind("<Return>", lambda event: self.start_game())
        self.window.bind("<space>", lambda event: self.start_game())
        self.display_setting()

    def initialize_board(self):
        self.canvas = Canvas(self.window, width=Util.SIZE_BOARD, height=Util.SIZE_BOARD, bg="White")
        self.canvas.pack()

    def initialize_title(self):
        self.canvas.create_text(
            Util.SIZE_BOARD / 2,
            3 * Util.SIZE_BOARD / 8,
            font="cmr 30 bold",
            fill=Color.GREEN_COLOR,
            text="Welcome SnakeAndApple Game 😄",
        )

    def display_start(self):
        button = tkinter.Button(
            self.window,
            text="시작하기 🐍",
            width=10,
            padx=20,
            pady=5,
            borderwidth=0.2,
            font="cmr 14 bold",
            command=self.start_game
        )
        button.pack(side="bottom", anchor="se", padx=5)

    def display_setting(self):
        button = tkinter.Button(
            self.window,
            text="게임설정 ⚙️",
            width=10,
            padx=20,
            pady=5,
            borderwidth=0.2,
            font="cmr 14 bold",
            command=self.move_setting_page
        )
        button.pack(side="bottom", anchor="se", padx=5)

    def setting_speed(self, speed):
        self.speed = speed

    def setting_poison(self, poison):
        self.poison = poison

    def setting_size(self, size):
        self.size = size

    def setting_color(self, color):
        self.color = color

    def start_game(self):
        self.window.withdraw()
        SnakeAndApple(speed=self.speed, size=self.size, color=self.color, poison=self.poison).mainloop()

    def move_setting_page(self):
        self.window.withdraw()
        SettingPage(self)


game_instance = StartPage()
game_instance.window.mainloop()
