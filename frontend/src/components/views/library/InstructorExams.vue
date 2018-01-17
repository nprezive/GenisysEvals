<template>
  <div>
    <div v-if="exams" class="row">
      <q-toolbar inverted color="dark" class="bg-light col-12">
        <q-toolbar-title>
          Exam Tools
        </q-toolbar-title>
        <q-fab color="primary" active-icon="fa-times" icon="fa-cogs" v-model="open" direction="left">
          <q-fab-action color="warning" @click="uploadExam" icon="fa-upload">
            <q-tooltip anchor="center left" self="center right" :offset="[20, 0]">Import Exam</q-tooltip>
          </q-fab-action>
          <q-fab-action color="secondary" @click="createExam" icon="fa-plus-square">
            <q-tooltip anchor="center left" self="center right" :offset="[20, 0]">Create Exam</q-tooltip>
          </q-fab-action>
          <q-fab-action color="primary" @click="createBlankExam" icon="fa-plus-square-o">
            <q-tooltip anchor="center left" self="center right" :offset="[20, 0]">Create Blank Exam</q-tooltip>
          </q-fab-action>
        </q-fab>
      </q-toolbar>
      <div class="row w-100">
        <div class="col-1"></div>
        <div class="col-md-6 col-lg-4 col-xl-3 col-sm-7 col-xs-10 row">
          <div class="col-12 row">
            <div class="col-4">Exams</div>
            <div class="col-4">Shared</div>
            <div class="col-3">Deleted</div>
            <div class="col-1">All</div>
          </div>
          <div class="col-12">
            <q-slider v-model="showArchived" snap :min="0" :max="3" @change="toggleArchived"></q-slider>
          </div>
        </div>
        <div class="col-md-6 col-lg-8 col-xl-9 col-sm-5 col-xs-12"></div>
      </div>
      <better-data-table
        :rows="currentExams"
        :config="config"
        :columns="columns"
        class="col-12"
        @rowclick="rowclick"
      >
        <template slot="audience" scope="cell">
          <span>
            <span v-for="(lc, index) in cell.data" :key="index">
              {{ lc.id }}<span v-if="cell.data.length > index + 1">,</span>
              <q-tooltip>{{ lc.name }}</q-tooltip>
            </span>
          </span>
        </template>
        <template slot="daterange" scope="cell">
          <span>
            {{ cell.data }}
            <q-tooltip>Exam is available between these dates.</q-tooltip>
          </span>
        </template>
        <template slot="selection" scope="selection">
          <q-btn color="primary" @click="changeDate(selection.props)">
            <q-icon name="fa-calendar"></q-icon>
            <q-tooltip anchor="top right" self="bottom middle">Change Date</q-tooltip>
          </q-btn>
          <q-btn color="secondary" @click="libraryAudience(selection.props)">
            <q-icon name="fa-user-plus"></q-icon>
            <q-tooltip anchor="top right" self="bottom middle">Add/Remove Audience</q-tooltip>
          </q-btn>
          <q-btn color="faded" @click="shareExam(selection.props)">
            <q-icon name="fa-share-square-o"></q-icon>
            <q-tooltip anchor="top right" self="bottom middle">Share</q-tooltip>
          </q-btn>
          <q-btn color="warning" @click="transferExam(selection.props)">
            <q-icon name="fa-mail-forward"></q-icon>
            <q-tooltip anchor="top right" self="bottom middle">Transfer</q-tooltip>
          </q-btn>
          <q-btn color="negative" @click="deleteExam(selection.props)">
            <q-icon name="fa-trash-o"></q-icon>
            <q-tooltip anchor="top right" self="bottom middle">Delete</q-tooltip>
          </q-btn>
        </template>
      </better-data-table>
    </div>
    <q-modal ref="changeDate" minimized>
      <exam-date ref="libraryDate" :changeDates="changeDates" :selectedExams="selectedExams"></exam-date>
    </q-modal>
    <q-modal ref="libraryAudience" minimized :content-css="{minWidth: '50%'}">
      <exam-audience :selectedExams="selectedExams" :changeLC="changeLC"></exam-audience>
    </q-modal>
    <q-modal ref="shareExam" minimized :content-css="{minWidth: '50%'}">
      <exam-share :transferredExams="transferredExams" :selectedExams="selectedExams"></exam-share>
    </q-modal>
    <q-modal ref="transferExam" minimized :content-css="{minWidth: '50%'}">
      <exam-transfer :transferredExams="transferredExams" :selectedExams="selectedExams"></exam-transfer>
    </q-modal>
    <q-modal ref="deleteExam" position="bottom" :content-css="{minWidth: '50%'}">
      <exam-delete :deletedExams="deletedExams" :undeletedExams="undeletedExams"
                      :selectedExams="selectedExams"></exam-delete>
    </q-modal>
    <q-modal ref="createExam" minimized :content-css="{minWidth: '50%'}">
      <q-card flat>
        <q-card-title>
          Create Exam Wizard
        </q-card-title>
        <q-card-separator></q-card-separator>
        <q-card-main>
          <library-create-exam></library-create-exam>
        </q-card-main>
      </q-card>
    </q-modal>
    <q-modal ref="createBlankExam" minimized :content-css="{minWidth: '50%'}">
      <q-card flat>
        <q-card-title>
          Create Blank Exam
        </q-card-title>
        <q-card-separator></q-card-separator>
        <q-card-main>
          <div class="row">
            <q-input class="col-md-6 col-lg-6 col-xl-6 col-sm-6 col-xs-12" v-model="blankExamName" float-label="Name your exam"></q-input>
            <div class="col-md-6 col-lg-6 col-xl-6 col-sm-6 col-xs-12 text-center mt-2">
              <q-btn @click="submitBlankExam">Create</q-btn>
            </div>
          </div>
        </q-card-main>
      </q-card>
      <q-inner-loading :visible="spinner">
        <q-spinner-gears size="50px" color="primary"></q-spinner-gears>
      </q-inner-loading>
    </q-modal>
    <q-inner-loading :visible="!exams">
      <q-spinner-gears size="50px" color="primary"></q-spinner-gears>
    </q-inner-loading>
  </div>
</template>

<script>
  import BetterDataTable from '../components/BetterDataTable.vue'
  import ExamAudience from './ExamAudience.vue'
  import ExamDate from './ExamDate.vue'
  import ExamTransfer from './ExamTransfer.vue'
  import ExamDelete from './ExamDelete.vue'
  import LibraryCreateExam from './LibraryCreateExam.vue'
  import ExamShare from './ExamShare.vue'
  import moment from 'moment'
  import {Toast} from 'quasar'

  export default {
    name: 'InstructorExams',
    components: {
      BetterDataTable,
      ExamAudience,
      ExamDate,
      ExamTransfer,
      ExamDelete,
      LibraryCreateExam,
      ExamShare
    },
    data () {
      return {
        exams: false,
        showArchived: 0,
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
            label: 'Test ID',
            field: 'id',
            sort: true,
            type: 'string'
          },
          {
            label: 'Name',
            field: 'name',
            sort: true,
            type: 'string'
          },
          {
            label: 'Audience',
            field: 'audience',
            type: 'template'
          },
          {
            label: 'Date Range',
            field: 'daterange',
            type: 'template'
          }
        ],
        open: false,
        selectedExams: [],
        currentExams: [],
        blankExamName: '',
        spinner: false
      }
    },
    mounted () {
      this.$http({
        method: 'get',
        url: '/api/getexams/'
      }).then(response => {
        if (response.status === 250) {
          this.$router.error = response.data
          this.$router.push({path: '/error'})
        } else {
          this.exams = response.data
          this.currentExams = []
          for (let i = 0; i < this.exams.length; i++) {
            if (this.showArchived) {
              if (this.exams[i]['archived']) {
                this.currentExams.push(this.exams[i])
              }
            } else if (!this.showArchived) {
              if (!this.exams[i]['archived']) {
                this.currentExams.push(this.exams[i])
              }
            }
          }
        }
      }).catch(error => {
        console.log(error)
      })
    },
    computed: {
      selectedAudiences () {
        let audience = []
        let alreadyName = []
        for (let i = 0; i < this.selectedExams.length; i++) {
          for (let j = 0; j < this.selectedExams[i]['audience'].length; j++) {
            if (!alreadyName.includes(this.selectedExams[i]['audience'][j].name)) {
              audience.push(this.selectedExams[i]['audience'][j])
              alreadyName.push(this.selectedExams[i]['audience'][j].name)
            }
          }
        }
        return audience
      }
    },
    methods: {
      submitBlankExam () {
        let sites = []
        let audience = []
        let exam = {name: this.blankExamName, audience: audience, sites: sites, date: {to: moment().format(), from: moment().format()}}
        this.spinner = true
        this.$http({
          method: 'post',
          url: '/api/createexam/',
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
          this.currentExams.push({archived: false, id: response.data, daterange: moment(exam['date']['from']).format('MM-DD-YYYY hh:mm') + ' to ' + moment(exam['date']['from']).format('MM-DD-YYYY hh:mm'), name: this.blankExamName, audience: []})
          this.spinner = false
          Toast.create.positive(this.blankExamName + ' has been created.')
          this.$refs.createBlankExam.close()
        }).catch(error => {
          console.log(error)
        })
      },
      transferredExams (exams) {
        for (let i = 0; i < this.exams.length; i++) {
          for (let j = 0; j < exams.length; j++) {
            if (this.exams[i].id === exams[j].id) {
              this.exams.splice(i, 1)
            }
          }
        }
        for (let i = 0; i < this.currentExams.length; i++) {
          for (let j = 0; j < exams.length; j++) {
            if (this.currentExams[i].id === exams[j].id) {
              this.currentExams.splice(i, 1)
            }
          }
        }
        for (let i = 0; i < this.selectedExams.length; i++) {
          for (let j = 0; j < exams.length; j++) {
            if (this.selectedExams[i].id === exams[j].id) {
              this.selectedExams.splice(i, 1)
            }
          }
        }
        this.$refs.transferExam.close()
      },
      rowclick (row) {
        this.$router.cName = row.name
        this.$router.push({path: '/library/exam/' + row.id})
      },
      uploadExam () {
      },
      createExam () {
        this.$refs.createExam.open()
      },
      createBlankExam () {
        this.$refs.createBlankExam.open()
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
      setDates (exams) {
        this.$refs.libraryDate.newDate = []
        for (let i = 0; i < exams.length; i++) {
          let examDate = exams[i]['daterange'].split(' to ')
          let to = moment(examDate[1]).format()
          let from = moment(examDate[0]).format()
          this.$refs.libraryDate.newDate.push({to: to, from: from})
        }
      },
      changeDate (exams) {
        this.setDates(exams)
        this.selectedExams = exams
        this.$refs.changeDate.open()
      },
      libraryAudience (exams) {
        this.setDates(exams)
        this.selectedExams = exams
        this.$refs.libraryAudience.open()
      },
      shareExam (exams) {
        for (let i = 0; i < exams.length; i++) {
          if (exams[i]['shared']) {
            Toast.create.warning(exams[i]['name'] + ' is shared with you, and cannot be shared.')
            exams.splice(i, 1)
          }
        }
        if (exams.length > 0) {
          this.setDates(exams)
          this.selectedExams = exams
          this.$refs.shareExam.open()
        }
      },
      transferExam (exams) {
        for (let i = 0; i < exams.length; i++) {
          if (exams[i]['shared']) {
            Toast.create.warning(exams[i]['name'] + ' is shared with you, and cannot be transferred.')
            exams.splice(i, 1)
          }
        }
        if (exams.length > 0) {
          this.setDates(exams)
          this.selectedExams = exams
          this.$refs.transferExam.open()
        }
      },
      deleteExam (exams) {
        for (let i = 0; i < exams.length; i++) {
          if (exams[i]['shared']) {
            Toast.create.warning(exams[i]['name'] + ' is shared with you, and cannot be deleted.')
            exams.splice(i, 1)
          }
        }
        if (exams.length > 0) {
          this.setDates(exams)
          this.selectedExams = exams
          this.$refs.deleteExam.open()
        }
      },
      changeLC (exam, lc, rm) {
        for (let i = 0; i < this.selectedExams.length; i++) {
          for (let j = 0; j < exam.length; j++) {
            if (this.selectedExams[i].id === exam[j].id) {
              let included = false
              let lcpos = null
              for (let l = 0; l < this.selectedExams[i].audience.length; l++) {
                if (this.selectedExams[i].audience[l].id === lc.id) {
                  included = true
                  lcpos = l
                }
              }
              if (!included && !rm) {
                this.selectedExams[i].audience.push(lc)
              }
              if (included && rm) {
                this.selectedExams[i].audience.splice(lcpos, 1)
              }
            }
          }
        }
      },
      changeDates (exams, revert) {
        for (let i = 0; i < this.selectedExams.length; i++) {
          for (let j = 0; j < exams.length; j++) {
            if (this.selectedExams[i].id === exams[j].id) {
              if (revert) {
                this.selectedExams[i].daterange = moment(exams[j].oldDate['from']).format('MM-DD-YYYY hh:mm') + ' to ' + moment(exams[j].oldDate['to']).format('MM-DD-YYYY hh:mm')
              } else {
                this.selectedExams[i].daterange = moment(exams[j].date['from']).format('MM-DD-YYYY hh:mm') + ' to ' + moment(exams[j].date['to']).format('MM-DD-YYYY hh:mm')
              }
            }
          }
        }
      },
      toggleArchived () {
        this.currentExams = []
        for (let i = 0; i < this.exams.length; i++) {
          // Delete Exams
          if (this.showArchived === 3 || this.showArchived === 2) {
            if (this.exams[i]['archived'] && !this.exams[i]['shared']) {
              this.currentExams.push(this.exams[i])
            }
          }
          // Shared Exams
          if (this.showArchived === 3 || this.showArchived === 1) {
            if (this.exams[i]['shared'] && !this.exams[i]['archived']) {
              this.currentExams.push(this.exams[i])
            }
          }
          // Non Deleted Exams
          if (this.showArchived === 3 || this.showArchived === 0) {
            if (!this.exams[i]['archived']) {
              this.currentExams.push(this.exams[i])
            }
          }
        }
      },
      deletedExams (exams) {
        for (let i = 0; i < this.selectedExams.length; i++) {
          for (let j = 0; j < exams.length; j++) {
            if (this.selectedExams[i].id === exams[j].id) {
              this.selectedExams[i]['archived'] = true
            }
          }
        }
        this.toggleArchived()
      },
      undeletedExams (exams) {
        for (let i = 0; i < this.selectedExams.length; i++) {
          for (let j = 0; j < exams.length; j++) {
            if (this.selectedExams[i].id === exams[j].id) {
              this.selectedExams[i]['archived'] = false
            }
          }
        }
        this.toggleArchived()
      }
    }
  }
</script>
