import React, { Component } from 'react'
import Search from './Search'
import { Switch, Route, Link } from 'react-router-dom'
import axios from 'axios'
import SchoolDetails from './SchoolDetails'

const API_URL = 'http://127.0.0.1:5000'

/*expect a state named suggested_schools*/
class Posts extends Component {
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
                <h2>Posts</h2>
                {this.state.school.postsCount > 0 ?
                    (<ul>
                        {this.state.school.postsList.map(post => <li key={'post' + post.post_id}>{post.raw_text}</li>)}
                    </ul>) :
                    <p>No posts available at this moment</p>
                }
            </div>
        )
    }
}

export default Posts