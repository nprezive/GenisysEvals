<template>
  <div class="animated fadeIn">
    <table class="q-table responsive
                  table table-striped
                  table-hover
                  table-outline
                  hidden-sm-down">
      <thead class="bg-faded">
      <tr>
        <th class="text-center"><i class="icon-people"></i></th>
        <th>Name</th>
        <th>Position</th>
        <th class="text-center">Fee</th>
        <th class="text-center">Phone</th>
        <th class="text-center">Email</th>
        <th class="text-center">Address</th>
      </tr>
      </thead>
      <tbody>
      <tr>
        <td class="text-center">
          <div>
            <q-checkbox v-model="proctor.isDefault"></q-checkbox>
            <q-tooltip>Set Proctor As Default</q-tooltip>
          </div>
        </td>
        <td>
          <div class="text-center">{{ proctor.firstname }} {{ proctor.lastname }}</div>
          <div class="text-center">
            {{ proctor.registered }}
          </div>
        </td>
        <td class="text-center">{{ proctor.position }} - {{ proctor.institution }}</td>
        <td class="text-center">{{ proctor.fee }}</td>
        <td class="text-center">{{ proctor.phone }}</td>
        <td class="text-center">{{ proctor.email }}</td>
        <td class="text-center">{{ proctor.streetaddress }} {{ proctor.zip }}</td>
      </tr>
      </tbody>
    </table>
    <div class="row">
      <div class="col-sm-12 col-md-6 pr-2">
        <q-card-title class="m-0 bg-secondary text-white">Request a Exam</q-card-title>
        <q-card class="m-0">
        <q-card-main>
          <better-data-table striped hover
                             :rows="nonRequested"
                             :columns="examFields"
                             :config="configSitesNotTargeted"
                             @rowclick="nonRequestedTable">
            <template slot="name" scope="item">
              <q-tooltip :offset="[0, 5]">
                <div class="row">
                  <div class="col-12">
                    {{cell.data}}
                  </div>
                </div>
              </q-tooltip>
            </template>
          </better-data-table>
        </q-card-main>
          </q-card>
      </div>
      <div class="col-sm-12 col-md-6 pl-2">
        <q-card-title class="m-0 bg-primary">Requested Exams</q-card-title>
        <q-card class="m-0">
        <q-card-main>
          <better-data-table striped hover
                             :rows="requested"
                             :columns="examFields"
                             :config="configSitesNotTargeted"
                             @rowclick="emptyClick">
            <template slot="name" scope="item">
              <q-tooltip :offset="[0, 5]">
                <div class="row">
                  <div class="col-12">
                    {{cell.data}}
                  </div>
                </div>
              </q-tooltip>
            </template>
          </better-data-table>
        </q-card-main>
          </q-card>
      </div>
    </div>
  </div>
</template>
<script>
  import BetterDataTable from '../components/BetterDataTable'
  export default {
    name: 'Proctor',
    props: {
      proctor: {
        type: Object,
        twoWay: true
      },
      setDefaultProctor: {
        type: Function
      }
    },
    components: {
      BetterDataTable
    },
    data () {
      return {
        requested: [
          {
            id: 7,
            legacy_id: null,
            legacy_user_id: null,
            name: 'Cadens Exam',
            created: '2017-02-23T14:40:54.616000Z',
            archived: null,
            user_id: 1,
            exam_type_id: 1
          }
        ],
        nonRequested: [
          {
            id: 1,
            legacy_id: null,
            legacy_user_id: null,
            name: 'Collins Exam',
            created: '2017-02-23T14:40:54.616000Z',
            archived: null,
            user_id: 1,
            exam_type_id: 1,
            begin_date: '2017-02-23 11:59 PM',
            end_date: '2017-09-23 11:59 PM',
            sites: [
              'Remote Proctors', 'Math Lampros Hub', 'Student Union'
            ]
          },
          {
            id: 2,
            legacy_id: null,
            legacy_user_id: null,
            name: 'Collins 2nd Exam',
            created: '2017-05-12T10:05:03.025000Z',
            archived: null,
            user_id: 1,
            exam_type_id: 1
          },
          {
            id: 3,
            legacy_id: null,
            legacy_user_id: null,
            name: 'Collins 3rd Exam',
            created: '2017-05-12T10:05:03.025000Z',
            archived: null,
            user_id: 1,
            exam_type_id: 1
          },
          {
            id: 4,
            legacy_id: null,
            legacy_user_id: null,
            name: 'Trevors 1st Exam',
            created: '2017-05-12T10:05:03.025000Z',
            archived: null,
            user_id: 1,
            exam_type_id: 1
          },
          {
            id: 5,
            legacy_id: null,
            legacy_user_id: null,
            name: 'Trevors 2nd Exam',
            created: '2017-05-12T10:05:03.025000Z',
            archived: null,
            user_id: 1,
            exam_type_id: 1
          },
          {
            id: 6,
            legacy_id: null,
            legacy_user_id: null,
            name: 'Trevors 3rd Exam',
            created: '2017-05-12T10:05:03.025000Z',
            archived: null,
            user_id: 1,
            exam_type_id: 1
          }
        ],
        examFields: [
          {
            label: 'Exam Name',
            sort: true,
            field: 'name',
            type: 'string'
          },
          {
            label: 'Created',
            sort: true,
            field: 'created',
            type: 'string'
          }
        ],
        configSitesNotTargeted: {
          title: 'Table Title',
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
        perPage: 5,
        filter: null,
        requestCurrentPage: 1,
        requestedCurrentPage: 1,
        size: 'small',
        page: 1,
        minPages: 1,
        maxPages: 3,
        ClickFlag: false,
        targetedTableRows: [],
        notTargetedTableRows: [],
        selectedEnrollment: {}
      }
    },
    methods: {
      nonRequestedTable (row) {
        let toAdd = this.nonRequested.filter(function (obj) {
          return obj.name === row.name
        })
        let toRemove = this.nonRequested.findIndex(function (obj) {
          return obj.name === row.name
        })
        this.nonRequested.splice(toRemove, 1)
        this.requested.push(toAdd[0])
      },
      requestedTable (row) {
        let toAdd = this.requested.filter(function (obj) {
          return obj.name === row.name
        })
        let toRemove = this.requested.findIndex(function (obj) {
          return obj.name === row.name
        })
        this.requested.splice(toRemove, 1)
        this.nonRequested.push(toAdd[0])
      },
      emptyClick () {}
    }
  }
</script>
<style>
  *,
  *::before,
  *::after {
    box-sizing: border-box;
  }
  html {
    font-size: 100%;
  }
</style>
