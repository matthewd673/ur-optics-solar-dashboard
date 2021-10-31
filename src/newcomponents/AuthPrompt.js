import './AuthPrompt.css';
import { Button, Alert } from 'react-bootstrap';
import { useState, useEffect } from 'react';

const AuthButton = () => {
    return (
        <Button 
            onClick={() => { window.location.href = 'http://localhost:5000/box/get_auth_url'}}
            >
                Login with Box
            </Button>
    );
}

const AuthPrompt = () => {

    const [authStatus, setAuthStatus] = useState([]);

    useEffect(() => {
        checkHasAuth();
    }, []);

    const checkHasAuth = async () => { //check if the backend has an access_token
        const response = await fetch('/box/get_has_auth');
        const data = await response.text();
        setAuthStatus(data);
    }

    if (authStatus === 'false') { //no access token, so prompt for sign in
        return (
            <>
                <Alert className="d-flex align-items-center justify-content-between" variant='primary'>
                    <p style={{marginBottom: 0}}>You must log in with your Box account to view and download sensor data.</p>
                    <div><AuthButton /></div>
                </Alert>
            </>
        );
    }
    else { //auth token is already stored, no need for a new one
        return <></>
    }
}

export { AuthPrompt, AuthButton };