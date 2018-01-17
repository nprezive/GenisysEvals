<template>
  <q-card flat class="relative-position">
    <q-card-title>
      Edit Audience to Selected Exams
    </q-card-title>
    <q-card-separator></q-card-separator>
    <q-card-main>
      <div class="row">
        <div class="col-xl-4 col-lg-4 col-md-12 col-sm-12 col-xs-12">
          <h6 class="text-center">Remove Audience</h6>
          <q-card-separator></q-card-separator>
          <div v-for="(exam, index) in selectedExams" :key="index">
            <q-collapsible :label="'ID:' + exam.id + '  ' + exam.name">
              <q-list highlight>
                <q-item v-for="(lc, lindex) in exam.audience" :key="lindex">
                  <q-item-main class="cursor-pointer" @click="removedLC(lc, exam)">
                    {{ lc.name }}
                  </q-item-main>
                </q-item>
              </q-list>
            </q-collapsible>
            <q-card-separator></q-card-separator>
          </div>
        </div>
        <div class="col-xl-8 col-lg-8 col-md-12 col-sm-12 col-xs-12">
          <h6 class="text-center">Add Audience</h6>
          <better-data-table
            :rows="addAudienceRows"
            :columns="addAudienceColumns"
            :config="addAudienceConfig"
            :ajaxCall="addAudienceAjax"
            @rowclick="addAudienceRowClick">
          </better-data-table>
        </div>
      </div>
    </q-card-main>
    <q-inner-loading :visible="spinner">
      <q-spinner-gears size="50px" color="primary"></q-spinner-gears>
    </q-inner-loading>
  </q-card>
</template>

<script>
  import BetterDataTable from '../components/BetterDataTable.vue'
  import {Toast} from 'quasar'

  export default {
    name: 'LibraryAudience',
    props: ['selectedExams', 'changeLC'],
    components: {
      BetterDataTable
    },
    data () {
      return {
        spinner: false,
        addAudienceConfig: {
          title: 'This will add to all selected exams.',
          header: true,
          columnPicker: true,
          ajaxSearch: true,
          bodyStyle: {
            height: '300px'
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
        addAudienceColumns: [
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
        addAudienceRows: []
      }
    },
    methods: {
      addAudienceAjax (searchTerm, page, rowsPerPage, ordering) {
        if (searchTerm) {
          this.$http({
            method: 'get',
            url: '/api/getlibraryaudience?page=' + page + '&page_size=' + rowsPerPage + '&search=' + searchTerm + '&ordering=' + ordering
          }).then(response => {
            if (response.status === 250) {
              this.$router.error = response.data
              this.$router.push({path: '/error'})
            }
            this.addAudienceConfig.pagination.itemCount = response.data.count
            this.addAudienceRows = response.data.results
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
            this.addAudienceConfig.pagination.itemCount = response.data.count
            this.addAudienceRows = response.data.results
          }).catch(error => {
            console.log(error)
          })
        }
      },
      addAudienceRowClick (row) {
        this.spinner = true
        this.$http({
          method: 'post',
          url: '/api/learningcontext/' + row.id + '/targetExams/',
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          },
          data: {
            exams: this.selectedExams
          }
        }).then(response => {
          if (response.status === 250) {
            this.$router.error = response.data
            this.$router.push({path: '/error'})
          }
          this.spinner = false
          this.changeLC(this.selectedExams, row, false)
          let that = this
          Toast.create.positive({
            html: row.name + 'has been added to exams.',
            timeout: 2500,
            color: '#fff',
            bgColor: 'white',
            button: {
              label: 'Undo',
              handler () {
                that.spinner = true
                that.$http({
                  method: 'post',
                  url: '/api/learningcontext/' + row.id + '/untargetExams/',
                  headers: {
                    'X-CSRFToken': that.getCookie('csrftoken')
                  },
                  data: {
                    exams: that.selectedExams
                  }
                }).then(response => {
                  if (response.status === 250) {
                    that.$router.error = response.data
                    that.$router.push({path: '/error'})
                  }
                  that.spinner = false
                  that.changeLC(that.selectedExams, row, true)
                  Toast.create.warning('Undone')
                }).catch(error => {
                  console.log(error)
                })
              },
              color: '#fff'
            }
          })
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
      },
      removedLC (lc, exam) {
        let that = this
        this.spinner = true
        this.$http({
          method: 'post',
          url: '/api/learningcontext/' + lc.id + '/untargetExams/',
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          },
          data: {
            exams: [exam]
          }
        }).then(response => {
          if (response.status === 250) {
            this.$router.error = response.data
            this.$router.push({path: '/error'})
          }
          this.spinner = false
          this.changeLC([exam], lc, true)
          Toast.create.negative({
            html: lc.id + ' has been removed from ' + exam.name,
            timeout: 2500,
            color: '#fff',
            bgColor: 'white',
            button: {
              label: 'Undo',
              handler () {
                that.spinner = true
                that.$http({
                  method: 'post',
                  url: '/api/learningcontext/' + lc.id + '/targetExams/',
                  headers: {
                    'X-CSRFToken': that.getCookie('csrftoken')
                  },
                  data: {
                    exams: [exam]
                  }
                }).then(response => {
                  if (response.status === 250) {
                    that.$router.error = response.data
                    that.$router.push({path: '/error'})
                  }
                  that.spinner = false
                  that.changeLC([exam], lc, false)
                  Toast.create.warning('Undone')
                }).catch(error => {
                  console.log(error)
                })
              },
              color: '#fff'
            }
          })
        }).catch(error => {
          console.log(error)
        })
      }
    }
  }
</script>
