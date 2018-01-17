<template>
  <div class="error-page window-height window-width bg-light column items-center no-wrap">
    <div class="error-code bg-primary flex items-center justify-center">
      250
    </div>
    <div>
      <div class="error-card shadow-4 bg-white column items-center justify-center no-wrap">
        <q-icon name="error_outline" color="grey-5"></q-icon>
        <p class="caption text-center">An Unexpected Error Has Occurred</p>
        <p>{{ $router.error }}</p>
        <p>Please Try Again Later</p>
        <p class="text-center group">
          <q-btn
            color="primary"
            push
            @click="navigate"
            icon-right="home"
          >
            Go home
          </q-btn>
        </p>
      </div>
    </div>
  </div>
</template>

<script>

  export default {
    components: {},
    data () {
      return {
        canGoBack: window.history.length > 1
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
          this.$router.push({path: '/login'})
        }
      }).catch(error => {
        console.log(error)
      })
    },
    beforeDestroy () {
      this.$router.error = ''
    },
    methods: {
      navigate () {
        this.$router.error = ''
        this.$router.push({path: '/courses'})
      }
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
