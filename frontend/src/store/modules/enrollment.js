import enrollment from '../api/enrollment'

const enrollmentModule = {
  state: {
    instructorEnrollments: [],
    studentEnrollments: []
  },
  actions: {
    GET_INSTRUCTOR_ENROLLMENTS: ({commit}, id) => {
      return new Promise((resolve, reject) => {
        enrollment.getEnrollments(id).then((response) => {
          if (response.status !== 250) {
            let arr = []
            for (let i = 0; i < response.data.length; i++) {
              if (response.data[i].role.id === 2) {
                arr.push(response.data[i])
              }
            }
            commit('SET_INSTRUCTOR_ENROLLMENTS', {instructorEnrollments: arr})
          }
          resolve(response)
        }, (err) => {
          console.log(err)
          reject(err)
        })
      })
    },
    GET_STUDENT_ENROLLMENTS: ({commit}, id) => {
      return new Promise((resolve, reject) => {
        enrollment.getEnrollments(id).then((response) => {
          if (response.status !== 250) {
            let arr = []
            for (let i = 0; i < response.data.length; i++) {
              if (response.data[i].role.id === 1) {
                arr.push(response.data[i])
              }
            }
            commit('SET_STUDENT_ENROLLMENTS', {studentEnrollments: arr})
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
    SET_INSTRUCTOR_ENROLLMENTS: (state, {instructorEnrollments}) => {
      state.instructorEnrollments = instructorEnrollments
    },
    SET_STUDENT_ENROLLMENTS: (state, {studentEnrollments}) => {
      state.studentEnrollments = studentEnrollments
    }
  },
  getters: {
    instructorEnrollments: state => {
      return state.instructorEnrollments
    },
    studentEnrollments: state => {
      return state.studentEnrollments
    }
  }
}

export default enrollmentModule
