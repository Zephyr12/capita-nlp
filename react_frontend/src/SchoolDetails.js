import React, { Component } from 'react'
import Search from './Search'
import { Switch, Route, Link } from 'react-router-dom'
import axios from 'axios'
import Posts from './Posts'

const API_URL = 'http://127.0.0.1:5000'

/*expect a state named suggested_schools*/
class SchoolDetails extends Component {
   constructor(){
        super();
        this.state = {
            school: {}
        }
    }

  componentWillMount() {
    axios.get(`${API_URL}/schools/${this.props.match.params.establishmentName}`) //the prefix/query/field should make the suggestions match the query (hopefully)
        .then((response) => {
            return response.data
        }).then((data) => {
            axios.get(data.posts).then(res => {
                return ({
                    ...data,
                    postsCount: res.data.count,
                    postsList: res.data.data
                });
          }).then(data => {
            axios.get(data.topics).then(res => {
                this.setState({
                    school: {
                        ...data,
                        topicsCount: res.data.count,
                        topicsList: res.data.data
                    }
                })
            })
          });
      }).catch(e => console.log(e))
  }

    componentDidUpdate(prevProps, prevState) {
        if(prevProps.match.params.establishmentName != this.props.match.params.establishmentName) {
            console.log('update here', this.props.match.params.establishmentName)
            axios.get(`${API_URL}/schools/${this.props.match.params.establishmentName}`) //the prefix/query/field should make the suggestions match the query (hopefully)
                .then((response) => {
                    return response.data
                }).then((data) => {
                    axios.get(data.posts).then(res => {
                        return ({
                            ...data,
                            postsCount: res.data.count,
                            postsList: res.data.data
                        })
                }).then(data => {
                    axios.get(data.topics).then(res => {
                        this.setState({
                            school: {
                                ...data,
                                topicsCount: res.data.count,
                                topicsList: res.data.data
                            }
                        })
                    })
                })
            }).catch(e => console.log(e))
        }
    }

    render(){
      return(
            <div>
                <h2>{this.state.school.establishment_name}</h2> 
                <h4>Phase of education: {this.state.school.phase_of_education}</h4>
                <h4>Postcode: {this.state.school.postcode}</h4>
                <h2>Topics</h2>
                {this.state.school.topicsCount > 0 ?
                    (<ul>
                        {this.state.school.topicsList.map(topic => <li key={'topic' + topic.topic_id}><Link to={`/schools/${this.props.match.params.establishmentName}/${this.props.match.params.topicPosts}`}>{topic.topic_description}</Link></li>)}
                    </ul>) :
                    <p>No topics available at this moment</p>
                }
            </div>
        )
    }
}

export default SchoolDetails