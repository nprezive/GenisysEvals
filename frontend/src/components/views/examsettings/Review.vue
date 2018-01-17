<template>
  <div id="review">
    <div class="row">
      <div class="col-md-6">
        <div class="row">
          <div class="col-md-10 col-sm-12">
            <div class="q-if-label font-size-12">Review</div>
            <q-list link dense no-border>
              <q-item tag="label" class="pl-0">
                <q-item-side>
                  <q-checkbox color="primary" v-model="settings.allowReviewOfExam"></q-checkbox>
                </q-item-side>
                <q-item-main>
                  <q-item-tile label>Allow students to review this exam</q-item-tile>
                  <q-item-tile v-if="!settings.allowReviewOfExam" sublabel>
                    Check this option to configure additional settings
                  </q-item-tile>
                </q-item-main>
              </q-item>
            </q-list>
          </div>
        </div>
        <div class="row" v-if="settings.allowReviewOfExam">
          <div class="col-md-10 col-sm-12">
            <q-list link dense no-border>
              <div class="q-if-label font-size-12 pb-2">When Review Will Be Available</div>
              <q-item tag="label" class="pl-0">
                <q-item-side>
                  <q-radio color="primary" v-model="settings.whenGroup" val="any-time"></q-radio>
                </q-item-side>
                <q-item-main>
                  <q-item-tile label>Any time after the student completes the exam</q-item-tile>
                </q-item-main>
              </q-item>
              <q-item tag="label" class="pl-0">
                <q-item-side>
                  <q-radio color="secondary" v-model="settings.whenGroup" val="after-run"></q-radio>
                </q-item-side>
                <q-item-main>
                  <q-item-tile label>Only after the exam run is completed</q-item-tile>
                </q-item-main>
              </q-item>
            </q-list>
          </div>
        </div>
        <div class="row" v-if="settings.allowReviewOfExam">
          <div class="col-md-10 col-sm-12">
            <div class="q-if-label font-size-12 pb-2">
              You can limit the length of time after the exam students are able to review
            </div>
            <div class="row">
              <div class="col-6">
                <q-input v-if="settings.timeLimitIdentifier !== 'none' && settings.timeLimitIdentifier !== 'date'"
                         type="number" :min="0" @change="updatePluralTimeLimitSelect()"
                         v-model="settings.timeLimit"></q-input>
                <q-datetime v-model="settings.timeLimit" type="datetime" format="MM-DD-YYYY H:mm" inverted
                            color="secondary" @change="dateChange"
                            class="mr-1 mt-2"
                            v-if="settings.timeLimitIdentifier !== 'none' && settings.timeLimitIdentifier === 'date'"
                ></q-datetime>
              </div>
              <div
                :class="{'col-6':settings.timeLimitIdentifier !== 'none', 'col-12': settings.timeLimitIdentifier === 'none'}">
                <q-select v-model="settings.timeLimitIdentifier" :options="timeLimitSelect"
                          @change="updateTimeLimit()"></q-select>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-6" v-if="settings.allowReviewOfExam">
        <div class="row">
          <div class="col-md-10 col-sm-12">
            <div class="q-if-label font-size-12">Review Settings</div>
            <q-list link dense no-border>
              <q-item tag="label" class="pl-0">
                <q-item-side>
                  <q-checkbox color="primary" v-model="settings.allowReviewAnyComputer"></q-checkbox>
                </q-item-side>
                <q-item-main>
                  <q-item-tile label>Allow review at any computer, not just at the sites where the exam was available
                  </q-item-tile>
                </q-item-main>
              </q-item>
              <q-item tag="label" class="pl-0">
                <q-item-side>
                  <q-checkbox color="secondary" v-model="settings.allowReviewQuestionsMissed"></q-checkbox>
                </q-item-side>
                <q-item-main>
                  <q-item-tile label>Allow students to review only those questions they missed</q-item-tile>
                </q-item-main>
              </q-item>
              <q-item tag="label" class="pl-0">
                <q-item-side>
                  <q-checkbox color="negative" v-model="settings.showCorrectAnswers"></q-checkbox>
                </q-item-side>
                <q-item-main>
                  <q-item-tile label>Show correct answers</q-item-tile>
                </q-item-main>
              </q-item>
              <q-item tag="label" class="pl-0">
                <q-item-side>
                  <q-checkbox color="primary" v-model="settings.allowDownload"></q-checkbox>
                </q-item-side>
                <q-item-main>
                  <q-item-tile label>Allow students to download uploaded files</q-item-tile>
                </q-item-main>
              </q-item>
              <q-item tag="label" class="pl-0">
                <q-item-side>
                  <q-checkbox color="secondary" v-model="settings.allowReviewWithoutPassword"></q-checkbox>
                </q-item-side>
                <q-item-main>
                  <q-item-tile label>Allow students to review without having to enter the exam password</q-item-tile>
                </q-item-main>
              </q-item>
            </q-list>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>

  import moment from 'moment'

  export default {
    name: 'Review',
    props: ['settings'],
    components: {},
    data () {
      return {
        timeLimitSelect: [],
        timeLimitSelectPlural: [
          {
            label: 'No Time Limit',
            value: 'none'
          },
          {
            label: 'Minutes',
            value: 'minutes'
          },
          {
            label: 'Hours',
            value: 'hours'
          },
          {
            label: 'Days',
            value: 'days'
          },
          {
            label: 'Weeks',
            value: 'weeks'
          },
          {
            label: 'By Date',
            value: 'date'
          }
        ],
        timeLimitSelectSingular: [
          {
            label: 'No Time Limit',
            value: 'none'
          },
          {
            label: 'Minute',
            value: 'minutes'
          },
          {
            label: 'Hour',
            value: 'hours'
          },
          {
            label: 'Day',
            value: 'days'
          },
          {
            label: 'Week',
            value: 'weeks'
          },
          {
            label: 'By Date',
            value: 'date'
          }
        ],
        rememberDate: '',
        rememberInput: 0,
        timeLimitSelectWas: ''
      }
    },
    mounted () {
      this.timeLimitSelect = this.timeLimitSelectPlural
      if (this.settings.timeLimitIdentifier === 'date') {
        this.rememberDate = this.settings.timeLimit
      } else if (this.settings.timelimitIdentifier !== 'none') {
        this.rememberInput = this.settings.timeLimit
        this.updatePluralTimeLimitSelect()
      }
      this.timeLimitSelectWas = this.settings.timeLimitIdentifier
    },
    methods: {
      dateChange (newVal) {
        if (typeof newVal === 'object') {
          this.settings.timeLimit = moment(newVal).format()
        }
      },
      updateTimeLimit () {
        if (this.timeLimitSelectWas === 'date') {
          this.rememberDate = this.settings.timeLimit
        } else if (this.timeLimitSelectWas !== 'none') {
          this.rememberInput = this.settings.timeLimit
        }
        if (this.settings.timeLimitIdentifier === 'date') {
          this.settings.timeLimit = this.rememberDate
        } else if (this.settings.timeLimitIdentifier !== 'none') {
          this.settings.timeLimit = this.rememberInput
        }
        this.timeLimitSelectWas = this.settings.timeLimitIdentifier
      },
      updatePluralTimeLimitSelect () {
        if (this.settings.timeLimit === 1) {
          this.timeLimitSelect = this.timeLimitSelectSingular
        } else {
          this.timeLimitSelect = this.timeLimitSelectPlural
        }
      }
    }
  }
</script>
<style lang="stylus">

</style>
