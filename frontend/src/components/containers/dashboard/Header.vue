<template>
  <q-toolbar slot='header' color="white" id="header">
    <!--<img to='/courses' class="logo ml-4" src="../../../statics/img/logo.svg" alt="Dispute Bills">-->
    <router-link to="/courses" class="logo ml-4 cursor-pointer" tag="img" src="../../../statics/img/logo.svg"></router-link>
    <q-btn flat class="ml-4" @click="toggle"><q-icon name="menu"></q-icon></q-btn>
    <q-toolbar-title class="hidden-md-down">
      <form class="form-inline px-2 gt-sm">
        <i class="fa fa-search text-black"></i>
        <input class="form-control search-input text-grey" type="text" v-model="term" @keyup.enter="search" placeholder="Are you looking for something?"/>
      </form>
    </q-toolbar-title>
    <!--<modal title="Take Exam" v-model="takeExamModal" @ok="takeExamModal = false" effect="fade/zoom" class="modal-danger">-->
      <!--<div slot="modal-header" class="modal-header">-->
        <!--<h4 class="modal-title">Take Exam</h4>-->
      <!--</div>-->
      <!--Are You Sure You Want To Take This Exam?-->
      <!--<div slot="modal-footer" class="modal-footer">-->
        <!--<button type="button" class="btn btn-default" @click.prevent="takeExamModal = false">Go Back</button>-->
        <!--<button type="button" class="btn btn-primary" @click="takeExam">Take Exam</button>-->
      <!--</div>-->
    <!--</modal>-->
    <q-btn flat href="#"><i class="fa fa-question-circle fa-2x"></i></q-btn>
  </q-toolbar>
</template>
<script>
  import navbar from './Navbar'
  import {createElement, compile} from 'elliptical'
  import {eventBus} from '../../../main'

  var exam = document.getElementById('audio')

  // Some data to work with
  const examData = [
    {text: 'WEB 2310 Exam 1', value: '12341'},
    {text: 'WEB 2320 Exam 1', value: '12342'},
    {text: 'WEB 2330 Exam 1', value: '12343'},
    {text: 'WEB 2340 Exam 1', value: '12344'},
    {text: 'WEB 2350 Exam 1', value: '12345'}
  ]

  // Define a Phrase
  const Exam = {
    describe: function () {
      return createElement(
        'placeholder',
        { argument: 'Exam' },
        createElement('list', { items: examData, strategy: 'fuzzy' })
      )
    }
  }

  // Build our grammar out of Elements
  const grammar = createElement(
    'sequence',
    null,
    createElement('literal', { text: 'take ' }),
    createElement(Exam, { id: 'exam' })
  )

  export default {
    name: 'Header',
    components: {
      navbar
    },
    data () {
      return {
        term: '',
        outputs: [],
        takeExamModal: false,
        user: {},
        wNumber: '',
        userImage: '',
        userName: '',
        smallSidebar: false,
        sidebarDisplay: true,
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
    methods: {
      toggle () {
        eventBus.toggleSideNavSize()
      },
      toggleSidebar () {
        if (window.innerWidth < 991) {
          this.sidebarDisplay = !this.sidebarDisplay
          eventBus.toggleSideNavSize()
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
      click () {
        // do nothing
      },
      toggleExam () {
        exam.toggleExam()
      },
      search () {
        this.takeExamModal = true
        const parse = compile(grammar)
        this.outputs = parse(this.term)
      },
      takeExam () {
        this.$router.push({path: '/takeexam/' + this.outputs[0].result.exam})
      },
      sidebarToggle (e) {
        e.preventDefault()
        document.body.classList.toggle('sidebar-hidden')
      },
      sidebarMinimize (e) {
        e.preventDefault()

        let x = document.getElementById('sidebar-minimized-userMenu')
        if (x.style.display === 'block') {
          x.style.display = 'none'
        } else {
          x.style.display = 'block'
        }

        document.body.classList.toggle('sidebar-minimized')
      },
      mobileSidebarToggle (e) {
        e.preventDefault()
        document.body.classList.toggle('sidebar-mobile-show')
      },
      asideToggle (e) {
        e.preventDefault()
        document.body.classList.toggle('aside-menu-hidden')
      }
    }
  }
</script>

<style lang="stylus">
  #header .logo
    height: 30px

  #header .search-input
    border: 0
    width: 300px !important

  #header i
    color: lightgrey

</style>
