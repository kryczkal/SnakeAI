import random
from collections import deque

import numpy as np
import torch

from settings import Settings
from src.Linear_QNET import Linear_QNet
from src.Qtrainer import Qtrainer


class Agent:
    def __init__(self, game):
        self.n_games = 0
        self.epsilon = 0  # randomness
        self.gamma = 0.9  # unlearn factor
        self.memory = deque(maxlen=Settings.MAX_MEMORY)  #
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = Qtrainer(self.model, lr=Settings.LR, gamma=self.gamma)
        self.game_played = game

    def get_state(self):
        state = self.game_played.get_game_state()
        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, game_over):
        self.memory.append((state, action, reward, next_state, game_over))

    def train_long_memory(self):
        if len(self.memory) > Settings.BATCH_SIZE:
            mini_sample = random.sample(self.memory, Settings.BATCH_SIZE)
        else:
            mini_sample = self.memory
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, game_over):
        self.trainer.train_step(state, action, reward, next_state, game_over)

    def get_action(self, state, training):
        if training:
            self.epsilon = 80 - self.n_games
        else:
            self.epsilon = -1
        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        return final_move