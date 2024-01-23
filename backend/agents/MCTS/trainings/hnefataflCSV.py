import csv
from math import sqrt
import sys
from pathlib import Path
import numpy as np

project_root = Path(__file__).resolve().parents[4]  # Ajusta el número de parents según la estructura
sys.path.append(str(project_root))

import gymnasium as gym
from tqdm import tqdm
from backend.agents.MCTS.mctsAgent import MCTSHnefataflAgent
import matplotlib.pyplot as plt

env = gym.make('hnefatafl/Hnefatafl-v0', board=3, max_movements=1000, render_mode="human")

n_episodes = 5

agentes = {
    1: {
        "simulations_number": 100,
        "exploration_factor": 1,
    },
    2: {
        "simulations_number": 100,
        "exploration_factor": 0,
    },
    3: {
        "simulations_number": 100,
        "exploration_factor": 0.5,
    },
    4: {
        "simulations_number": 200,
        "exploration_factor": 1 / sqrt(2),
    },
}

with open("C:\\Users\\vicen\\MASTER\\MLE\\TRABAJOS\\ajedrez-vikinga\\documentacion\\result_mcts.csv", "w+",
          newline="") as f:
    writer = csv.writer(f)
    cabecera = ["simulations_number_whites", "exploration_factor_whites", "simulations_number_blacks",
                "exploration_factor_blacks", "average_time_whites", "chess_pieces_whites",
                "average_time_blacks", "chess_pieces_blacks", "result"]
    writer.writerow(cabecera)

    for a in agentes:
        whitesAgent = MCTSHnefataflAgent(
            env=env,
            player=2,
            simulations_number=agentes[a]["simulations_number"],
            exploration_factor=agentes[a]["exploration_factor"]
        )

        for b in agentes:

            if a == b:
                continue

            blacksAgent = MCTSHnefataflAgent(
                env=env,
                player=1,
                simulations_number=agentes[b]["simulations_number"],
                exploration_factor=agentes[b]["exploration_factor"],
                color="black"
            )

            whites_plot_entries = {
                "x": [],
                "y": []
            }

            blacks_plot_entries = {
                "x": [],
                "y": []
            }

            for episode in tqdm(range(n_episodes)):
                obs, info = env.reset()
                done = False

                # play one episode
                while not done:

                    state = (obs["board"], obs["turn"], obs["movements_left"])

                    if obs["turn"] == 1:
                        agent = blacksAgent
                    else:
                        agent = whitesAgent

                    action = agent.get_action(state)

                    next_obs, reward, terminated, truncated, info = env.step(action)

                    # update the agent
                    # agent.update(obs, action, reward, terminated, next_obs) Se deja comentado para mejorar las estadísticas que se obtienen de él en el futuro
                    blacksAgent.update(next_obs, len(env.unwrapped.possible_actions), reward, state)
                    r = whitesAgent.update(next_obs, len(env.unwrapped.possible_actions), reward, state)

                    # update if the environment is done and the current obs
                    done = terminated or truncated
                    obs = next_obs

                    average_time_whites = np.mean(whitesAgent.average_time)
                    average_time_blacks = np.mean(blacksAgent.average_time)
                    chess_pieces_whites = np.sum(whitesAgent.chess_pieces_whites)
                    chess_pieces_blacks = np.sum(blacksAgent.chess_pieces_blacks)



                    if r != "":
                        writer.writerow([agentes[a]["simulations_number"], agentes[a]["exploration_factor"],
                                        agentes[b]["simulations_number"], agentes[b]["exploration_factor"],
                                         average_time_whites, chess_pieces_whites,
                                         average_time_blacks, chess_pieces_blacks, r])

                        blacksAgent.number_of_pieces_whites = 0
                        blacksAgent.number_of_pieces_blacks = 0
                        blacksAgent.chess_pieces_blacks = []
                        blacksAgent.chess_pieces_whites = []

                        whitesAgent.number_of_pieces_whites = 0
                        whitesAgent.number_of_pieces_blacks = 0
                        whitesAgent.chess_pieces_whites = []
                        whitesAgent.chess_pieces_blacks = []


            final_white_agent_reward = whitesAgent.accumulated_reward[-1]
            final_black_agent_reward = blacksAgent.accumulated_reward[-1]

            whites_plot_entries["x"].append(episode)
            whites_plot_entries["y"].append(final_white_agent_reward)
            blacks_plot_entries["x"].append(episode)
            blacks_plot_entries["y"].append(final_black_agent_reward)

            plt.plot(whites_plot_entries["x"], whites_plot_entries["y"], label="Whites")
            plt.plot(blacks_plot_entries["x"], blacks_plot_entries["y"], label="Blacks")
            plt.title("Evolución de recompensas de agentes")
            plt.xlabel("Episodio")
            plt.ylabel("Recompensa")
            plt.legend()
            plt.show()
