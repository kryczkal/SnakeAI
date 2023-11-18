import copy as copy
import random

import pygame as pg

from settings import Settings


class Snake:
    def __init__(self, graphic_on):
        self.pos_x = random.randrange(0, Settings.grid_size_x - 1)
        self.pos_y = random.randrange(0, Settings.grid_size_y - 1)
        self.body = [[-1, -1]]
        if graphic_on:
            self.head_sprite = pg.image.load('assets/sprites/snek.png').convert()
            self.head_sprite = pg.transform.scale(self.head_sprite, (Settings.tile_size, Settings.tile_size))
            self.body_sprite = pg.image.load('assets/sprites/body.png').convert()
            self.body_sprite = pg.transform.scale(self.body_sprite, (Settings.tile_size, Settings.tile_size))
        self.rotation = 0
        self.direction = random.randint(1, 4)
        self.is_alive = True
        self.graphic_on = graphic_on

    def direction_detection(self):
        up = 0
        down = 0
        left = 0
        right = 0
        if self.direction == 1:
            left = 1
        if self.direction == 2:
            right = 1
        if self.direction == 3:
            up = 1
        if self.direction == 4:
            down = 1
        return up, down, left, right

    def movement(self):
        if self.direction == 1:
            self.pos_x = self.pos_x - 1
        if self.direction == 2:
            self.pos_x = self.pos_x + 1
        if self.direction == 3:
            self.pos_y = self.pos_y - 1
        if self.direction == 4:
            self.pos_y = self.pos_y + 1

    def pos_correction(self):
        if self.pos_y > Settings.grid_size_y - 1:
            self.pos_y = 0
        if self.pos_y < 0:
            self.pos_y = Settings.grid_size_y - 1

        if self.pos_x > Settings.grid_size_x - 1:
            self.pos_x = 0
        if self.pos_x < 0:
            self.pos_x = Settings.grid_size_x - 1

    def danger_detection(self):
        up = 0
        down = 0
        left = 0
        right = 0
        point_right = [(self.pos_x + 1) % Settings.grid_size_x, self.pos_y]
        point_left = [(self.pos_x - 1) % Settings.grid_size_x, self.pos_y]
        point_up = [self.pos_x, (self.pos_y - 1) % Settings.grid_size_y]
        point_down = [self.pos_x, (self.pos_y + 1) % Settings.grid_size_y]
        for body_part in range(1, len(self.body)):
            if self.body[body_part] == point_right:
                right = 1
            if self.body[body_part] == point_left:
                left = 1
            if self.body[body_part] == point_down:
                down = 1
            if self.body[body_part] == point_up:
                up = 1
        return up, down, left, right

    def fruits_detection(self, fruits):
        fruit = fruits['fruit ' + str(0)]
        fruit_x = fruit.location[0]
        fruit_y = fruit.location[1]
        up = 0
        down = 0
        left = 0
        right = 0
        if fruit_x > self.pos_x:
            right = 1
        elif fruit_x < self.pos_x:
            left = 1
        if fruit_y > self.pos_y:
            up = 1
        elif fruit_y < self.pos_y:
            down = 1
        return up, down, left, right

    def collision_body(self):
        if len(self.body) > 0:
            for body_part in range(1, len(self.body)):
                if self.body[body_part] == [self.pos_x, self.pos_y]:
                    self.is_alive = False

    def collision_fruit(self, Fruit):
        reward = 0
        if [self.pos_x, self.pos_y] == Fruit.location:
            self.body.append([-1, -1])
            reward = 10
            if self.graphic_on:
                Fruit.sound.play()
            Fruit.location = Fruit.generate(self.body)
        return [Fruit.location, reward]

    def tail_update(self):
        if len(self.body) > 0:
            for body_part in range(len(self.body) - 1, -1, -1):
                self.body[body_part] = self.body[body_part - 1]
        self.body[0] = copy.copy([self.pos_x, self.pos_y])

    def handle_input(self, keys):
        if keys[0] == 'a' and self.direction != 2:
            self.direction = 1
            if self.graphic_on:
                self.head_sprite = pg.transform.rotate(self.head_sprite, self.rotation - 270)
            self.rotation = 270
            return
        if keys[0] == 'd' and self.direction != 1:
            self.direction = 2
            if self.graphic_on:
                self.head_sprite = pg.transform.rotate(self.head_sprite, self.rotation - 90)
            self.rotation = 90
            return
        if keys[0] == 'w' and self.direction != 4:
            self.direction = 3
            if self.graphic_on:
                self.head_sprite = pg.transform.rotate(self.head_sprite, self.rotation)
            self.rotation = 0
            return
        if keys[0] == 's' and self.direction != 3:
            self.direction = 4
            if self.graphic_on:
                self.head_sprite = pg.transform.rotate(self.head_sprite, self.rotation - 180)
            self.rotation = 180
            return

    def draw(self, screen):
        if len(self.body) > 0:
            for body_part in range(1, len(self.body)):
                screen.blit(self.body_sprite,
                            (self.body[body_part][0] * Settings.tile_size, self.body[body_part][1] * Settings.tile_size))
        screen.blit(self.head_sprite, (self.pos_x * Settings.tile_size, self.pos_y * Settings.tile_size))

    def update(self, keys):
        if len(keys) >= 1:
            self.handle_input(keys)
        self.movement()
        self.pos_correction()
        self.tail_update()
        self.collision_body()
