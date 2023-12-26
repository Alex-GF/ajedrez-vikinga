from backend.api import es_estado_final_api, aplica_movimiento_api, obtiene_movimientos_api, ganan_blancas_api, ganan_negras_api
import random

def default_policy(v, heuristic):

    state = (v.state[0].copy(), v.state[1])
    movs = v.movements
    player = v.parent.state[1]
    i = 0
    capture = 0
    max_movements = v.max_movements

    while not es_estado_final_api.get(state, len(movs), max_movements):
        
        mov = random.choice(movs)
        state = aplica_movimiento_api.get(state, mov, max_movements)
        movs = obtiene_movimientos_api.get(state)
        
        if(heuristic == 1):
            capture += (state[3]/(i+1)) if(player!=None and player%2 == i%2) else -(state[3]/(i+1))
        elif(heuristic == 2):
            if(player!=None and player%2 == i%2):
                capture += (state[3]/(i+1))
        i+=1
        
        if(heuristic !=4 and i==v.max_movements):
            max_movements = 0
            break
        
    if(heuristic != 4):
        if ganan_blancas_api.get(state, len(movs)) and player == 2:
            return 1000000 + (capture*10000) - (i**2)
        elif ganan_negras_api.get(state, len(movs)) and player == 1:
            return 1000000 + (capture*10000) - (i**2)
        elif max_movements == 0:
            return -100000 + (capture*10000) - (i**2)
        else:
            return -1000000 + (capture*10000) - (i**2)
    else:
        if ganan_blancas_api.get(state, len(movs)) and player == 2:
            return 1
        elif ganan_negras_api.get(state, len(movs)) and player == 1:
            return 1
        else:
            return -1