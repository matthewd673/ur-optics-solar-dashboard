import './FlashView.css';
import { Alert } from 'react-bootstrap';
import { useState, useEffect } from 'react';

const FlashBubble = (props) => {

    const [show, setShow] = useState(true);

    let variant = 'secondary';
    
    if (props.category === 'info') { variant = 'info' }
    if (props.category === 'error') { variant = 'danger' }
    if (props.category === 'success') { variant = 'success' }
    if (show) {
        return <Alert
            variant={variant}
            onClose={() => setShow(false)}
            dismissible>
                {props.text}
            </Alert>
    } else { return null; }
}

const FlashView = () => {
    const [flashMessages, setFlashMessages] = useState([]);

    useEffect(() => {
        getFlashMessages();
    }, []);

    const getFlashMessages = async () => {
        const response = await fetch('/get_flashes');
        const data = await response.json();

        setFlashMessages(data.flashes.reverse());
    }

    return (
        <>
            <div className="flash-view-wrapper">
                {flashMessages.map(message =>
                    <FlashBubble
                        key={message['text']}
                        text={message['text']}
                        category={message['category']}
                        />
                )}
            </div>
        </>
    );
}

export default FlashView;