from .objects.nodo import Nodo
from backend.api import obtiene_movimientos_api

def crea_nodo(state, parent, max_movements):
    
    v = Nodo(state, obtiene_movimientos_api.get(state), 0., 0., 0, [], parent, parent.max_movements-1 if(max_movements==None) else max_movements)
    
    return v