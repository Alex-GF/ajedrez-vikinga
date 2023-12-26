import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[4]  # Ajusta el número de parents según la estructura
sys.path.append(str(project_root))

import gymnasium as gym
from gymnasium.wrappers import FlattenObservation
import numpy as np
from tqdm import tqdm
from backend.agents.MCTS.mctsAgent import MCTSHnefataflAgent
import matplotlib.pyplot as plt

env = gym.make('hnefatafl/Hnefatafl-v0', board=1, max_movements=100, render_mode="human")
wrapped_env = FlattenObservation(env)

learning_rate = 0.01
n_episodes = 1000

whitesAgent = MCTSHnefataflAgent(
    env=env,
    player=2,
    learning_rate=learning_rate,
    simulations_number=100,
)

blacksAgent = MCTSHnefataflAgent(
    env=env,
    player=1,
    learning_rate=learning_rate,
    simulations_number=10,
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
        agent.update(next_obs, len(env.unwrapped.possible_actions), reward)
        
        # update if the environment is done and the current obs
        done = terminated or truncated
        obs = next_obs
    
    final_white_agent_reward = whitesAgent.accumulated_reward[-1]
    final_black_agent_reward = blacksAgent.accumulated_reward[-1]
    
    whites_plot_entries["x"].append(episode)
    whites_plot_entries["y"].append(final_white_agent_reward)
    blacks_plot_entries["x"].append(episode)
    blacks_plot_entries["y"].append(final_black_agent_reward)
    
plt.plot(whites_plot_entries["x"], whites_plot_entries["y"])
plt.plot(blacks_plot_entries["x"], blacks_plot_entries["y"])
plt.show()