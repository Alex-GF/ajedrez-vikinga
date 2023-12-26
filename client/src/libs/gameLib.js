import gameAPI from "../api/gameAPI";

const gameLib = {

    doMovement: (oldCell, newCell, newToken, boardState, setBoardState, turnState, setTurnState, maxMovements, setMaxMovements) => {

        let movement = []

        let oldCellId = oldCell.getAttribute('id').split('-')[1];
        let newCellId = newCell.getAttribute('id').split('-')[1];
        let rowLength = boardState.length

        movement.push(Math.trunc(oldCellId/rowLength));
        movement.push(oldCellId%rowLength);
        movement.push(Math.trunc(newCellId/rowLength));
        movement.push(newCellId%rowLength);    

        let previousToken = oldCell.firstChild;
        let rect = newToken.getBoundingClientRect();
        let previousRect = previousToken.getBoundingClientRect();
        if(movement[0] !== movement[2]){
            previousToken.style.transform = 'translateY('+(rect.top-previousRect.top)+'px)';
        }else{
            previousToken.style.transform = 'translateX('+(rect.right-previousRect.right)+'px)';
        }
        
        setTimeout(()=>{
            gameAPI.doMovement(boardState, turnState, movement, maxMovements)
                    .then(response => {

                        updateElementClases();

                        setBoardState(response.board);
                        setTurnState(response.turn);
                        setMaxMovements(response.max_movements);
                    }).catch(error=>console.log(error));
        },1250);
    }

}

//---------------------- Funciones auxiliares --------------------------

function updateElementClases(){

    let possibleMovementCells = document.querySelectorAll(".possible-movement");
    let cellSelected = document.querySelector(".cell-selected");

    for(let cell of possibleMovementCells){
        cell.classList.remove("possible-movement");
    }

    if(cellSelected !== null) {
        cellSelected.classList.remove("cell-selected");
        cellSelected.classList.remove("cell-hover");
    }
}

export default gameLib;