<template>
  <div class="app">
    <div class="app-body">
      <main class="main">
        <div class="takeexam h-100">
          <div class="animated fadeIn takeexam" v-if="examQuestions">
            <q-toolbar inverted color="dark" class="bg-light">
              <q-toolbar-title>
                <div class="row">
                  <div class="col-lg-5 col-md-12">
                    Review Tools
                  </div>
                  <div class="col-lg-2 col-md-12">
                  </div>
                  <div class="col-lg-5 col-md-12"></div>
                </div>
              </q-toolbar-title>
              <q-btn icon="fa-list" color="primary" round push @click="$refs.allQuestions.open()">
                <q-tooltip anchor="center left" self="center right" :offset="[20, 0]">
                  View Questions
                </q-tooltip>
              </q-btn>
              <q-btn icon="fa-close" color="danger" round push @click="$refs.endReview.open()">
                <q-tooltip anchor="center left" self="center right" :offset="[20, 0]">
                  Stop Reviewing
                </q-tooltip>
              </q-btn>
            </q-toolbar>
            <q-carousel ref="examRef" arrows>
              <div class="centered" slot="slide" v-for="(question, index) in examQuestions" :key="index">
                <multiple-choice-question :review="review" v-if="question.question_type_id === 1"
                                          class="w-100 carousel-cell"
                                          :question="question" :ref="'question' + index"
                                          :index="index" :result="$route.params.id"
                                          :questionresponse="questionResponses[index]"
                ></multiple-choice-question>
                <multiple-response-question :review="review" v-if="question.question_type_id === 2"
                                            class="w-100 carousel-cell"
                                            :question="question" :ref="'question' + index"
                                            :index="index" :result="$route.params.id"
                                            :questionresponse="questionResponses[index]"
                ></multiple-response-question>
                <short-answer-question :review="review" v-if="question.question_type_id === 3"
                                       class="w-100 carousel-cell" :question="question"
                                       :ref="'question' + index"
                                       :index="index" :result="$route.params.id"
                                       :questionresponse="questionResponses[index]"
                ></short-answer-question>
                <essay-question :review="review" v-if="question.question_type_id === 4" class="w-100 carousel-cell"
                                :question="question"
                                :ref="'question' + index"
                                :index="index" :result="$route.params.id"
                                :questionresponse="questionResponses[index]"
                ></essay-question>
                <matching-question :review="review" v-if="question.question_type_id === 5" class="w-100 carousel-cell"
                                   :question="question"
                                   :ref="'question' + index"
                                   :index="index" :result="$route.params.id"
                                   :questionresponse="questionResponses[index]"
                ></matching-question>
                <file-upload-question :review="review" v-if="question.question_type_id === 7"
                                      class="w-100 carousel-cell" :question="question"
                                      :ref="'question' + index"
                                      :index="index" :result="$route.params.id"
                                      :questionresponse="questionResponses[index]"
                ></file-upload-question>
                <true-false-question :review="review" v-if="question.question_type_id === 9" class="w-100 carousel-cell"
                                     :question="question"
                                     :ref="'question' + index"
                                     :index="index" :result="$route.params.id"
                                     :questionresponse="questionResponses[index]"
                ></true-false-question>
              </div>
            </q-carousel>
            <q-modal ref="endReview">
              <div class="m-3">
                <div>
                  <h4>All done?</h4>
                </div>
                <div>
                  Are you done reviewing?
                </div>
                <div class="float-right mt-3">
                  <q-btn push @click="$refs.endReview.close()" color="primary">Go Back</q-btn>
                  <q-btn push @click="endReview()" color="secondary">Stop Reviewing</q-btn>
                </div>
              </div>
            </q-modal>
            <q-modal ref="allQuestions">
              <div class="m-3">
                <q-list>
                  <q-list-header>Exam Questions</q-list-header>
                  <div class="row">
                    <q-item v-for="(question, index) in examQuestions" :key="index"
                            @click="$refs.examRef.goToSlide(index); $refs.allQuestions.close();"
                            class="col-md-4 col-sm-4">
                      <q-btn push class="m-auto">
                        <span v-if="questionsLoaded">
                          <q-item-side>
                            <i v-if="questionResponses[index].score === question.weight" class="fa fa-check"
                               aria-hidden="true"></i>
                            <i
                              v-else-if="questionResponses[index].score < question.weight && questionResponses[index].score !== 0"
                              class="fa fa-warning" aria-hidden="true"></i>
                            <i v-else-if="!questionResponses[index].graded" class="fa fa-edit" aria-hidden="true"></i>
                            <i class="fa fa-times" aria-hidden="true" v-else></i>
                          </q-item-side>
                        </span>
                        <q-item-side v-else></q-item-side>
                        <q-item-main>{{ index + 1 }}</q-item-main>
                        <q-item-side></q-item-side>
                      </q-btn>
                    </q-item>
                  </div>
                </q-list>
              </div>
            </q-modal>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script>
  import MultipleChoiceQuestion from '../takeexam/MultipleChoiceQuestion'
  import MultipleResponseQuestion from '../takeexam/MultipleResponseQuestion'
  import ShortAnswerQuestion from '../takeexam/ShortAnswerQuestion'
  import EssayQuestion from '../takeexam/EssayQuestion'
  import MatchingQuestion from '../takeexam/MatchingQuestion'
  import FileUploadQuestion from '../takeexam/FileUploadQuestion.vue'
  import TrueFalseQuestion from '../takeexam/TrueFalseQuestion.vue'
  import {
    Loading
  } from 'quasar'

  export default {
    name: 'takeexam',
    props: ['result'],
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
        examQuestions: false,
        prevQuestion: 0,
        firstSwitch: true,
        review: true,
        questionsLoaded: false,
        questionResponses: false
      }
    },
    mounted () {
      this.$http({
        method: 'post',
        url: '/api/isloggedin/'
      }).then(response => {
        if (response.status === 200) {
          this.checked = true
        }
        if (response.status === 250) {
          this.$router.push({path: '/login'})
        }
        // Get Exam
        this.$http({
          method: 'get',
          url: '/api/result/' + this.$route.params.id + '/getexam/'
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
        this.$http({
          method: 'get',
          url: '/api/result/' + this.$route.params.id + '/questionresponse/'
        }).then(response => {
          if (response.status === 250) {
            this.$router.error = response.data
            this.$router.push({path: '/error'})
          }
          this.questionResponses = response.data
          // Get Exam Questions
          this.$http({
            method: 'get',
            url: '/api/result/' + this.$route.params.id + '/questions/'
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
        }).catch(error => {
          console.log(error)
        })
        this.questionsTimer = window.setInterval(() => this.checkQuestions(), 1000)
      }).catch(error => {
        console.log(error)
      })
      Loading.show({
        message: 'Retrieving Results'
      })
    },
    methods: {
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
      },
      endReview () {
        this.$router.push({path: '/'})
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
