<template>
  <div class="SiteOptions" v-if="stations && siteOptions">
    <q-tabs align="justify" inverted style="background-color: white;" class="m-3">
      <q-tab default slot="title" name="Site Info">Site Info</q-tab>
      <q-tab slot="title" name="Computers">Computers</q-tab>

      <q-tab-pane name="Site Info" class="p-3">
        <div class="row">
          <q-field class="col-6"
          >
            <q-input v-model="site.name" float-label="Site Name" ></q-input>
          </q-field>
          <q-field class="col-6"
          >
            <q-input v-model="siteOptions.location" float-label="Location" ></q-input>
          </q-field>
        </div>
        <div class="row">
          <q-field class="col-12" :count="256" :max="256" :error="site.description.length > 256" error-label="Description too long."
          >
            <q-input type="textarea" v-model="site.description" float-label="Description" ></q-input>
          </q-field>
        </div>
        <div class="row">
          <q-field class="col-12" :count="256" :max="256" :error="siteOptions.contact.length > 256" error-label="Contact Info too long."
          >
            <q-input type="textarea" v-model="siteOptions.contact" float-label="Contact Info" ></q-input>
          </q-field>
        </div>
        <div class="row">
          <q-field class="col-6 ml-auto mr-auto">
            <q-select v-model="siteOptions.manager" :options="availableManagers" float-label="Site Manager"></q-select>
          </q-field>
        </div>
        <div class="row">
          <h5 class="ml-auto mr-auto">
            Available Exams
          </h5>
        </div>
        <div class="row">
          <q-toggle class="col-4" v-model="siteOptions.examtype.online" label="Online"></q-toggle>
          <q-toggle class="col-4" v-model="siteOptions.examtype.scantron" label="Scantron"></q-toggle>
          <q-toggle class="col-4" v-model="siteOptions.examtype.paper" label="Paper"></q-toggle>
        </div>
        <div class="row">
          <q-toggle class="col-4" v-model="siteOptions.examtype.survey" label="Survey"></q-toggle>
          <q-toggle class="col-4" v-model="siteOptions.examtype.eval" label="Evaluations"></q-toggle>
        </div>
        <div class="row">
          <h5 class="ml-auto mr-auto col-6">
            Review Allowed at Site
          </h5>
          <h5 class="ml-auto mr-auto col-6">
            Show Student Picture on Check-In
          </h5>
        </div>
        <div class="row">
          <q-toggle class="ml-auto mr-auto col-6" v-model="siteOptions.review"></q-toggle>
          <q-toggle class="ml-auto mr-auto col-6" v-model="siteOptions.studentpicture"></q-toggle>
        </div>
        <div class="row">
          <h5 class="ml-auto mr-auto col-6">
            Ignore Holds on User's Account
          </h5>
          <h5 class="ml-auto mr-auto col-6">
            Exit Browser on Student Logout
          </h5>
        </div>
        <div class="row">
          <q-toggle class="ml-auto mr-auto col-6" v-model="siteOptions.ignoreholds"></q-toggle>
          <q-toggle class="ml-auto mr-auto col-6" v-model="siteOptions.exitonlogout"></q-toggle>
        </div>
      </q-tab-pane>
      <q-tab-pane name="Computers">
        <q-data-table
          highlight
          :data="stations"
          :config="config"
          :columns="columns"
          @refresh="refresh"
          @selection="selection"
          @rowclick="rowClick"
        >
          <template slot="col-name" scope="cell">
            <q-field
            >
              <q-input v-model.sync="cell.data" float-label="Station Name" ></q-input>
            </q-field>
          </template>
          <template slot="col-ip" scope="cell">
            <q-field
            >
              <q-input v-model.sync="cell.data" float-label="Station IP" ></q-input>
            </q-field>
          </template>
          <template slot="selection" scope="props">
            <q-btn flat color="primary" @click="changeMessage(props)">
              <q-icon name="edit"></q-icon>
            </q-btn>
            <q-btn flat color="primary" @click="deleteRow(props)">
              <q-icon name="delete"></q-icon>
            </q-btn>
          </template>
        </q-data-table>
      </q-tab-pane>
    </q-tabs>
  </div>
</template>
<script>

  export default {
    name: 'SiteOptions',
    props: {
      site: {
        type: Object,
        required: true
      },
      stations: {
        type: Array
      }
    },
    data () {
      return {
        siteOptions: false,
        config: {
          title: '',
          refresh: true,
          noHeader: true,
          columnPicker: true,
          leftStickyColumns: 0,
          rightStickyColumns: 0,
          bodyStyle: {
            maxHeight: '500px'
          },
          rowHeight: '100px',
          responsive: true,
          pagination: {
            rowsPerPage: 5,
            options: [5, 10, 15, 30, 50, 500]
          }
        },
        columns: [
          {
            label: 'ID',
            field: 'id',
            width: '120px',
            filter: false,
            sort: true,
            type: 'number'
          },
          {
            label: 'Station Name',
            field: 'name',
            width: '300px',
            filter: false,
            sort: true,
            type: 'string'
          },
          {
            label: 'IP/Host',
            field: 'ip',
            width: '80px',
            sort: false,
            type: 'number'
          }
        ]
      }
    },
    mounted () {
      // API Call for siteOptions
      this.$http({
        method: 'get',
        url: '/api/site/' + this.site.id + '/siteoptions/'
      }).then(response => {
        if (response.status === 250) {
          this.$router.error = response.data
          this.$router.push({path: '/error'})
        }
        if (response.data !== '') {
          this.siteOptions = response.data
        } else {
          this.siteOptions = {
            manager: '',
            description: '',
            contact: '',
            location: '',
            examtype: {online: false, paper: false, survey: false, eval: false, scantron: false},
            review: false,
            studentpicture: false,
            ignoreholds: false,
            exitonlogout: false
          }
        }
      }).catch(error => {
        console.log(error)
      })
    },
    computed: {
      availableManagers () {
//         Get available site managers
        let APICall = [{
          value: 'Trevor',
          label: 'Trevor'
        }, {
          value: 'Cody',
          label: 'Cody'
        }, {
          value: 'Collin',
          label: 'Collin'
        }, {
          value: 'Lance',
          label: 'Lance'
        }, {
          value: 'Tom',
          label: 'Tom'
        }, {
          value: 'Caden',
          label: 'Caden'
        }]
        return APICall
      }
    },
    methods: {
      refresh (done) {
        this.timeout = setTimeout(() => {
          done()
        }, 3000)
      },
      selection (number, rows) {
      },
      rowClick () {
      },
      updateSiteOptions (id) {
        this.siteOptions = false
        // API Call for siteOptions
        this.$http({
          method: 'get',
          url: '/api/site/' + id + '/siteoptions/'
        }).then(response => {
          if (response.status === 250) {
            this.$router.error = response.data
            this.$router.push({path: '/error'})
          }
          if (response.data !== '') {
            this.siteOptions = response.data
          } else {
            this.siteOptions = {
              manager: '',
              contact: '',
              location: '',
              examtype: {online: false, paper: false, survey: false, eval: false, scantron: false},
              review: false,
              studentpicture: false,
              ignoreholds: false,
              exitonlogout: false
            }
          }
        }).catch(error => {
          console.log(error)
        })
      }
    }
  }
</script>
<style lang="stylus">
  .SiteOptions .q-tabs-head {
    padding: 0 !important
  }

  .SiteOptions {
    background-color: #e4e5e6
  }

  .SiteOptions .q-tab-pane {
    padding: 0
  }
</style>
