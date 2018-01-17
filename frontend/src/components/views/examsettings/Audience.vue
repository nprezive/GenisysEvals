<template>
  <div id="audience">
    <div class="row">
      <div class="col-md-6">
        <div class="row">
          <div class="col-12">
            <q-card>
              <q-card-title class="bg-secondary text-white">
                Associations Not Targeted
              </q-card-title>
              <q-card-main>
                <better-data-table
                  :rows="notTargetedTableRows"
                  :columns="notTargetedTableColumns"
                  :config="notTargetedTableConfig"
                  :ajaxCall="ajaxCall"
                  @rowclick="rowClickNotTargetedTable"
                  ref="notTargetedLearningContextTable">
                </better-data-table>
              </q-card-main>
            </q-card>
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <div class="row">
          <div class="col-12">
            <q-card>
              <q-card-title class="bg-primary">
                Associations Targeted
              </q-card-title>
              <q-card-main>
                <better-data-table
                  :rows="targetedTableRows"
                  :config="targetedTableConfig"
                  :columns="targetedTableColumns"
                  @rowclick="rowClickTargetedTable"
                  ref="targetedLearningContextTable">
                  <template slot="enrollments" scope="cell">
                    <q-btn flat @click="showEnrollmentsIntercept()">
                      <q-icon name="fa-cog"></q-icon>
                      <q-tooltip>tooltip</q-tooltip>
                    </q-btn>
                  </template>
                </better-data-table>
              </q-card-main>
            </q-card>
          </div>
        </div>
      </div>
    </div>
    <q-modal id="changeSettingsModal" ref="changeSettingsModal" :content-css="{minWidth: '30%', minHeight: '55%'}">
      <q-modal-layout header-class="bg-red">
        <div color="primary" slot="header">
          <h5 class="text-center font-size-20">Enrollments For {{ selectedEnrollment.name }}</h5>
        </div>
        <div class="row p-3">
          <div class="col-12">
            <q-list highlight inset-separator no-border>
              <q-item v-for="(student, index) in enrollments" :key="index">
                <q-item-side :avatar="student.picture"></q-item-side>
                <q-item-main :label="student.name"></q-item-main>
                <q-item-side right :stamp="student.wnumber"></q-item-side>
              </q-item>
            </q-list>
          </div>
        </div>
        <div slot="footer">
          <div class="row m-2">
            <div class="col-12">
              <q-btn color="primary" class="start-exam-btn pull-right" @click="$refs.changeSettingsModal.close()">
                Done
              </q-btn>
            </div>
          </div>
        </div>
      </q-modal-layout>
    </q-modal>
  </div>
</template>
<script>

  import BetterDataTable from '../components/BetterDataTable.vue'
  import {Toast} from 'quasar'
  import _ from 'lodash'

  export default {
    name: 'Audience',
    props: ['settings', 'examID'],
    components: {
      BetterDataTable
    },
    data () {
      return {
        enrollmentClickFlag: false,
        selectedEnrollment: {},
        enrollments: [
          {
            name: 'John',
            wnumber: 'W1234567',
            picture: 'statics/img/misc/me.jpg'
          },
          {
            name: 'Jacob',
            wnumber: 'W4567123',
            picture: 'statics/img/misc/me.jpg'
          },
          {
            name: 'Jingleheimer',
            wnumber: 'W1234567',
            picture: 'statics/img/misc/me.jpg'
          },
          {
            name: 'Schmidt',
            wnumber: 'W7654321',
            picture: 'statics/img/misc/me.jpg'
          }
        ],
        notTargetedTableConfig: {
          title: 'Enter the subject code, course, number, crn, W#, or student name',
          header: true,
          columnPicker: true,
          ajaxSearch: true,
          bodyStyle: {
            height: '300px'
          },
          rowHeight: '55px',
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
        notTargetedTableRows: [],
        notTargetedTableColumns: [
          {
            label: 'ID',
            field: 'id',
            sort: true,
            type: 'string'
          },
          {
            label: 'Name',
            field: 'name',
            sort: true,
            type: 'string'
          }
        ],
        targetedTableConfig: {
          title: 'Enter the subject code, course, number, crn, W#, or student name',
          header: true,
          ajaxSearch: false,
          columnPicker: true,
          bodyStyle: {
            height: '300px'
          },
          rowHeight: '55px',
          pagination: {
            rowsPerPage: 5,
            options: [2, 5, 10, 15]
          },
          messages: {
            noData: '<i>warning</i> No data available to show.',
            noDataAfterFiltering: '<i>warning</i> No results. Please refine your search terms.'
          }
        },
        targetedTableRows: [],
        targetedTableColumns: [
          {
            label: 'ID',
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
            label: 'Enrollments',
            field: 'enrollments',
            type: 'template'
          }
        ]
      }
    },
    methods: {
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
      notifyRevert (targetedContexts) {
        this.getTargetedAudience(targetedContexts)
        this.$refs.notTargetedLearningContextTable.ajaxSearch()
      },
      getTargetedAudience (targetedContexts) {
        this.$refs.targetedLearningContextTable.tableSpinner = true
        this.$http({
          method: 'post',
          url: '/api/gettargetedaudience/',
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          },
          data: {
            learningcontextids: targetedContexts
          }
        }).then(response => {
          if (response.status === 250) {
            this.$router.error = response.data
            this.$router.push({path: '/error'})
          }
          this.targetedTableRows = response.data
          this.$refs.targetedLearningContextTable.tableSpinner = false
        }).catch(error => {
          console.log(error)
        })
      },
      ajaxCall (searchTerm, page, rowsPerPage, ordering) {
        this.$refs.notTargetedLearningContextTable.tableSpinner = true
        if (searchTerm) {
          this.$http({
            method: 'get',
            url: '/api/getsearchaudience/' + this.examID + '?search=' + searchTerm + '&page=' + page + '&page_size=' + rowsPerPage + '&ordering=' + ordering,
            headers: {}
          }).then(response => {
            if (response.status === 250) {
              this.$router.error = response.data
              this.$router.push({path: '/error'})
            }
            this.notTargetedTableConfig.pagination.itemCount = response.data.count
            this.notTargetedTableRows = response.data.results
            this.$refs.notTargetedLearningContextTable.tableSpinner = false
          }).catch(error => {
            console.log(error)
          })
        } else {
          this.$http({
            method: 'get',
            url: '/api/getdefaultaudience/' + this.examID + '?page=' + page + '&page_size=' + rowsPerPage + '&ordering=' + ordering,
            headers: {}
          }).then(response => {
            if (response.status === 250) {
              this.$router.error = response.data
              this.$router.push({path: '/error'})
            }
            this.notTargetedTableConfig.pagination.itemCount = response.data.count
            this.notTargetedTableRows = response.data.results
            this.$refs.notTargetedLearningContextTable.tableSpinner = false
          }).catch(error => {
            console.log(error)
          })
        }
      },
      rowClickNotTargetedTable (row) {
        let toRemove = this.notTargetedTableRows.findIndex(function (obj) {
          return obj.name === row.name
        })
        let toAdd = this.notTargetedTableRows.filter(function (obj) {
          return obj.name === row.name
        })
        if (toAdd.length === 1) {
          if (this.settings.targetedContexts.indexOf(toAdd[0].id) === -1) {
            this.notTargetedTableRows.splice(toRemove, 1)
            this.targetedTableRows.push(toAdd[0])
            this.settings.targetedContexts.push(toAdd[0].id)
          } else {
            Toast.create(toAdd[0].name + ' already targeted')
          }
        }
      },
      rowClickTargetedTable (row) {
        if (this.enrollmentClickFlag === false) {
          let toRemove = this.targetedTableRows.findIndex(function (obj) {
            return obj.name === row.name
          })
          let toAdd = this.targetedTableRows.filter(function (obj) {
            return obj.name === row.name
          })
          let duplicateObject = false
          if (toAdd.length === 1) {
            for (let i = 0; i < this.notTargetedTableRows.length; i++) {
              if (_.includes(this.notTargetedTableRows[i], toAdd[0].id)) {
                duplicateObject = true
              }
            }
            this.targetedTableRows.splice(toRemove, 1)
            if (!duplicateObject) {
              this.notTargetedTableRows.push(toAdd[0])
            }
            this.settings.targetedContexts.splice(this.settings.targetedContexts.indexOf(toAdd[0].id), 1)
          }
        } else {
          this.selectedEnrollment = row // so modal has access to course enrollments
          // TODO separate api call to get enrollments for this.selectedEnrollment.id
          this.$refs.changeSettingsModal.open()
        }
        this.enrollmentClickFlag = false
      },
      showEnrollmentsIntercept (that) {
        this.enrollmentClickFlag = true
      }
    }
  }
</script>
<style lang="stylus">

  #changeSettingsModal .modal-content
    flex-direction: unset
    display: block
    border: none
    outline: none

  /*override several core-ui styles messing with quasar modal*/

  #audience table
    border-collapse: unset

  /*overwrites core-ui border-collapse that messes up multiple selection boxes on quasar data table*/

  #audience .q-data-table
    border: none

  #audience .q-data-table tbody tr
    cursor: pointer

  #audience .q-data-table-toolbar.bottom-toolbar div.q-select
    padding-left: 15px

  /*padding to fix pagination at bottom of table*/

</style>
