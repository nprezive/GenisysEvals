import axios from 'axios'

export default {
  getEnrollments () {
    return axios.get('/api/getenrollments/')
  }
}
