import '../App.css';

import 'react-pro-sidebar/dist/css/styles.css';

import SidebarLayout from '../newcomponents/SidebarLayout';
import { AuthButton } from '../newcomponents/AuthPrompt';
import FlashView from '../newcomponents/FlashView';

const Auth = () => {
    return (
        <>
        <SidebarLayout width={290}>
            <h1>Login</h1>
            <p>You must log in with your Box account in order to view and download sensor data.</p>
            <AuthButton></AuthButton>
            <FlashView />
        </SidebarLayout>
        </>
    )
}

export default Auth;