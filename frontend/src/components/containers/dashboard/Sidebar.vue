<template>
  <div id="sidebar">
    <div id="big-sidebar-content">
      <div class="sidebar-header">
        <img v-bind:src="userImage" class="image-avatar" alt="Avatar" @error="imageLoad"/>
        <!--<img v-else="" src="../../../statics/img/avatar.png" class="image-avatar" alt="Avatar"/>-->
        <div class="sidebar-user">
          <div><strong>{{userName}}</strong></div>
          <div class="text-muted">
            <small>{{wNumber}}</small>
          </div>
        </div>
        <div class="btn-group" role="group" aria-label="Button group with nested dropdown">
          <button type="button" class="btn btn-link">
            <i class="icon-user"></i>
          </button>
          <button type="button" class="btn btn-link" @click="loadSettings">
            <i class="icon-settings"></i>
          </button>
          <button type="button" class="btn btn-link cursor-pointer" @click="logout()">
            <i class="icon-logout"></i>
          </button>
        </div>
      </div>

      <ul  class="text-tertiary" >
        <li class="q-toolbar-title">
          Navigation
        </li>

        <q-side-link item class="cursor-pointer" :to="item.route" v-for="(item, index) in minSidebarData" :key="index">
          <i :class="item.iconClass"></i> {{ item.name }}
        </q-side-link>

        <li class="divider"></li>
      </ul>
    </div>

    <div class="hidden" id="small-sidebar-content">

      <div ref="target" @mouseenter="openUserPopover" @mouseleave="closeUserPopover">
        <img :src="userImage" class="avatar-min" alt="user" @error="imageLoad">
        <!--<img v-else="" src="../../../statics/img/avatar.png" class="avatar-min" alt="Avatar"/>-->
        <q-popover id="user-popover" class="cursor-pointer pop-nav pl-3 bg-blue-grey-10" anchor="top right" self="top left" ref="userPopover" @mouseleave.native="leaveUserPopover">
          <div class="sidebar-user">
            <div><strong>{{userName}}</strong></div>
            <div class="text-muted">
              <small>{{wNumber}}</small>
            </div>
          </div>
          <div class="btn-group" role="group" aria-label="Button group with nested dropdown">
            <button type="button" class="btn btn-link">
              <i class="icon-user"></i>
            </button>
            <button type="button" class="btn btn-link" @click="loadSettings">
              <i class="icon-settings"></i>
            </button>
            <button type="button" class="btn btn-link cursor-pointer" @click="logout()">
              <i class="icon-logout"></i>
            </button>
          </div>
        </q-popover>
      </div>

      <q-side-link item :to="item.route" v-for="(item, index) in minSidebarData" :key="index" color="tertiary" ref="target" @mouseenter.native="mouseEnter(item.ref)">
        <i :class=item.iconClass></i>
        <q-popover class="cursor-pointer pop-nav pl-3 bg-primary" @click.native="redirect(item.route)" @mouseleave.native="mouseLeave(item.ref)" anchor="top left" self="top left" :ref="item.ref">
          <div>
            <i :class=item.iconClass></i><span class="pl-4"> {{ item.name }} </span>
          </div>
        </q-popover>

      </q-side-link>

    </div>
  </div>
</template>
<script>
  import {eventBus} from '../../../main'
  import { Dialog, Toast } from 'quasar'

  export default {
    name: 'Sidebar',
    methods: {
      loadSettings () {
        let dialogContent = {
          title: 'Default Settings',
          form: {
            header1: {
              type: 'heading',
              label: 'Sort courses by: '
            },
            option: {
              type: 'radio',
              model: 'opt1',
              items: [
                {label: 'Course', value: 'opt1'},
                {label: 'Section', value: 'opt2'}
              ]
            },
            header2: {
              type: 'heading',
              label: 'Select the default number of rows in tables: '
            },
            slider: {
              type: 'slider',
              label: 'Default rows displayed',
              min: 5,
              max: 15,
              step: 5,
              withLabel: true,
              model: 5,
              color: 'primary'
            }
          },
          buttons: [
            'Cancel',
            {
              label: 'Save',
              handler (data) {
                Toast.create({
                  html: 'Defaults Updated',
                  color: 'white',
                  bgColor: 'grey'
                })
              }
            }
          ]
        }

        if (!this.isInstructor) {
          // does user have instructor role
          delete dialogContent.form['header1']
          delete dialogContent.form['option']
        }

        // display dialog
        Dialog.create(
          dialogContent
        )
      },
      imageLoad () {
        // replace image with avatar
        this.userImage = '../../../statics/img/avatar.png'
      },
      windowSizeChange () {
        // if width smaller than 991 make sidebar big
        if (window.innerWidth < 991) {
          document.getElementById('small-sidebar-content').classList.add('hidden')
          document.getElementById('big-sidebar-content').classList.remove('hidden')

          // make so that sidebar overlaps content instead of squeezing it to the side
          eventBus.updateBreakpoint(0)

          var elems = document.getElementsByTagName('aside')

          for (var i = 0; i < elems.length; i++) {
            elems[i].classList.add('big-sidebar-style')
            elems[i].classList.remove('small-sidebar-style')
          }
          this.smallSidebar = false
        } else {
          eventBus.updateBreakpoint(1)

          if (!this.sidebarDisplay) {
            eventBus.toggleSideNav()
            this.sidebarDisplay = !this.sidebarDisplay
          }
        }
      },
      redirect (path) {
        this.$router.push({path: path})
      },
      openUserPopover () {
        this.$refs.userPopover.open()
      },
      leaveUserPopover () {
        this.$refs.userPopover.close()
      },
      closeUserPopover () {

      },
      mouseLeave (element) {
        this.$refs[element][0].close()
      },
      mouseEnter (element) {
        this.$refs[element][0].open()
      },
      toggleSidebar () {
        if (window.innerWidth < 991) {
          this.sidebarDisplay = !this.sidebarDisplay
          eventBus.toggleSideNav()
          return
        }

        if (this.smallSidebar) {
          document.getElementById('small-sidebar-content').classList.add('hidden')
          document.getElementById('big-sidebar-content').classList.remove('hidden')
        } else {
          document.getElementById('big-sidebar-content').classList.add('hidden')
          document.getElementById('small-sidebar-content').classList.remove('hidden')
        }

        var elems = document.getElementsByTagName('aside')

        for (var i = 0; i < elems.length; i++) {
          if (this.smallSidebar) {
            elems[i].classList.add('big-sidebar-style')
            elems[i].classList.remove('small-sidebar-style')
          } else {
            elems[i].classList.add('small-sidebar-style')
            elems[i].classList.remove('big-sidebar-style')
          }
        }

        this.smallSidebar = !this.smallSidebar
      },
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
    },
    data () {
      return {
        user: {},
        wNumber: '',
        userImage: '',
        userName: '',
        smallSidebar: false,
        sidebarDisplay: true,
        isInstructor: false,
        minSidebarData: {
          courses: {name: 'My Courses', route: '/courses', ref: 'popoverCourses', iconClass: 'icon-note'},
          library: {name: 'Library', route: '/library', ref: 'popoverLibrary', iconClass: 'icon-folder'},
          proctoring: {name: 'Proctoring', route: '/proctoring', ref: 'popoverProctoring', iconClass: 'icon-globe'},
          results: {name: 'Results', route: '/results', ref: 'popoverResults', iconClass: 'icon-pie-chart'},
          checkin: {name: 'Check-In', route: '/checkin', ref: 'popoverCheckin', iconClass: 'icon-paper-clip'},
          evals: {name: 'Evaluations', route: '/evals', ref: 'popoverEvals', iconClass: 'icon-star'}
        }
      }
    },
    mounted () {
      // add listener when window is resized
      window.addEventListener('resize', this.windowSizeChange)

      this.$http({
        method: 'get',
        url: '/api/getuser'
      }).then(response => {
        this.wNumber = response.data.student_id
        this.userImage = response.data.picture_id
        this.userName = response.data.first_name + ' ' + response.data.last_name
      }).catch(error => {
        console.log(error)
      })

      // get user role
      // test api call
      this.$http({
        method: 'get',
        url: '/api/getroles'
      }).then(response => {
        for (let i = 0; i < response.data.length; i++) {
          if (response.data[i]['role']['name'] === 'instructor') {
            this.isInstructor = true
          }
        }
      }).catch(error => {
        console.log(error)
      })
    },
    created () {
      eventBus.$on('toggleSize', () => {
        this.toggleSidebar()
      })
    }
  }
</script>

<style lang="stylus">
@import '~variables'

  #sidebar
    background: #202f35

  #sidebar .q-item:hover
    background: $primary

  #sidebar #small-sidebar .q-item-link:hover
    background: $primary

  .q-popover .sidebar-user
    text-align: center

  // remove default padding from popover
  .q-popover #popover-content p
    margin-bottom: 0 !important
    font-size: 0.875rem

  .pop-nav
    color: #cfd8dc
    padding-right: 20px
    padding-top: 12px
    padding-bottom: 12px
    box-shadow: none

  #sidebar ul
    padding-left: 0

  #sidebar i
    padding-right: 10px

  #nav-sidebar aside
    background: #202f35 !important
    width: 200px

  .small-sidebar-style
    width: 53px !important

  .big-sidebar-style
    width: 200px !important
    overflow: hidden
    white-space: nowrap

  #sidebar .q-item
    display: block
    padding: 0.75rem 1rem
    color: #fff
    text-decoration: none
    font-size: 0.875rem

  #sidebar .q-item i
    color: #cfd8dc

  #sidebar .q-toolbar-title
    padding: 0.75rem 1rem
    font-size: 11px
    font-weight: 600
    color: #cfd8dc
    text-transform: uppercase

  #sidebar .image-avatar
    width: 80px
    margin: 0px auto 10px
    border-radius: 50em
    display: block
    text-align: center

  #sidebar .avatar-min
    width: 35px
    border-radius: 50em
    margin: 10px 10px 10px 8px

  #sidebar .sidebar-header
    height: 200px
    padding-bottom: 10px
    padding-top: 20px
    text-align: center
    background: rgba(0, 0, 0, 0.2)

  #sidebar .sidebar-user
    color: white

  // prevents user from pulling out sidebars by draging from left side with mouse
  #sidebar .layout-side-opener
    display: none

  .q-slider.label-always, .q-slider.with-padding
    padding: 5px 0 5px
    height: 25px

</style>
