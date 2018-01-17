<template>
  <router-view v-if="checked"></router-view>
</template>

<script>
  import QuestionSets from '../views/library/InstructorQuestionSets.vue'
  import Exams from '../views/library/InstructorExams.vue'

  export default {
    name: 'Library',
    components: {
      QuestionSets,
      Exams
    },
    data () {
      return {
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
    }
  }
</script>
