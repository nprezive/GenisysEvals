<template>
  <div id="sites">
    <div class="row">
      <div class="col-md-6">
        <div class="row">
          <div class="col-12">
            <q-card>
              <q-card-title class="bg-secondary text-white">
                Sites Not Targeted
              </q-card-title>
              <q-card-main>
                <better-data-table
                  :rows="notTargetedTableRows"
                  :columns="notTargetedTableColumns"
                  :config="notTargetedTableConfig"
                  ref="notTargetedSitesTable"
                  @rowclick="rowClickSitesNotTargeted">
                  <template slot="name" scope="cell">
                    {{ cell.data }}
                    <q-tooltip :offset="[0, 5]">
                      <div class="row" v-if="cell.row.description">
                        <div class="col-12">
                          {{cell.row.description}}
                        </div>
                      </div>
                      <span v-else>No Information Available</span>
                    </q-tooltip>
                  </template>
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
                Targeted Sites
              </q-card-title>
              <q-card-main>
                <better-data-table
                  :rows="targetedTableRows"
                  :config="targetedTableConfig"
                  :columns="targetedTableColumns"
                  ref="targetedSitesTable"
                  @rowclick="rowClickSitesTargeted">
                  <template slot="enrollments" scope="cell">
                    <q-btn flat @click="showEnrollmentsIntercept()">
                      <q-icon name="fa-cog"></q-icon>
                      <q-tooltip>tooltip</q-tooltip>
                    </q-btn>
                  </template>
                  <template slot="name" scope="cell">
                    {{ cell.data }}
                    <q-tooltip :offset="[0, 5]">
                      <div class="row" v-if="cell.row.description">
                        <div class="col-12">
                          {{cell.row.description}}
                        </div>
                      </div>
                      <span v-else>No Information Available</span>
                    </q-tooltip>
                  </template>
                </better-data-table>
              </q-card-main>
            </q-card>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>

  import BetterDataTable from '../components/BetterDataTable.vue'
  import {Toast} from 'quasar'
  import _ from 'lodash'

  export default {
    name: 'Sites',
    props: ['settings', 'examID'],
    components: {
      BetterDataTable
    },
    data () {
      return {
        notTargetedTableConfig: {
          header: true,
          columnPicker: true,
          ajaxSearch: false,
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
            label: 'Name',
            field: 'name',
            sort: true,
            type: 'template'
          }
        ],
        targetedTableConfig: {
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
            label: 'Name',
            field: 'name',
            sort: true,
            type: 'template'
          }
        ]
      }
    },
    mounted () {
      this.getTargetedExamSites(this.settings.targetedSites)
      this.getAllExamSites(this.settings.targetedSites)
    },
    methods: {
      rowClickSitesNotTargeted (row) {
        let toRemove = this.notTargetedTableRows.findIndex(function (obj) {
          return obj.name === row.name
        })
        let toAdd = this.notTargetedTableRows.filter(function (obj) {
          return obj.name === row.name
        })
        if (toAdd.length === 1) {
          if (this.settings.targetedSites.indexOf(toAdd[0].id) === -1) {
            this.notTargetedTableRows.splice(toRemove, 1)
            this.targetedTableRows.push(toAdd[0])
            this.settings.targetedSites.push(toAdd[0].id)
          } else {
            Toast.create(toAdd[0].name + ' already targeted')
          }
        }
      },
      rowClickSitesTargeted (row) {
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
          this.settings.targetedSites.splice(this.settings.targetedSites.indexOf(toAdd[0].id), 1)
        }
      },
      notifyRevert (targetedContexts) {
        this.getTargetedExamSites(targetedContexts)
        this.getAllExamSites(targetedContexts)
      },
      getTargetedExamSites (siteids) {
        this.$refs.targetedSitesTable.tableSpinner = true
        this.$http({
          method: 'post',
          url: '/api/getexamsites/',
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          },
          data: {
            siteids: siteids
          }
        }).then(response => {
          if (response.status === 250) {
            this.$router.error = response.data
            this.$router.push({path: '/error'})
          }
          this.targetedTableRows = response.data
          this.$refs.targetedSitesTable.tableSpinner = false
        }).catch(error => {
          console.log(error)
        })
      },
      getAllExamSites (siteids) {
        this.$refs.notTargetedSitesTable.tableSpinner = true
        this.$http({
          method: 'post',
          url: '/api/allsites/',
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          },
          data: {
            siteids: siteids
          }
        }).then(response => {
          if (response.status === 250) {
            this.$router.error = response.data
            this.$router.push({path: '/error'})
          }
          this.notTargetedTableRows = response.data
          this.$refs.notTargetedSitesTable.tableSpinner = false
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
<style lang="stylus">

  #sites table
    border-collapse: unset

  /*overwrites core-ui border-collapse that messes up multiple selection boxes on quasar data table*/

  #sites .q-data-table
    border: none

  #sites .q-data-table tbody tr
    cursor: pointer

  #sites .q-data-table-toolbar.bottom-toolbar div.q-select
    padding-left: 15px

  /*padding to fix pagination at bottom of table*/

</style>
