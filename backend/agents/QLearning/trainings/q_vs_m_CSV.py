import csv
from math import sqrt
import sys
from pathlib import Path

import numpy as np

from backend.agents.MCTS.mctsAgent import MCTSHnefataflAgent

project_root = Path(__file__).resolve().parents[4]  # Ajusta el número de parents según la estructura
sys.path.append(str(project_root))

import gymnasium as gym
from tqdm import tqdm
from backend.agents.QLearning.qlearningAgent import QlearningAgent
import matplotlib.pyplot as plt

env = gym.make('hnefatafl/Hnefatafl-v0', board=3, max_movements=1000, render_mode="human")

n_episodes = 5

agentes = {
    1: {
        "learning_rate": 0.2,
        "initial_epsilon": 0.9,
        "epsilon_decay": 0.85,
        "final_epsilon": 0.05
    },
    3: {
        "learning_rate": 0.07,
        "initial_epsilon": 0.7,
        "epsilon_decay": 0.97,
        "final_epsilon": 0.15
    },
    2: {
        "simulations_number": 100,
        "exploration_factor": 0,
    },
    4: {
        "simulations_number": 200,
        "exploration_factor": 1 / sqrt(2),
    }
}

agentes_whites = {
    1: {
        "learning_rate": 0.2,
        "initial_epsilon": 0.9,
        "epsilon_decay": 0.85,
        "final_epsilon": 0.05
    },
    2: {
        "simulations_number": 100,
        "exploration_factor": 0,
    },
}

agentes_blacks = {
    3: {
        "learning_rate": 0.07,
        "initial_epsilon": 0.7,
        "epsilon_decay": 0.97,
        "final_epsilon": 0.15
    },
    4: {
        "simulations_number": 100,
        "exploration_factor": 0,
    },
}

with open("C:\\Users\\vicen\\MASTER\\MLE\\TRABAJOS\\ajedrez-vikinga\\documentacion\\result_q_mcts.csv", "w+",
          newline="") as f:
    writer = csv.writer(f)
    cabecera = ["agent_white", "agent_black", "average_time_whites", "chess_pieces_whites", "average_time_blacks",
                "chess_pieces_blacs", "result"]
    writer.writerow(cabecera)

    for a in agentes_whites:

        if a % 2 != 0:

            whitesAgent = QlearningAgent(
                env=env,
                player=2,
                learning_rate=agentes_whites[a]['learning_rate'],
                initial_epsilon=agentes_whites[a]['initial_epsilon'],
                epsilon_decay=agentes_whites[a]['epsilon_decay'],
                final_epsilon=agentes_whites[a]['final_epsilon'],
                q_values_path="whites_q_values.pickle"
            )
        else:
            whitesAgent = MCTSHnefataflAgent(
                env=env,
                player=2,
                simulations_number=agentes_whites[a]["simulations_number"],
                exploration_factor=agentes_whites[a]["exploration_factor"]
            )

        for b in agentes_blacks:

            if (a % 2 != 0 and b % 2 != 0) or (a % 2 == 0 and b % 2 == 0):
                continue

            if b % 2 != 0:
                blacksAgent = QlearningAgent(
                    env=env,
                    player=1,
                    learning_rate=agentes_blacks[b]['learning_rate'],
                    initial_epsilon=agentes_blacks[b]['initial_epsilon'],
                    epsilon_decay=agentes_blacks[b]['epsilon_decay'],
                    final_epsilon=agentes_blacks[b]['final_epsilon'],
                    q_values_path="blacks_q_values.pickle",
                    color="black"

                )

            else:
                blacksAgent = MCTSHnefataflAgent(
                    env=env,
                    player=1,
                    simulations_number=agentes_blacks[b]["simulations_number"],
                    exploration_factor=agentes_blacks[b]["exploration_factor"],
                    color="black"
                )

            print(f'{a}-{b}')

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

                    if b % 2 != 0:
                        blacksAgent.update(state, action, reward, next_obs=next_obs, terminated=terminated,
                                       possible_moves=len(env.unwrapped.possible_actions))
                    else:
                        blacksAgent.update(next_obs, len(env.unwrapped.possible_actions), reward, state)

                    if a % 2 != 0:
                        r = whitesAgent.update(state, action, reward, next_obs=next_obs, terminated=terminated,
                                           possible_moves=len(env.unwrapped.possible_actions))
                    else:
                        r = whitesAgent.update(next_obs, len(env.unwrapped.possible_actions), reward, state)

                    # update if the environment is done and the current obs
                    done = terminated or truncated
                    obs = next_obs

                    average_time_whites = np.mean(whitesAgent.average_time)
                    average_time_blacks = np.mean(blacksAgent.average_time)
                    chess_pieces_whites = np.sum(whitesAgent.chess_pieces_whites)
                    chess_pieces_blacks = np.sum(blacksAgent.chess_pieces_blacks)

                    if r != "":
                        writer.writerow([a, b, average_time_whites, chess_pieces_whites,
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
