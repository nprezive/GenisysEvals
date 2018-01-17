<template>
  <q-card flat>
    <q-card-title>
      Share Selected Exams
    </q-card-title>
    <q-card-separator></q-card-separator>
    <q-card-main>
      <div class="row">
        <q-list class="col-md-5 col-lg-5 col-xl-5 col-sm-12 col-xs-12 mr-3">
          <q-list-header>
            Exams to be shared
          </q-list-header>
          <q-item v-for="(exam, index) in selectedExams" :key="index">
            <q-item-side icon="fa-minus-square"></q-item-side>
            <q-item-main>{{ exam.id }}.  {{ exam.name }}</q-item-main>
          </q-item>
        </q-list>
        <q-field :error="searchError && terms.length > 0" error-label="Please enter at least 3 characters"
                 class="col-md-6 col-lg-6 col-xl-6 col-sm-12 col-xs-12"
                 helper="Enter Instructor's Name/Username/Id"
        >
          <q-search v-model="terms" placeholder="Select Instructor">
            <q-autocomplete @search="search" @selected="selected"></q-autocomplete>
          </q-search>
        </q-field>
      </div>
    </q-card-main>
    <q-inner-loading :visible="spinner">
      <q-spinner-gears size="50px" color="primary"></q-spinner-gears>
    </q-inner-loading>
  </q-card>
</template>

<script>
  import {ActionSheet, Toast} from 'quasar'

  export default {
    name: 'ExamShare',
    props: ['selectedExams', 'transferredExams'],
    data () {
      return {
        spinner: false,
        terms: '',
        searchSpinner: false,
        searchError: false
      }
    },
    methods: {
      search (terms, done) {
        this.searchError = false
        if (this.terms.length < 3) {
          this.searchError = true
          this.searchSpinner = false
          return done([])
        }
        this.searchSpinner = true
        this.$http({
          method: 'get',
          url: '/api/searchinstructor/' + terms
        }).then(response => {
          if (response.status === 250) {
            this.$router.error = response.data
            this.$router.push({path: '/error'})
          }
          this.searchSpinner = false
          let data = []
          for (let i = 0; i < response.data.length; i++) {
            data.push({
              id: response.data[i]['id'],
              label: response.data[i]['first_name'] + ' ' + response.data[i]['last_name'],
              value: response.data[i]['first_name'] + ' ' + response.data[i]['last_name'],
              sublabel: 'UserID: ' + response.data[i]['id'],
              username: response.data[i]['username']
            })
          }
          return done(data)
        }).catch(error => {
          console.log(error)
          return done([])
        })
      },
      selected (item) {
        let that = this
        ActionSheet.create({
          title: 'Once you share, ' + item.name + ' will have access to your exam.',
          actions: [
            {
              label: 'Share',
              icon: 'fa-share-square-o',
              handler: function () {
                that.spinner = true
                that.$http({
                  method: 'post',
                  url: '/api/shareexams/',
                  headers: {
                    'X-CSRFToken': that.getCookie('csrftoken')
                  },
                  data: {
                    exams: that.selectedExams,
                    instructor: item.username
                  }
                }).then(response => {
                  if (response.status === 250) {
                    that.$router.error = response.data
                    that.$router.push({path: '/error'})
                  }
                  if (that.selectedExams.length < 2) {
                    Toast.create.warning('Exam Shared')
                  } else {
                    Toast.create.warning('Exams Shared')
                  }
                  that.spinner = false
                }).catch(error => {
                  console.log(error)
                })
              }
            },
            {
              label: 'Cancel',
              icon: 'fa-times',
              handler: function () {
              }
            }
          ]
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
