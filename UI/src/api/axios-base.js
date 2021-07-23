/// Basic Configuration of Axios
import Vue from 'vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import store from '@/store' /// by default index.js leta haii...

const token = localStorage.getItem('access_token') || null

axios.defaults.baseURL=process.env.VUE_APP_API_URL
axios.defaults.headers.contentType='application/json'
console.log(process.env)
if(token)
axios.defaults.headers['HTTP_AUTHORIZATION'] = `Bearer ${token}`;


axios.interceptors.response.use(undefined, function (err) {
  // if error response status is 401, it means the request was invalid due to expired access token
  if (err.config && err.response && err.response.status === 401) {
    store.dispatch('auth/refreshToken') // attempt to obtain new access token by running 'refreshToken' action
      .then(access => {
        // if successful re-send the request to get the data from server
        axios.request({
          baseURL: process.env.VUE_APP_API_URL,
          method: 'get',
          headers: { Authorization: `Bearer ${access}` }, // the new access token is attached to the authorization header
          url: '/'
        }).then(response => {
          // if successfully received the data store it in store.state.APIData so that 'Downloads' component can grab the
          // data from it and display to the client.
          console.log('Success getting the Audios',response)
          // store.state.audio_data = response.data
        }).catch(err => {
          console.log('Got the new access token but error while trying to fetch data from the API using it')
          return Promise.reject(err)
        })
      })
      .catch(err => {
        return Promise.reject(err)
      })
  }
})

Vue.use(VueAxios, axios)
export default axios