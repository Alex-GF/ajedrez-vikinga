import PropTypes from "prop-types";
import useQuery from "../hooks/useQuery";

import {useEffect, useState} from "react";

const State = ({movements, turnState, setTurnState, blacksWin, whitesWin, isDraw, movementsLeft, tokens, initialTokens, searchedNodes, blackSearchedNodes, whiteSearchedNodes, AISearchedNodes, isAITurn}) => {

    // eslint-disable-next-line
    const[time, setTime] = useState(new Date().getTime());
    const[newTime, setNewTime] = useState();

    let query = useQuery();
    let mode = query.get("mode");

    function getPrettyTime(time){
        let miliTime = time/1000;
        if(miliTime>=60){
            if(miliTime>3600){
                return Math.trunc(miliTime/3600) + " hora" + (Math.trunc(miliTime/3600)!==1?"s ":" ") + Math.trunc((miliTime/3600%1)*100) + " minuto" + (Math.trunc((miliTime/3600%1)*60)!==1?"s ":" ") + Math.trunc((((miliTime/3600%1)*60)%1)*60) + " segundo" + (Math.trunc((((miliTime/3600%1)*60)%1)*60)!==1?"s ":" ") + (miliTime%1).toFixed(3)*1000 + " milisegundos";
            }else{
                return Math.trunc(miliTime/60) + " minuto" + (Math.trunc(miliTime/60)!==1?"s ":" ") + Math.trunc((miliTime/60%1)*60) + " segundo" + (Math.trunc((miliTime/60%1)*60)!==1?"s ":" ") + (miliTime%1).toFixed(3)*1000 + " milisegundos";
            }
        }else{
            return Math.trunc(miliTime) + " segundo" + (Math.trunc(miliTime)!==1?"s ":" ") + (miliTime%1).toFixed(3)*1000 + " milisegundos";
        }
    }

    useEffect(() => {

        if(blacksWin || whitesWin || isDraw){
            setTurnState(0);
            setNewTime(new Date().getTime()-time);
        }

    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [blacksWin, whitesWin, isDraw])

    return(
        movements && initialTokens && (
            <>
                <div className="d-flex flex-column ml-5 class-options-box">
                    <h1 style={{fontSize: "50px"}} className="mt-5">Información de la partida</h1>
                    <div className="d-flex justify-content-center align-items-center flex-column mt-5 ml-3 mr-3 mb-5">
                        {
                            blacksWin || whitesWin ?
                            (
                                <>
                                    <h3>Ganan {blacksWin&&"negras"}{whitesWin&&"blancas"}</h3>
                                    <h3>Quedaban {movementsLeft} movimientos para llegar a tablas</h3>
                                    <h3>La partida ha durado {getPrettyTime(newTime)}</h3>
                                    <h3>Fichas capturadas (negras): {initialTokens.black-tokens.black}</h3>
                                    <h3>Fichas restantes (negras): {tokens.black}</h3>
                                    <h3>Fichas capturadas (blancas): {initialTokens.white-tokens.white}</h3>
                                    <h3>Fichas restantes (blancas): {tokens.white}</h3>
                                    <h3>{(mode==="P2AI" && !isAITurn) || mode==="AI2AI"?"En el turno anterior se han explorado " + searchedNodes + " nodos del árbol":""}</h3>
                                    <h3>{mode==="AI2AI"?"En total, la IA 1 (equipo negro), ha explorado " + blackSearchedNodes + " nodos del árbol durante toda la partida":""}</h3>
                                    <h3>{mode==="AI2AI"?"En total, la IA 2 (equipo blanco), ha explorado " + whiteSearchedNodes + " nodos del árbol durante toda la partida":""}</h3>
                                    <h3>{mode==="P2AI"?"En total, la IA ha explorado " + AISearchedNodes + " nodos del árbol durante toda la partida":""}</h3>
                                </>
                            )
                            :
                            isDraw ?
                            (
                                <>
                                    <h3>Es un empate</h3>
                                    <h3>Quedaban {movementsLeft} movimientos para llegar a tablas</h3>
                                    <h3>La partida ha durado {getPrettyTime(newTime)} segundos</h3>
                                    <h3>Fichas capturadas (negras): {initialTokens.black-tokens.black}</h3>
                                    <h3>Fichas restantes (negras): {tokens.black}</h3>
                                    <h3>Fichas capturadas (blancas): {initialTokens.white-tokens.white}</h3>
                                    <h3>Fichas restantes (blancas): {tokens.white}</h3>
                                    <h3>{(mode==="P2AI" && !isAITurn) || mode==="AI2AI"?"En el turno anterior se han explorado " + searchedNodes + " nodos del árbol":""}</h3>
                                    <h3>{mode==="AI2AI"?"En total, la IA 1 (equipo negro), ha explorado " + blackSearchedNodes + " nodos del árbol durante toda la partida":""}</h3>
                                    <h3>{mode==="AI2AI"?"En total, la IA 2 (equipo blanco), ha explorado " + whiteSearchedNodes + " nodos del árbol durante toda la partida":""}</h3>
                                    <h3>{mode==="P2AI"?"En total, la IA ha explorado " + AISearchedNodes + " nodos del árbol durante toda la partida":""}</h3>
                                </>
                            )
                            :
                            (
                                <>
                                    <h2>Juegan {turnState===1?"negras":"blancas"}</h2>
                                    <h2>Posibles movimientos: {movements}</h2>
                                    <h2>Quedan {movementsLeft} movimientos</h2>
                                    <h2>Fichas capturadas ({turnState===1?"blancas":"negras"}): {initialTokens[turnState===1?"white":"black"]-tokens[turnState===1?"white":"black"]}</h2>
                                    <h2>Fichas restantes ({turnState===1?"negras":"blancas"}): {tokens[turnState===1?"black":"white"]}</h2>
                                    <h2>{(mode==="P2AI" && !isAITurn) || mode==="AI2AI"?"En el turno anterior se han explorado " + searchedNodes + " nodos del árbol":""}</h2>
                                </>
                            )
                        }
                    </div>
                </div>
            </>
        )
    );
}

State.propTypes = {
    turnState: PropTypes.number,
    movements: PropTypes.number,
    setTurnState: PropTypes.func,
    blacksWin: PropTypes.bool,
    white: PropTypes.bool,
    isDraw: PropTypes.bool,
    movementsLeft: PropTypes.number,
    tokens: PropTypes.object,
    initialTokens: PropTypes.object,
    searchedNodes: PropTypes.number,
    blackSearchedNodes: PropTypes.number,
    whiteSearchedNodes: PropTypes.number,
    AISearchedNodes: PropTypes.number,
    isAITurn: PropTypes.bool
}

export default State;