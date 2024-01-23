import csv
from math import sqrt
import sys
from pathlib import Path

import numpy as np

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
    2: {
        "learning_rate": 0.05,
        "initial_epsilon": 0.5,
        "epsilon_decay": 0.95,
        "final_epsilon": 0.2
    },
    3: {
        "learning_rate": 0.15,
        "initial_epsilon": 0.8,
        "epsilon_decay": 0.92,
        "final_epsilon": 0.1
    },
    4: {
        "learning_rate": 0.07,
        "initial_epsilon": 0.7,
        "epsilon_decay": 0.97,
        "final_epsilon": 0.15
    }
}

with open("C:\\Users\\vicen\\MASTER\\MLE\\TRABAJOS\\ajedrez-vikinga\\documentacion\\result_qlearning.csv", "w+",
          newline="") as f:
    writer = csv.writer(f)
    cabecera = ["learning_rate_whites", "initial_epsilon_whites", "epsilon_decay_whites", "final_epsilon_whites",
                "learning_rate_blacks", "initial_epsilon_blacks", "epsilon_decay_blacks", "final_epsilon_blacls",
                "average_time_whites", "chess_pieces_whites", "average_time_blacks", "chess_pieces_blacs", "result"]
    writer.writerow(cabecera)

    for a in agentes:
        whitesAgent = QlearningAgent(
            env=env,
            player=2,
            learning_rate=agentes[a]['learning_rate'],
            initial_epsilon=agentes[a]['initial_epsilon'],
            epsilon_decay=agentes[a]['epsilon_decay'],
            final_epsilon=agentes[a]['final_epsilon'],
            q_values_path="whites_q_values.pickle"
        )

        for b in agentes:

            if a == b:
                continue

            blacksAgent = QlearningAgent(
                env=env,
                player=1,
                learning_rate=agentes[a]['learning_rate'],
                initial_epsilon=agentes[a]['initial_epsilon'],
                epsilon_decay=agentes[a]['epsilon_decay'],
                final_epsilon=agentes[a]['final_epsilon'],
                q_values_path="blacks_q_values.pickle",
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
                    blacksAgent.update(state, action, reward, next_obs=next_obs, terminated=terminated,
                                       possible_moves=len(env.unwrapped.possible_actions))
                    r = whitesAgent.update(state, action, reward, next_obs=next_obs, terminated=terminated,
                                       possible_moves=len(env.unwrapped.possible_actions))

                    # update if the environment is done and the current obs
                    done = terminated or truncated
                    obs = next_obs

                    average_time_whites = np.mean(whitesAgent.average_time)
                    average_time_blacks = np.mean(blacksAgent.average_time)
                    chess_pieces_whites = np.sum(whitesAgent.chess_pieces_whites)
                    chess_pieces_blacks = np.sum(blacksAgent.chess_pieces_blacks)

                    if r != "":
                        writer.writerow([agentes[a]["learning_rate"], agentes[a]["initial_epsilon"],
                                        agentes[a]["epsilon_decay"], agentes[a]["final_epsilon"],
                                        agentes[b]["learning_rate"], agentes[b]["initial_epsilon"],
                                        agentes[b]["epsilon_decay"], agentes[b]["final_epsilon"],
                                        average_time_whites, chess_pieces_whites,
                                        average_time_blacks, chess_pieces_blacks,r])

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
