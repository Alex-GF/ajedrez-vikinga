import os.path
import pickle
import random
import time
from collections import defaultdict

import numpy as np
from backend.agents.MCTS.api import es_estado_final_api, aplica_movimiento_api, obtiene_movimientos_api, \
    ganan_negras_api, ganan_blancas_api

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
                 accumulated_reward: list = [0],
                 q_values_path=None,
                 average_time: list = [],
                 chess_pieces_whites: list = [],
                 chess_pieces_blacks: list = [],
                 color: str = "white",
                 number_of_pieces_whites: int = 0,
                 number_of_pieces_blacks: int = 0
                 ):
        self.env = env

        if player < 1 or player > 2:
            raise ValueError("Player must be 1 or 2.")
        self.player = player

        self.q_values = defaultdict(lambda: defaultdict(float)) if q_values_path is None else self.load_q_values(
            q_values_path)

        self.lr = learning_rate
        self.discount_factor = discount_factor

        self.epsilon = initial_epsilon
        self.epsilon_decay = epsilon_decay
        self.final_epsilon = final_epsilon

        self.training_error = []

        self.seed = seed

        self.accumulated_reward = accumulated_reward

        self.q_values_path = q_values_path

        self.average_time = average_time
        self.chess_pieces_whites = chess_pieces_whites
        self.chess_pieces_blacks = chess_pieces_blacks
        self.color = color
        self.number_of_pieces_whites = number_of_pieces_whites
        self.number_of_pieces_blacks = number_of_pieces_blacks

    def get_action(self, obs):
        """
        Returns the best action with probability (1 - epsilon)
        otherwise a random action with probability epsilon to ensure exploration.
        """
        # with probability epsilon return a random action to explore the environment

        t = time.time()
        self.rng = np.random.default_rng(seed=self.seed)

        if self.rng.random() < self.epsilon:
            result = self.rng.choice(self.env.unwrapped.possible_actions)
            self.average_time.append(time.time() - t)
            return result

        # with probability (1 - epsilon) act greedily (exploit)
        else:
            _obs = ' '.join(map(str, obs[0]))
            result = self._best_action(_obs)
            self.average_time.append(time.time() - t)
            return result

    def _best_action(self, obs):
        actions = self.q_values.get(obs)
        max_value = np.max(actions.values()) if actions else 0
        best_actions = [action for action, value in actions.items() if value == max_value] if actions else []
        return random.choice(best_actions) if best_actions else self.rng.choice(self.env.unwrapped.possible_actions)

    def update(
            self,
            obs,
            action: int,
            reward: float,
            terminated: bool,
            next_obs,
            possible_moves: list
    ):

        _obs = obs
        obs = ' '.join(map(str, obs[0]))
        """Updates the Q-value of an action."""
        _next_obs = ''.join(map(str, next_obs['board']))
        _action = ' '.join(map(str, action))

        next_state = (_obs[0], _obs[1])
        next_turn = _obs[1]
        movements_left = _obs[2]

        if terminated:
            possible_moves = 0

        r=""
        if ganan_negras_api.get(next_state, possible_moves) and self.player == 1:
            # print("Ganan negras")
            print("Ganan blancas")
            reward += 1000
            r = "Ganan blancas"
        elif ganan_blancas_api.get(next_state, possible_moves) and self.player == 2:
            # print("Ganan blancas")
            print("Ganan negras")
            reward += 1000
            r = "Ganan negras"
        elif movements_left == 0:
            print("Tablas")
            reward += 100
            r = "Tablas"
        elif ganan_negras_api.get(next_state, possible_moves) and self.player == 2:
            # print("Ganan negras")
            print("Ganan blancas")
            reward -= 1000
            r = "Ganan blancas"
        elif ganan_blancas_api.get(next_state, possible_moves) and self.player == 1:
            # print("Ganan blancas")
            print("Ganan negras")
            reward -= 1000
            r = "Ganan negras"


        future_q_value = (not terminated) * np.max(self.get_q_values(_next_obs, _action))
        temporal_difference = (
                reward + self.discount_factor * future_q_value - self.get_q_values(obs, _action)
        )

        if obs not in self.q_values:
            self.q_values[obs] = defaultdict(float)

        if _action not in self.q_values[obs]:
            self.q_values[obs][_action] = 0.0

        self.q_values[obs][_action] = (
                self.get_q_values(obs, _action) + self.lr * temporal_difference
        )
        self.training_error.append(temporal_difference)



        self.accumulated_reward.append(self.accumulated_reward[-1] + reward)

        self.epsilon = self.epsilon * self.epsilon_decay

        self.save_q_values(self.q_values, self.q_values_path)

        self._removed_tokens(_obs, next_state)

        return r

    def decay_epsilon(self):
        self.epsilon = max(self.final_epsilon, self.epsilon - self.epsilon_decay)


    def get_q_values(self, state, action, default=0):
        return self.q_values.get(state, {}).get(action, default)

    def save_q_values(self, q_values, filename):
        with open(filename, 'wb') as file:
            pickle.dump(dict(q_values), file)

    def load_q_values(self, filename):

        if not os.path.getsize(filename) <= 0:
            with open(filename, 'rb') as file:
                return pickle.load(file)
        else:
            return defaultdict(lambda: defaultdict(float))

    def _removed_tokens(self, old_state, new_state):

            old_board = old_state[0]
            new_board = new_state[0]

            old_board = np.array(old_board)
            new_board = np.array(new_board)

            old_board = old_board.flatten()
            new_board = new_board.flatten()

            if self.color == "white":

                _old_board = sum(old_board == 1)
                _new_board = sum(new_board == 1)

                if _new_board < self.number_of_pieces_whites:
                    self.chess_pieces_whites.append(1)

                self.number_of_pieces_whites = _new_board

            else:
                _old_board = sum((old_board == 2) | (old_board == 3))
                _new_board = sum((new_board == 2) | (new_board == 3))

                if _new_board < self.number_of_pieces_blacks:
                    self.chess_pieces_blacks = _new_board

                self.number_of_pieces_blacks = _new_board
