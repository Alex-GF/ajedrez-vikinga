import { useNavigate } from "react-router-dom";

const Error = () => {

    let navigate = useNavigate();

    return(
        <section className="class-page-body" style={{flexDirection:"column"}}>
            <h1 style={{zIndex: 10, fontSize: "75px", color: "white"}}>Oops... Esta URL no es de nuestra página</h1>
            <button style={{
            outline: 'none',
            border: 'none',
            borderRadius: '15px',
            padding: '10px',
            width: 'auto',
            height: 'auto'
            }} className="class-options-button" onClick={() => navigate("/")}><h2>Volver a la pantalla de inicio</h2></button>
        </section>

    );
} 

export default Error;