# -*- coding: utf-8 -*-

from tkinter import *

import Sounds
import Util
import Images
import Color
import random
import time
import numpy as np
from collections import deque
from PIL import ImageTk, Image
import pygame

SNAKE_INITIAL_LENGTH = 3


def initialize_music():
    pygame.mixer.init()
    pygame.mixer.music.load(Sounds.BACK_GROUND)
    pygame.mixer.music.set_volume(0.2)  # 음악 크기 조절
    pygame.mixer.music.play(-1)  # -1은 음악을 무한 반복 재생


class SnakeAndApple:
    def __init__(self, parent, speed, size, color, poison):
        self.window = Toplevel()
        self.window.title("Snake-and-Apple")
        initialize_music()
        self.canvas = Canvas(self.window, width=Util.SIZE_BOARD, height=Util.SIZE_BOARD)
        self.canvas.pack()
        self.speed = speed
        self.color = color
        self.poison_apple_enabled = poison
        self.size = size
        self.window.bind("<Key>", self.key_input)
        self.game_over_by_poison = False
        self.apple_image = self.initialize_image(Images.APPLE_IMAGE_PATH)
        self.poison_apple_image = self.initialize_image(Images.POISON_APPLE_IMAGE_PATH)
        self.play_again()
        self.begin = False
        self.eat_apple_sound = pygame.mixer.Sound(Sounds.EAT_APPLE)
        self.gameover_sound = pygame.mixer.Sound(Sounds.GAME_OVER)
        self.eat_poison_sound = pygame.mixer.Sound(Sounds.EAT_POISON)
        self.parent = parent

    # -------------------------------
    # SnakeAndApple UI 관련 로직 함수
    # -------------------------------
    def initialize_image(self, path):
        image = Image.open(path).resize((int(Util.SIZE_BOARD / self.size), int(Util.SIZE_BOARD / self.size)))
        image = ImageTk.PhotoImage(image)
        return image

    def initialize_board(self):
        self.board = []
        self.apple_obj = []
        self.old_apple_cell = []
        self.poison_apple_obj = []
        self.old_poison_apple_cell = []

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

    def move_startpage(self):
        self.parent.window.deiconify()
        self.window.destroy()

    def mainloop(self):
        while True:
            self.window.update()
            if self.begin:
                if not self.crashed:
                    self.window.after(self.speed, self.update_snake(self.last_key))
                else:
                    self.begin = False
                    self.display_gameover()
                    pygame.mixer.music.stop()
                    self.gameover_sound.play()

    def display_gameover(self):
        score = 0 if self.game_over_by_poison and len(self.snake) == 1 else len(self.snake)
        self.canvas.delete("all")
        score_text = "점수 \n"
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
        time_spent = '생존시간: ' + str(np.round(time.time() - self.begin_time, 1)) + '초'
        self.canvas.create_text(
            Util.SIZE_BOARD / 2,
            3 * Util.SIZE_BOARD / 4,
            font="cmr 20 bold",
            fill=Color.BLUE_COLOR,
            text=time_spent,
        )
        score_text = "다시 시작하기 (R)"
        self.canvas.create_text(
            Util.SIZE_BOARD / 2,
            530,
            font="cmr 20 bold",
            fill="gray",
            text=score_text,
        )
        move_start_text = "처음으로 돌아가기 (E) \n"
        self.canvas.create_text(
            Util.SIZE_BOARD / 2,
            580,
            font="cmr 20 bold",
            fill="gray",
            text=move_start_text
        )

    def place_item(self, excluded_cells, item_image):
        unoccupied_cells = set(self.board) - set(self.snake) - excluded_cells
        chosen_cell = random.choice(list(unoccupied_cells))
        x1 = chosen_cell[0] * int(Util.SIZE_BOARD / self.size)
        y1 = chosen_cell[1] * int(Util.SIZE_BOARD / self.size)
        item_obj = self.canvas.create_image(
            x1 + int(Util.SIZE_BOARD / self.size) / 2,
            y1 + int(Util.SIZE_BOARD / self.size) / 2,
            anchor=CENTER,
            image=item_image
        )
        return chosen_cell, item_obj

    def place_apple(self):
        self.apple_cell, self.apple_obj = self.place_item(excluded_cells=set(), item_image=self.apple_image)

    def place_poison_apple(self):
        self.poison_apple_cell, self.poison_apple_obj = self.place_item(
            excluded_cells={self.apple_cell},
            item_image=self.poison_apple_image
        )

    def draw_snake(self, cell):
        x1 = cell[0] * int(Util.SIZE_BOARD / self.size)
        y1 = cell[1] * int(Util.SIZE_BOARD / self.size)
        x2 = x1 + int(Util.SIZE_BOARD / self.size)
        y2 = y1 + int(Util.SIZE_BOARD / self.size)
        return self.canvas.create_rectangle(
            x1, y1, x2, y2, fill=self.color, outline=Color.PURPLE_COLOR
        )

    def display_snake(self, mode=""):
        if self.snake_objects != deque():
            self.canvas.delete(self.snake_objects.popleft())
        if mode == "complete":
            for i, cell in enumerate(self.snake):
                self.snake_objects.append(self.draw_snake(cell))
        else:
            cell = self.snake[-1]
            self.snake_objects.append(self.draw_snake(cell))

            if self.snake[-1] == self.old_apple_cell:
                self.snake.appendleft(self.old_apple_cell)
                self.old_apple_cell = []
                tail = self.snake[0]
                self.snake_objects.append(self.draw_snake(tail))

            if self.snake[-1] == self.old_poison_apple_cell:
                self.canvas.delete(self.snake_objects.popleft())

            self.window.update()

    # --------------------------------
    # 뱀의 로직 관련 함수
    # --------------------------------

    def update_snake(self, key):
        # 벽, 뱀의 몸통 충돌 체크
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
            # 벽이나 몸통에 충돌하는 경우
            self.crashed = True
        elif self.apple_cell == head:  # 사과를 먹는 경우
            self.eat_apple_sound.play()
            self.old_apple_cell = self.apple_cell
            self.canvas.delete(self.apple_obj)
            self.place_apple()
            self.display_snake()
        elif self.poison_apple_enabled and self.poison_apple_cell == head:  # 독사과를 먹는 경우
            self.eat_poison_sound.play()
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
            if key_pressed == "p" or key_pressed == "P":
                self.begin = not self.begin
            elif self.check_if_key_valid(key_pressed):
                self.begin = True
                self.last_key = key_pressed
        else:
            if event.keysym == "r" or event.keysym == "R":
                self.play_again()
                pygame.mixer.music.play(-1)  # 게임을 다시 시작할 때 배경 음악 재생
            if event.keysym == "e" or event.keysym == "E":
                self.move_startpage()
