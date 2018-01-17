<template>
  <q-stepper ref="stepper" v-model="currentStep">
    <q-step name="settings" title="Select Settings">
      <div class="row">
        <div class="col-4">Name</div>
        <div class="col-2"></div>
        <div class="col-3">From</div>
        <div class="col-3">To</div>
        <q-field class="col-4" :error="nameError" error-label="Please Enter Exam Name">
          <q-input v-model="examName"></q-input>
        </q-field>
        <div class="col-2"></div>
        <q-datetime-range class="col-6" type="datetime" v-model="newDate" no-clear></q-datetime-range>
      </div>
      <q-stepper-navigation>
        <q-btn color="primary" @click="switchStep">Next</q-btn>
      </q-stepper-navigation>
    </q-step>
    <q-step name="audience" title="Select Exam Audience">
      <div class="row">
        <div class="col-xl-4 col-lg-4 col-md-4 col-sm-12 col-xs-12" style="max-height: 400px; overflow-y: scroll">
          <div v-if="newAudience.length < 1">No Audience Selected</div>
          <q-list highlight v-if="newAudience.length > 0" no-border>
            <q-list-header class="text-center">Selected Audiences</q-list-header>
            <q-item v-for="(lc, lindex) in newAudience" :key="lindex">
              <q-item-main class="cursor-pointer" @click="removeLC(lc)">
                {{ lc.name }}
              </q-item-main>
            </q-item>
          </q-list>
        </div>
        <better-data-table
          class="col-xl-8 col-lg-8 col-md-8 col-sm-12 col-xs-12"
          style="border-top: 1px black solid"
          :rows="newAudienceRows"
          :columns="newAudienceColumns"
          :config="newAudienceConfig"
          :ajaxCall="newAudienceAjax"
          @rowclick="newAudienceRowClick">
        </better-data-table>
      </div>
      <q-stepper-navigation>
        <q-btn flat @click="currentStep='settings'">Back</q-btn>
        <q-btn color="primary" @click="switchStep">Next</q-btn>
      </q-stepper-navigation>
    </q-step>
    <q-step name="sites" title="Select Where Exam Is Available">
      <div class="row">
        <div class="col-xl-4 col-lg-4 col-md-4 col-sm-12 col-xs-12" style="max-height: 400px; overflow-y: scroll;">
          <div v-if="newSites.length < 1">No Sites Selected</div>
          <q-list highlight v-if="newSites.length > 0" no-border>
            <q-list-header class="text-center">Selected Audiences</q-list-header>
            <q-item v-for="(site, sindex) in newSites" :key="sindex">
              <q-item-main class="cursor-pointer" @click="removeSite(site)">
                {{ site.name }}
              </q-item-main>
            </q-item>
          </q-list>
        </div>
        <better-data-table
          class="col-xl-8 col-lg-8 col-md-8 col-sm-12 col-xs-12"
          style="border-top: 1px black solid"
          :rows="newSitesRows"
          :columns="newSitesColumns"
          :config="newSitesConfig"
          @rowclick="newSitesRowClick">
        </better-data-table>
      </div>
      <q-stepper-navigation>
        <q-btn flat @click="currentStep='audience'">Back</q-btn>
        <q-btn color="primary" @click="createExam">Create</q-btn>
      </q-stepper-navigation>
    </q-step>
  </q-stepper>
</template>

<script>
  import moment from 'moment'
  import BetterDataTable from '../components/BetterDataTable.vue'
  import {Toast} from 'quasar'

  export default {
    name: 'LibraryCreateExam',
    components: {
      BetterDataTable
    },
    data () {
      return {
        currentStep: 'settings',
        examName: '',
        nameError: false,
        stepperError: false,
        newDate: {to: moment().format(), from: moment().format()},
        newAudience: [],
        newAudienceConfig: {
          title: 'Click to target a section.',
          header: true,
          columnPicker: true,
          ajaxSearch: true,
          bodyStyle: {
            height: '210px'
          },
          rowHeight: '30px',
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
        newAudienceColumns: [
          {
            label: 'ID',
            field: 'id',
            sort: false,
            type: 'string'
          },
          {
            label: 'Name',
            field: 'name',
            sort: false,
            type: 'string'
          }
        ],
        newAudienceRows: [],
        spinner: false,
        newSites: [],
        newSitesConfig: {
          title: 'Click to target a site.',
          header: true,
          columnPicker: true,
          ajaxSearch: false,
          bodyStyle: {
            height: '210px'
          },
          rowHeight: '30px',
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
        newSitesColumns: [
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
        newSitesRows: []
      }
    },
    mounted () {
      this.$http({
        method: 'get',
        url: '/api/getsites/'
      }).then(response => {
        if (response.status === 250) {
          this.$router.error = response.data
          this.$router.push({path: '/error'})
        }
        this.newSitesRows = response.data
      }).catch(error => {
        console.log(error)
      })
    },
    methods: {
      switchStep () {
        this.nameError = false
        if (this.currentStep === 'settings') {
          if (this.examName.length < 1) {
            this.nameError = true
          } else {
            this.currentStep = 'audience'
          }
        } else if (this.currentStep === 'audience') {
          this.currentStep = 'sites'
        } else if (this.currentStep === 'sites') {
        }
      },
      removeLC (lc) {
        for (let i = 0; i < this.newAudience.length; i++) {
          if (lc.id === this.newAudience[i].id) {
            this.newAudience.splice(i, 1)
          }
        }
      },
      newAudienceAjax (searchTerm, page, rowsPerPage, ordering) {
        this.spinner = true
        if (searchTerm) {
          this.$http({
            method: 'get',
            url: '/api/getlibraryaudience?page=' + page + '&page_size=' + rowsPerPage + '&search=' + searchTerm + '&ordering=' + ordering
          }).then(response => {
            if (response.status === 250) {
              this.$router.error = response.data
              this.$router.push({path: '/error'})
            }
            this.spinner = false
            this.newAudienceConfig.pagination.itemCount = response.data.count
            this.newAudienceRows = response.data.results
          }).catch(error => {
            console.log(error)
          })
        } else {
          this.$http({
            method: 'get',
            url: '/api/getlibrarydefaultaudience?page=' + page + '&page_size=' + rowsPerPage + '&ordering=' + ordering
          }).then(response => {
            if (response.status === 250) {
              this.$router.error = response.data
              this.$router.push({path: '/error'})
            }
            this.spinner = false
            this.newAudienceConfig.pagination.itemCount = response.data.count
            this.newAudienceRows = response.data.results
          }).catch(error => {
            console.log(error)
          })
        }
      },
      newAudienceRowClick (row) {
        let inside = false
        for (let i = 0; i < this.newAudience.length; i++) {
          if (row.id === this.newAudience[i].id) {
            inside = true
          }
        }
        if (!inside) {
          this.newAudience.push(row)
        } else {
          Toast.create.warning(row.name + ' is already selected.')
        }
      },
      newSitesRowClick (row) {
        let inside = false
        for (let i = 0; i < this.newSites.length; i++) {
          if (row.id === this.newSites[i].id) {
            inside = true
          }
        }
        if (!inside) {
          this.newSites.push(row)
        } else {
          Toast.create.warning(row.name + ' is already selected.')
        }
      },
      removeSite (site) {
        for (let i = 0; i < this.newSites.length; i++) {
          if (site.id === this.newSites[i].id) {
            this.newSites.splice(i, 1)
          }
        }
      },
      createExam () {
        let sites = []
        for (let i = 0; i < this.newSites.length; i++) {
          sites.push(this.newSites[i]['id'])
        }
        let audience = []
        for (let i = 0; i < this.newAudience.length; i++) {
          audience.push(this.newAudience[i]['id'])
        }
        let exam = {name: this.examName, audience: audience, sites: sites, date: this.newDate}
        exam['date']['from'] = moment(exam['date']['from']).format()
        exam['date']['to'] = moment(exam['date']['to']).format()
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
          this.spinner = false
          this.$router.cName = this.examName
          this.$router.push({path: '/library/exam/' + response.data})
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
