from .crea_nodo import crea_nodo
from time import time
from .tree_policy import tree_policy
from .default_policy import default_policy
from .best_child import best_child
from .backup import backup

def busca_solucion(s0, max_time, max_movements, cp, heuristic):
    
    start_time = time()
    computing_time = time() - start_time

    v0 = crea_nodo(s0, None, max_movements)

    while computing_time < max_time:

        v1 = tree_policy(v0, cp)
        delta = default_policy(v1, heuristic)
        backup(v1, delta)

        computing_time = time() - start_time
    
    return (v0.movements[best_child(v0, 0)], v0.n+1)