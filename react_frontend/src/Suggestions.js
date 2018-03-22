import React from 'react'
import Search from './Search'
import { Switch, Route, Link } from 'react-router-dom'
import SchoolDetails from './SchoolDetails'
import './Search.css'

/*expect a state named suggested_schools*/
const Suggestions = (state) => {
  const options = state.suggested_schools.data.map(r =>
		<p> <Link to={`/schools/${r.establishment_name}`}>{r.establishment_name}</Link></p>)
  return <ol class="TextStyle">{options}</ol>
}


export default Suggestions