from backend.agents.MCTS.mcts import mcts
from . import aplica_movimiento_api

def get(current_state, time, max_movements, cp, heuristic):

    movement, searched_nodes = mcts.busca_solucion(current_state, time, max_movements, cp, heuristic)

    state = aplica_movimiento_api.get(current_state, movement, max_movements)

    return (movement, state, searched_nodes)