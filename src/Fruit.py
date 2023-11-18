import random

import pygame as pg

from settings import Settings


class Fruit:
    def __init__(self, graphic_on):
        self.location = [-1, -1]
        if graphic_on:
            self.sprite = pg.image.load('assets/sprites/fruit.png')
            self.sprite = pg.transform.scale(self.sprite, (Settings.tile_size, Settings.tile_size))
            self.sound = pg.mixer.Sound('assets/sounds/fruit.mp3')
            self.sound.set_volume(0.3)

    def generate(self, snake_body):
        self.location = [random.randrange(0, Settings.grid_size_x), random.randrange(0, Settings.grid_size_y)]
        for body_part in snake_body:
            if body_part == self.location:
                self.location = self.generate(snake_body)
        return self.location

    def draw(self, screen):
        screen.blit(self.sprite, (self.location[0] * Settings.tile_size, self.location[1] * Settings.tile_size))
