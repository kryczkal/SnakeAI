import random

from Old.game import next_frame
from Old.game import restart
from Old.game import Score
from Old.game import Reward, Framerate_on
from src.Agent import Agent
from src.Plotter import plot, plot_complete

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001
TRAINING_INSTANCES = 100


def train():
    plot_score = []
    plot_mean_score = []
    total_score = 0
    record = 0
    agent = Agent()
    score = Score()
    restart()
    while agent.n_games < TRAINING_INSTANCES:
        state_old = agent.get_state()
        final_move = agent.get_action(state_old, True)
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
            if agent.n_games == TRAINING_INSTANCES:
                plot_complete(plot_score, plot_mean_score)

def play():
    restart()
    agent = Agent()
    Framerate_on()
    agent.model.load()
    while True:
        state_old = agent.get_state()
        final_move = agent.get_action(state_old, False)
        game_over = next_frame(final_move)
        if game_over:
            restart()
            Framerate_on()

if __name__ == '__main__':
    play()


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
