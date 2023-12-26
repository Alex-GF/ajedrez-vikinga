import { useRef } from "react";
import { useNavigate } from "react-router-dom";
import customConfirm from "../functions/customConfirm";
import "../static/css/menu.css";

const Menu = () =>{

    let menuImg = useRef();
    let menu = useRef();
    let closeMenuImg = useRef();
    let navigate = useNavigate();

    const overMenu = () => {
        menuImg.current.src = '../images/menu-select.png';
    }

    const outMenu = () => {
        menuImg.current.src = '../images/menu.png';
    }

    const outCloseMenu = () => {
        closeMenuImg.current.src = "../images/close.png";
    }

    const overCloseMenu = () => {
        closeMenuImg.current.src = "../images/close-edited.png";
    }

    const openMenu = () => {
        menu.current.style.left = "0";
    }

    const closeMenu = () => {
        menu.current.style.left = "-30vw";
    }

    return(
        <>
            <div className="class-menu d-flex justify-content-center align-items-center">
                <img ref={menuImg} className="class-menu-img" title="Abrir el menú" src="../images/menu.png" alt="Imagen que indica abrir menú" onMouseOver={overMenu} onMouseOut={outMenu} onClick={openMenu} />
            </div>

            <div className="class-menu-div d-flex flex-column" ref={menu}>
                <img
                    className="class-close-menu"
                    src="../images/close.png"
                    ref={closeMenuImg}
                    onClick={closeMenu}
                    onMouseOver={overCloseMenu}
                    onMouseOut={outCloseMenu}
                    alt="Cruz para cerrar el menu"
                    title="Cerrar el menú"
                />
                <div className="class-menu-option d-flex justify-content-center align-items-center" title="El juego volverá a comenzar con la misma configuración" onClick={()=>customConfirm("¿Está seguro de que quiere volver a empezar? Su progreso se perderá.").then(c=>window.location.reload())}>
                    <strong>Volver a empezar</strong>
                </div>

                <div className="class-menu-option d-flex justify-content-center align-items-center" title="Exit to the initial page" onClick={()=>customConfirm("¿Está seguro de que quiere salir de la partida? Su progreso se perderá.").then(c=>navigate("/"))}>
                    <strong>Salir</strong>
                </div>
            </div>
        </>
    )
}

export default Menu;