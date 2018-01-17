<template>
  <div class="h-100 bg-light column items-center no-wrap">
    <div class="row mt-auto mb-auto" v-if="settings">
      <div class="col-2 gt-sm"></div>
      <div class="col-md-8 col-sm-12">
        <exam-information-card :settings="settings" :showStartExamOptions="showStartExamOptions" :startExam="startExam"
                           :examStatus="examStatus"></exam-information-card>
      </div>
      <div class="col-2 gt-sm"></div>
    </div>
    <q-card v-if="examError" class="mt-auto mb-auto w-50 bg-white text-center">
      <q-card-title class="bg-negative text-white">
        You are not allowed to take this exam.
      </q-card-title>
      <q-card-separator></q-card-separator>
      <q-card-main>
        <div class="row">
          <div class="col-12">Reason you are unable to take exam: <b>{{ examError }}</b></div>
          <div class="col-12">Please contact your instructor for more information.</div>
          <div class="col-5"></div>
          <q-btn color="primary" class="col-2" @click="goBack">
            Home
          </q-btn>
          <div class="col-5"></div>
        </div>
      </q-card-main>
    </q-card>
  </div>
</template>

<script>
  import {
    Loading
  } from 'quasar'

  import ExamInformationCard from '../components/ExamInformationCard.vue'

  export default {
    props: ['startExam'],
    components: {
      ExamInformationCard
    },
    data () {
      return {
        showStartExamOptions: true,
        settings: false,
        examStatus: 'Unable to Take Exam',
        examError: ''
      }
    },
    mounted () {
//      Getting exam settings
      Loading.show({
        message: 'Checking Exam Status'
      })
      this.$http({
        method: 'get',
        url: '/api/exam/' + this.$route.params.id + '/resultstatus/'
      }).then(response => {
        Loading.hide()
        if (response.status === 250) {
          this.examError = response.data
        } else {
          this.examStatus = response.data
          Loading.show({
            message: 'Retrieving Exam Information'
          })
          this.$http({
            method: 'get',
            url: '/api/exam/' + this.$route.params.id + '/takeexamlanding/'
          }).then(response => {
            if (response.status === 250) {
              this.$router.error = response.data
              this.$router.push({path: '/error'})
            }
            Loading.hide()
            this.settings = response.data
          }).catch(error => {
            console.log(error)
          })
        }
      }).catch(error => {
        console.log(error)
      })
    }
  }
</script>

<style lang="stylus">
  .error-page
    .error-code
      height 50vh
      width 100%
      padding-top 15vh
      font-size 30vmax
      color rgba(255, 255, 255, .2)
      overflow hidden
    .error-card
      border-radius 2px
      margin-top -50px
      width 80vw
      max-width 600px
      padding 25px
      > i
        font-size 5rem
</style>
