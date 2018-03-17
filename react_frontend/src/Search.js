import React, { Component } from 'react';
import axios from 'axios';
import Suggestions from './Suggestions';
import Autosuggest from 'react-autosuggest';
import { Switch, Route } from 'react-router-dom';
import SchoolDetails from './schoolDetails';


/*change KEY and URL in order to make a request to the schools API endpoint*/

const API_URL = 'http://127.0.0.1:5000'



class Search extends Component {
  constructor(){
    super();
    this.state = {
      query: '',
      suggested_schools: {"count": 0, "data": []},
      data: [],
      error: false
    }

    this.getInfo=this.getInfo.bind(this);
    this.handleInputChange=this.handleInputChange.bind(this);
  }

  //axios example: axios.get('/user?ID=12345')Make a request for a user with a given ID
  getInfo () {

    axios.get(`${API_URL}/schools/?field=${this.state.query}&n=10`) //the prefix/query/field should make the suggestions match the query (hopefully)
      .then((response) => {
            console.log(response);
        this.setState({
          suggested_schools: response.data // API returns an object named api_name_object; axios returns an object named data
                             // =>api_name_object.data                             
        })
      })
   .catch(() => {
    console.log();
    this.setState({ error: true })
  })
  }


  clearSuggestions (){
    this.setState({
      query: '',
      suggested_schools: {"count": 0, "data": []},
      data: [],
      showHello: false,
      error: false
    });
  };

  /*changed it because it doesn't need to make an API call for every single onChange event,
  or when the input is cleared*/
  handleInputChange (){
    this.setState({
      query: this.search.value
    }, () => {
      if (this.state.query && this.state.query.length > 0) {
        this.getInfo()
      } else if (this.state.query.length === 0) {
        this.clearSuggestions()
      }
    })
  }


  render() {
    return (
      <form>
        <input
          placeholder="Search for..."
          ref={input => this.search = input}
          onChange={this.handleInputChange} />
        <Suggestions suggested_schools={this.state.suggested_schools} />
      </form>
      
      )
  }

}

export default Search