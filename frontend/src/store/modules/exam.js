import exam from '../api/exam'

const examModule = {
  state: {
    instructorExamList: [],
    studentExamList: []
  },
  actions: {
    GET_INSTRUCTOR_EXAMS: ({commit}, id) => {
      return new Promise((resolve, reject) => {
        exam.getInstructorExam(id).then((response) => {
          if (response.status !== 250) {
            commit('LOAD_INSTRUCTOR_EXAMS', {instructorExamList: response.data})
          }
          resolve(response)
        }, (err) => {
          console.log(err)
          reject(err)
        })
      })
    },
    GET_STUDENT_EXAMS: ({commit}, id) => {
      return new Promise((resolve, reject) => {
        exam.getStudentExam(id).then((response) => {
          if (response.status !== 250) {
            commit('LOAD_STUDENT_EXAMS', {studentExamList: response.data})
          }
          resolve(response)
        }, (err) => {
          console.log(err)
          reject(err)
        })
      })
    }
  },
  mutations: {
    LOAD_INSTRUCTOR_EXAMS: (state, {instructorExamList}) => {
      state.instructorExamList = instructorExamList
    },
    LOAD_STUDENT_EXAMS: (state, {studentExamList}) => {
      state.studentExamList = studentExamList
    }
  },
  getters: {
    instructorExamList: state => {
      return state.instructorExamList
    },
    studentExamList: state => {
      return state.studentExamList
    }
  }
}

export default examModule
