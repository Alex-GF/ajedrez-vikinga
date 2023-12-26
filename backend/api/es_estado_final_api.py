from . import ganan_negras_api, ganan_blancas_api

def get(state, movements_number, max_movements):

    return  ganan_negras_api.get(state, movements_number) or ganan_blancas_api.get(state, movements_number) or max_movements == 0
