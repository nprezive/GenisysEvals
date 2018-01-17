<template>
  <div v-if="question">
    <div v-if="question.question_type_id === 1">
      <multiple-choice-question :typeChange="typeChange" :question="question" :questiontypes="questiontypes"></multiple-choice-question>
    </div>
    <div v-if="question.question_type_id === 2">
      <multiple-response-question :typeChange="typeChange" :question="question" :questiontypes="questiontypes"></multiple-response-question>
    </div>
    <div v-if="question.question_type_id === 3">
      <short-answer-question :typeChange="typeChange" :question="question" :questiontypes="questiontypes"></short-answer-question>
    </div>
    <div v-if="question.question_type_id === 4">
      <essay-question :typeChange="typeChange" :question="question" :questiontypes="questiontypes"></essay-question>
    </div>
    <div v-if="question.question_type_id === 5">
      <matching-question :typeChange="typeChange" :question="question" :questiontypes="questiontypes"></matching-question>
    </div>
    <div v-if="question.question_type_id === 7">
      <file-upload-question :typeChange="typeChange" :question="question" :questiontypes="questiontypes"></file-upload-question>
    </div>
    <div v-if="question.question_type_id === 9">
      <true-false-question :typeChange="typeChange" :question="question" :questiontypes="questiontypes"></true-false-question>
    </div>
  </div>
</template>

<script>
  import EssayQuestion from '../questiontemplates/EssayQuestion.vue'
  import FileUploadQuestion from '../questiontemplates/FileUploadQuestion.vue'
  import MatchingQuestion from '../questiontemplates/MatchingQuestion.vue'
  import MultipleChoiceQuestion from '../questiontemplates/MultipleChoiceQuestion.vue'
  import MultipleResponseQuestion from '../questiontemplates/MultipleResponseQuestion.vue'
  import ShortAnswerQuestion from '../questiontemplates/ShortAnswerQuestion.vue'
  import TrueFalseQuestion from '../questiontemplates/TrueFalseQuestion.vue'
  import {Alert} from 'quasar'

  export default {
    name: 'EditQuestion',
    props: ['question', 'questiontypes'],
    components: {
      EssayQuestion,
      FileUploadQuestion,
      MatchingQuestion,
      MultipleChoiceQuestion,
      MultipleResponseQuestion,
      ShortAnswerQuestion,
      TrueFalseQuestion
    },
    data () {
      return {
        spinner: false
      }
    },
    methods: {
      typeChange (id, cid) {
        this.question.question_type_id = cid
        let that = this
        const alert = Alert.create({
          html: 'If you change question type now you will lose your question settings.',
          position: 'top-center',
          actions: [
            {
              label: 'Continue',
              handler () {
                if (id === 1) { //  Multiple Choice Question
                  if (cid === 2) {
                  } else {
                    that.question.settings = {distractors: []}
                  }
                }
                if (id === 2) { //  Multiple Response Question
                  if (cid === 1) {
                  } else {
                    that.question.settings = {distractors: []}
                  }
                }
                if (id === 3) { //  Short Answer Question
                  that.question.settings = {answers: []}
                }
                if (id === 4) { //  Essay Question
                  that.question.settings = {}
                }
                if (id === 5) { //  Matching Question
                  that.question.settings = {distractors: [], options: []}
                }
                if (id === 7) { //  File Upload Question
                  that.question.settings = {}
                }
                if (id === 9) { //  True/False Question
                  that.question.settings = {answer: false}
                }
                that.question.question_type_id = id
              }
            },
            {
              label: 'Dismiss',
              handler () {
                alert.dismiss()
              }
            }
          ]
        })
      }
    }
  }
</script>
