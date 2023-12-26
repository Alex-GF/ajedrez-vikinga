from math import sqrt
from backend.agents.MCTS.api import es_estado_final_api, aplica_movimiento_api, obtiene_movimientos_api, ganan_negras_api, ganan_blancas_api
from backend.agents.MCTS.mcts.objects.nodo import Nodo
from backend.agents.MCTS.mcts.crea_nodo import crea_nodo
from backend.agents.MCTS.mcts.backup import backup
from backend.agents.MCTS.mcts.best_child import best_child
from backend.agents.MCTS.mcts.expand import expand
from hnefatafl.hnefatafl.envs.hnefatafl import HnefataflEnv
import numpy as np

class MCTSHnefataflAgent:
    
    def __init__(self, 
        env: HnefataflEnv,
        player: int,
        learning_rate: float,
        exploration_factor: float = sqrt(2),
        epsilon: float = 0.1,
        simulations_number: int = 1000,
        movement_selection_policy: str = "random",
        seed: int = None
    ):  
        self.env = env
        if player < 1 or player > 2:
            raise ValueError("Player must be 1 or 2.")
        self.player = player
        self.lr = learning_rate
        self.simulations_number = simulations_number
        self.exploration_factor = exploration_factor
        self.epsilon = epsilon
        self.movement_selection_policy = movement_selection_policy
        self.seed = seed
        
        # Agent evolution data
        self.accumulated_reward = [0]
        
        
    def get_action(self, state):
        
        self.rng = np.random.default_rng(seed=self.seed)
        
        if self.rng.random() < self.epsilon:
            return self.rng.choice(self.env.possible_actions)
        else:
            v0 = crea_nodo(state, None, self.env.unwrapped.max_movements)
            
            i = 0
            
            while i < self.simulations_number:
                v1 = self._tree_policy(v0, self.exploration_factor)
                delta = self._default_policy(v1)
                #delta = delta if v1.parent.state[1] == self.player else -delta
                backup(v1, delta)
                
                i += 1
            
            return v0.movements[best_child(v0, 0)]
        
    def update(self, next_obs, possible_moves, obtained_reward):
        
        reward = 0
        
        removed_tokens = obtained_reward
        
        next_state = (next_obs["board"], next_obs["turn"])
        next_turn = next_obs["turn"]
        movements_left = next_obs["movements_left"]
        
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
        
        print("Reward: ", self.accumulated_reward)
        
    
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
            
            # Premios/castigos por captura de fichas
            
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