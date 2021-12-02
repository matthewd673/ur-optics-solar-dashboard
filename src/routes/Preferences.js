import '../App.css';

import 'react-pro-sidebar/dist/css/styles.css';

import SidebarLayout from '../newcomponents/SidebarLayout';
import { useEffect } from 'react';

import Toast from '../newcomponents/Toast';
import { Form, Button } from 'react-bootstrap';

const Preferences = () => {
    return (
        <>
        <SidebarLayout width={290}>
            <h1>Preferences</h1>
            <Form>
                <Form.Check type="checkbox" label="Remember Data Selection" />
                <Form.Check type="checkbox" label="Cache some data points to improve load times" />
                <Button variant="primary" type="submit">
                    Save Preferences
                </Button>
            </Form>
            <Toast />
        </SidebarLayout>
        </>
    )
}

export default Preferences;