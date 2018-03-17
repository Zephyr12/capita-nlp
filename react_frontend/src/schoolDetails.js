import React from 'react'
import Search from './Search'
import { Switch, Route } from 'react-router-dom'




/*expect a state named suggested_schools*/
const SchoolDetails = (state) => {
	this.state = state;
	console.log(this.state)
	if (this.state)
	return <div> {this.state.establishment_name}</div>
	return <div></div>
}


export default SchoolDetails