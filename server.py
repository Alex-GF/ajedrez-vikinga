from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import random

from backend.api import obtiene_estado_inicial_api, obtiene_movimientos_api, ganan_negras_api, ganan_blancas_api, aplica_movimiento_api, busca_solucion_api

API_VERSION = '/v1'
BASE_URL = '/api' + API_VERSION

app = Flask(__name__, static_folder='client/build', static_url_path='')
CORS(app)

@app.route(BASE_URL + '/game/obtener-estado-inicial', methods=['GET'])
def obtiene_estado_inicial():

    initial = request.args.get('initial')

    state = obtiene_estado_inicial_api.get(initial)

    return jsonify({"board": state[0], "turn": state[1]})

#------------------------------------------------------------------

@app.route(BASE_URL + '/game/obtener-movimientos', methods=['POST'])
def obtiene_movimientos():

    current_state = (request.json['board'], request.json['turn'])

    return jsonify({"movements": obtiene_movimientos_api.get(current_state)})

#------------------------------------------------------------------

@app.route(BASE_URL + '/game/aplica-movimiento', methods=['POST'])
def aplica_movimiento():

    current_state = (request.json['board'], request.json['turn'])
    movement = request.json['movement']
    max_movements = request.json['max_movements']

    if max_movements < 1:
        return jsonify({"board": current_state[0], "turn": current_state[1], "max_movements": 0}) 
    
    movements = obtiene_movimientos_api.get(current_state)
    movement_tuple = (movement[0], movement[1], movement[2], movement[3])
    
    if movement_tuple not in movements:
        new_movement_tuple = random.choice(movements)
        row, col, new_row, new_col = new_movement_tuple
        movement = [row, col, new_row, new_col]

    state = aplica_movimiento_api.get(current_state, movement, max_movements)

    return jsonify({"board": state[0], "turn": state[1], "max_movements": state[2]})

#------------------------------------------------------------------

@app.route(BASE_URL + '/game/es-estado-final', methods=['POST'])
def es_estado_final():

    current_state = (request.json['board'], request.json['turn'])
    max_movements = request.json['max_movements']
    movements_number = len(obtiene_movimientos_api.get(current_state))
    
    blacks_win = ganan_negras_api.get(current_state, movements_number)
    whites_win = ganan_blancas_api.get(current_state, movements_number)
    is_draw = max_movements==0
    
    if not (blacks_win or whites_win or is_draw):
        return jsonify({"black": False, "white": False, "draw": False})
    elif whites_win:
        return jsonify({"black": False, "white": True, "draw": False})
    elif is_draw:
        return jsonify({"black": False, "white": False, "draw": True})  
    else:
        return jsonify({"black": True, "white": False, "draw": False})

#------------------------------------------------------------------

@app.route(BASE_URL + '/game/busca-solucion', methods=['POST'])
def busca_solucion():

    current_state = (request.json['board'], request.json['turn'])
    time = request.json['time']
    max_movements = request.json['max_movements']
    cp = request.json['cp']
    heuristic = request.json['heuristic']

    next_movement, next_state, searched_nodes = busca_solucion_api.get(current_state, time, max_movements, cp, heuristic )
    movements_list = obtiene_movimientos_api.get(next_state)

    return jsonify({"board": next_state[0], "turn": next_state[1], "max_movements": next_state[2], 
                    "movements": movements_list, "next_movement": next_movement, "searched_nodes": searched_nodes})

#------------------------------------------------------------------

@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

@app.errorhandler(404)
def not_found(e):
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True, use_debugger=False, use_reloader=False, port=8080)