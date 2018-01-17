<template>
  <div class="animated fadeIn takeexam">
    <q-toolbar inverted color="dark" class="bg-light">
      <q-toolbar-title>
        <div class="row">
          <div class="col-lg-5 col-md-12">
            Exam Tools
          </div>
          <div class="col-lg-2 col-md-12">
            <!--If there isn't a timeLimit-->
            <div v-if="timeLimit === 0">
              <div v-if="timer.hours > 0">
                Time Elapsed: {{ timer.hours }}
                <span v-if="timer.hours == 1">Hour</span>
                <span v-else>Hours</span>
                : {{ timer.minutes }}
                <span v-if="timer.minutes == 1">Minute</span>
                <span v-else>Minutes</span>
              </div>
              <div v-if="timer.hours == 0">
                <div v-if="timer.minutes > 0">
                  Time Elapsed: {{ timer.minutes }}
                  <span v-if="timer.minutes == 1">Minute</span>
                  <span v-else>Minutes</span>
                </div>
                <div v-if="timer.minutes == 0">
                  < 1 Minute
                </div>
              </div>
            </div>
            <!--If there is a time limit-->
            <div v-if="timeLimit !== 0">
              <div v-if="timeLimit - timer.hours * 60 - timer.minutes - 1 > 0">
                <span v-if="timeLimit - timer.hours * 60 - timer.minutes > 5">
                  Time Remaining: {{ timeLimit - timer.hours * 60 - timer.minutes }}
                </span>
                <span v-if="timeLimit - timer.hours * 60 - timer.minutes <= 5">
                  Time Remaining: {{ timeLimit - timer.hours * 60 - timer.minutes - 1 }}
                </span>
                <span v-if="timeLimit - timer.hours * 60 - timer.minutes - 1 > 1">Minutes</span>
                <span v-if="timeLimit - timer.hours * 60 - timer.minutes - 1 === 1">Minute</span>
                <span v-if="timeLimit - timer.hours * 60 - timer.minutes - 1 < 5">
                  {{ (timeLimit * 60 - timer.hours * 60 * 60 - timer.minutes * 60 - timer.seconds) % 60 }}
                <span
                  v-if="timeLimit * 60 - timer.hours * 60 * 60 - timer.minutes * 60 - timer.seconds > 1">Seconds</span>
                <span
                  v-if="timeLimit * 60 - timer.hours * 60 * 60 - timer.minutes * 60 - timer.seconds === 1">Second</span>
                </span>
              </div>
              <div v-if="timeLimit - timer.hours * 60 - timer.minutes - 1 === 0">
                Time Remaining: {{ timeLimit * 60 - timer.hours * 60 * 60 - timer.minutes * 60 - timer.seconds }}
                <span
                  v-if="timeLimit * 60 - timer.hours * 60 * 60 - timer.minutes * 60 - timer.seconds > 1">Seconds</span>
                <span
                  v-if="timeLimit * 60 - timer.hours * 60 * 60 - timer.minutes * 60 - timer.seconds === 1">Second</span>
              </div>
            </div>
          </div>
          <div class="col-lg-5 col-md-12"></div>
        </div>
      </q-toolbar-title>
      <q-btn icon="fa-list" color="primary" round push @click="$refs.allQuestions.open()">
        <q-tooltip anchor="center left" self="center right" :offset="[20, 0]">
          View Questions
        </q-tooltip>
      </q-btn>
      <q-btn icon="fa-close" color="danger" round push @click="$refs.endExam.open()">
        <q-tooltip anchor="center left" self="center right" :offset="[20, 0]">
          End Exam
        </q-tooltip>
      </q-btn>
    </q-toolbar>
    <q-carousel ref="examRef" arrows @slide="switchQuestion">
      <div class="centered" slot="slide" v-for="(question, index) in examQuestions" :key="index" v-if="examQuestions.length > 0">
        <multiple-choice-question :review="review" v-if="question.question_type_id === 1" class="w-100 carousel-cell"
                                  :question="question" :ref="'question' + index"
                                  :index="index" :result="result"></multiple-choice-question>
        <multiple-response-question :review="review" v-if="question.question_type_id === 2" class="w-100 carousel-cell"
                                    :question="question" :ref="'question' + index"
                                    :index="index" :result="result"></multiple-response-question>
        <short-answer-question :review="review" v-if="question.question_type_id === 3" class="w-100 carousel-cell" :question="question"
                               :ref="'question' + index"
                               :index="index" :result="result"></short-answer-question>
        <essay-question :review="review" v-if="question.question_type_id === 4" class="w-100 carousel-cell" :question="question"
                        :ref="'question' + index"
                        :index="index" :result="result"></essay-question>
        <matching-question :review="review" v-if="question.question_type_id === 5" class="w-100 carousel-cell" :question="question"
                           :ref="'question' + index"
                           :index="index" :result="result"></matching-question>
        <file-upload-question :review="review" v-if="question.question_type_id === 7" class="w-100 carousel-cell" :question="question"
                              :ref="'question' + index"
                              :index="index" :result="result"></file-upload-question>
        <true-false-question :review="review" v-if="question.question_type_id === 9" class="w-100 carousel-cell" :question="question"
                             :ref="'question' + index"
                             :index="index" :result="result"></true-false-question>
      </div>
      <div class="centered" slot="slide" v-if="examQuestions.length < 1">
        There are no questions to take on this exam.
      </div>
    </q-carousel>
    <q-modal ref="endExam">
      <div class="m-3" v-if="examQuestions.length > 0">
        <div>
          <h4>End Exam</h4>
        </div>
        <div>
          Are you sure that you want to end your exam?
        </div>
        <div class="float-right mt-3">
          <q-btn push @click="$refs.endExam.close()" color="primary">Go Back</q-btn>
          <q-btn push @click="endExam()" color="secondary">Submit Exam</q-btn>
        </div>
      </div>
      <div class="m-3" v-if="examQuestions.length < 1">
        <div>
          <h4>End Exam</h4>
        </div>
        <div>
          Are you sure that you want to end your exam?
        </div>
        <div class="float-right mt-3">
          <q-btn push @click="$refs.endExam.close()" color="primary">Go Back</q-btn>
          <q-btn push @click="endExam()" color="secondary">Submit Exam</q-btn>
        </div>
      </div>
    </q-modal>
    <q-modal ref="allQuestions">
      <div class="m-3">
        <q-list v-if="examQuestions.length > 0">
          <q-list-header>Exam Questions</q-list-header>
          <div class="row">
            <q-item v-for="(question, index) in examQuestions" :key="index" @click="$refs.examRef.goToSlide(index); $refs.allQuestions.close();" class="col-md-4 col-sm-4">
              <q-btn push>
                <span v-if="questionsLoaded">
                  <q-item-side><i v-if="$refs['question' + index][0].bookmarked" class="fa fa-bookmark" aria-hidden="true"></i></q-item-side>
                </span>
                <q-item-side v-else></q-item-side>
                <q-item-main>{{ index + 1 }}</q-item-main>
                <span v-if="questionsLoaded">
                  <q-item-side><i v-if="$refs['question' + index][0].answered" class="fa fa-check" aria-hidden="true"></i></q-item-side>
                </span>
                <q-item-side v-else></q-item-side>
              </q-btn>
            </q-item>
          </div>
        </q-list>
        <q-list v-if="examQuestions.length < 1">
          <q-item>There are no questions on this exam.</q-item>
        </q-list>
        <div class="row m-2">
          <div class="col-12">
            <q-btn color="primary" class="start-exam-btn pull-right" @click="$refs.allQuestions.close()">
              Done
            </q-btn>
          </div>
        </div>
      </div>
    </q-modal>
  </div>
</template>

<script>
  import MultipleChoiceQuestion from './MultipleChoiceQuestion'
  import MultipleResponseQuestion from './MultipleResponseQuestion'
  import ShortAnswerQuestion from './ShortAnswerQuestion'
  import EssayQuestion from './EssayQuestion'
  import MatchingQuestion from './MatchingQuestion'
  import FileUploadQuestion from './FileUploadQuestion.vue'
  import TrueFalseQuestion from './TrueFalseQuestion.vue'
  import {
    Loading
  } from 'quasar'

  export default {
    name: 'takeexam',
    props: ['result', 'timer', 'outOfTime', 'timeLimit', 'nullResult'],
    components: {
      MultipleChoiceQuestion,
      MultipleResponseQuestion,
      ShortAnswerQuestion,
      EssayQuestion,
      MatchingQuestion,
      FileUploadQuestion,
      TrueFalseQuestion
    },
    data () {
      return {
        exam: {},
        examQuestions: [],
        prevQuestion: 0,
        firstSwitch: true,
        keepTime: true,
        submitted: false,
        questionsLoaded: false,
        questionsTimer: 0,
        timerTimer: 0,
        review: false
      }
    },
    mounted () {
      if (this.result === null || this.result === undefined || this.result === '') {
        this.$router.push({path: '/takeexam/start/' + this.$route.params.id})
      } else {
        // Get Exam
        this.$http({
          method: 'get',
          url: '/api/exam/' + this.$route.params.id,
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          }
        }).then(response => {
          if (response.status === 250) {
            this.$router.error = response.data
            this.$router.push({path: '/error'})
          }
          this.exam = response.data
        }).catch(error => {
          console.log(error)
        })

        // Get Exam Questions
        Loading.show({
          message: 'Retrieving Exam Questions'
        })
        this.$http({
          method: 'get',
          url: '/api/exam/' + this.$route.params.id + '/questions/',
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          }
        }).then(response => {
          if (response.status === 250) {
            this.$router.error = response.data
            this.$router.push({path: '/error'})
          }
          Loading.hide()
          this.examQuestions = response.data
        }).catch(error => {
          console.log(error)
        })

        this.timerTimer = window.setInterval(() => this.secondPassed(), 1000)
        this.questionsTimer = window.setInterval(() => this.checkQuestions(), 1000)
      }
    },
    methods: {
      endExam () {
        this.submitResults()
        window.clearInterval(this.timerTimer)
        this.outOfTime()
      },
      submitResults () {
        Loading.show({
          message: 'Submitting Exam'
        })
        let exam = []
        for (let i = 0; i < this.examQuestions.length; i++) {
          exam.push({
            question_id: this.$refs['question' + i][0]._data.questionid,
            settings: {
              response: this.$refs['question' + i][0].response,
              bookmarked: this.$refs['question' + i][0].bookmarked
            },
            question_type_id: this.$refs['question' + i][0]._data.questiontype
          })
        }
        this.$http({
          method: 'post',
          url: '/api/result/' + this.result + '/exam/',
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          },
          data: {
            exam: exam
          }
        }).then(response => {
          if (response.status === 250) {
            this.$router.error = response.data
            this.$router.push({path: '/error'})
          }
          let result = this.result
          this.nullResult()
          this.$router.push({path: '/takeexam/end/' + result + '/'})
        }).catch(error => {
          console.log(error)
        })
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
      },
      switchQuestion (i, d) {
        if (this.examQuestions.length < 1) {
          return
        }
        if (this.firstSwitch) {
          this.firstSwitch = false
          return
        }
        let questionNum = 0
        if (d === 'previous') {
          if (this.prevQuestion === i) {
//            Did this to prevent Errors
          } else {
            questionNum = i + 1
            this.prevQuestion = i
          }
        }
        if (d === 'next') {
          if (this.prevQuestion === i) {
//            Did this to prevent Errors
            questionNum = i
          } else {
            questionNum = i - 1
            this.prevQuestion = i
          }
        }
        this.$http({
          method: 'post',
          url: '/api/result/' + this.result + '/question/',
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          },
          data: {
            question_id: this.$refs['question' + questionNum][0]._data.questionid,
            settings: {
              response: this.$refs['question' + questionNum][0].response,
              bookmarked: this.$refs['question' + questionNum][0].bookmarked
            },
            question_type_id: this.$refs['question' + questionNum][0]._data.questiontype
          }
        }).then(response => {
          if (response.status === 250) {
            this.$router.error = response.data
            this.$router.push({path: '/error'})
          }
        }).catch(error => {
          console.log(error)
        })
      },
      secondPassed () {
        if (this.keepTime) {
          this.timer.seconds++
          if (this.timer.seconds === 60) {
            this.timer.minutes++
            this.timer.seconds = 0
            if (this.timer.minutes === 60) {
              this.timer.hours++
              this.timer.minutes = 0
            }
          }
          if (this.timeLimit !== 0) {
            if ((this.timer.minutes + this.timer.hours * 60 >= this.timeLimit)) {
              this.keepTime = false
              if (!this.submitted) {
                this.submitted = true
                window.clearInterval(this.timerTimer)
                this.submitResults()
              }
              this.outOfTime()
            }
          }
        }
      },
      checkQuestions () {
        let isLoaded = true
        for (let i = 0; i < this.examQuestions.length; i++) {
          if (!this.$refs['question' + i]) {
            isLoaded = false
          }
        }
        if (this.examQuestions.length === 0) {
          isLoaded = false
        }
        if (isLoaded) {
          window.clearInterval(this.questionsTimer)
          this.questionsLoaded = true
        }
      }
    }
  }
</script>

<style lang="stylus">
  .q-carousel-left-button i
    height 100%
    width 100%
    border-radius 0
    opacity 0.2

  .q-carousel-right-button i
    height 100%
    width 100%
    border-radius 0
    opacity 0.2

  .takeexam
    height 100%

  .q-carousel
    height 100%

  .takeexam .q-toolbar
    box-shadow 0 0 2px rgba(0, 0, 0, .12), 0 2px 2px rgba(0, 0, 0, .2)
    position absolute !important
    z-index 1

</style>
