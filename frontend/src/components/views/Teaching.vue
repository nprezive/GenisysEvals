<template>
  <div class="wrapper">
    <div id="teaching">
      <div class="row">
        <div class="row col-lg-12 p-0 bg-light center">
          <div class="col-sm-8">
            <q-toolbar inverted color="dark">
              <q-toolbar-title>
                Instructor Tools
                <q-toggle v-model="courseSectionToggle" color="teal-8" @change="toggleList()"
                          :label="toggleLabel"></q-toggle>
              </q-toolbar-title>
            </q-toolbar>
          </div>
          <div class="col-sm-4 py-1">
            <q-fab class="float-right right-padding" color="primary" active-icon="fa-times" icon="fa-cogs" direction="left">
              <q-fab-action color="warning" @click="toast('alarm')" icon="fa-pencil">
                <q-tooltip anchor="center left" self="center right" :offset="[20, 0]">Question Bank</q-tooltip>
              </q-fab-action>
              <q-fab-action color="red" @click="toast('alarm')" icon="fa-cloud-upload">
                <q-tooltip anchor="center left" self="center right" :offset="[20, 0]">Upload Media</q-tooltip>
              </q-fab-action>
              <q-fab-action color="secondary" @click="toast('alarm')" icon="fa-magic">
                <q-tooltip anchor="center left" self="center right" :offset="[20, 0]">Create Exam Wizard</q-tooltip>
              </q-fab-action>
              <q-fab-action color="primary" @click="toast('mail')" icon="fa-plus">
                <q-tooltip anchor="center left" self="center right" :offset="[20, 0]">Create Blank Exam</q-tooltip>
              </q-fab-action>
            </q-fab>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-md-3 pl-0">
          <span v-if="courseSectionToggle">
            <q-list no-border link v-for="(course, firstIndex) in bySectionList" :key="firstIndex">
              <q-list-header>{{ course.name }}</q-list-header>
              <q-item :class="{active: (firstIndex.toString() + secondIndex.toString()) === activeSection()}"
                      v-for="(section, secondIndex) in course.sections" :key="secondIndex"
                      @click="selectSection(section, firstIndex, secondIndex)">
                <q-item-side v-if="section.campus == 'WSU'" color="secondary"
                             icon="fa-users"></q-item-side>
                <q-item-side v-else-if="section.campus == 'ONL'" color="primary"
                             icon="fa-desktop"></q-item-side>
                <q-item-side v-else color="negative" icon="fa-exclamation-triangle"></q-item-side>
                <q-item-main>
                  <q-item-tile label class="font-sm">
                    {{ section.short_code }} {{ section.number }}
                  </q-item-tile>
                </q-item-main>
                <q-item-side right>
                  <q-item-tile stamp class="font-xs">
                    {{ section.name }}
                  </q-item-tile>
                </q-item-side>
              </q-item>
          </q-list>
          </span>
          <q-list no-border separator link v-else>
            <q-item :class="{active: index === activeCourse()}" v-for="(course, index) in byCourseList"
                    :key="index" @click="selectCourse(course, index)">
              <q-item-side color="primary" icon="fa-slideshare"></q-item-side>
              <q-item-main>
                <q-item-tile label class="font-sm">
                  {{ course.name }}
                </q-item-tile>
                <q-item-tile sublabel class="font-xs">{{ course.sublabel }}</q-item-tile>
              </q-item-main>
            </q-item>
          </q-list>
        </div>
        <div class="col-md-9 p-3">
          <better-data-table
            :rows="instructorExamList"
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
    </div>
    <q-inner-loading :visible="pageSpinner">
      <q-spinner-gears size="50px" color="primary"></q-spinner-gears>
    </q-inner-loading>
  </div>
</template>

<script>

  import BetterDataTable from './components/BetterDataTable.vue'
  import {mapGetters} from 'vuex'

  export default {
    name: 'Teaching',
    props: ['enrollments'],
    components: {
      BetterDataTable
    },
    data () {
      return {
        pageSpinner: false,
        courseSectionToggle: false,
        toggleLabel: 'By Course',
        byCourseList: [],
        bySectionList: [],
        setActiveCourse: 0,
        setActiveSection: 0,
        config: {
          title: 'Enter the ID, Exam Name, or Dates to Filter Your Exams',
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
          selection: 'multiple',
          messages: {
            noData: '<i>warning</i> No data available to show.',
            noDataAfterFiltering: '<i>warning</i> No results. Please refine your search terms.'
          }
        },
        columns: [
          {
            label: 'ID',
            field: 'id',
            sort: true,
            type: 'number'
          },
          {
            label: 'Exam Name',
            field: 'name',
            sort: true,
            type: 'string'

          },
          {
            label: 'Results',
            field: 'results',
            style: {'width': '100px'},
            sort: true,
            type: 'number'
          },
          {
            label: 'Start Date',
            field: 'dateRange',
            style: {'width': '200px'},
            classes: ['bg-teal-4', 'text-white'],
            type: 'string',
            format (value, row) {
              return new Date(value.from).toLocaleString()
            }
          },
          {
            label: 'End Date',
            field: 'dateRange',
            style: {'width': '200px'},
            classes: ['bg-red-4', 'text-white'],
            type: 'string',
            format (value, row) {
              return new Date(value.to).toLocaleString()
            }
          }
        ]
      }
    },
    mounted () {
      if (this.enrollments && this.enrollments[0]) {
        let holder = []
        for (let i = 0; i < this.enrollments.length; i++) {
          if (holder.indexOf(this.enrollments[i].learning_context.parent_id) === -1) {
            holder.push(this.enrollments[i].learning_context.parent_id)
            let courseObj = {
              name: this.enrollments[i].learning_context.parent,
              sublabel: this.enrollments[i].learning_context.short_code + ' ' + this.enrollments[i].learning_context.number,
              id: this.enrollments[i].learning_context.parent_id
            }
            this.byCourseList.push(courseObj)

            let sectionObj = {
              name: this.enrollments[i].learning_context.parent,
              sublabel: this.enrollments[i].learning_context.short_code + ' ' + this.enrollments[i].learning_context.number,
              sections: [this.enrollments[i].learning_context]
            }
            this.bySectionList.push(sectionObj)
          } else {
            for (let j = 0; j < this.bySectionList.length; j++) {
              if (this.bySectionList[j].name === this.enrollments[i].learning_context.parent) {
                this.bySectionList[j].sections.push(this.enrollments[i].learning_context)
              }
            }
          }
        }
        if (this.byCourseList && this.byCourseList[0] && this.byCourseList[0].id) {
          this.examApiCall(this.byCourseList[0].id)
        }
      }
      this.setActiveCourse = 0
      this.setActiveSection = '00'
    },
    computed: {
      ...mapGetters([
        'instructorExamList'
      ])
    },
    methods: {
      activeCourse () {
        return this.setActiveCourse
      },
      selectCourse (course, index) {
        this.pageSpinner = true
        this.setActiveCourse = index
        this.examApiCall(course.id)
      },
      activeSection () {
        return this.setActiveSection
      },
      selectSection (section, firstIndex, secondIndex) {
        this.pageSpinner = true
        this.setActiveSection = firstIndex.toString() + secondIndex.toString()
        this.examApiCall(section.id)
      },
      examApiCall (id) {
        this.pageSpinner = true
        this.$store.dispatch('GET_INSTRUCTOR_EXAMS', id).then(response => {
          if (response.status === 250) {
            this.$router.error = response.data
            this.$router.push({path: '/error'})
          }
          this.pageSpinner = false
        }, error => {
          console.log(error)
        })
      },
      changeMessage (props) {
        props.rows.forEach(row => {
          row.data.name = 'Gogu'
        })
      },
      deleteRow (props) {
        props.rows.forEach(row => {
          this.instructorExamList.splice(row.index, 1)
        })
      },
      rowClick (row) {
        this.$router.push({path: '/library/exam/' + row.id})
        this.$router.cName = row.name
      },
      toggleList () {
        this.pageSpinner = true
        if (this.courseSectionToggle) {
          this.toggleLabel = 'By Section'
          if (this.bySectionList && this.bySectionList[0] && this.bySectionList[0].sections && this.bySectionList[0].sections[0] && this.bySectionList[0].sections[0].id) {
            this.examApiCall(this.bySectionList[0].sections[0].id)
          }
        } else {
          this.toggleLabel = 'By Course'
          if (this.byCourseList && this.byCourseList[0] && this.byCourseList[0].id) {
            this.examApiCall(this.byCourseList[0].id)
          }
        }
      }
    }
  }
</script>

<style lang="stylus">

  #teaching table
    border-collapse: unset

  /*overwrites core-ui border-collapse that messes up multiple selection boxes on quasar data table*/

  #teaching .q-data-table
    border: none

  #teaching .q-data-table tbody tr
    cursor: pointer

  #teaching .q-data-table-toolbar.bottom-toolbar > div
    padding-left: 15px
    padding-right: 15px

  /*padding to fix pagination at bottom of table*/

  #teaching .q-data-table-toolbar.bottom-toolbar div.q-select
    padding-left: 15px

  /*padding to fix pagination at bottom of table*/

  #teaching .q-list + .q-list
    margin-top: 0

  /*overwrite quasar margin of 25px on two q-lists*/

  #teaching .center
    -webkit-box-align: center
    -ms-flex-align: center
    align-items: center

  #teaching .right-padding
    padding-right: 12px


</style>
