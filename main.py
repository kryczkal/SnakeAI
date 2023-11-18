from src.Agent import Agent
from src.Game import Game
from src.Plotter import Plotter

TRAINING_INSTANCES = 100
def train(game):
    agent = Agent(game)
    plotter = Plotter()
    game.restart()

    plot_score = []
    plot_mean_score = []

    total_score = 0
    record = 0

    while agent.n_games < TRAINING_INSTANCES:
        state_old = agent.get_state()
        final_move = agent.get_action(state_old, True)
        score = game.score

        game_over = game.next_frame(final_move)
        reward = game.reward
        state_new = agent.get_state()

        agent.train_short_memory(state_old, final_move, reward, state_new, game_over)
        agent.remember(state_old, final_move, reward, state_new, game_over)

        if game_over:
            # train long memory, plot result
            score = game.score
            game.restart()
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
            plotter.plot(plot_score, plot_mean_score)
            if agent.n_games == TRAINING_INSTANCES:
                plotter.plot_complete(plot_score, plot_mean_score)


def play(game: Game):
    game.restart()
    # game.Framerate_on()
    agent = Agent(game)
    agent.model.load()
    while True:
        state_old = agent.get_state()
        final_move = agent.get_action(state_old, False)
        game_over = game.next_frame(final_move)
        if game_over:
            game.restart()
            game.cap_framerate()


if __name__ == '__main__':
    game = Game()
    train(game)
    play(game)
