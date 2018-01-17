<template>
  <div>
    <div v-if="questionsets">
      <q-toolbar inverted color="dark" class="bg-light col-12">
        <q-toolbar-title>
          Question Set Tools
        </q-toolbar-title>
        <q-fab color="primary" active-icon="fa-times" icon="fa-cogs" v-model="open" direction="left">
          <q-fab-action color="secondary" @click="createQuestion" icon="fa-plus-square">
            <q-tooltip anchor="center left" self="center right" :offset="[20, 0]">Create Question</q-tooltip>
          </q-fab-action>
          <q-fab-action color="primary" @click="createQuestionset" icon="fa-plus-square-o">
            <q-tooltip anchor="center left" self="center right" :offset="[20, 0]">Create Questionset</q-tooltip>
          </q-fab-action>
        </q-fab>
      </q-toolbar>
      <div class="row w-100">
        <div class="col-1"></div>
        <div class="col-md-6 col-lg-4 col-xl-3 col-sm-7 col-xs-10 row">
          <div class="col-12 row">
            <div class="col-6">Question Sets</div>
            <div class="col-5">Shared</div>
            <div class="col-1">All</div>
          </div>
          <div class="col-12">
            <q-slider v-model="displayOption" snap :min="0" :max="2" @change="toggleOptions"></q-slider>
          </div>
        </div>
        <div class="col-md-6 col-lg-8 col-xl-9 col-sm-5 col-xs-12"></div>
      </div>
      <better-data-table
        :rows="displayedQuestionsets"
        :config="config"
        :columns="columns"
        class="col-12"
        @rowclick="rowclick"
      >
        <template slot="questions" scope="cell">
          <span>
            <span v-for="(question, index) in cell.row.questions" :key="index" v-if="cell.row.id !== 0">
              <q-btn @click="editQuestion(question, cell.row.id)">{{ question.sequence }}</q-btn>
              <q-tooltip>{{ question.text.substring(0, 100)}}<span
                v-if="question.text.length > 99">...</span></q-tooltip>
            </span>
            <span v-else>
              <q-btn @click="editQuestion(question, cell.row.id)">{{ question.sequence }}</q-btn>
              <q-tooltip>{{ question.text.substring(0, 100)}}<span
                v-if="question.text.length > 99">...</span></q-tooltip>
            </span>
            <span v-if="cell.row.questions.length < 1">No Questions to Show</span>
          </span>
        </template>
        <template slot="selection" scope="selection">
          <q-btn color="primary" class="mr-2" @click="associateQuestionsets(selection.props)">
            <q-icon name="fa-handshake-o"/>
            <q-tooltip anchor="top right" self="bottom middle">Associate</q-tooltip>
          </q-btn>
          <q-btn color="faded" class="mr-2" @click="shareQuestionsets(selection.props)">
            <q-icon name="fa-share-square-o"/>
            <q-tooltip anchor="top right" self="bottom middle">Share</q-tooltip>
          </q-btn>
          <q-btn color="warning" class="mr-2" @click="transferQuestionsets(selection.props)">
            <q-icon name="fa-mail-forward"/>
            <q-tooltip anchor="top right" self="bottom middle">Transfer</q-tooltip>
          </q-btn>
        </template>
      </better-data-table>
    </div>
    <q-modal minimized @close="question = false" ref="editQuestion" :content-css="{minWidth: '50%'}">
      <q-card flat>
        <q-card-title>
          Edit Question {{ question.sequence }}
        </q-card-title>
        <q-card-separator></q-card-separator>
        <q-card-main>
          <q-select float-label="Select a Question Set" :options="questionsetsOptions"
                    v-model="newQuestionset"></q-select>
          <edit-question :questiontypes="questiontypes" :question="question"></edit-question>
          <q-btn class="float-right" color="primary" :disabled="spinner" @click="save(question)">Save</q-btn>
          <q-inner-loading :visible="spinner">
            <q-spinner-gears size="50px" color="primary"></q-spinner-gears>
          </q-inner-loading>
        </q-card-main>
      </q-card>
    </q-modal>
    <q-modal minimized @close="newquestion = {}" ref="createQuestion" :content-css="{minWidth: '50%'}">
      <create-question :questionsetsOptions="questionsetsOptions" :questiontypes="questiontypes"
                       :newquestion="newquestion" :createdQuestion="createdQuestion"></create-question>
    </q-modal>
    <q-modal minimized ref="createQuestionset" :content-css="{minWidth: '50%'}">
      <create-questionset :noExam="true" :examOptions="examOptions"
                          :createdQuestionset="createdQuestionset"></create-questionset>
    </q-modal>
    <q-modal minimized ref="transferQuestionsets" :content-css="{minWidth: '50%'}">
      <transfer-questionset :selectedQuestionsets="selectedQuestionsets" :transferredQuestionsets="transferredQuestionsets"></transfer-questionset>
    </q-modal>
    <q-modal minimized ref="shareQuestionsets" :content-css="{minWidth: '50%'}">
      <share-questionset :selectedQuestionsets="selectedQuestionsets" :sharedQuestionsets="sharedQuestionsets"></share-questionset>
    </q-modal>
    <q-modal minimized ref="associateQuestionsets" :content-css="{minWidth: '50%'}">
      <associate-questionset :selectedQuestionsets="selectedQuestionsets" :sharedQuestionsets="sharedQuestionsets"></associate-questionset>
    </q-modal>
    <q-inner-loading :visible="!questionsets">
      <q-spinner-gears size="50px" color="primary"></q-spinner-gears>
    </q-inner-loading>
  </div>
</template>

<script>
  import BetterDataTable from '../components/BetterDataTable.vue'
  import EditQuestion from './EditQuestion.vue'
  import CreateQuestionset from './CreateQuestionset.vue'
  import CreateQuestion from './CreateQuestion.vue'
  import TransferQuestionset from './TransferQuestionset.vue'
  import ShareQuestionset from './ShareQuestionset.vue'
  import AssociateQuestionset from './AssociateQuestionset.vue'
  import {Toast} from 'quasar'

  export default {
    name: 'InstructorQuestionSets',
    components: {
      BetterDataTable,
      EditQuestion,
      CreateQuestionset,
      CreateQuestion,
      TransferQuestionset,
      ShareQuestionset,
      AssociateQuestionset
    },
    data () {
      return {
        questionsets: false,
        newQuestionset: '',
        open: false,
        config: {
          title: '',
          header: true,
          columnPicker: true,
          ajaxSearch: false,
          bodyStyle: {
            height: '100%'
          },
          rowHeight: '50px',
          pagination: {
            itemCount: 0,
            rowsPerPage: 5,
            options: [2, 5, 10, 15]
          },
          messages: {
            noData: '<i>warning</i> No data available to show.',
            noDataAfterFiltering: '<i>warning</i> No results. Please refine your search terms.'
          },
          selection: 'multiple'
        },
        columns: [
          {
            label: 'Questionset Name',
            field: 'name',
            sort: true,
            type: 'string'
          },
          {
            label: 'Questions',
            field: 'questions',
            type: 'template'
          }
        ],
        question: false,
        questiontypes: [],
        spinner: false,
        newquestion: {},
        examList: [],
        selectedQuestionsets: [],
        displayOption: 0,
        displayedQuestionsets: []
      }
    },
    mounted () {
      this.$http({
        method: 'get',
        url: '/api/getquestionsets/'
      }).then(response => {
        if (response.status === 250) {
          this.$router.error = response.data
          this.$router.push({path: '/error'})
        } else {
          this.questionsets = response.data
          this.displayedQuestionsets = response.data
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
          this.questiontypes = response.data
        }
      }).catch(error => {
        console.log(error)
      })
      this.$http({
        method: 'get',
        url: '/api/getexams/'
      }).then(response => {
        if (response.status === 250) {
          this.$router.error = response.data
          this.$router.push({path: '/error'})
        } else {
          for (let i = 0; i < response.data.length; i++) {
            if (!response.data[i]['archived']) {
              this.examList.push(response.data[i])
            }
          }
        }
      }).catch(error => {
        console.log(error)
      })
    },
    computed: {
      examOptions () {
        let options = []
        for (let i = 0; i < this.examList.length; i++) {
          if (this.examList[i].id !== 0) {
            options.push({'label': this.examList[i].name, 'value': this.examList[i].id})
          }
        }
        return options
      },
      questionsetsOptions () {
        let options = []
        for (let i = 0; i < this.questionsets.length; i++) {
          if (this.questionsets[i].id !== 0) {
            options.push({'label': this.questionsets[i].name, 'value': this.questionsets[i].id})
          } else {
            options.push({'label': 'None', 'value': this.questionsets[i].id})
          }
        }
        return options
      }
    },
    methods: {
      associateQuestionsets (questionsets) {
        this.selectedQuestionsets = questionsets
        this.$refs.associateQuestionsets.open()
      },
      sharedQuestionsets () {
        this.$refs.shareQuestionsets.close()
      },
      transferredQuestionsets (questionsets) {
        for (let i = 0; i < this.questionsets.length; i++) {
          for (let j = 0; j < questionsets.length; j++) {
            if (this.questionsets[i].id === questionsets[j].id) {
              this.questionsets.splice(i, 1)
            }
          }
        }
        for (let i = 0; i < this.displayedQuestionsets.length; i++) {
          for (let j = 0; j < questionsets.length; j++) {
            if (this.displayedQuestionsets[i].id === questionsets[j].id) {
              this.displayedQuestionsets.splice(i, 1)
            }
          }
        }
        for (let i = 0; i < this.selectedQuestionsets.length; i++) {
          for (let j = 0; j < questionsets.length; j++) {
            if (this.selectedQuestionsets[i].id === questionsets[j].id) {
              this.selectedQuestionsets.splice(i, 1)
            }
          }
        }
        this.$refs.transferQuestionsets.close()
      },
      toggleOptions () {
        this.displayedQuestionsets = []
        for (let i = 0; i < this.questionsets.length; i++) {
          if (this.displayOption === 0) {
            if (!this.questionsets[i]['shared']) {
              this.displayedQuestionsets.push(this.questionsets[i])
            }
          }
          if (this.displayOption === 1) {
            if (this.questionsets[i]['shared']) {
              this.displayedQuestionsets.push(this.questionsets[i])
            }
          }
          if (this.displayOption === 2) {
            this.displayedQuestionsets.push(this.questionsets[i])
          }
        }
      },
      shareQuestionsets (questionsets) {
        for (let i = 0; i < questionsets.length; i++) {
          if (questionsets[i]['shared']) {
            Toast.create.warning(questionsets[i]['name'] + ' is shared with you, and cannot be shared.')
            questionsets.splice(i, 1)
          }
        }
        if (questionsets.length > 0) {
          this.selectedQuestionsets = questionsets
          this.$refs.shareQuestionsets.open()
        }
      },
      createdQuestion (question, QSid) {
        for (let i = 0; i < this.questionsets.length; i++) {
          if (this.questionsets[i].id === QSid) {
            this.questionsets[i].questions.push(question)
          }
        }
        this.$refs.createQuestion.close()
      },
      createdQuestionset (questionset) {
        this.questionsets.push(questionset)
        this.$refs.createQuestionset.close()
      },
      transferQuestionsets (questionsets) {
        for (let i = 0; i < questionsets.length; i++) {
          if (questionsets[i]['shared']) {
            Toast.create.warning(questionsets[i]['name'] + ' is shared with you, and cannot be transferred.')
            questionsets.splice(i, 1)
          }
        }
        if (questionsets.length > 0) {
          this.selectedQuestionsets = questionsets
          this.$refs.transferQuestionsets.open()
        }
      },
      rowclick (row) {
      },
      editQuestion (question, QSid) {
        this.question = question
        this.newQuestionset = QSid
        this.$refs.editQuestion.open()
      },
      createQuestion () {
        this.newquestion = {
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
      createQuestionset () {
        this.$refs.createQuestionset.open()
      },
      save (question) {
        this.spinner = true
        question['questionset'] = this.newQuestionset
        let questions = [question]
        this.$http({
          method: 'post',
          url: '/api/savequestion/',
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          },
          data: {
            question: questions
          }
        }).then(response => {
          if (response.status === 250) {
            this.$router.error = response.data
            this.$router.push({path: '/error'})
          }
          this.spinner = false
          for (let i = 0; i < this.questionsets.length; i++) {
            for (let j = 0; j < this.questionsets[i].questions.length; j++) {
              if (this.questionsets[i].questions[j].id === question.id) {
                if (this.questionsets[i].id === this.newQuestionset) {
                  // Do nothing because it didn't move questions set
                  Toast.create.positive('Question Saved')
                  return
                } else {
                  this.questionsets[i].questions.splice(j, 1)
                  for (let k = 0; k < this.questionsets[i].questions.length; k++) {
                    this.questionsets[i].questions[k].sequence = k + 1
                  }
                  for (let k = 0; k < this.questionsets.length; k++) {
                    if (this.questionsets[k].id === this.newQuestionset) {
                      question.sequence = this.questionsets[k].questions.length + 1
                      this.questionsets[k].questions.push(question)
                    }
                  }
                  Toast.create.positive('Question Saved')
                  return
                }
              }
            }
          }
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
      }
    }
  }
</script>
