import React from 'react'
import Search from './Search'
import { Switch, Route, Link } from 'react-router-dom'
import SchoolDetails from './schoolDetails'


/*expect a state named suggested_schools*/
const Suggestions = (state) => {
  const options = state.suggested_schools.data.map(r =>
  	<p> <Link to={`${r.establishment_name}`}>{r.establishment_name}</Link></p>)
  return <ol>{options}</ol>
}


export default Suggestions