<template>
  <div class="wrapper">
    <div id="enrolled">
      <div class="row">
        <div class="col-12 p-0">
          <q-toolbar inverted color="dark" class="bg-light">
            <q-toolbar-title>
              Student Tools
            </q-toolbar-title>
            <q-fab color="primary" active-icon="fa-times" icon="fa-cogs" direction="left">
              <q-fab-action color="red" @click="toast('alarm')" icon="fa-info">
                <q-tooltip anchor="center left" self="center right" :offset="[20, 0]">Exam Information</q-tooltip>
              </q-fab-action>
              <q-fab-action color="secondary" @click="toast('alarm')" icon="fa-globe">
                <q-tooltip anchor="center left" self="center right" :offset="[20, 0]">Request Proctored Exam</q-tooltip>
              </q-fab-action>
              <q-fab-action color="primary" @click="toast('mail')" icon="fa-file-text">
                <q-tooltip anchor="center left" self="center right" :offset="[20, 0]">Review Exam</q-tooltip>
              </q-fab-action>
            </q-fab>
          </q-toolbar>
        </div>
      </div>
      <div class="row">
        <div class="col-md-3 pl-0">
          <q-list no-border separator link>
            <q-item :class="{active: index === activeSection()}" v-for="(enrollment, index) in enrollments"
                    :key="index" @click="selectSection(enrollment.learning_context, index)">
              <q-item-side v-if="enrollment.learning_context.campus === 'WSU'" color="secondary"
                           icon="fa-users"></q-item-side>
              <q-item-side v-else-if="enrollment.learning_context.campus === 'ONL'" color="primary"
                           icon="fa-desktop"></q-item-side>
              <q-item-side v-else color="negative" icon="fa-exclamation-triangle"></q-item-side>
              <q-item-main>
                <q-item-tile label class="font-sm">
                  {{ enrollment.learning_context.parent }}
                </q-item-tile>
                <q-item-tile sublabel class="font-xs">{{ enrollment.learning_context.short_code
                  }} {{ enrollment.learning_context.number }}
                </q-item-tile>
              </q-item-main>
            </q-item>
          </q-list>
        </div>
        <div class="col-md-9 p-3">
          <better-data-table
            :rows="studentExamList"
            :config="config"
            :columns="columns"
            @rowclick="rowClick"
            ref="instructorExamsTable"
          >
            <template slot="selection" scope="props">
              <q-btn flat color="primary" @click="changeMessage(props)">
                <q-icon name="edit"></q-icon>
              </q-btn>
              <q-btn flat color="primary" @click="deleteRow(props)">
                <q-icon name="delete"></q-icon>
              </q-btn>
            </template>
          </better-data-table>
        </div>
      </div>
      <exam-actions-modal :exam="exam" :review="review" :settings="settings"
                          :closeModal="closeModal" ref="examActionsModal">
      </exam-actions-modal>
    </div>
    <q-inner-loading :visible="!pageSpinner">
      <q-spinner-gears size="50px" color="primary"></q-spinner-gears>
    </q-inner-loading>
  </div>
</template>

<script>
  import {
    Loading
  } from 'quasar'
  import BetterDataTable from './components/BetterDataTable.vue'
  import ExamActionsModal from './components/ExamActionsModal.vue'
  import {mapGetters} from 'vuex'

  export default {
    name: 'Enrolled',
    props: ['enrollments'],
    components: {
      BetterDataTable,
      ExamActionsModal
    },
    data () {
      return {
        pageSpinner: false,
        examList: [],
        settings: false,
        exam: {
          status: false,
          tooltip: '',
          disableTooltip: true,
          button: false
        },
        review: {
          button: false,
          tooltip: '',
          disableTooltip: true
        },
        setActiveCourse: 0,
        config: {
          title: 'Enter the Exam Name, Sites Available, or Date to Filter Exams',
          header: true,
          columnPicker: true,
          ajaxSearch: false,
          bodyStyle: {
            maxHeight: '500px'
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
          }
        },
        columns: [
          {
            label: 'Exam Name',
            field: 'name',
            sort: true,
            type: 'string'
          },
          {
            label: 'Start Date',
            field: 'dateRange',
            style: {'width': '200px'},
            filter: true,
            classes: ['bg-teal-4', 'text-white'],
            type: 'string',
            format (value, row) {
              if (value && value.from) {
                return new Date(value.from).toLocaleString()
              } else {
                return 'No Date Set'
              }
            }
          },
          {
            label: 'End Date',
            field: 'dateRange',
            style: {'width': '200px'},
            classes: ['bg-red-4', 'text-white'],
            type: 'string',
            format (value, row) {
              if (value && value.to) {
                return new Date(value.to).toLocaleString()
              } else {
                return 'No Date Set'
              }
            }
          }
        ]
      }
    },
    mounted: function () {
      this.setActiveCourse = 0
      if (this.enrollments && this.enrollments[0]) {
        this.examApiCall(this.enrollments[0].learning_context.id)
      }
    },
    computed: {
      ...mapGetters([
        'studentExamList'
      ])
    },
    methods: {
      activeSection () {
        return this.setActiveCourse
      },
      selectSection (learningContext, index) {
        this.setActiveCourse = index
        this.examApiCall(learningContext.id)
      },
      examApiCall (id) {
        this.$store.dispatch('GET_STUDENT_EXAMS', id).then(response => {
          if (response.status === 250) {
            this.$router.error = response.data
            this.$router.push({path: '/error'})
          }
          this.pageSpinner = true
        }, error => {
          console.log(error)
        })
        this.pageSpinner = false
      },
      changeMessage (props) {
        props.rows.forEach(row => {
          row.data.name = 'Gogu'
        })
      },
      deleteRow (props) {
        props.rows.forEach(row => {
          this.studentExamList.splice(row.index, 1)
        })
      },
      closeModal () {
        this.settings = false
        this.exam.status = false
      },
      rowClick (row) {
        Loading.show({message: 'Loading Exam Actions'})
        this.$http({
          method: 'get',
          url: '/api/exam/' + row.id + '/takeexamlanding/'
        }).then(response => {
          if (response.status === 250) {
            this.$router.error = response.data
            this.$router.push({path: '/error'})
          }
          this.settings = response.data
        }).catch(error => {
          console.log(error)
        })
        this.$http({
          method: 'get',
          url: '/api/exam/' + row.id + '/canreview/',
          headers: {}
        }).then(response => {
          if (response.status === 250) {
            this.$router.error = response.data
            this.$router.push({path: '/error'})
          }
          if (response.data.canreview) {
            this.review.button = false
            this.review.disableTooltip = true
          } else {
            this.review.button = true
            this.review.tooltip = response.data.info
            this.review.disableTooltip = false
          }
        }).catch(error => {
          console.log(error)
        })
        this.$http({
          method: 'get',
          url: '/api/exam/' + row.id + '/resultstatus/',
          headers: {}
        }).then(response => {
          if (response.status === 250) {
            this.exam.status = 'Exam Unavailable'
            this.exam.tooltip = response.data
            this.exam.disableTooltip = false
            this.exam.button = true
          } else {
            this.exam.status = response.data
            this.exam.disableTooltip = true
            this.exam.button = false
          }
          Loading.hide()
        }).catch(error => {
          console.log(error)
        })
        this.$refs.examActionsModal.openModal()
      }
    }
  }
</script>
<style lang="stylus">

  #enrolled table
    border-collapse: unset

  /*overwrites core-ui border-collapse that messes up multiple selection boxes on quasar data table*/

  #enrolled .q-data-table
    border: none

  #enrolled .q-data-table tbody
    tr
      cursor: pointer
    tr:hover
      background: rgba(189, 189, 189, 0.5)

  #enrolled .q-data-table-toolbar.bottom-toolbar > div
    padding-left: 15px
    padding-right: 15px

  /*padding to fix pagination at bottom of table*/

  #enrolled .q-data-table-toolbar.bottom-toolbar div.q-select
    padding-left: 15px

  /*padding to fix pagination at bottom of table*/

</style>
