from backend.api import es_estado_final_api
from .expand import expand
from .best_child import best_child

def tree_policy(v, cp):

    while not es_estado_final_api.get(v.state, len(v.movements), v.max_movements):
        if v.i < len(v.movements):
            return expand(v)
        else:
            v = v.children[best_child(v, cp)]
            
    return v