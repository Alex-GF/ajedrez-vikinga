from math import sqrt
from backend.agents.MCTS.api import es_estado_final_api, aplica_movimiento_api, obtiene_movimientos_api, ganan_negras_api, ganan_blancas_api
from backend.agents.MCTS.mcts.objects.nodo import Nodo
from backend.agents.MCTS.mcts.crea_nodo import crea_nodo
from backend.agents.MCTS.mcts.backup import backup
from backend.agents.MCTS.mcts.best_child import best_child
from backend.agents.MCTS.mcts.expand import expand
from hnefatafl.envs.hnefatafl import HnefataflEnv
import numpy as np
import time

class MCTSHnefataflAgent:
    
    def __init__(self, 
        env: HnefataflEnv,
        player: int,
        exploration_factor: float = 1/sqrt(2),
        epsilon: float = 0.1,
        simulations_number: int = 1000,
        movement_selection_policy: str = "random",
        seed: int = None,
        average_time: list = [],
        color: str = "white",
        chess_pieces_whites: list = [],
        chess_pieces_blacks: list = [],
        number_of_pieces_whites: int = 0,
        number_of_pieces_blacks: int = 0
    ):  
        self.env = env
        if player < 1 or player > 2:
            raise ValueError("Player must be 1 or 2.")
        self.player = player
        self.simulations_number = simulations_number
        self.exploration_factor = exploration_factor
        self.epsilon = epsilon
        self.epsilon_decay = 1 - 1/self.env.unwrapped.max_movements
        self.movement_selection_policy = movement_selection_policy
        self.seed = seed
        
        # Agent evolution data
        self.accumulated_reward = [0]
        self.average_time = average_time
        self.color = color
        self.chess_pieces_whites = chess_pieces_whites
        self.chess_pieces_blacks = chess_pieces_blacks
        self.number_of_pieces_whites = number_of_pieces_whites
        self.number_of_pieces_blacks = number_of_pieces_blacks
        
        
    def get_action(self, state):

        t = time.time()
        
        self.rng = np.random.default_rng(seed=self.seed)
        
        if self.rng.random() < self.epsilon:
            self.average_time.append(time.time() - t)
            return self.rng.choice(self.env.unwrapped.possible_actions)
        else:
            v0 = crea_nodo(state, None, self.env.unwrapped.max_movements)
            
            i = 0
            
            while i < self.simulations_number:
                v1 = self._tree_policy(v0, self.exploration_factor)
                delta = self._default_policy(v1)
                backup(v1, delta)
                
                i += 1

            self.average_time.append(time.time() - t)

            return v0.movements[best_child(v0, 0)]
        
    def update(self, next_obs, possible_moves, obtained_reward, state=None):
        
        reward = 0
        
        removed_tokens = obtained_reward
        
        next_state = (next_obs["board"], next_obs["turn"])
        next_turn = next_obs["turn"]
        movements_left = next_obs["movements_left"]
        
        # Por ahora se quedan comentadas las recompensas por captura de fichas, se valorará su eliminación en futuras actualizaciones

        # if next_turn != self.player:
        #     reward += removed_tokens
        # else:
        #     reward -= removed_tokens
            
        # Premios/castigos por victoria/derrota
        r=""
        if ganan_negras_api.get(next_state, possible_moves) and self.player == 1:
            print("Ganan negras")
            reward += 1000
            r = "Ganan negras"
        elif ganan_blancas_api.get(next_state, possible_moves) and self.player == 2:
            print("Ganan blancas")
            reward += 1000
            r = "Ganan blancas"
        elif movements_left == 0:
            print("Tablas")
            reward += 100
            r = "Tablas"
        elif ganan_negras_api.get(next_state, possible_moves) and self.player == 2:
            print("Ganan negras")
            reward -= 1000
            r = "Ganan negras"
        elif ganan_blancas_api.get(next_state, possible_moves) and self.player == 1:
            print("Ganan blancas")
            reward -= 1000
            r = "Ganan blancas"

        self.accumulated_reward.append(self.accumulated_reward[-1] + reward)
        
        self.epsilon = self.epsilon * self.epsilon_decay

        self._removed_tokens(state, next_state)

        return r
    
    # --------------------------- PRIVATE FUNCTIONS --------------------------- #
    
    def _tree_policy(self, v: Nodo, cp):

        while not es_estado_final_api.get(v.state, len(v.movements), v.max_movements):
            if v.i < len(v.movements):
                return expand(v)
            else:
                v = v.children[best_child(v, cp)]
            
        return v
    
    def _default_policy(self, v: Nodo):
        
        state = (v.state[0].copy(), v.state[1])
        movs = v.movements
        player = v.parent.state[1]
        movements_left = v.max_movements
        total_reward = self.accumulated_reward[-1]
        
        while not es_estado_final_api.get(state, len(movs), movements_left):
            
            mov = self.rng.choice(movs)
            next_board, next_turn, movements_left, removed_tokens = aplica_movimiento_api.get(state, mov, movements_left)
            next_state = (next_board, next_turn)
            movs = obtiene_movimientos_api.get(next_state)
            state = next_state
            
            # Premios/castigos por captura de fichas # Por ahora se quedan comentadas las recompensas por captura de fichas, se valorará su eliminación en futuras actualizaciones
            
            # if player == self.player:
            #     total_reward += removed_tokens
            # else:
            #     total_reward -= removed_tokens
                
            # Premios/castigos por victoria/derrota
                
            if ganan_negras_api.get(next_state, movements_left) and player == 1:
                #print("Deduce Ganan Negras")
                total_reward += 1000
            elif ganan_blancas_api.get(next_state, movements_left) and player == 2:
                #print("Deduce Ganan Blancas")
                total_reward += 1000
            elif movements_left == 0:
                total_reward += 100
            elif ganan_negras_api.get(next_state, movements_left) and player == 2:
                #print("Deduce Ganan Negras")
                total_reward -= 1000
            elif ganan_blancas_api.get(next_state, movements_left) and player == 1:
                #print("Deduce Ganan Blancas")
                total_reward -= 1000
        
        return total_reward

    ## quiero una funcion a la que le pase un estado antiguo y un estado nuevo y me devuelva el numero de fichas que se han eliminado

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
