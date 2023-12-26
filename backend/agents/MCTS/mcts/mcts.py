from .crea_nodo import crea_nodo
from time import time
from .tree_policy import tree_policy
from .default_policy import default_policy
from .best_child import best_child
from .backup import backup

def busca_solucion(s0, simulations_number, max_movements, cp, heuristic):

    v0 = crea_nodo(s0, None, max_movements)

    i = 0

    while i < simulations_number:

        v1 = tree_policy(v0, cp)
        delta = default_policy(v1, heuristic)
        backup(v1, delta)

        i += 1
    
    return (v0.movements[best_child(v0, 0)], v0.n+1)