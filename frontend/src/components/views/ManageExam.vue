<template>
  <div class="wrapper">
    <div class="animated fadeIn manage-exam">
      <div class="row">
        <div class="col-12 mt-3">
          <q-tabs v-if="APIFinished" class="teaching-enrolled-tabs" align="justify" inverted
                  style="background-color: white">
            <!--TODO remove inline style or fix core-ui background color-->
            <q-tab default label="Exam Settings" slot="title" name="tab-1"></q-tab>
            <q-tab label="Exam Editor" slot="title" name="tab-2"></q-tab>
            <q-tab-pane name="tab-1" class="p-0">
              <exam-settings :examSettings="examSettings" :examID="examID" :examName="examName"
                             :questionSets="questionSets" :updateExamName="updateExamName"
                             :updateExamSettings="updateExamSettings"></exam-settings>
            </q-tab-pane>
            <q-tab-pane name="tab-2" class="p-0">
              <exam-editor :examName="examName" :examID="examID"
                           :questionSequence="examSettings['QuestionSequence']"></exam-editor>
            </q-tab-pane>
          </q-tabs>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import ExamSettings from './ExamSettings'
  import ExamEditor from './ExamEditor'

  import {
    Loading
  } from 'quasar'

  export default {
    name: 'Courses',
    props: [''],
    components: {
      ExamSettings,
      ExamEditor
    },
    data () {
      return {
        examSettings: {},
        examName: '',
        examID: 0,
        questionSets: [],
        APIFinished: false
      }
    },
    mounted () {
      Loading.show({message: 'Loading Exam Settings'})
      this.$http({
        method: 'get',
        url: '/api/exam/' + this.$route.params.id,
        headers: {}
      }).then(response => {
        if (response.status === 250) {
          this.$router.error = response.data
          this.$router.push({path: '/error'})
        }
        this.examSettings = response.data.settings
        this.examName = response.data.name
        this.examID = response.data.id
        this.questionSets = response.data.questionsets
        this.APIFinished = true
        Loading.hide()
      }).catch(error => {
        console.log(error)
      })
    },
    methods: {
      updateExamName (name) {
        this.examName = name
      },
      updateExamSettings (settings) {
        this.examSettings = settings
      }
    }
  }
</script>
<style lang="stylus">
  *, *::before, *::after
    box-sizing: border-box

  html
    font-size: 100%

  .ui-tabs--text-color-active-primary .ui-tab-header-item.is-active
    outline: 0 !important
    color: #20a8d8 !important

  ui-tab-header-item ui-tab-header-item--type-text is-active
    color: #20a8d8 !important

  .ui-tabs--indicator-color-primary .ui-tabs__active-tab-indicator
    background-color: #20a8d8 !important

</style>
