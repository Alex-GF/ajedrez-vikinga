import { Modal } from 'react-bootstrap';

import {render} from "react-dom";

import {useState} from "react";

function customAlert(string) {

    const Alert = () => {

        const [show, setShow] = useState(true);

        const handleClose = () => {
            setShow(false);
        }

        return (
            <Modal
                size="md"
                aria-labelledby="contained-modal-title-vcenter"
                show={show}
                onHide={handleClose}
                centered
            >
                <Modal.Body>
                    <h3 style={{textAlign: 'center'}}>{string}</h3>
                </Modal.Body>
            </Modal>
        );
    }

    render(<Alert/>, document.getElementById('alert'));
}

export default customAlert;