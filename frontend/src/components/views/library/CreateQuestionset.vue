<template>
  <q-card flat>
    <q-card-title>
      Create Question Set
    </q-card-title>
    <q-card-separator/>
    <q-card-main>
      <div class="row">
        <q-field v-if="noExam" class="row col-xl-5 col-lg-5 col-md-5 col-sm-12 col-xs-12" :error="newQuestionsetExamError"
                 error-label="Must Select an Exam" helper="Associated Exam">
          <q-select filter float-label="Select an Exam" :options="examOptions"
                    v-model="newQuestionsetExam"></q-select>
        </q-field>
        <div class="col-1"></div>
        <q-field class="row col-xl-6 col-lg-6 col-md-6 col-sm-12 col-xs-12" :error="newQuestionsetExamNameError"
                 error-label="Must Select an Exam">
          <q-input float-label="New Question Set Name" v-model="newQuestionsetExamName"></q-input>
        </q-field>
        <div class="row col-xl-8 col-lg-8 col-md-8 col-sm-6 col-xs-6"></div>
        <div class="row col-xl-4 col-lg-4 col-md-4 col-sm-6 col-xs-6">
          <q-btn class="ml-auto mr-auto mt-2" color="primary" @click="saveQuestionset">Create</q-btn>
        </div>
      </div>
      <q-inner-loading :visible="spinner">
        <q-spinner-gears size="50px" color="primary"></q-spinner-gears>
      </q-inner-loading>
    </q-card-main>
  </q-card>
</template>

<script>
  import {Toast} from 'quasar'

  export default {
    name: 'CreateQuestionset',
    props: ['examOptions', 'createdQuestionset', 'noExam', 'examID'],
    components: {
    },
    data () {
      return {
        newQuestionsetExamNameError: false,
        newQuestionsetExamName: '',
        newQuestionsetExam: '',
        newQuestionsetExamError: false,
        spinner: false
      }
    },
    mounted () {
    },
    methods: {
      saveQuestionset () {
        if (this.newQuestionsetExamName === '') {
          this.newQuestionsetExamNameError = true
        } else if (this.newQuestionsetExam === '' && this.noExam) {
          this.newQuestionsetExamNameError = false
          this.newQuestionsetExamError = true
        } else {
          this.newQuestionsetExamNameError = false
          this.newQuestionsetExamError = false
          this.spinner = true
          let questionset = {name: this.newQuestionsetExamName, exam: this.newQuestionsetExam}
          if (!this.noExam) {
            questionset = {name: this.newQuestionsetExamName, exam: this.examID}
          }
          this.$http({
            method: 'post',
            url: '/api/createquestionset/',
            headers: {
              'X-CSRFToken': this.getCookie('csrftoken')
            },
            data: {
              questionset: questionset
            }
          }).then(response => {
            if (response.status === 250) {
              this.$router.error = response.data
              this.$router.push({path: '/error'})
            }
            this.createdQuestionset(response.data)
            this.spinner = false
            Toast.create.positive('Question Set Created')
          }).catch(error => {
            console.log(error)
          })
        }
      },
      getCookie (name) {
        let cookieValue = null
        if (document.cookie && document.cookie !== '') {
          let cookies = document.cookie.split(';')
          for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim()
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
              break
            }
          }
        }
        return cookieValue
      }
    }
  }
</script>
