# -*- coding: utf-8 -*-

from tkinter import *
import Util
import Color
import random
import time
import numpy as np
from collections import deque
from PIL import ImageTk, Image

SNAKE_INITIAL_LENGTH = 3


class SnakeAndApple:
    # ------------------------------------------------------------------
    # Initialization Functions:
    # ------------------------------------------------------------------
    def __init__(self, speed, size, poison):
        self.window = Tk()
        self.window.title("Snake-and-Apple")
        self.canvas = Canvas(self.window, width=Util.SIZE_BOARD, height=Util.SIZE_BOARD)
        self.canvas.pack()
        self.speed = speed
        self.poison_apple_enabled = poison
        self.poison_apple = None
        self.size = size
        # Input from user in form of clicks and keyboard
        self.window.bind("<Key>", self.key_input)
        self.game_over_by_poison = False
        self.play_again()
        self.begin = False

    def initialize_board(self):
        self.board = []
        self.apple_obj = []
        self.old_apple_cell = []
        self.old_poison_apple_cell= []

        for i in range(self.size):
            for j in range(self.size):
                self.board.append((i, j))

        for i in range(self.size):
            self.canvas.create_line(
                i * int(Util.SIZE_BOARD / self.size), 0, i * int(Util.SIZE_BOARD / self.size), Util.SIZE_BOARD,
            )

        for i in range(self.size):
            self.canvas.create_line(
                0, i * int(Util.SIZE_BOARD / self.size), Util.SIZE_BOARD, i * int(Util.SIZE_BOARD / self.size),
            )

    def initialize_snake(self):
        self.snake = deque()
        self.crashed = False
        self.snake_heading = "Right"
        self.last_key = self.snake_heading
        self.forbidden_actions = {}
        self.forbidden_actions["Right"] = "Left"
        self.forbidden_actions["Left"] = "Right"
        self.forbidden_actions["Up"] = "Down"
        self.forbidden_actions["Down"] = "Up"
        self.snake_objects = deque()
        for i in range(SNAKE_INITIAL_LENGTH):
            self.snake.append((i, 0))

    def play_again(self):
        self.canvas.delete("all")
        self.initialize_board()
        self.initialize_snake()
        self.place_apple()
        if self.poison_apple_enabled:
            self.place_poison_apple()
        self.display_snake(mode="complete")
        self.begin_time = time.time()
        self.game_over_by_poison = False

    def mainloop(self):
        while True:
            self.window.update()
            if self.begin:
                if not self.crashed:
                    self.window.after(self.speed, self.update_snake(self.last_key))
                else:
                    self.begin = False
                    self.display_gameover()

    # ------------------------------------------------------------------
    # Drawing Functions:
    # The modules required to draw required game based object on canvas
    # ------------------------------------------------------------------
    def display_gameover(self):
        score = 0 if self.game_over_by_poison and len(self.snake) == 1 else len(self.snake)
        self.canvas.delete("all")
        score_text = "Scores \n"

        # put gif image on canvas
        # pic's upper left corner (NW) on the canvas is at x=50 y=10

        self.canvas.create_text(
            Util.SIZE_BOARD / 2,
            3 * Util.SIZE_BOARD / 8,
            font="cmr 40 bold",
            fill=Color.GREEN_COLOR,
            text=score_text,
        )
        score_text = str(score)
        self.canvas.create_text(
            Util.SIZE_BOARD / 2,
            1 * Util.SIZE_BOARD / 2,
            font="cmr 50 bold",
            fill=Color.BLUE_COLOR,
            text=score_text,
        )
        time_spent = str(np.round(time.time() - self.begin_time, 1)) + 'sec'
        self.canvas.create_text(
            Util.SIZE_BOARD / 2,
            3 * Util.SIZE_BOARD / 4,
            font="cmr 20 bold",
            fill=Color.BLUE_COLOR,
            text=time_spent,
        )
        score_text = "Push R(r) key to play again \n"
        self.canvas.create_text(
            Util.SIZE_BOARD / 2,
            15 * Util.SIZE_BOARD / 16,
            font="cmr 20 bold",
            fill="gray",
            text=score_text,
        )

    def place_apple(self):
        # Place apple randomly anywhere except at the cells occupied by snake
        unoccupied_cels = set(self.board) - set(self.snake)
        self.apple_cell = random.choice(list(unoccupied_cels))
        x1 = self.apple_cell[0] * int(Util.SIZE_BOARD / self.size)
        y1 = self.apple_cell[1] * int(Util.SIZE_BOARD / self.size)
        x2 = x1 + int(Util.SIZE_BOARD / self.size)
        y2 = y1 + int(Util.SIZE_BOARD / self.size)
        self.apple_obj = self.canvas.create_rectangle(
            x1, y1, x2, y2, fill=Color.RED_COLOR_LIGHT, outline=Color.BLUE_COLOR,
        )
    
    def place_poison_apple(self):
        unoccupied_cels = set(self.board) - set(self.snake) - {self.apple_cell}
        self.poison_apple_cell = random.choice(list(unoccupied_cels))
        x1 = self.poison_apple_cell[0] * int(Util.SIZE_BOARD / self.size)
        y1 = self.poison_apple_cell[1] * int(Util.SIZE_BOARD / self.size)
        x2 = x1 + int(Util.SIZE_BOARD / self.size)
        y2 = y1 + int(Util.SIZE_BOARD / self.size)
        self.poison_apple_obj = self.canvas.create_rectangle(
            x1, y1, x2, y2, fill=Color.PURPLE_COLOR, outline=Color.BLUE_COLOR,
        )

    def display_snake(self, mode=""):
        # Remove tail from display if it exists
        if self.snake_objects != deque():
            self.canvas.delete(self.snake_objects.popleft())
        if mode == "complete":
            for i, cell in enumerate(self.snake):
                # print(cell)
                x1 = cell[0] * int(Util.SIZE_BOARD / self.size)
                y1 = cell[1] * int(Util.SIZE_BOARD / self.size)
                x2 = x1 + int(Util.SIZE_BOARD / self.size)
                y2 = y1 + int(Util.SIZE_BOARD / self.size)
                self.snake_objects.append(
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2, fill=Color.BLUE_COLOR, outline=Color.BLUE_COLOR,
                    )
                )
        else:
            # only update head
            cell = self.snake[-1]
            x1 = cell[0] * int(Util.SIZE_BOARD / self.size)
            y1 = cell[1] * int(Util.SIZE_BOARD / self.size)
            x2 = x1 + int(Util.SIZE_BOARD / self.size)
            y2 = y1 + int(Util.SIZE_BOARD / self.size)
            self.snake_objects.append(
                self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=Color.BLUE_COLOR, outline=Color.RED_COLOR,
                )
            )

            if self.snake[-1] == self.old_apple_cell:
                self.snake.appendleft(self.old_apple_cell)
                self.old_apple_cell = []
                tail = self.snake[0]
                x1 = tail[0] * int(Util.SIZE_BOARD / self.size)
                y1 = tail[1] * int(Util.SIZE_BOARD / self.size)
                x2 = x1 + int(Util.SIZE_BOARD / self.size)
                y2 = y1 + int(Util.SIZE_BOARD / self.size)
                self.snake_objects.appendleft(
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2, fill=Color.BLUE_COLOR, outline=Color.RED_COLOR
                    ),
                )

            if self.snake[-1] == self.old_poison_apple_cell:
                self.canvas.delete(self.snake_objects.popleft())
                
            self.window.update()

    # ------------------------------------------------------------------
    # Logical Functions:
    # The modules required to carry out game logic
    # ------------------------------------------------------------------
    def update_snake(self, key):
        # Check if it hit the wall or its own body
        tail = self.snake[0]
        head = self.snake[-1]
        if tail != self.old_apple_cell:
            self.snake.popleft()
        if key == "Left":
            self.snake.append((head[0] - 1, head[1]))
        elif key == "Right":
            self.snake.append((head[0] + 1, head[1]))
        elif key == "Up":
            self.snake.append((head[0], head[1] - 1))
        elif key == "Down":
            self.snake.append((head[0], head[1] + 1))

        head = self.snake[-1]
        if (
                head[0] > self.size - 1
                or head[0] < 0
                or head[1] > self.size - 1
                or head[1] < 0
                or len(set(self.snake)) != len(self.snake)
        ):
            # Hit the wall / Hit on body
            self.crashed = True
        elif self.apple_cell == head:
            # Got the apple
            self.old_apple_cell = self.apple_cell
            self.canvas.delete(self.apple_obj)
            self.place_apple()
            self.display_snake()
        elif self.poison_apple_enabled and self.poison_apple_cell == head:
            self.old_poison_apple_cell = self.poison_apple_cell
            if len(self.snake) > 1:
                self.snake.popleft()
            else:
                self.game_over_by_poison = True
                self.crashed = True
            self.canvas.delete(self.poison_apple_obj)
            self.place_poison_apple()
            self.display_snake()             
        else:
            self.snake_heading = key
            self.display_snake()


    def check_if_key_valid(self, key):
        valid_keys = ["Up", "Down", "Left", "Right"]
        if key in valid_keys and self.forbidden_actions[self.snake_heading] != key:
            return True
        else:
            return False

    def key_input(self, event):
        if not self.crashed:
            key_pressed = event.keysym
            if key_pressed == 'p':
                self.begin = not self.begin
            elif self.check_if_key_valid(key_pressed):
                self.begin = True
                self.last_key = key_pressed
        else:
            if event.keysym == "r" or event.keysym == "R":
                self.play_again()
