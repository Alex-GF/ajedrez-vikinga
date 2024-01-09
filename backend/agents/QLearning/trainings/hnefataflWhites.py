from math import sqrt
import sys
from pathlib import Path

from backend.agents.QLearning.qlearningAgent import QlearningAgent

project_root = Path(__file__).resolve().parents[4]  # Ajusta el número de parents según la estructura
sys.path.append(str(project_root))

import gymnasium as gym
from tqdm import tqdm
import matplotlib.pyplot as plt

env = gym.make('hnefatafl/Hnefatafl-v0', board=3, max_movements=1000, render_mode="human")

n_episodes = 5

whitesAgent = QlearningAgent(
    env=env,
    player=2,
    learning_rate=0.1,
    initial_epsilon=0.1,
    epsilon_decay=0.9,
    final_epsilon=0.01,
)

blacksAgent = QlearningAgent(
    env=env,
    player=1,
    learning_rate=0.1,
    initial_epsilon=0.1,
    epsilon_decay=0.9,
    final_epsilon=0.01
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
        blacksAgent.update(state, action, reward, next_obs=next_obs, terminated=terminated, possible_moves=len(env.action_space))
        whitesAgent.update(state, action, reward, next_obs=next_obs, terminated=terminated, possible_moves=(env.action_space))

        # update if the environment is done and the current obs
        done = terminated or truncated
        obs = next_obs

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