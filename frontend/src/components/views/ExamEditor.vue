<template>
  <div class="wrapper">
    <div class="teaching">
      <div class="row">
        <div class="col-12 p-0">
          <q-toolbar inverted color="dark" class="bg-light">
            <div class="col-xl-2 col-lg-2 col-md-2 col-sm-3 col-xs-3">
              <q-toolbar-title>
                Instructor Tools
              </q-toolbar-title>
            </div>
            <div class="col-xl-4 col-lg-4 col-md-4 col-sm-7 col-xs-7">
              <span v-if="questionsChanged" class="pl-4 animated fadeIn">
                <q-btn small :disable="!APIFinished" color="secondary" @click=revertChanges()
                       class="mr-1">Revert</q-btn>
                <q-btn small :disable="!APIFinished" color="primary" @click="saveChanges()">Save</q-btn>
                <q-spinner-hourglass v-if="!APIFinished" size="40px" color="tertiary"></q-spinner-hourglass>
              </span>
            </div>
            <div class="col-xl-6 col-lg-6 col-md-6 col-sm-2 col-xs-2">
              <div class="pull-right">
                <q-fab color="primary" active-icon="fa-times" icon="fa-cogs" direction="left">
                  <q-fab-action color="secondary" @click="createQuestion" icon="fa-plus-square">
                    <q-tooltip anchor="center left" self="center right" :offset="[20, 0]">Create Question</q-tooltip>
                  </q-fab-action>
                  <q-fab-action color="primary" @click="createQuestionSet" icon="fa-plus-square-o">
                    <q-tooltip anchor="center left" self="center right" :offset="[20, 0]">Create Question Set
                    </q-tooltip>
                  </q-fab-action>
                  <q-fab-action color="tertiary" @click="toast('alarm')" icon="fa-cloud-download">
                    <q-tooltip anchor="center left" self="center right" :offset="[20, 0]">Associate Question Set
                    </q-tooltip>
                  </q-fab-action>
                  <q-fab-action color="warning" @click="toast('alarm')" icon="fa-pencil">
                    <q-tooltip anchor="center left" self="center right" :offset="[20, 0]">Question Bank</q-tooltip>
                  </q-fab-action>
                  <q-fab-action color="red" @click="toast('alarm')" icon="fa-cloud-upload">
                    <q-tooltip anchor="center left" self="center right" :offset="[20, 0]">Upload Media</q-tooltip>
                  </q-fab-action>
                </q-fab>
              </div>
            </div>
          </q-toolbar>
        </div>
      </div>
      <div class="row">
        <div class="col-xs-3 col-sm-3 col-md-3 col-lg-3 col-xl-3 pl-0">
          <q-list no-border separator link class="scroll" style="max-height: 600px">
            <q-list-header>Exam Questions</q-list-header>
            <draggable v-model="questions">
              <q-item :class="{active: aindex === activeQuestion()}" v-for="(question, aindex) in questions"
                      :key="aindex" class="cursor-pointer row"
                      @click="selectQuestion(question, aindex)">
                <q-item-tile v-if="question.question_type_id === 1" color="secondary" icon="fa-users"
                             class="col-1"></q-item-tile>
                <q-item-tile v-else-if="question.question_type_id === 2" color="primary"
                             icon="fa-desktop" class="col-1"></q-item-tile>
                <q-item-tile v-else color="warning" icon="fa-exclamation-triangle" class="col-1"></q-item-tile>
                <q-item-main class="pl-3 col-xs-11 col-sm-11 col-md-7 col-lg-7 col-xl-8">
                  <q-item-tile label class="font-sm">
                    {{ aindex + 1}} - <span class="text-black" v-for="(type, bindex) in questionTypes" :key="bindex">
                    <span v-if="question.question_type_id === type.value">{{ type.label}}</span></span>
                  </q-item-tile>
                  <q-item-tile sublabel lines="1" class="font-xs">
                    {{ question.text }}
                  </q-item-tile>
                </q-item-main>
                <q-item-tile right class="font-size-12 col-xs-3 col-sm-12 col-md-4 col-lg-4 col-xl-3">
                  <div ref="target" small flat no-caps class="text-faded text-center">
                    {{ question.questionSetName }}
                  </div>
                </q-item-tile>
              </q-item>
            </draggable>
          </q-list>
        </div>
        <div class="col-xs-9 col-sm-9 col-md-9 col-lg-9 col-xl-9 pl-0" v-if="selectedQuestion">
          <div class="pl-3 scroll" style="max-height: 600px">
            <q-select float-label="Associated Question Set" v-model="selectedQuestion.questionSetID"
                      :options="questionSetsOptions"
                      @change="changeQuestionSet(selectedQuestion.questionSetID)"></q-select>
            <edit-question :questiontypes="questionTypes" :question="selectedQuestion"></edit-question>
          </div>
        </div>
      </div>
    </div>
    <q-modal minimized @close="newquestion = {}" ref="createQuestion" :content-css="{minWidth: '50%'}">
      <create-question :questionsetsOptions="questionSetsOptions" :questiontypes="questionTypes"
                       :newquestion="newQuestion" :createdQuestion="createdQuestion"></create-question>
    </q-modal>
    <q-modal minimized ref="createQuestionSet" :content-css="{minWidth: '50%'}">
      <create-questionset :noExam="false" :examID="examID"
                          :createdQuestionset="createdQuestionSet"></create-questionset>
    </q-modal>
    <q-inner-loading :visible="spinner">
      <q-spinner-gears size="50px" color="primary"></q-spinner-gears>
    </q-inner-loading>
  </div>
</template>

<script>

  import draggable from 'vuedraggable'
  import {Toast} from 'quasar'
  import _ from 'lodash'
  import EditQuestion from './library/EditQuestion.vue'
  import CreateQuestion from './library/CreateQuestion.vue'
  import CreateQuestionset from './library/CreateQuestionset.vue'

  export default {
    name: 'ExamEditor',
    props: ['examName', 'examID', 'questionSequence'],
    components: {
      EditQuestion,
      draggable,
      CreateQuestion,
      CreateQuestionset
    },
    data () {
      return {
        questions: [],
        questionTypes: [],
        questionSets: [],
        setActive: 0,
        selectedQuestion: false,
        newQuestion: {},
        spinner: false,
        originalQuestions: {},
        questionsChanged: false,
        APIFinished: true
      }
    },
    mounted: function () {
      console.log('here', this.questionSequence)
      this.spinner = true
      this.$http({
        method: 'get',
        url: '/api/exam/' + this.examID + '/questionsets/'
      }).then(response => {
        if (response.status === 250) {
          this.$router.error = response.data
          this.$router.push({path: '/error'})
        } else {
          this.questions = response.data.questions
          this.questionSetOptions = response.data.questionSetOptions
          if (this.questionSequence.length === 0) {
            for (let i = 0; i < this.questionSets.length; i++) {
              for (let j = 0; j < this.questionSets[i].questions.length; j++) {
                let obj = this.questionSets[i].questions[j]
                this.questions.push(obj)
                this.questionSequence.push(obj.id)
              }
            }
          } else {
            for (let i = 0; i < this.questionSets.length; i++) {
              for (let j = 0; j < this.questionSets[i].questions.length; j++) {
                let obj = this.questionSets[i].questions[j]
                this.questions.push(obj)
              }
            }
            if (this.questionSequence.length === this.questions.length) {

            }
            for (let j = 0; j < this.questionSequence.length; j++) {

            }
          }
          if (this.questions && this.questions[0] && this.questions[0].id) {
            this.selectedQuestion = this.questions[0]
          }
          this.originalQuestions = _.cloneDeep(this.questions)
          this.spinner = false
        }
      }).catch(error => {
        console.log(error)
      })
      this.$http({
        method: 'get',
        url: '/api/getquestiontypes/'
      }).then(response => {
        if (response.status === 250) {
          this.$router.error = response.data
          this.$router.push({path: '/error'})
        } else {
          this.questionTypes = response.data
        }
      }).catch(error => {
        console.log(error)
      })

      this.setActive = 0
    },
    computed: {
      questionSetsOptions () {
        let options = []
        for (let i = 0; i < this.questionSets.length; i++) {
          if (this.questionSets[i].id !== 0) {
            options.push({'label': this.questionSets[i].name, 'value': this.questionSets[i].id})
          }
        }
        return options
      }
    },
    watch: {
      questions: {
        handler: function (newVal, oldVal) {
          if (_.isEqual(this.originalQuestions, newVal)) {
            this.questionsChanged = false
          } else {
            this.questionsChanged = true
          }
        },
        deep: true
      }
    },
    methods: {
      activeQuestion () {
        return this.setActive
      },
      selectQuestion (question, index) {
        this.setActive = index
        this.selectedQuestion = question
      },
      createQuestion () {
        this.newQuestion = {
          'sequence': 0,
          'weight': 1,
          'text': 'New Question Text',
          'settings': {
            'distractors': []
          },
          'question_type_id': 1
        }
        this.$refs.createQuestion.open()
      },
      createdQuestion (question, QSid) {
        for (let i = 0; i < this.questionSets.length; i++) {
          if (this.questionSets[i].id === QSid) {
            this.questionSets[i].questions.push(question)
          }
        }
        this.$refs.createQuestion.close()
      },
      createQuestionSet () {
        this.$refs.createQuestionSet.open()
      },
      createdQuestionSet (questionSet) {
        this.questionSets.push(questionSet)
        this.$refs.createQuestionSet.close()
      },
      changeQuestionSet (newVal) {
        for (let i = 0; i < this.questionSetsOptions.length; i++) {
          if (this.questionSetsOptions[i].value === newVal) {
            this.selectedQuestion.questionSetID = this.questionSetsOptions[i].value
            this.selectedQuestion.questionSetName = this.questionSetsOptions[i].label
          }
        }
      },
      saveChanges () {
        if (this.questionsChanged) {
          this.APIFinished = false
          this.$http({
            method: 'post',
            url: '/api/savequestion/',
            headers: {
              'X-CSRFToken': this.getCookie('csrftoken')
            },
            data: {
              questions: this.questions,
              questionSequence: this.questionSequence,
              examID: this.examID
            }
          }).then(response => {
            if (response.status === 250) {
              this.$router.error = response.data
              this.$router.push({path: '/error'})
            }
            this.APIFinished = true
            this.questionsChanged = false
            this.originalQuestions = _.cloneDeep(this.questions)
            Toast.create.positive('Questions Saved')
          }).catch(error => {
            console.log(error)
          })
        }
      },
      revertChanges () {
        if (this.questionsChanged) {
          let clone = _.cloneDeep(this.originalQuestions)
          this.questions = clone
          this.selectedQuestion = this.questions[this.setActive]
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

<style lang="stylus">

</style>
