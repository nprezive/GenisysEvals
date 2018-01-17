<template>
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
          @change="typeChange(question.question_type_id, 2)"
        ></q-select>
      </div>
    </div>
    <div class="col-xl-4 col-lg-12 col-md-12 col-sm-12 col-xs-12">
      <q-list no-border>
        <q-list-header>Question Options</q-list-header>
        <draggable v-model="question['settings']['distractors']" @end="distractorMoved">
          <q-item class="cursor-pointer" v-for="(distractor, index) in question['settings']['distractors']" :key="index">
            <q-item-side>
              <q-icon @click="distractor.correct = false" class="cursor-pointer" name="fa-check" v-if="distractor.correct" color="primary"></q-icon>
              <q-icon @click="distractor.correct = true" class="cursor-pointer" name="fa-circle-o" v-else color="tertiary"></q-icon>
            </q-item-side>
            <q-item-main>
              {{index + 1}}. {{distractor.text}}
            </q-item-main>
            <q-item-side>
              <q-icon name="fa-times" color="negative" class="cursor-pointer" @click="deleteDistractor(index)"></q-icon>
            </q-item-side>
          </q-item>
          <q-item>
            <q-item-main>
              <q-field class="col-9" :error="newDistractorTouched && newDistractor.length < 1" error-label="Distractor cannot be blank." helper="Add an Distractor.">
                <q-input v-model="newDistractor" @focus="newDistractorTouched = true"></q-input>
              </q-field>
            </q-item-main>
            <q-item-side><q-icon @click="addDistractor" class="cursor-pointer" name="fa-plus" color="primary"></q-icon></q-item-side>
          </q-item>
        </draggable>
      </q-list>
    </div>
  </div>
</template>

<script>
  import draggable from 'vuedraggable'

  export default {
    name: 'MultipleResponseQuestion',
    props: ['question', 'questiontypes', 'typeChange'],
    components: {
      draggable
    },
    data () {
      return {
        newDistractor: '',
        newDistractorTouched: false
      }
    },
    methods: {
      addDistractor () {
        if (this.newDistractor.length > 0) {
          this.question['settings']['distractors'].push({
            text: this.newDistractor,
            correct: false,
            sequence: this.question['settings']['distractors'].length + 1
          })
          this.newDistractor = ''
          this.newDistractorTouched = false
        } else {
          this.newDistractorTouched = true
        }
      },
      deleteDistractor (index) {
        this.question['settings']['distractors'].splice(index, 1)
      },
      distractorMoved () {
        for (let i = 1; i <= this.question['settings']['distractors'].length; i++) {
          this.question['settings']['distractors'][i - 1]['sequence'] = i
        }
      }
    }
  }
</script>
