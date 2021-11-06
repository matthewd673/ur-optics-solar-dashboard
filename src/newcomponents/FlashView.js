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
    const [flashes, setFlashes] = useState([]);

    useEffect(() => {
        const getFlashes = async () => {
            const response = await fetch('/get_flashes');
            const data = await response.json();
    
            if (data.flashes.length !== 0) { //skip if no flashes
                setFlashes(data.flashes.reverse());
            }
        }

        const interval = setInterval(() => {
            getFlashes();
        }, 5000);
        return () => clearInterval(interval);
    }, []);

    return (
        <>
            <div className="flash-view-wrapper">
                {flashes.map((message, i) =>
                    <FlashBubble
                        key={i}
                        text={message['text']}
                        category={message['category']}
                        />
                )}
            </div>
        </>
    );
}

export default FlashView;