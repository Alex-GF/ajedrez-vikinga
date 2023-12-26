import '../static/css/board.css'

import {useState, useEffect} from 'react';

import useQuery from "../hooks/useQuery";
import gameAPI from "../api/gameAPI";
import Board from "../components/board";
import State from '../components/state';
import Menu from '../components/menu';
import customAlert from '../functions/customAlert';

const BoardView = () => {

    const DEFAULT_TIME = 5;
    const MIN_TIME = 1;
    const DEFAULT_MAX_MOVEMENTS = 50;
    const MIN_MAX_MOVEMENTS = 30;
    const MIN_CP = 0;
    const DEFAULT_CP = 1/Math.sqrt(2);

    let [boardState, setBoardState] = useState();
    let [turnState, setTurnState] = useState();
    let [movementsList, setMovementsList] = useState();
    let [movements, setMovements] = useState();
    let [maxMovements, setMaxMovements] = useState(0);
    let [isDraw, setIsDraw] = useState(false);
    let [blacksWin, setBlacksWin] = useState(false);
    let [whitesWin, setWhitesWin] = useState(false);
    let [tokens, setTokens] = useState();
    let [initialTokens, setInitialTokens] = useState();
    let [isAITurn, setIsAITurn] = useState(false);
    let [searchedNodes, setSearchedNodes] = useState(0);
    let [blackSearchedNodes, setBlackSearchedNodes] = useState(0);
    let [whiteSearchedNodes, setWhiteSearchedNodes] = useState(0);
    let [AISearchedNodes, setAISearchedNodes] = useState(0);

    let query = useQuery();

    let initial = query.get("initial");
    let time = query.get("time");
    let mode = query.get("mode");
    let initialMaxMovements = query.get("maxMovements");
    let team = query.get("team");
    let time1 = query.get("time1");
    let time2 = query.get("time2");
    let cp = query.get("cp");
    let cp1 = query.get("cp1");
    let cp2 = query.get("cp2");
    let heuristic = query.get("heuristic");
    let heuristic1 = query.get("heuristic1");
    let heuristic2 = query.get("heuristic2");
    let tokenMap = {black:0, white:0};

    time = time>=MIN_TIME?time:DEFAULT_TIME;
    time1 = time1>=MIN_TIME?time1:DEFAULT_TIME;
    time2 = time2>=MIN_TIME?time2:DEFAULT_TIME;
    cp = cp>MIN_CP?cp:DEFAULT_CP;
    cp1 = cp1>MIN_CP?cp1:DEFAULT_CP;
    cp2 = cp2>MIN_CP?cp2:DEFAULT_CP;
    initialMaxMovements = initialMaxMovements>=MIN_MAX_MOVEMENTS?Math.round(initialMaxMovements):DEFAULT_MAX_MOVEMENTS;

    function doAnimation(movement) {
        let oldCell = document.getElementById("cell-"+(movement[0]*boardState.length + movement[1]));
        let newCell = document.getElementById("cell-"+(movement[2]*boardState.length + movement[3]));
        let previousToken = oldCell.firstChild;
        let newToken = newCell.firstChild;
        let rect = newToken.getBoundingClientRect();
        let previousRect = previousToken.getBoundingClientRect();
        if(movement[0] !== movement[2]){
            previousToken.style.transform = 'translateY('+(rect.top-previousRect.top)+'px)';
        }else{
            previousToken.style.transform = 'translateX('+(rect.right-previousRect.right)+'px)';
        }
    }

    useEffect(() => {
        gameAPI.getInitialState(initial)
                .then(response =>{
                    console.log(response);
                    setBoardState(response.board);
                    setTurnState(response.turn);

                    gameAPI.getMovements(response.board, response.turn)
                    .then(response =>{
                        setMovementsList(response.movements);
                        setMovements(response.movements.length);
                    })

                    let rowLength = response.board.length;
                    for(let i=0; i<rowLength; i++) {
                        for(let j=0; j<rowLength; j++) {
                            let cell = response.board[i][j];
                            if(cell===1) tokenMap.black += 1;
                            if(cell===2 || cell===3) tokenMap.white += 1;
                        }
                    }

                    setInitialTokens(tokenMap);
                    // eslint-disable-next-line react-hooks/exhaustive-deps
                    tokenMap = {black:0, white:0};
                })
                .catch(error=>console.log(error));
        setMaxMovements(initialMaxMovements);

    }, [initial]);

    useEffect(() => {
        if(mode === "P2AI"){
            let turn = team==="black"?1:2;
            if (boardState && turnState===turn){
                setIsAITurn(false);
                gameAPI.getMovements(boardState, turnState)
                .then(response =>{
                    setMovementsList(response.movements);
                    setMovements(response.movements.length);
                })
                .catch(error=>console.log(error));
            }else if(boardState && turnState!==turn){
                setIsAITurn(true);
                gameAPI.searchSolution(boardState, turnState, time, maxMovements, cp, heuristic)
                    .then(response => {
                        doAnimation(response.next_movement);
                        setTimeout(()=>{
                            setBoardState(response.board);
                            setTurnState(response.turn);
                            setMovementsList(response.movements);
                            setMovements(response.movements.length);
                            setMaxMovements(response.max_movements);
                            setSearchedNodes(response.searched_nodes);
                            setAISearchedNodes(AISearchedNodes+response.searched_nodes);
                        },1250);
                    }).catch(error=>console.log(error));
            }
        }else if(mode === "P2P"){
            if (boardState){
                setIsAITurn(false);
                gameAPI.getMovements(boardState, turnState)
                .then(response =>{
                    setMovementsList(response.movements);
                    setMovements(response.movements.length);
                })
                .catch(error=>console.log(error));
            }
        } else{
            if(boardState && turnState){
                setIsAITurn(true);
                if(turnState === 1){
                    gameAPI.searchSolution(boardState, turnState, time1, maxMovements, cp1, heuristic1)
                    .then(response => {
                        doAnimation(response.next_movement);
                        setTimeout(()=>{
                            setBoardState(response.board);
                            setTurnState(response.turn);
                            setMovementsList(response.movements);
                            setMovements(response.movements.length);
                            setMaxMovements(response.max_movements);
                            setSearchedNodes(response.searched_nodes);
                            setBlackSearchedNodes(blackSearchedNodes+response.searched_nodes);
                        },1250);
                    }).catch(error=>console.log(error));
                }else{
                    gameAPI.searchSolution(boardState, turnState, time2, maxMovements, cp2, heuristic2)
                    .then(response => {
                        doAnimation(response.next_movement);
                        setTimeout(()=>{
                            setBoardState(response.board);
                            setTurnState(response.turn);
                            setMovementsList(response.movements);
                            setMovements(response.movements.length);
                            setMaxMovements(response.max_movements);
                            setSearchedNodes(response.searched_nodes);
                            setWhiteSearchedNodes(whiteSearchedNodes+response.searched_nodes);
                        },1250);
                    }).catch(error=>console.log(error));
                }         
                
            }
        }
        
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [turnState]);

    useEffect(() => {
        if (boardState && turnState){
            let rowLength = boardState.length;
            for(let i=0; i<rowLength; i++) {
                for(let j=0; j<rowLength; j++) {
                    let cell = boardState[i][j];
                    if(cell===1) tokenMap.black += 1;
                    if(cell===2 || cell===3) tokenMap.white += 1;
                }
            }
            setTokens(tokenMap);

            gameAPI.isEndGame(boardState, turnState, maxMovements)
            .then(response =>{

                if(response.black){
                    setBlacksWin(true);
                    customAlert("El juego ha terminado. ¡Felicidades al equipo negro!");
                }else if(response.white){
                    setWhitesWin(true);
                    customAlert("El juego ha terminado. ¡Felicidades al equipo blanco!");
                }else if(response.draw){
                    setIsDraw(true);
                    customAlert("El juego ha terminado. ¡Felicidades, es un empate!");
                }
            })
            .catch(error=>console.log(error));
        }
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [boardState]);


    return(
        <section className="class-page-body">
            <Menu/>
            {
                boardState && movementsList &&
                (
                    <>
                        <Board boardState={boardState} setBoardState={setBoardState} movementsList={movementsList} turnState={turnState} setTurnState={setTurnState} setMovements={setMovements} maxMovements={maxMovements} 
                        setMaxMovements={setMaxMovements} isAITurn={isAITurn}/>
                    </>
                )
            }
            {
                movements &&
                (
                    <State movementsLeft={maxMovements} turnState={turnState} setTurnState={setTurnState} blacksWin={blacksWin} whitesWin={whitesWin} isDraw={isDraw} movements={movements} initialTokens={initialTokens} tokens={tokens} 
                    searchedNodes={searchedNodes} blackSearchedNodes={blackSearchedNodes} whiteSearchedNodes={whiteSearchedNodes} AISearchedNodes={AISearchedNodes} isAITurn={isAITurn}/>
                )
            }
        </section>
    );
}

export default BoardView;