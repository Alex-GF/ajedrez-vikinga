import gymnasium as gym
import numpy as np
import pygame
from gymnasium import spaces
from hnefatafl.api import obtiene_estado_inicial_api, obtiene_movimientos_api, ganan_negras_api, ganan_blancas_api, aplica_movimiento_api, es_estado_final_api

board_ids = {
    1: "hnefatafl",
    2: "tablut",
    3: "ard-ri",
    4: "brandubh",
    5: "tawlbwrdd",
    6: "alea-evangelii",
}

class HnefataflEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array", "ansi"], "render_fps": 4}
    
    def __init__(self, board, max_movements, render_mode=None):
        
        if board < 1 or board > 6:
            raise ValueError("Board size must be between 1 and 6. Each one:\n\n1: Hnefatafl\n2: Tablut\n3: Ard Ri\n4: Brandubh\n5: Tawlbwrdd\n6: Alea Evangelii")
        
        if max_movements < 1:
            raise ValueError("Max movements must be greater than 0.")
        
        self.selected_board = board
        self.max_movements = max_movements
        self.window_size = 512
        
        initial_state = obtiene_estado_inicial_api.get(board_ids[self.selected_board])
        
        self.board_size = len(initial_state[0][0])
        
        self.observation_space = spaces.Dict(
            {
                "board": spaces.Box(0, 3, shape=(self.board_size, self.board_size), dtype=int),
                "turn": spaces.Discrete(2, start=1),
                "movements_left": spaces.Discrete(max_movements),
            }
        )
        
        self.action_space = spaces.MultiDiscrete([self.board_size-1, self.board_size-1, self.board_size-1, self.board_size-1])
        self.possible_actions = obtiene_movimientos_api.get(initial_state)
        self.initial_actions = self.possible_actions.copy()
        
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        
        self.render_mode = render_mode
        
        self.window = None
        self.clock = None
        
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        
        initial_state = obtiene_estado_inicial_api.get(board_ids[self.selected_board])
        
        self._board = initial_state[0]
        self._turn = initial_state[1]
        self._movements_left = self.max_movements
        self.possible_actions = self.initial_actions.copy()
        
        observation = self._get_obs()
        info = self._get_info()
        
        return observation, info
    
    def step(self, action):
        
        current_state = (self._board, self._turn)
        
        next_board, next_turn, movements_left, removed_tokens = aplica_movimiento_api.get(current_state, action, self._movements_left)
        
        next_state = (next_board, next_turn)
        
        possible_moves = obtiene_movimientos_api.get(next_state)
        
        reward = removed_tokens
        
        terminated = es_estado_final_api.get(next_state, len(possible_moves), movements_left)
        
        self._board = next_board
        self._turn = next_turn
        self._movements_left = movements_left
        self.possible_actions = obtiene_movimientos_api.get(next_state)
        
        observation = self._get_obs()
        info = self._get_info()
        
        if self.render_mode == "human":
            self._render_frame()
        
        return observation, reward, terminated, False, info
    
    def render(self):
        if self.render_mode == "rgb_array":
            return self._render_frame()
        
    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
    
    # ------------------------ PRIVATE FUNCTIONS ------------------------
        
    def _get_obs(self):
        return {
            "board": self._board, 
            "turn": self._turn, 
            "movements_left": self._movements_left
        }
    
    def _get_info(self):
        return {}
    
    # def _compute_reward(self, next_state, possible_moves, removed_tokens, movements_left, turn, next_turn):
    #     reward = 0
        
    #     # Premios/castigos por captura de fichas
        
    #     if turn != next_turn:
    #         reward += removed_tokens
    #     else:
    #         reward -= removed_tokens
            
    #     # Premios/castigos por victoria/derrota
            
    #     if ganan_negras_api.get(next_state, possible_moves) and next_turn == 2:
    #         reward += 1000
    #     elif ganan_blancas_api.get(next_state, possible_moves) and next_turn == 1:
    #         reward += 1000
    #     elif movements_left == 0:
    #         reward += 100
    #     elif ganan_negras_api.get(next_state, possible_moves) and next_turn == 1:
    #         reward -= 1000
    #     elif ganan_blancas_api.get(next_state, possible_moves) and next_turn == 2:
    #         reward -= 1000
            
    #     return reward
    
    def _render_frame(self):
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode(
                (self.window_size, self.window_size)
            )
        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()

        canvas = pygame.Surface((self.window_size, self.window_size))
        canvas.fill((255, 165, 0))
        pix_square_size = (
            self.window_size / self.board_size
        )  # The size of a single grid square in pixels

        # First we draw the throne
        pygame.draw.rect(
            canvas,
            (0, 255, 0),
            pygame.Rect(
                self.window_size/2 - pix_square_size/2,
                self.window_size/2 - pix_square_size/2,
                pix_square_size,
                pix_square_size
            ),
        )
        
        # Next we draw the corners
        
        pygame.draw.rect(
            canvas,
            (0, 255, 0),
            pygame.Rect(
                0,
                0,
                pix_square_size, 
                pix_square_size
            ),
        )
        pygame.draw.rect(
            canvas,
            (0, 255, 0),
            pygame.Rect(
                self.window_size-pix_square_size,
                0,
                pix_square_size, 
                pix_square_size
            ),
        )
        pygame.draw.rect(
            canvas,
            (0, 255, 0),
            pygame.Rect(
                0,
                self.window_size-pix_square_size,
                pix_square_size, 
                pix_square_size
            ),
        )
        pygame.draw.rect(
            canvas,
            (0, 255, 0),
            pygame.Rect(
                self.window_size-pix_square_size,
                self.window_size-pix_square_size,
                pix_square_size, 
                pix_square_size
            ),
        )
        
        
        # Now we draw the pieces
        for i in range(len(self._board)):
            for j in range(len(self._board)):
                if self._board[i][j] == 1:
                    pygame.draw.circle(
                        canvas,
                        (0, 0, 0),
                        (i*pix_square_size + 0.5 * pix_square_size, j*pix_square_size + 0.5 * pix_square_size),
                        0.3 * pix_square_size
                    )
                elif self._board[i][j] == 2:
                    pygame.draw.circle(
                        canvas,
                        (255, 255, 255),
                        (i*pix_square_size + 0.5 * pix_square_size, j*pix_square_size + 0.5 * pix_square_size),
                        0.3 * pix_square_size,
                    )
                elif self._board[i][j] == 3:
                    pygame.draw.circle(
                        canvas,
                        (255, 0, 0),
                        (i*pix_square_size + 0.5 * pix_square_size, j*pix_square_size + 0.5 * pix_square_size),
                        0.3 * pix_square_size,
                    )

        # Finally, add some gridlines
        for x in range(self.board_size + 1):
            pygame.draw.line(
                canvas,
                0,
                (0, pix_square_size * x),
                (self.window_size, pix_square_size * x),
                width=3,
            )
            pygame.draw.line(
                canvas,
                0,
                (pix_square_size * x, 0),
                (pix_square_size * x, self.window_size),
                width=3,
            )

        if self.render_mode == "human":
            # The following line copies our drawings from `canvas` to the visible window
            self.window.blit(canvas, canvas.get_rect())
            pygame.event.pump()
            pygame.display.update()

            # We need to ensure that human-rendering occurs at the predefined framerate.
            # The following line will automatically add a delay to keep the framerate stable.
            self.clock.tick(self.metadata["render_fps"])
        else:  # rgb_array
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2)
            )