from collections import defaultdict

import numpy as np
from backend.agents.MCTS.api import es_estado_final_api, aplica_movimiento_api, obtiene_movimientos_api, ganan_negras_api, ganan_blancas_api

from hnefatafl.envs import HnefataflEnv


class QlearningAgent:

    def __init__(self,
                 env: HnefataflEnv,
                 player: int,
                 learning_rate: float,
                 initial_epsilon: float,
                 epsilon_decay: float,
                 final_epsilon: float,
                 discount_factor: float = 0.95,
                 seed: int = None,
                 rng: np.random.Generator = None,
                 accumulated_reward: list = [0]
                 ):
        self.env = env

        if player < 1 or player > 2:
            raise ValueError("Player must be 1 or 2.")
        self.player = player

        self.q_values = defaultdict(lambda: np.zeros(len(self.env.action_space)))

        self.lr = learning_rate
        self.discount_factor = discount_factor

        self.epsilon = initial_epsilon
        self.epsilon_decay = epsilon_decay
        self.final_epsilon = final_epsilon

        self.training_error = []

        self.seed = seed

        self.accumulated_reward = accumulated_reward

    def get_action(self, obs):
        """
        Returns the best action with probability (1 - epsilon)
        otherwise a random action with probability epsilon to ensure exploration.
        """
        # with probability epsilon return a random action to explore the environment
        self.rng = np.random.default_rng(seed=self.seed)

        if self.rng.random() < self.epsilon:
            return self.rng.choice(self.env.unwrapped.possible_actions)

        # with probability (1 - epsilon) act greedily (exploit)
        else:
            _obs = ' '.join(map(str, obs[0]))
            q = self.q_values.get(_obs, 0)
            return q if q and np.argmax(q, 0) else self.rng.choice(self.env.unwrapped.possible_actions)

    def update(
            self,
            obs,
            action: int,
            reward: float,
            terminated: bool,
            next_obs,
            possible_moves: list,
    ):
        _obs = obs
        obs = ' '.join(map(str, obs[0]))
        """Updates the Q-value of an action."""
        _next_obs = ''.join(map(str, next_obs['board']))
        future_q_value = (not terminated) * np.max(self.q_values[_next_obs])
        temporal_difference = (
                reward + self.discount_factor * future_q_value - self.q_values.get(obs, 0)
        )

        self.q_values[obs] = (
                self.q_values.get(obs, 0) + self.lr * temporal_difference
        )
        self.training_error.append(temporal_difference)

        reward = 0


        next_state = (_obs[0], _obs[1])
        next_turn = _obs[1]
        movements_left = _obs[2]

        # Por ahora se quedan comentadas las recompensas por captura de fichas, se valorará su eliminación en futuras actualizaciones

        # if next_turn != self.player:
        #     reward += removed_tokens
        # else:
        #     reward -= removed_tokens

        # Premios/castigos por victoria/derrota

        if ganan_negras_api.get(next_state, possible_moves) and self.player == 1:
            print("Ganan negras")
            reward += 1000
        elif ganan_blancas_api.get(next_state, possible_moves) and self.player == 2:
            print("Ganan blancas")
            reward += 1000
        elif movements_left == 0:
            print("Tablas")
            reward += 100
        elif ganan_negras_api.get(next_state, possible_moves) and self.player == 2:
            print("Ganan negras")
            reward -= 1000
        elif ganan_blancas_api.get(next_state, possible_moves) and self.player == 1:
            print("Ganan blancas")
            reward -= 1000

        self.accumulated_reward.append(self.accumulated_reward[-1] + reward)

        self.epsilon = self.epsilon * self.epsilon_decay

    def decay_epsilon(self):
        self.epsilon = max(self.final_epsilon, self.epsilon - self.epsilon_decay)
