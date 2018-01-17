<template>
  <router-view v-if="checked"></router-view>
</template>

<script>

  export default {
    name: 'ManageExam',
    data () {
      return {
        msg: 'Courses',
        user: null,
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
