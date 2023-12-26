import '../static/css/options.css';

const Options = () => {

    const isAIMode = (e) =>{
        if(e.target.value === "P2AI"){
            document.getElementById("AI2AI").style.height="0";
            document.getElementById("P2AI").style.height="325px";
            document.getElementById("main-options-box").style.minHeight="65vh";
        }else if(e.target.value === "AI2AI"){
            document.getElementById("P2AI").style.height="0";
            document.getElementById("AI2AI").style.height="500px";
            document.getElementById("main-options-box").style.minHeight="80vh";
        }else{
            document.getElementById("P2AI").style.height="0";
            document.getElementById("AI2AI").style.height="0";
            document.getElementById("main-options-box").style.minHeight="50vh";
        }

    }

    return(
        <section className="class-page-body">
            <form action="/board" id="carform">
                <div className="class-options-box" id="main-options-box">
                    
                        <h1>Ajedrez Vikingo</h1>

                        <h4 className="mt-5">Seleccione un tablero:</h4>
                        <select name="initial" className="class-initial-selector">
                            <option value="hnefatafl">Hnefatafl</option>
                            <option value="tablut">Tablut</option>
                            <option value="ard-ri">Ard Ri</option>
                            <option value="brandubh">Brandubh</option>
                            <option value="tawlbwrdd">Tawlbwrdd</option>
                            <option value="alea-evangelii">Alea Evangelii</option>
                        </select>

                        <h4>Seleccione un modo de juego:</h4>
                        <select id="select-mode" name="mode" className="class-initial-selector" onChange={isAIMode}>
                            <option value="P2P">Jugador vs jugador</option>
                            <option value="P2AI">Jugador vs IA</option>
                            <option value="AI2AI">IA vs IA</option>
                        </select>

                        <h4>Número máximo de movimientos para la partida:</h4>
                        <input style={{width: "80%"}} type="number" id="maxMovements" name="maxMovements" min="30" placeholder="Movimientos máximos" required/>

                        <div id="P2AI" className="class-options-elements mt-3 ml-3 mr-3">
                            <h4>Seleccione un equipo:</h4>
                            <select name="team" className="class-initial-selector">
                                <option value="black">Fichas negras</option>
                                <option value="white">Fichas blancas</option>
                            </select>
                            <h4>Seleccione una heurística:</h4>
                            <select name="heuristic" className="class-initial-selector">
                                <option value="1">Heurística en capturas positivas, negativas, en estado final y tablas</option>
                                <option value="2">Heurística en capturas positivas, en estado final y tablas</option>
                                <option value="3">Heurística en estado final y tablas</option>
                                <option value="4">Sin heurística</option>
                            </select>
                            <h4>Tiempo que la IA va a tardar para cada movimiento:</h4>
                            <input style={{width: "80%"}} type="number" id="time" name="time" min="1" placeholder="Tiempo (en segundos)"/>
                            <h4 className="mt-3">{"CP (debe ser un valor positivo):"}</h4>
                            <input style={{width: "80%"}} type="number" id="cp1" name="cp" min="0" placeholder="CP (si se deja en blanco se usará el valor por defecto => 1/√2)"/>
                        </div>

                        <div id="AI2AI" className="class-options-elements mt-3 ml-3 mr-3">
                            <h4>Seleccione una heurística para la IA 1 (fichas negras):</h4>
                            <select name="heuristic1" className="class-initial-selector">
                                <option value="1">Heurística en capturas positivas, negativas, en estado final y tablas</option>
                                <option value="2">Heurística en capturas positivas, en estado final y tablas</option>
                                <option value="3">Heurística en estado final y tablas</option>
                                <option value="4">Sin heurística</option>
                            </select>
                            <h4>Tiempo que la IA 1 va a tardar para cada movimiento:</h4>
                            <input style={{width: "80%"}} type="number" id="time1" name="time1" min="1" placeholder="Tiempo para la primera IA (en segundos)"/>
                            <h4 className="mt-3">{"CP1 (debe ser un valor positivo):"}</h4>
                            <input style={{width: "80%"}} type="number" id="cp1" name="cp1" min="0" placeholder="CP1 (si se deja en blanco se usará el valor por defecto => 1/√2)"/>
                            <h4 className="mt-3">Seleccione una heurística para la IA 2 (fichas blancas):</h4>
                            <select name="heuristic2" className="class-initial-selector">
                                <option value="1">Heurística en capturas positivas, negativas, en estado final y tablas</option>
                                <option value="2">Heurística en capturas positivas, en estado final y tablas</option>
                                <option value="3">Heurística en estado final y tablas</option>
                                <option value="4">Sin heurística</option>
                            </select>
                            <h4>Tiempo que la IA 2 va a tardar para cada movimiento:</h4>
                            <input style={{width: "80%"}} type="number" id="time2" name="time2" min="1" placeholder="Tiempo para la segunda IA (en segundos)"/>
                            <h4 className="mt-3">{"CP2 (debe ser un valor positivo):"}</h4>
                            <input style={{width: "80%"}} type="number" id="cp2" name="cp2" min="0" placeholder="CP2 (si se deja en blanco se usará el valor por defecto => 1/√2)"/>
                        </div>

                        <button className="mt-5 class-options-button" type="submit">Jugar</button>

                </div>
            </form>
        </section>
    );
}

export default Options;