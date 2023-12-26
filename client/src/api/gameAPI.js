import axios from "axios";

const BASE_URL = process.env.REACT_APP_API_BASE_URL;

const gameAPI = {

    getInitialState: function(initial){
        return new Promise((resolve, reject) => {
            axios.get(BASE_URL + `/api/v1/game/obtener-estado-inicial?initial=${initial}`)
            .then(response => resolve(response.data))
            .catch(error => reject(error));
        })
    }, 

    getMovements: function(boardState, turnState){
        return new Promise((resolve, reject) => {
            axios({
                method: 'POST',
                url: BASE_URL + `/api/v1/game/obtener-movimientos`,
                data: {
                    board: boardState,
                    turn: turnState
                },
                crossOrigin: true
            })
            .then(response => resolve(response.data))
            .catch(error => reject(error));
        })
    },

    doMovement: function(boardState, turnState, movement, maxMovements){
        return new Promise((resolve, reject) => {
            axios({
                method: 'POST',
                url: BASE_URL + `/api/v1/game/aplica-movimiento`,
                data: {
                    board: boardState,
                    turn: turnState,
                    movement: movement,
                    max_movements: parseInt(maxMovements)
                },
                crossOrigin: true
            })
            .then(response => resolve(response.data))
            .catch(error => reject(error));
        })
    },

    isEndGame: function(boardState, turnState, maxMovements){
        return new Promise((resolve, reject) => {
            axios({
                method: 'POST',
                url: BASE_URL + `/api/v1/game/es-estado-final`,
                data: {
                    board: boardState,
                    turn: turnState,
                    max_movements: parseInt(maxMovements)
                },
                crossOrigin: true
            })
            .then(response => resolve(response.data))
            .catch(error => reject(error));
        })
    },

    searchSolution: function(boardState, turnState, time, maxMovements, cp, heuristic){
        return new Promise((resolve, reject) => {
            axios({
                method: 'POST',
                url: BASE_URL + `/api/v1/game/busca-solucion`,
                data: {
                    board: boardState,
                    turn: turnState,
                    time: parseInt(time),
                    max_movements: parseInt(maxMovements),
                    cp: parseFloat(cp),
                    heuristic: parseInt(heuristic)
                },
                crossOrigin: true
            })
            .then(response => resolve(response.data))
            .catch(error => reject(error));
        })
    },

}

export default gameAPI;