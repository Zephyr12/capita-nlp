import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import Search from './Search';
import Suggestions from './Suggestions';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import SchoolDetails from './SchoolDetails';


export default class App extends React.Component {
  render() {
    return (
        <Router>
        <div>
        <Route path='/' component = {Search}/>
        <Route path='/schools/:establishmentName' component ={SchoolDetails}/>
        </div>
        </Router>
    );
  }
}