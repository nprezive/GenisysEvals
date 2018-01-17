<template>
  <div class="app" v-if="checked">
    <div class="app-body">
      <main class="main">
        <div class="takeexam h-100">
          <router-view :nullResult="nullResult" :outOfTime="outOfTime" :timeLimit='timeLimit' :timer="timer" :result="result" :startExam="startExam" :error="error" :loadForbidden="loadForbidden"></router-view>
        </div>
      </main>
    </div>
  </div>
</template>

<script>
  import {
    Loading
  } from 'quasar'

  export default {
    name: 'full',
    data () {
      return {
        msg: 'TakeExam',
        result: null,
        error: 'There was an error starting your exam.',
        timer: 0,
        timeLimit: '',
        ended: false,
        checked: false
      }
    },
    mounted () {
      this.$http({
        method: 'post',
        url: '/api/isloggedin/'
      }).then(response => {
        if (response.status === 200) {
          this.checked = true
        }
        if (response.status === 250) {
          this.$router.push({ path: '/login' })
        }
      }).catch(error => {
        console.log(error)
      })
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
      startExam () {
        Loading.show({
          message: 'Starting Exam'
        })
        // Create/get result
        this.$http({
          method: 'post',
          url: '/api/getresult/',
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          },
          data: {
            exam_id: this.$route.params.id
          }
        }).then(response => {
          if (response.status === 250) {
            this.$router.error = response.data
            this.$router.push({path: '/error'})
          }
          Loading.hide()
          if (response.status === 250) {
            this.error = response.data
            this.$router.push({path: '/takeexam/error/'})
          } else if (response.status === 200) {
            this.result = response.data['result']
            this.timer = {'hours': Math.floor(response.data['time'] / 60 / 60), 'minutes': Math.floor(response.data['time'] / 60 % 60), 'seconds': Math.floor(response.data['time'] % 60)}
            if (response.data['timeLimit'] === null) {
              this.timeLimit = 0
            } else {
              this.timeLimit = response.data['timeLimit']
            }
            this.$router.push({path: '/takeexam/exam/' + this.$route.params.id})
          }
        }).catch(error => {
          console.log(error)
        })
      },
      outOfTime () {
        this.error = 'Your Exam Has Been Submitted'
        this.ended = true
      },
      loadForbidden (error) {
        this.error = error
        this.$router.push({path: '/takeexam/error/'})
      },
      nullResult () {
        this.result = ''
      }
    }
  }
</script>

<style lang="stylus">
  @media (max-width: 991px)
    .app-body
      margin-top 0
</style>
