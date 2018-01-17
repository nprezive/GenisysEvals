<template>
  <div class="wrapper">
    <div id="exam-settings">
      <div class="row">
        <div class="col-12">
          <q-toolbar inverted color="dark" class="bg-light">
            <div class="col-xl-6 col-lg-6 col-md-7 col-sm-9 col-xs-10">
              <div class="row">
                <div class="col-lg-6 col-md-5">
                  <q-toolbar-title  id="tools-title" style="overflow: visible">
                    Exam Setting Tools
                  </q-toolbar-title>
                </div>
                <div class="col-lg-6 col-md-7 m-0">
                  <span v-if="settingsChanged || nameChanged" class="p-md-4 p-3 animated fadeIn">
                    <q-btn small :disable="!APIFinished" color="secondary" @click=revertChanges()
                           class="">Revert</q-btn>
                    <q-btn small :disable="!APIFinished" color="primary" @click="saveChanges()" class="ml-1">Save</q-btn>
                    <q-spinner-hourglass v-if="!APIFinished" size="40px" color="tertiary"></q-spinner-hourglass>
                  </span>
                </div>
              </div>

            </div>
            <div class="col-xl-6 col-lg-6 col-md-5 col-sm-3 col-xs-2">
              <div class="pull-right">
                <q-fab color="primary" active-icon="fa-times" icon="fa-cogs" direction="left">
                  <q-fab-action color="red" @click="toast('alarm')" icon="fa-print">
                    <q-tooltip anchor="center left" self="center right" :offset="[20, 0]">Print Exam</q-tooltip>
                  </q-fab-action>
                  <q-fab-action color="warning" @click="toast('alarm')" icon="fa-bar-chart">
                    <q-tooltip anchor="center left" self="center right" :offset="[20, 0]">Reports</q-tooltip>
                  </q-fab-action>
                  <q-fab-action color="secondary" @click="toast('alarm')" icon="fa-check-square-o">
                    <q-tooltip anchor="center left" self="center right" :offset="[20, 0]">Results</q-tooltip>
                  </q-fab-action>
                  <q-fab-action color="primary" @click="toast('mail')" icon="fa-exchange">
                    <q-tooltip anchor="center left" self="center right" :offset="[20, 0]">Export / Import</q-tooltip>
                  </q-fab-action>
                </q-fab>
              </div>
            </div>
          </q-toolbar>
        </div>
      </div>
      <div class="row">
        <div class="col-lg-3 col-md-3">
          <q-list no-border separator link>
            <q-item :class="{active: index === activeCourse()}" v-for="(component, index) in manageExamComponents"
                    :key="index" @click="selectComponent(component, index)" v-if="component !== 'QuestionSequence'">
              <q-item-side :color="component.color" :icon="component.icon"></q-item-side>
              <q-item-main>
                <q-item-tile label class="font-sm">
                  {{ component.name }}
                </q-item-tile>
              </q-item-main>
            </q-item>
          </q-list>
        </div>
        <div class="col-lg-9 col-md-9 p-3 relative-position">
          <component :is="activeComponent" :settings="examSettings[activeComponent]"
                     :examName="examName" :examID="examID" :questionSets="questionSets"
                     :ref="activeComponent"></component>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
  import ExamInfo from './examsettings/ExamInfo'
  import Security from './examsettings/Security'
  import Audience from './examsettings/Audience'
  import Sites from './examsettings/Sites'
  import Questions from './examsettings/Questions'
  import ExamAids from './examsettings/ExamAids'
  import Feedback from './examsettings/Feedback'
  import Review from './examsettings/Review'
  import Sharing from './examsettings/Sharing'
  import Notifications from './examsettings/Notifications'
  import _ from 'lodash'

  export default {
    name: 'ExamSettings',
    props: ['examSettings', 'examID', 'examName', 'questionSets', 'updateExamName', 'updateExamSettings'],
    components: {
      ExamInfo,
      Security,
      Audience,
      Sites,
      Questions,
      ExamAids,
      Feedback,
      Review,
      Sharing,
      Notifications
    },
    data () {
      return {
        APIFinished: true,
        settingsChanged: false,
        nameChanged: false,
        originalSettings: {},
        originalExamName: '',
        setActive: 0,
        activeComponent: 'ExamInfo',
        manageExamComponents: [
          {
            name: 'Exam Information',
            component: 'ExamInfo',
            icon: 'fa-info-circle',
            color: 'primary'
          },
          {
            name: 'Security',
            component: 'Security',
            icon: 'fa-shield',
            color: 'negative'
          },
          {
            name: 'Audience',
            component: 'Audience',
            icon: 'fa-users',
            color: 'secondary'
          },
          {
            name: 'Sites',
            component: 'Sites',
            icon: 'fa-sitemap',
            color: 'dark'
          },
          {
            name: 'Questions',
            component: 'Questions',
            icon: 'fa-question-circle',
            color: 'primary'
          },
          {
            name: 'Exam Aids',
            component: 'ExamAids',
            icon: 'fa-medkit',
            color: 'negative'
          },
          {
            name: 'Feedback',
            component: 'Feedback',
            icon: 'fa-comments',
            color: 'secondary'
          },
          {
            name: 'Review',
            component: 'Review',
            icon: 'fa-eye',
            color: 'dark'
          },
          {
            name: 'Sharing',
            component: 'Sharing',
            icon: 'fa-share-alt',
            color: 'primary'
          },
          {
            name: 'Notifications',
            component: 'Notifications',
            icon: 'fa-exclamation-triangle',
            color: 'negative'
          }
        ]
      }
    },
    mounted: function () {
      this.originalSettings = _.cloneDeep(this.examSettings)
      this.originalExamName = _.clone(this.examName)
      this.activeComponent = this.manageExamComponents[0].component // set active component to first manageExamComponent
    },
    watch: {
      examName (newVal) {
        if (this.originalExamName === newVal) {
          this.nameChanged = false
        } else {
          this.nameChanged = true
        }
      },
      examSettings: {
        handler: function (newVal, oldVal) {
          if (_.isEqual(this.originalSettings, newVal)) {
            this.settingsChanged = false
          } else {
            this.settingsChanged = true
          }
        },
        deep: true
      }
    },
    methods: {
      activeCourse () {
        return this.setActive
      },
      selectComponent (component, index) {
        this.setActive = index
        this.activeComponent = component.component
      },
      saveChanges () {
        if (this.settingsChanged || this.nameChanged) {
          this.APIFinished = false
          this.$http({
            method: 'post',
            url: '/api/exam/' + this.examID + '/allsettings/',
            headers: {'X-CSRFToken': this.getCookie('csrftoken')},
            data: {
              settingValue: this.examSettings,
              name: this.examName
            }
          }).then(response => {
            if (response.status === 250) {
              this.$router.error = response.data
              this.$router.push({path: '/error'})
            }
            this.APIFinished = true
            this.settingsChanged = false
            this.originalSettings = _.cloneDeep(this.examSettings)
            this.updateExamSettings(this.examSettings)
            this.nameChanged = false
            this.originalExamName = _.clone(this.examName)
            this.updateExamName(this.examName)
          }).catch(error => {
            console.log(error)
          })
        }
      },
      revertChanges () {
        if (this.nameChanged) {
          let clone = _.clone(this.originalExamName)
          this.updateExamName(clone)
        }
        if (this.settingsChanged) {
          let clone = _.cloneDeep(this.originalSettings)
          this.updateExamSettings(clone)
          if (this.activeComponent === 'Audience') {
            this.$refs.Audience.notifyRevert(this.originalSettings.Audience.targetedContexts)
          }
          if (this.activeComponent === 'Sites') {
            this.$refs.Sites.notifyRevert(this.originalSettings.Sites.targetedSites)
          }
        }
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
