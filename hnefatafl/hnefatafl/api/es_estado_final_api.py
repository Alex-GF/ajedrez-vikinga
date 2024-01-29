from . import ganan_negras_api, ganan_blancas_api

def get(state, movements_number, movements_left):

    return  ganan_negras_api.get(state, movements_number) or ganan_blancas_api.get(state, movements_number) or movements_left == 0
