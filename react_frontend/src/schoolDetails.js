import React from 'react'
import Search from './Search'
import { Switch, Route } from 'react-router-dom'




/*expect a state named suggested_schools*/
class SchoolDetails extends Component{
	constructor(){
		super();
		this.state = {
			school: {

			}
		}
		this.componentDidMount=this.componentDidMount.bind(this);
	}

	componentDidMount = () => {
		axios.get(`http://127.0.0.1:5000/schools/${this.props.match.params.establishmentName}`).then((response) => {
			console.log(response);
		this.setState({
			school: response.data
		})
		})
	}

	render(){
		console.log(this.state.school)
		return(<div>fmmmmmmmm</div>)
	}
}


export default SchoolDetails