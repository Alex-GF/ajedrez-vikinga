import PropTypes from "prop-types";
import {useRef, useEffect, useState} from "react";

import gameLib from "../libs/gameLib";

const Cell = ({id, situation, isThrone, isExit, boardState, setBoardState, movementsCell, turnState, 
                setTurnState, rowLength, setMovements, movements, previousClickedCell, 
                setPreviousClickedCell, maxMovements, setMaxMovements, isAITurn}) =>{

    let token = useRef();
    let cell = useRef();

    const[isValidCell, setIsValidCell] = useState();
    const[change, setChange] = useState(true);

    const showMovement = (e) => {
        let possibilitiesList = document.querySelectorAll(".possible-movement");
        let hover = document.querySelectorAll(".cell-selected");
        let isNotSameCell = true;
        if(isValidCell){
            for(let element of hover){
                element.classList.remove("cell-selected");
                if(element === cell.current) isNotSameCell = false;
            }
            for(let element of possibilitiesList){
                element.classList.remove("possible-movement");
            }
            if(isNotSameCell || (change && isNotSameCell)){
                if(movementsCell){
                    cell.current.classList.add("cell-selected");
                    for(let movement of movementsCell){
                        let c = document.getElementById("cell-" + (movement[2]*rowLength+movement[3]));
                        c.classList.add("possible-movement");
                    }
                }
                setMovements(movementsCell.length!==0?movementsCell.length.toString():"0");
            }else{
                setMovements(movements!==0?movements.toString():"0");
            }
        }

        if(cell.current.classList.contains("possible-movement")){
           gameLib.doMovement(previousClickedCell.current, cell.current, token.current, boardState, setBoardState, turnState, setTurnState, maxMovements, setMaxMovements);
        }

        setChange(!change);
        setPreviousClickedCell(cell)
    }

    const enterHover = () => {
        if(isValidCell){
            cell.current.classList.add("cell-hover");
        }
    }

    const exitHover = () => {
        if(isValidCell){
            cell.current.classList.remove("cell-hover");
        }
    }

    useEffect(() => {

        token.current.classList.remove("black-token", "white-token", "king-token", "no-token");
        token.current.style.transform = "none";

        switch(situation){
            case 1:
                token.current.classList.add("black-token");
                break;
            case 2:
                token.current.classList.add("white-token");
                break;
            case 3:
                token.current.classList.add("king-token");
                break;
            default:
                token.current.classList.add("no-token");
        }

        setIsValidCell(((token.current.classList.contains("black-token") && turnState === 1) || ((token.current.classList.contains("white-token") || token.current.classList.contains("king-token")) && turnState === 2)) && isAITurn===false);

    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [situation, turnState, isAITurn])

    return(
        <div className={"class-cell" + (isExit?" exit":isThrone?" throne":"")} id={"cell-" + id} ref={cell} onClick={showMovement} onMouseOver={enterHover} onMouseOut={exitHover}>
            <div className={"class-token" + (isExit?" exit-cross":"")} ref={token}></div>
        </div>
    );
} 

Cell.propTypes = {
    id: PropTypes.number,
    situation: PropTypes.number,
    isThrone: PropTypes.bool,
    isExit: PropTypes.bool,
    movementsCell: PropTypes.array,
    turnState: PropTypes.number,
    rowLength: PropTypes.number,
    setMovements: PropTypes.func,
    movements: PropTypes.number,
    maxMovements: PropTypes.number,
    setMaxMovements: PropTypes.func,
    isAITurn: PropTypes.bool
}

export default Cell;