<template>
  <div id="exam-info">
    <div class="row">
      <div class="col-md-12">
        <form action="" method="post" enctype="multipart/form-data" class="form-horizontal ">
          <div class="row">
            <div class="col-md-6">
              <div class="row">
                <div class="col-md-10 col-sm-12">
                  <q-field>
                    <q-input float-label="Exam Name" type="text" clearable placeholder="Enter Exam Name"
                             v-model="localExamName" @change="updateName(localExamName)">
                    </q-input>
                  </q-field>
                </div>
              </div>
              <div class="row">
                <div class="col-md-10 col-sm-12">
                  <q-select float-label="Exam Type" :options="examTypeOptions" separator
                            v-model="settings.type">
                  </q-select>
                </div>
                <div class="col-md-10 col-sm-12">
                  <q-field class="time-limit-q-field" helper="Leave blank to impose no limit">
                    <q-input float-label="Time Limit" clearable type="number" :min="0" v-model="settings.timeLimit">
                    </q-input>
                  </q-field>
                </div>
              </div>
              <div class="row">
                <div class="col-md-10 col-sm-12">
                  <q-field helper="Choose a Start and End Date">
                    <q-datetime-range
                      type="datetime"
                      v-model="dateRange"
                      inverted
                      color="secondary"
                      @change="dateChange"
                      format="MM-DD-YYYY H:mm"
                    ></q-datetime-range>
                  </q-field>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="row">
                <div class="col-12">
                  <q-card>
                    <q-card-title class="bg-primary">
                      Exam Details
                    </q-card-title>
                    <q-card-separator></q-card-separator>
                    <q-card-main>
                      <ul class="pl-2" style="list-style-type:none">
                        <li><b>Owner:</b> {{ settings.owner }}</li>
                        <li><b>Exam ID:</b> {{ examID }}</li>
                        <li class="link-overflow"><b>Link to Exam:</b> A link for students to use to take this exam: <a
                          :href="settings.linkToExam + examID">{{ settings.linkToExam }}{{ examID }}</a></li>
                        <li>
                          <q-field
                            helper="Entering a complete URL above will give the student a link to that page upon completing a exam.">
                            <q-input float-label="Return to URL" type="text" placeholder="Enter URL Here"
                                     v-model="settings.returnURL"></q-input>
                          </q-field>
                        </li>
                      </ul>
                    </q-card-main>
                  </q-card>
                </div>
              </div>
            </div>
          </div>
          <div class="row">
            <div class="col-md-12">
              <q-list inset-separator>
                <q-collapsible icon="fa-calendar-minus-o" label="Score Reduction By Date"
                               sublabel="Have your exam open longer, but for less credit for late exam takers">
                  <div class="row">
                    <div class="col-12">
                      <span>
                Please ensure that your close until date is set to the last date students can take the exam for ANY credit, and then use the date below to set the last date to receive full credit. Deductions are not additive (each point deduction is calculated independently).
                      </span>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-3">
                      <q-datetime inverted color="orange-6" float-label="Last date for full credit"
                                  v-model="settings.scoreReductionDate"
                                  type="datetime"></q-datetime>
                    </div>
                    <div class="col-9 pt-4 pl-3">
                      <q-btn color="primary">
                        Clear All
                      </q-btn>
                    </div>
                  </div>
                </q-collapsible>
                <q-collapsible icon="fa-info" label="Instructions"
                               sublabel="For students, examination personnel, and notes to self">
                  <div>
                    <div class="row">
                      <div class="col-md-12">
                        <q-field>
                          <q-input float-label="Instructions for students" type="textarea"
                                   v-model="settings.instructionsToStudents">
                          </q-input>
                        </q-field>
                      </div>
                    </div>
                    <div class="row">
                      <div class="col-md-12">
                        <q-field>
                          <q-input float-label="Instructions for examination personnel and proctors" type="textarea"
                                   v-model="settings.instructionsToOther">
                          </q-input>
                        </q-field>

                      </div>
                    </div>
                    <div class="row">
                      <div class="col-md-12">
                        <q-field>
                          <q-input float-label="Notes to self" type="textarea"
                                   v-model="settings.instructionsToSelf">
                          </q-input>
                        </q-field>
                      </div>
                    </div>
                  </div>
                </q-collapsible>
              </q-list>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
<script>

  import moment from 'moment'

  export default {
    name: 'ExamInfo',
    props: ['settings', 'examName', 'examID', 'updateExamName'],
    data () {
      return {
        localExamName: '',
        dateRange: {
          to: moment().format(),
          from: moment().format()
        },
        examTypeOptions: [
          {label: 'Online', value: 'online'},
          {label: 'Paper', value: 'paper'},
          {label: 'Survey', value: 'survey'},
          {label: 'Course Eval', value: 'course-eval'},
          {label: 'Download', value: 'download'},
          {label: 'Attendance', value: 'attendance'}
        ]
      }
    },
    mounted () {
      this.localExamName = this.examName
      if (this.settings.dateRange) {
        if (this.settings.dateRange.from) {
          this.dateRange.from = this.settings.dateRange.from
        }
        if (this.settings.dateRange.to) {
          this.dateRange.to = this.settings.dateRange.to
        }
      }
    },
    watch: {
      examName (newVal) {
        this.localExamName = newVal
      }
    },
    methods: {
      dateChange (newVal) {
        this.settings.dateRange.from = moment(newVal.from).format()
        this.settings.dateRange.to = moment(newVal.to).format()
      },
      updateName (name) {
        this.updateExamName(name)
      }
    }
  }
</script>
<style lang="stylus">

  #exam-info q-field.time-limit-q-field div.col
    padding-left: 0

  #exam-info .q-list
    border: none

  #exam-info .link-overflow
    overflow: hidden

</style>
