import React, { Component } from 'react';
import { Switch, Route } from 'react-router-dom';
import Search from './Search';


export default class Dashboard extends React.Component {
    render() {
    return (
        <Search/>
    );
    }
}