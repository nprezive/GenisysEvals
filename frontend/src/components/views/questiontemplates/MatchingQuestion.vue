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
          @change="typeChange(question.question_type_id, 5)"
        ></q-select>
      </div>
    </div>
    <div class="col-xl-6 col-lg-6 col-md-12 col-sm-12 col-xs-12">
      <q-list no-border>
        <q-list-header>Options</q-list-header>
        <q-item v-for="(distractor, index) in question['settings']['options']" :key="index">
          <q-item-main>
            <div class="row">
              <span class="col-xl-6 col-lg-6 col-md-6 col-sm-6 col-xs-12">{{distractor.text}}</span>
              <q-select class="col-xl-6 col-lg-6 col-md-6 col-sm-6 col-xs-12" :options="distractorOptions" v-model="distractor.answer"></q-select>
            </div>
          </q-item-main>
          <q-item-side>
            <q-icon name="fa-times" color="negative" class="cursor-pointer" @click="deleteOption(index)"></q-icon>
          </q-item-side>
        </q-item>
        <q-item>
          <q-item-main>
            <q-field class="col-9" :error="newOptionTouched && newOption.length < 1" error-label="Option cannot be blank." helper="Add an Option.">
              <q-input v-model="newOption" @focus="newOptionTouched = true"></q-input>
            </q-field>
          </q-item-main>
          <q-item-side>
            <q-icon @click="addOption" class="cursor-pointer" name="fa-plus" color="primary"></q-icon>
          </q-item-side>
        </q-item>
      </q-list>
    </div>
    <div class="col-xl-6 col-lg-6 col-md-12 col-sm-12 col-xs-12">
      <q-list no-border>
        <q-list-header>Distractors</q-list-header>
        <q-item v-for="(distractor, index) in question['settings']['distractors']"
                :key="index">
          <q-item-main>
            {{index + 1}}. {{distractor}}
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
          <q-item-side>
            <q-icon @click="addDistractor" class="cursor-pointer" name="fa-plus" color="primary"></q-icon>
          </q-item-side>
        </q-item>
      </q-list>
    </div>
  </div>
</template>

<script>
  import draggable from 'vuedraggable'

  export default {
    name: 'MatchingQuestion',
    props: ['question', 'questiontypes', 'typeChange'],
    components: {
      draggable
    },
    data () {
      return {
        newDistractor: '',
        newOption: '',
        newDistractorTouched: false,
        newOptionTouched: false
      }
    },
    computed: {
      distractorOptions () {
        let distractors = []
        for (let i = 0; i < this.question.settings.distractors.length; i++) {
          distractors.push({value: i, label: this.question.settings.distractors[i]})
        }
        return distractors
      }
    },
    methods: {
      addOption () {
        if (this.newOption.length > 0) {
          this.question.settings.options.push({answer: 0, text: this.newOption})
          this.newOption = ''
          this.newOptionTouched = false
        } else {
          this.newOptionTouched = true
        }
      },
      addDistractor () {
        if (this.newDistractor.length > 0) {
          this.question.settings.distractors.push(this.newDistractor)
          this.newDistractor = ''
          this.newDistractorTouched = false
        } else {
          this.newDistractorTouched = true
        }
      },
      deleteDistractor (index) {
        this.question['settings']['distractors'].splice(index, 1)
      },
      deleteOption (index) {
        this.question['settings']['options'].splice(index, 1)
      }
    }
  }
</script>
