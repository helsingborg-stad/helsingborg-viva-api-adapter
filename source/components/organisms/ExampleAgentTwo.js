import React, { Component } from 'react'

import ExampleAgent from './ExampleAgent';

import ChatBubble from '../atoms/ChatBubble';


export default class ExampleAgentTwo extends Component {
    componentDidMount() {
        const { chat } = this.props;

        chat.addMessages({
            Component: ChatBubble,
            componentProps: {
                content: 'Hello from agent 2!',
                modifiers: ['automated'],
            }
        });

        setTimeout(() => {
            chat.switchAgent(ExampleAgent);
        }, 1000);
    }

    render() {
        return null;
    }
}