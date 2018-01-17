<template>
  <q-card flat>
    <q-card-title>
      Exams to be Deleted/Undeleted
    </q-card-title>
    <q-card-separator></q-card-separator>
    <q-card-main>
      <div class="row">
        <q-list class="col-md-6 col-lg-6 col-xl-6 col-sm-12 col-xs-12 text-center">
          <q-list-header>
            Exams that will be deleted
          </q-list-header>
          <q-item v-for="(exam, index) in selectedExams" :key="index" v-if="!exam.archived">
            <q-item-side icon="fa-minus-square"></q-item-side>
            <q-item-main>{{ exam.id }}.  {{ exam.name }}</q-item-main>
          </q-item>
        </q-list>
        <div></div>
        <q-list class="col-md-6 col-lg-6 col-xl-6 col-sm-12 col-xs-12 text-center">
          <q-list-header>
            Exams that will be undeleted
          </q-list-header>
          <q-item v-for="(exam, index) in selectedExams" :key="index" v-if="exam.archived">
            <q-item-side icon="fa-minus-square"></q-item-side>
            <q-item-main>{{ exam.id }}.  {{ exam.name }}</q-item-main>
          </q-item>
        </q-list>
        <div class="col-12 row">
          <div class="col-md-6 col-lg-6 col-xl-6 col-sm-12 col-xs-12 text-center mt-3">
            <q-btn color="negative" @click="deleteExams">Delete Selected Exam<span v-if="selectedExams.length > 1">s</span></q-btn>
          </div>
          <div class="col-md-6 col-lg-6 col-xl-6 col-sm-12 col-xs-12 text-center mt-3">
            <q-btn color="primary" @click="undeleteExams">Undelete Selected Exam<span v-if="selectedExams.length > 1">s</span></q-btn>
          </div>
        </div>
      </div>
    </q-card-main>
    <q-inner-loading :visible="spinner">
      <q-spinner-gears size="50px" color="primary"></q-spinner-gears>
    </q-inner-loading>
  </q-card>
</template>

<script>
  import {Toast} from 'quasar'

  export default {
    name: 'LibraryDelete',
    props: ['selectedExams', 'deletedExams', 'undeletedExams'],
    data () {
      return {
        spinner: false
      }
    },
    methods: {
      deleteExams () {
        let exams = []
        for (let i = 0; i < this.selectedExams.length; i++) {
          if (!this.selectedExams[i].archived) {
            exams.push(this.selectedExams[i])
          }
        }
        this.spinner = true
        this.$http({
          method: 'post',
          url: '/api/deleteexams/',
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
          if (this.selectedExams.length < 2) {
            Toast.create.warning('Exam Deleted')
          } else {
            Toast.create.warning('Exams Deleted')
          }
          this.deletedExams(exams)
          this.spinner = false
        }).catch(error => {
          console.log(error)
        })
      },
      undeleteExams () {
        let exams = []
        for (let i = 0; i < this.selectedExams.length; i++) {
          if (this.selectedExams[i]['archived']) {
            exams.push(this.selectedExams[i])
          }
        }
        this.spinner = true
        this.$http({
          method: 'post',
          url: '/api/undeleteexams/',
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
          if (this.selectedExams.length < 2) {
            Toast.create.positive('Exam Undeleted')
          } else {
            Toast.create.positive('Exams Undeleted')
          }
          this.undeletedExams(exams)
          this.spinner = false
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
