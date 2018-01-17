<template>
  <div>
    <div class="row">
      <q-input class="col-12" type="textarea" :min-rows="7" :max-height="300" v-model="question.text"
               float-label="Question Text"></q-input>
      <div class="col-xl-3 col-lg-4 col-md-4 col-sm-6 col-xs-6">
        <q-input v-model="question.weight" type="number" :min="0"
                 float-label="Question Weight"></q-input>
      </div>
      <div class="row col-xl-4 col-lg-6 col-md-6 col-sm-6 col-xs-6">
        <div class="col-xl-10 col-lg-10 col-md-10 col-sm-12 col-xs-12 ml-auto mr-auto">
          <q-select
            v-model="question.question_type_id"
            float-label="Question Type"
            :options="questiontypes"
            @change="typeChange(question.question_type_id, 3)"
          ></q-select>
        </div>
      </div>
    </div>
    <div>
      <q-list highlight no-border class="row">
        <q-list-header class="col-12">Possible Answers</q-list-header>
        <q-item class="col-xl-3 col-lg-3 col-md-4 col-sm-6 col-xs-12"
                v-for="(answer, index) in question.settings.answers" :key="index">
          <q-item-main>{{answer}}</q-item-main>
          <q-item-side>
            <q-icon name="fa-times" color="negative" class="cursor-pointer" @click="deleteAnswer(index)"></q-icon>
          </q-item-side>
        </q-item>
        <q-item class="col-xl-3 col-lg-3 col-md-4 col-sm-6 col-xs-12">
          <q-item-main>
            <div class="row">
              <q-field class="col-9" :error="newAnswerTouched && newAnswer.length < 1"
                       error-label="Answer cannot be blank." helper="Add an answer.">
                <q-input v-model="newAnswer" @focus="newAnswerTouched = true"></q-input>
              </q-field>
              <div class="col-3 text-center">
                <q-btn round flat small icon="fa-plus" @click="addAnswer"></q-btn>
              </div>
            </div>
          </q-item-main>
        </q-item>
      </q-list>
    </div>
  </div>
</template>

<script>

  export default {
    name: 'ShortAnswerQuestion',
    props: ['question', 'questiontypes', 'typeChange'],
    data () {
      return {
        newAnswer: '',
        newAnswerTouched: false
      }
    },
    methods: {
      addAnswer () {
        if (this.newAnswer.length > 0) {
          this.question.settings.answers.push(this.newAnswer)
          this.newAnswer = ''
          this.newAnswerTouched = false
        } else {
          this.newAnswerTouched = false
        }
      },
      deleteAnswer (index) {
        this.question.settings.answers.splice(index, 1)
      }
    }
  }
</script>
