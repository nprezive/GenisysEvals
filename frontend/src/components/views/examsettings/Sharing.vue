<template>
  <div id="sharing">
    <div class="row">
      <div class="col-md-6">
        <div class="row">
          <div class="col-12">
            <q-card>
              <q-card-title class="bg-secondary text-white">
                Users Not Targeted
              </q-card-title>
              <q-card-main>
                <q-data-table
                  :data="notTargetedUsers"
                  :config="configNotTargetedUsers"
                  :columns="columnsNotTargetedUsers"
                  @rowclick="rowClickNotTargetedUsers"
                  class="mt-3">
                  <template slot="col-info" scope="cell">
                    <span class="">
                      <q-icon name="fa-info-circle fa-2x">
                        <q-tooltip>
                          <div class="row">
                            <div class="col-12">
                              Phone Number: {{cell.data.number}}
                            </div>
                          </div>
                          <div class="row">
                            <div class="col-12">
                              Information: {{cell.data.info}}
                            </div>
                          </div>
                        </q-tooltip>
                      </q-icon>
                    </span>
                  </template>
                </q-data-table>
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
                Targeted Users
              </q-card-title>
              <q-card-main>
                <q-data-table
                  :data="targetedUsers"
                  :config="configTargetedUsers"
                  :columns="columnsTargetedUsers"
                  @rowclick="rowClickTargetedUsers"
                  class="mt-3">
                  <template slot="col-settings" scope="cell">
                    <q-btn flat @click="changeSettingsIntercept">Sharing Settings</q-btn>
                  </template>
                </q-data-table>
              </q-card-main>
            </q-card>
          </div>
        </div>
      </div>
    </div>
    <q-modal ref="changeSettingsModal" :content-css="{minWidth: '30%', minHeight: '55%'}">
      <q-modal-layout header-class="bg-red">
        <div color="primary" slot="header">
          <h5 class="text-center">Sharing Settings For {{ selectedPerson.name }}</h5>
        </div>
        <div class="row p-3">
          <div class="col-12">
            <q-field helper="Leave blank to impose no limit">
              <q-datetime float-label="When to end sharing" v-model="selectedPerson.sharingSettings.date"
                          type="date"></q-datetime>
            </q-field>
            <q-list link dense no-border>
              <q-item tag="label" class="pl-0">
                <q-item-side>
                  <q-checkbox color="primary" v-model="selectedPerson.sharingSettings.settings"></q-checkbox>
                </q-item-side>
                <q-item-main>
                  <q-item-tile label>Exam Parameters and Settings
                  </q-item-tile>
                </q-item-main>
              </q-item>
              <q-item tag="label" class="pl-0">
                <q-item-side>
                  <q-checkbox color="secondary" v-model="selectedPerson.sharingSettings.results"></q-checkbox>
                </q-item-side>
                <q-item-main>
                  <q-item-tile label>Manage Results</q-item-tile>
                </q-item-main>
              </q-item>
              <q-item tag="label" class="pl-0">
                <q-item-side>
                  <q-checkbox color="negative" v-model="selectedPerson.sharingSettings.questions"></q-checkbox>
                </q-item-side>
                <q-item-main>
                  <q-item-tile label>Questions</q-item-tile>
                </q-item-main>
              </q-item>
              <q-item tag="label" class="pl-0">
                <q-item-side>
                  <q-checkbox color="primary" v-model="selectedPerson.sharingSettings.reports"></q-checkbox>
                </q-item-side>
                <q-item-main>
                  <q-item-tile label>Reports</q-item-tile>
                </q-item-main>
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

  export default {
    name: 'Sharing',
    props: ['settings'],
    data () {
      return {
        settingsFlag: false,
        selectedPerson: {
          sharingSettings: {
            date: new Date(2017, 7, 11),
            settings: false,
            results: false,
            questions: false,
            reports: false
          }
        },
        configNotTargetedUsers: {
          refresh: false,
          noHeader: false,
          columnPicker: false,
          leftStickyColumns: 0,
          rightStickyColumns: 0,
          bodyStyle: {
            height: '300px'
          },
          rowHeight: '50px',
          responsive: true,
          pagination: {
            rowsPerPage: 5,
            options: [5, 10, 15, 30]
          },
          messages: {
            noData: '<i>warning</i> No data available to show.',
            noDataAfterFiltering: '<i>warning</i> No results. Please refine your search terms.'
          }
        },
        configTargetedUsers: {
          refresh: false,
          noHeader: false,
          columnPicker: false,
          leftStickyColumns: 0,
          rightStickyColumns: 0,
          bodyStyle: {
            height: '300px'
          },
          rowHeight: '50px',
          responsive: true,
          pagination: {
            rowsPerPage: 5,
            options: [5, 10, 15, 30]
          },
          messages: {
            noData: '<i>warning</i> No data available to show.',
            noDataAfterFiltering: '<i>warning</i> No results. Please refine your search terms.'
          }
        },
        columnsNotTargetedUsers: [
          {
            label: 'W-Number',
            field: 'wnumber',
            width: '0px',
            filter: true,
            type: 'string'
          },
          {
            label: 'Username',
            field: 'username',
            width: '0px',
            filter: true,
            type: 'string'
          },
          {
            label: 'Name',
            field: 'name',
            width: '100px',
            filter: true,
            sort: true,
            type: 'string'
          }
        ],
        columnsTargetedUsers: [
          {
            label: 'W-Number',
            field: 'wnumber',
            width: '0px',
            filter: true,
            type: 'string'
          },
          {
            label: 'Username',
            field: 'username',
            width: '0px',
            filter: true,
            type: 'string'
          },
          {
            label: 'Name',
            field: 'name',
            width: '100px',
            filter: true,
            sort: true,
            type: 'string'
          },
          {
            label: 'Sharing',
            field: 'settings',
            width: '70px',
            type: 'string'
          }
        ],
        notTargetedUsers: [
          {
            wnumber: 1,
            name: 'Caden Mahoney',
            username: 'cadenmahoney',
            sharingSettings: {
              date: new Date(2017, 7, 11),
              settings: false,
              results: false,
              questions: false,
              reports: false
            }
          },
          {
            wnumber: 2,
            name: 'Collin Welker',
            username: 'collinwelker',
            sharingSettings: {
              date: new Date(2017, 7, 11),
              settings: false,
              results: false,
              questions: false,
              reports: false
            }
          },
          {
            wnumber: 3,
            name: 'Lance Ure',
            username: 'lanceure',
            sharingSettings: {
              date: new Date(2017, 7, 11),
              settings: false,
              results: false,
              questions: false,
              reports: false
            }
          }
        ],
        targetedUsers: [
          {
            wnumber: 4,
            name: 'Trevor Orgill',
            username: 'trevororgill',
            sharingSettings: {
              date: new Date(2017, 7, 11),
              settings: false,
              results: false,
              questions: false,
              reports: false
            }
          }
        ]
      }
    },
    mounted () {
//      TODO API call to get targeted users information via this.settings.targetedUsers id's
      console.log(this.settings)
    },
    methods: {
      rowClickNotTargetedUsers (row) {
        let toAdd = this.notTargetedUsers.filter(function (obj) {
          return obj.name === row.name
        })
        let toRemove = this.notTargetedUsers.findIndex(function (obj) {
          return obj.name === row.name
        })
        this.notTargetedUsers.splice(toRemove, 1)
        this.targetedUsers.push(toAdd[0])
      },
      rowClickTargetedUsers (row) {
        if (this.settingsFlag === false) {
          let toAdd = this.targetedUsers.filter(function (obj) {
            return obj.name === row.name
          })
          let toRemove = this.targetedUsers.findIndex(function (obj) {
            return obj.name === row.name
          })
          this.targetedUsers.splice(toRemove, 1)
          this.notTargetedUsers.push(toAdd[0])
        } else {
          this.selectedPerson = row // so modal has access to the selected persons settings
          this.$refs.changeSettingsModal.open()
        }
        this.settingsFlag = false
      },
      changeSettingsIntercept () {
        this.settingsFlag = true
      }
    }
  }
</script>
<style lang="stylus">

  #sharing .modal-content
    flex-direction: unset
    display: block
    border: none
    outline: none

  /*override several core-ui styles messing with quasar modal*/

  #sharing table
    border-collapse: unset

  /*overwrites core-ui border-collapse that messes up multiple selection boxes on quasar data table*/

  #sharing .q-data-table
    border: none

  #sharing .q-data-table tbody tr
    cursor: pointer

  #sharing .q-data-table-toolbar.bottom-toolbar div.q-select
    padding-left: 15px

  /*padding to fix pagination at bottom of table*/

</style>
