<template>
  <q-card flat>
    <q-card-title>
      Create Question
    </q-card-title>
    <q-card-separator/>
    <q-card-main>
      <q-field :error="newQuestionsetError" error-label="Must Select a Question Set">
        <q-select float-label="Select a Question Set" :options="questionsetsOptions"
                  v-model="newQuestionset"></q-select>
      </q-field>
      <edit-question :questiontypes="questiontypes" :question="newquestion"></edit-question>
      <q-btn class="float-right" color="primary" :disabled="spinner" @click="saveQuestion(newquestion)">Create
      </q-btn>
      <q-inner-loading :visible="spinner">
        <q-spinner-gears size="50px" color="primary"></q-spinner-gears>
      </q-inner-loading>
    </q-card-main>
  </q-card>
</template>

<script>
  import {Toast} from 'quasar'
  import EditQuestion from './EditQuestion.vue'

  export default {
    name: 'CreateQuestionset',
    props: ['newquestion', 'createdQuestion', 'questiontypes', 'questionsetsOptions'],
    components: {
      EditQuestion
    },
    data () {
      return {
        newQuestionsetError: false,
        newQuestionset: '',
        spinner: false
      }
    },
    mounted () {
    },
    methods: {
      saveQuestion (question) {
        if (this.newQuestionset === '') {
          this.newQuestionsetError = true
        } else {
          this.newQuestionsetError = false
          this.spinner = true
          question['questionset'] = this.newQuestionset
          this.$http({
            method: 'post',
            url: '/api/createquestion/',
            headers: {
              'X-CSRFToken': this.getCookie('csrftoken')
            },
            data: {
              question: question
            }
          }).then(response => {
            if (response.status === 250) {
              this.$router.error = response.data
              this.$router.push({path: '/error'})
            }
            this.createdQuestion(response.data, this.newQuestionset)
            this.spinner = false
            Toast.create.positive('Question Created')
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
