import pygame as pg

from src.Fruit import Fruit
from src.Snake import Snake
from settings import Settings


class Game:
    def __init__(self):
        # Constants
        # Game parameters adjustable by the user
        self.framerate_cap_flag = Settings.fps_on
        self.graphic_on = Settings.graphic_on
        # Initializing pygame
        if self.graphic_on:
            self.screen = pg.display.set_mode((Settings.screen_size_x, Settings.screen_size_y))
            pg.display.set_caption("snake")
            self.background = pg.image.load('assets/sprites/sand.png').convert()
            self.background = pg.transform.scale(self.background, (Settings.tile_size, Settings.tile_size))
            pg.init()
        # Variables changed as game progresses
        # Game internal variables
        self.keys = []
        self.clock = pg.time.Clock()
        self.snake = Snake(self.graphic_on)
        self.fruits = {}
        self.tick = int(Settings.fps / 10)
        # Game status
        self.score = 0
        self.number_of_fruits = 1
        self.reward = 0
        self.running = True

    def cap_framerate(self):
        self.framerate_cap_flag = True

    def draw_score(self):
        font = pg.font.SysFont(None, int(Settings.tile_size))
        img = font.render(str(len(self.snake.body)), True, 'BLACK')
        self.screen.blit(img, (20, 20))

    def restart(self):
        self.keys = []
        if self.graphic_on:
            pg.init()
        self.running = False
        self.snake = Snake(self.graphic_on)
        self.fruits = {}
        for x in range(0, self.number_of_fruits):
            self.fruits['fruit ' + str(x)] = Fruit(self.graphic_on)
            self.fruits['fruit ' + str(x)].generate(self.snake.body)

    def next_frame(self, final_move):
        self.reward = 0
        if not self.running:
            if self.graphic_on:
                self.screen.fill((255, 255, 255))
            # running = get_input(running)
            self.snake.update(self.key_pressed(final_move))
            # print(keys)
            # if len(keys) >= 1:
            #    keys.pop(0)
            if self.graphic_on:
                self.snake.draw(self.screen)

            for x in range(0, self.number_of_fruits):
                [self.fruits['fruit ' + str(x)].location, self.reward] = self.snake.collision_fruit(self.fruits['fruit ' + str(x)])
                if self.graphic_on:
                    self.fruits['fruit ' + str(x)].draw(self.screen)
            self.tick = 0
            self.score = len(self.snake.body)
            if self.graphic_on:
                self.draw_score()
                pg.display.update()
            if self.framerate_cap_flag:
                self.clock.tick(Settings.fps)
            if not self.snake.is_alive:
                self.running = True
                self.reward -= 50
        return self.running

    # Input
    def get_input(self, run):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_s:
                    self.keys.append('s')
                if event.key == pg.K_w:
                    self.keys.append('w')
                if event.key == pg.K_d:
                    self.keys.append('d')
                if event.key == pg.K_a:
                    self.keys.append('a')
        return run

    def key_pressed(self, move):
        # print(move)
        if self.snake.direction == 1:
            if move[0] == 1:
                return 'a'
            if move[1] == 1:
                return 'w'
            if move[2] == 1:
                return 's'
        if self.snake.direction == 2:
            if move[0] == 1:
                return 'd'
            if move[1] == 1:
                return 's'
            if move[2] == 1:
                return 'w'
        if self.snake.direction == 3:
            if move[0] == 1:
                return 's'
            if move[1] == 1:
                return 'a'
            if move[2] == 1:
                return 'd'
        if self.snake.direction == 4:
            if move[0] == 1:
                return 'w'
            if move[1] == 1:
                return 'd'
            if move[2] == 1:
                return 'a'

    # Current Game State for usage with neural network
    def get_game_state(self):
        d_up, d_down, d_left, d_right = self.snake.danger_detection()
        m_up, m_down, m_left, m_right = self.snake.direction_detection()
        f_up, f_down, f_left, f_right = self.snake.fruits_detection(self.fruits)
        # print(snake.direction_detection())
        # print(m_up,m_down,m_left,m_right)
        if m_up == 1:
            state = [d_up, d_right, d_left,
                     m_up, m_down, m_left, m_right,
                     f_up, f_down, f_left, f_right]
        if m_down == 1:
            state = [d_down, d_left, d_right,
                     m_up, m_down, m_left, m_right,
                     f_up, f_down, f_left, f_right]
        if m_left == 1:
            state = [d_left, d_up, d_down,
                     m_up, m_down, m_left, m_right,
                     f_up, f_down, f_left, f_right]
        if m_right == 1:
            state = [d_right, d_down, d_up,
                     m_up, m_down, m_left, m_right,
                     f_up, f_down, f_left, f_right]
        return state
