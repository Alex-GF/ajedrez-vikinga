import { Modal } from 'react-bootstrap';

import {render} from "react-dom";

import {useState} from "react";

import "../static/css/confirm.css";

function customConfirm(string) {

    return new Promise(function(resolve, reject) {
        const Confirm = () => {

            const [show, setShow] = useState(true);
    
            const handleClose = () => {
                setShow(false);
            }
    
            const confirmClick = () => {
                handleClose();
                resolve();
            }
    
            const denyClick = () => {
                handleClose();
                reject();
            }
    
            return (
                <Modal
                    size="md"
                    aria-labelledby="contained-modal-title-vcenter"
                    show={show}
                    centered
                >
                    <Modal.Body>
                        <h3 className="class-confirm-text">{string}</h3>
                        <div className="class-buttons-line d-flex justify-content-between">
                            <div className="class-confirm-btn" onClick={confirmClick}>Aceptar</div>
                            <div className="class-confirm-btn" onClick={denyClick}>Cancelar</div>
                        </div>
                    </Modal.Body>
                </Modal>
            );
        }
    
        render(<Confirm/>, document.getElementById('alert'));
    })
}

export default customConfirm;