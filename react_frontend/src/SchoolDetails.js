import React, { Component } from 'react'
import Search from './Search'
import { Switch, Route, Link } from 'react-router-dom'
import axios from 'axios'
import './Search.css'

const API_URL = 'http://127.0.0.1:5000'

/*expect a state named suggested_schools*/
class SchoolDetails extends Component {
   constructor(){
        super();
        this.state = {
            school: {},
            filteredPosts: [],
        }
        this.filterByTopic = this.filterByTopic.bind(this)
        this.getSchoolTopics = this.getSchoolTopics.bind(this)
    }

    getSchoolTopics() {
        axios.get(`${API_URL}/schools/${this.props.match.params.establishmentName}`) //the prefix/query/field should make the suggestions match the query (hopefully)
        .then((response) => {
            return response.data
        }).then((data) => {
            axios.get(data.topics).then(res => {
                this.setState({
                    school: {
                        ...data,
                        topicsCount: res.data.count,
                        topicsList: res.data.data,
                    },
                    filteredPosts: [],
                })
          })
      }).catch(e => console.log(e))
    }
    componentWillMount() {
        this.getSchoolTopics()
    }

    componentDidUpdate(prevProps, prevState) {
        if(prevProps.match.params.establishmentName != this.props.match.params.establishmentName) {
            console.log('update here', this.props.match.params.establishmentName)
            this.getSchoolTopics()
        }
    }
    filterByTopic(topicId){
        axios.get(`${this.state.school.topics}${topicId}/posts/`).then(res => {
            this.setState({
                filteredPosts: res.data.data,
            })
        })
        
    }
    render(){
      return(
            <div>
                <h2 class="TextStyle">{this.state.school.establishment_name}</h2> 
                <h4 class="TextStyle">Phase of education: {this.state.school.phase_of_education}</h4>
                <h4 class="TextStyle">Postcode: {this.state.school.postcode}</h4>
                <h2 class="TextStyle">Topics</h2>
                {this.state.school.topicsCount > 0 ?
                    (<ul class="List">
                        {this.state.school.topicsList.map(topic => 
                            <div class="List" onClick={() => this.filterByTopic(topic.id)}><li class="List" key={'topic' + topic.topic_id}>{topic.topic_description}</li></div>
                        )}
                    </ul>) :
                    <p class="List">No topics available at this moment</p>
                }
                <h2 class="TextStyle">Posts</h2>
                {this.state.filteredPosts.length > 0 ?
                    (<ul class="List">
                        {this.state.filteredPosts.map(post => <li key={'post' + post.post_id}>{post.raw_text}</li>)}
                    </ul>) :
                    <p class="List">No posts on this topic</p>
                }
            </div>
        )
    }
}

export default SchoolDetails