<template>
  <div class="wrapper">
    <div class="animated fadeIn courses">
      <div class="row">
        <div class="col-12">
          <q-tabs class="exam-settings-editor-tabs" align="justify" inverted
                  style="background-color: white">
            <q-tab v-if="instructorEnrollments.length > 0" :default="setTab" label="Teaching" slot="title"
                   name="tab-1"></q-tab>
            <q-tab-pane v-if="instructorEnrollments.length > 0" name="tab-1" class="p-0">
              <teaching :enrollments="instructorEnrollments"></teaching>
            </q-tab-pane>
            <q-tab v-if="studentEnrollments.length > 0" :default="!setTab" label="Enrolled" slot="title"
                   name="tab-2"></q-tab>
            <q-tab-pane v-if="studentEnrollments.length > 0" name="tab-2" class="p-0">
              <enrolled :enrollments="studentEnrollments"></enrolled>
            </q-tab-pane>
          </q-tabs>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import Teaching from './Teaching.vue'
  import Enrolled from './Enrolled.vue'
  import {mapGetters} from 'vuex'

  export default {
    name: 'Courses',
    props: [],
    components: {
      Enrolled,
      Teaching
    },
    data () {
      return {
        setTab: true,
        APIFinished: false
      }
    },
    mounted () {
      this.$store.dispatch('GET_INSTRUCTOR_ENROLLMENTS').then(response => {
        if (response.status === 250) {
          this.$router.error = response.data
          this.$router.push({path: '/error'})
        }
      }, error => {
        console.log(error)
      })
      this.$store.dispatch('GET_STUDENT_ENROLLMENTS').then(response => {
        if (response.status === 250) {
          this.$router.error = response.data
          this.$router.push({path: '/error'})
        }
      }, error => {
        console.log(error)
      })
    },
    computed: {
      ...mapGetters([
        'instructorEnrollments',
        'studentEnrollments'
      ])
    },
    methods: {
      click () {
        // do nothing
      }
    }
  }
</script>
<style>
  *,
  *::before,
  *::after {
    box-sizing: border-box !important;
  }

  html {
    font-size: 100% !important;
  }
</style>
