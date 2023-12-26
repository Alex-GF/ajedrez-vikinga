from backend.api import aplica_movimiento_api
from .crea_nodo import crea_nodo

def expand(v):

    state = aplica_movimiento_api.get(v.state, v.movements[v.i], v.max_movements)

    v.i = v.i + 1
    child = crea_nodo(state, v, None)
    v.children.append(child)
    
    return child