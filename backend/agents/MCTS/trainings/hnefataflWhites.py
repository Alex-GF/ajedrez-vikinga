import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[4]  # Ajusta el número de parents según la estructura
sys.path.append(str(project_root))

import gymnasium as gym
from tqdm import tqdm
from backend.agents.MCTS.mctsAgent import MCTSHnefataflAgent
import matplotlib.pyplot as plt

env = gym.make('hnefatafl/Hnefatafl-v0', board=1, max_movements=100, player=1, render_mode="human")

learning_rate = 0.01
n_episodes = 1000

agent = MCTSHnefataflAgent(
    env=env,
    learning_rate=learning_rate,
    simulations_number=1000,
)

plot_entries = {
    "x": [],
    "y": []
}

for episode in tqdm(range(n_episodes)):
    obs, info = env.reset()
    done = False

    # play one episode
    while not done:
        action = agent.get_action(obs)
        next_obs, reward, terminated, truncated, info = env.step(action)

        # update the agent
        # agent.update(obs, action, reward, terminated, next_obs) Se deja comentado para mejorar las estadísticas que se obtienen de él en el futuro
        agent.update(reward)
        
        # update if the environment is done and the current obs
        done = terminated or truncated
        obs = next_obs
    
    final_agent_reward = agent.accumulated_reward[-1]
    
    plot_entries["x"].append(episode)
    plot_entries["y"].append(final_agent_reward)
    
plt.plot(plot_entries["x"], plot_entries["y"])
plt.show()