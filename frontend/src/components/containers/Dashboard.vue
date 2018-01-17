<template>
  <div id="dashboard" class="app bg-light" v-if="checked">
    <q-layout id="nav-sidebar" ref="layout" view="hHr LpR fff" :left-breakpoint='breakpoint'>
      <app-header slot="header"></app-header>
      <div id="sidebar" slot="left">
        <sidebar></sidebar>
      </div>
      <main class="">
        <breadcrumb class="mb-0" :list="list"></breadcrumb>
        <div class="container-fluid py-3 main-content-padding">
          <router-view></router-view>
        </div>
      </main>
      <app-footer slot="footer" class="bg-white"></app-footer>
    </q-layout>
  </div>
</template>

<script>
  import AppHeader from './dashboard/Header'
  import Sidebar from './dashboard/Sidebar'
  import AppFooter from './dashboard/Footer'
  import Breadcrumb from './dashboard/Breadcrumb'
  import {eventBus} from '../../main'

  export default {
    name: 'full',
    components: {
      AppHeader,
      Sidebar,
      AppFooter,
      Breadcrumb
    },
    data () {
      return {
        checked: false,
        breakpoint: 1
      }
    },
    computed: {
      name () {
        return this.$route.name
      },
      list () {
        return this.$route.matched
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

      // if user is on small device set breakpoint so side navigation overlaps instead of pushing content
      if (window.innerWidth < 991) {
        this.breakpoint = 0
      }
    },
    created () {
      eventBus.$on('toggle', () => {
        this.$refs.layout.toggleLeft()
      })

      eventBus.$on('updateBreakpoint', (bkPoint) => {
        this.breakpoint = bkPoint
      })
    },
    methods: {
      logout: function () {
        this.$http({
          method: 'post',
          url: '/api/logout/',
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          }
        }).then(response => {
          if (response.status === 250) {
            this.$router.error = response.data
            this.$router.push({path: '/error'})
          }
          this.$router.push({path: '/login'})
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

<style lang="stylus">

  #dashboard .main-content-padding
    padding-left: 3%
    padding-right: 3%

</style>
