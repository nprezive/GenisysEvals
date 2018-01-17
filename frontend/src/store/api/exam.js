import axios from 'axios'

export default {
  getInstructorExam (id) {
    return axios.get('api/learningcontext/' + id + '/instructorExams/')
  },
  getStudentExam (id) {
    return axios.get('api/learningcontext/' + id + '/studentExams/')
  }
}
