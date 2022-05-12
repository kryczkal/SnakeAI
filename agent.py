import random
import torch
import numpy as np
from game import next_frame
from game import restart
from game import Score
import time
from collections import deque
from game import state_of_game, Reward, Framerate_on
from model import Linear_QNet, Qtrainer
from helper import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0  # randomness
        self.gamma = 0.9  # unlearn factor
        self.memory = deque(maxlen=MAX_MEMORY)  #
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = Qtrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self):
        state = state_of_game()
        #print(state)
        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, game_over):
        self.memory.append((state, action, reward, next_state, game_over))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, game_over):
        self.trainer.train_step(state, action, reward, next_state, game_over)

    def get_action(self, state):
        self.epsilon = 80 - self.n_games
        final_move = [0, 0, 0]
        if self.n_games > 240:
            Framerate_on()
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        return final_move


def train():
    plot_score = []
    plot_mean_score = []
    total_score = 0
    record = 0
    agent = Agent()
    score = Score()
    restart()
    while agent.n_games < 250:
        state_old = agent.get_state()
        final_move = agent.get_action(state_old)
        #print(final_move)
        score = Score()

        game_over = next_frame(final_move)
        reward = Reward()
        state_new = agent.get_state()

        agent.train_short_memory(state_old, final_move, reward, state_new, game_over)
        agent.remember(state_old, final_move, reward, state_new, game_over)

        if game_over:
            # train long memory, plot result
            score = Score()
            restart()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()
            print('Game', agent.n_games, 'Score', score, 'Record: ', record)

            plot_score.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_score.append(mean_score)
            plot(plot_score,plot_mean_score)


if __name__ == '__main__':
    train()


def draw_key():
    x = random.randrange(0, 3)
    if x == 0:
        return 'a'
    if x == 1:
        return 'd'
    if x == 2:
        return 'w'
    if x == 3:
        return 's'
