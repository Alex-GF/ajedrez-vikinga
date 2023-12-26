import Cell from "./cell";

import { useEffect, useRef, useState } from "react";
import PropTypes from "prop-types";

const Board = ({boardState, setBoardState, movementsList, turnState, setTurnState, setMovements, maxMovements, setMaxMovements, isAITurn}) => {

    let board = useRef();

    let [previousClickedCell, setPreviousClickedCell] = useState();

    let rowLength = boardState.length;
    let rowMaxId = rowLength-1;
    let half = (rowMaxId/2);
    let movementsListLength = movementsList.length;

    useEffect(() => {

        board.current.style = `grid-template-columns: repeat(${rowLength}, 1fr);
                                grid-template-rows: repeat(${rowLength}, 1fr);`;
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])

    return(
        <div className="class-board" ref={board}>
            {
                boardState && movementsList &&
                (
                    boardState.map((row, rowId) => {
                        return(
                            row.map((cell, id) => {
                                let cellId = rowId*rowLength + id;
                                let isExit = (cellId === 0) || 
                                                (rowId===0 && id === rowMaxId) ||
                                                (rowId===rowMaxId && (id===0 || id===rowMaxId));
                                let isThrone = (rowId===half && id===half);

                                return(
                                    <Cell id={cellId} situation={cell} isExit={isExit} isThrone={isThrone} key={cellId} movementsCell={movementsList.filter(c => c[0]===rowId && c[1]===id)} 
                                    turnState={turnState} setTurnState={setTurnState} rowLength={rowLength} setMovements={setMovements} movements={movementsListLength} previousClickedCell={previousClickedCell}
                                    setPreviousClickedCell={setPreviousClickedCell} boardState={boardState} setBoardState={setBoardState} maxMovements={maxMovements} setMaxMovements={setMaxMovements}
                                    isAITurn={isAITurn}/>
                                );
                            })
                        );
                    })
                )
            }
        </div>
    );
}

Board.propTypes = {
    boardState: PropTypes.array,
    movementsList: PropTypes.array,
    turnState: PropTypes.number,
    setMovements: PropTypes.func,
    maxMovements: PropTypes.number,
    setMaxMovements: PropTypes.func,
    isAITurn: PropTypes.bool
}

export default Board;