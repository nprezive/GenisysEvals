<template>
  <q-card flat>
    <q-card-title>
      Change To and From Dates of Selected Exams
    </q-card-title>
    <q-card-separator></q-card-separator>
    <q-card-main>
      <div v-for="(exam, index) in selectedExams" :key="index">
        <q-collapsible :label="'ID:' + exam.id + '  ' + exam.name">
          <q-datetime-range type="datetime" v-model="newDate[index]"></q-datetime-range>
        </q-collapsible>
        <q-card-separator></q-card-separator>
      </div>
      <q-btn flat color="primary" class="m-3 float-right" @click="saveDates">Save Dates</q-btn>
    </q-card-main>
    <q-inner-loading :visible="spinner">
      <q-spinner-gears size="50px" color="primary"></q-spinner-gears>
    </q-inner-loading>
  </q-card>
</template>

<script>
  import {Toast} from 'quasar'
  import moment from 'moment'

  export default {
    name: 'LibraryDate',
    props: ['selectedExams', 'changeDates'],
    data () {
      return {
        newDate: [],
        spinner: false
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
      saveDates () {
        let exams = []
        for (let i = 0; i < this.selectedExams.length; i++) {
          let examDate = this.selectedExams[i]['daterange'].split(' to ')
          let to = moment(examDate[1]).format()
          let from = moment(examDate[0]).format()
          exams.push({
            id: this.selectedExams[i]['id'],
            date: {'to': moment(this.newDate[i]['to']).format(), 'from': moment(this.newDate[i]['from']).format()},
            oldDate: {'to': to, 'from': from}})
        }
        this.spinner = true
        this.$http({
          method: 'post',
          url: '/api/savelibrarydates',
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          },
          data: {
            exams: exams
          }
        }).then(response => {
          if (response.status === 250) {
            this.$router.error = response.data
            this.$router.push({path: '/error'})
          }
          this.changeDates(exams, false)
          this.spinner = false
          let that = this
          Toast.create.positive({
            html: 'Dates Saved',
            timeout: 2500,
            color: '#fff',
            bgColor: 'white',
            button: {
              label: 'Undo',
              handler () {
                that.spinner = true
                that.$http({
                  method: 'post',
                  url: '/api/revertlibrarydates',
                  headers: {
                    'X-CSRFToken': that.getCookie('csrftoken')
                  },
                  data: {
                    exams: exams
                  }
                }).then(response => {
                  if (response.status === 250) {
                    that.$router.error = response.data
                    that.$router.push({path: '/error'})
                  }
                  that.spinner = false
                  that.changeDates(exams, true)
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
