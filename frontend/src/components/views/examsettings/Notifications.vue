<template>
  <div id="alerts">
    <div class="row">
      <div class="col-md-6">
        <div class="row">
          <div class="col-md-10 col-sm-12">
            <div class="q-if-label font-size-12">Alert Settings</div>
            <q-list link dense no-border>
              <q-item tag="label" class="pl-0">
                <q-item-side>
                  <q-checkbox color="primary" v-model="settings.emailInExam"></q-checkbox>
                </q-item-side>
                <q-item-main>
                  <q-item-tile label>
                    Allow students to email you directly from the exam or during review regarding concerns they have about a particular question
                  </q-item-tile>
                </q-item-main>
              </q-item>
              <q-item tag="label" class="pl-0">
                <q-item-side>
                  <q-checkbox color="secondary" v-model="settings.instructorNotifications"></q-checkbox>
                </q-item-side>
                <q-item-main>
                  <q-item-tile label>Email me when each student finishes this exam</q-item-tile>
                </q-item-main>
              </q-item>
              <q-item tag="label" class="pl-0">
                <q-item-side>
                  <q-checkbox color="negative" v-model="settings.studentReminders"></q-checkbox>
                </q-item-side>
                <q-item-main>
                  <q-item-tile label>Send a reminder email to students to take this exam</q-item-tile>
                  <q-item-tile sublabel v-if="!settings.studentReminders">
                    Check this option to configure additional settings
                  </q-item-tile>
                </q-item-main>
              </q-item>
            </q-list>
          </div>
        </div>
      </div>
      <div class="col-md-6" v-if="settings.studentReminders">
        <div class="row">
          <div class="col-12">
            <q-card>
              <q-card-title class="bg-primary">
                Email To Student Settings
              </q-card-title>
              <q-card-main>
                <div class="row">
                  <div class="col-2">
                    <q-field>
                      <q-input v-model="settings.beforeExamOpens" type="number"  :min="0"></q-input>
                    </q-field>
                  </div>
                  <div class="col-10">
                    <q-field helper="before the exam opens">
                      <q-select
                        separator
                        v-model="settings.beforeExamOpensSelect"
                        :options="beforeExamOpensOptions"></q-select>
                    </q-field>
                  </div>
                </div>
                <div class="row">
                  <div class="col-2">
                    <q-field>
                      <q-input v-model="settings.beforeExamCloses" type="number"  :min="0"></q-input>
                    </q-field>
                  </div>
                  <div class="col-10">
                    <q-field helper="before the exam opens">
                      <q-select
                        separator
                        v-model="settings.beforeExamClosesSelect"
                        :options="beforeExamClosesOptions"></q-select>
                    </q-field>

                  </div>
                </div>
                <div class="row">
                  <div class="col-12">
                    <q-list link dense no-border>
                      <div class="q-if-label font-size-12 pb-2">Message type</div>
                      <q-item tag="label" class="pl-0">
                        <q-item-side>
                          <q-radio color="primary" v-model="settings.messageGroup" val="standard"></q-radio>
                        </q-item-side>
                        <q-item-main>
                          <q-item-tile label>Any time after the student completes the exam (<a href>preview</a>)
                          </q-item-tile>
                        </q-item-main>
                      </q-item>
                      <q-item tag="label" class="pl-0">
                        <q-item-side>
                          <q-radio color="secondary" v-model="settings.messageGroup" val="custom"></q-radio>
                        </q-item-side>
                        <q-item-main>
                          <q-item-tile label>Include custom message with the standard message</q-item-tile>
                        </q-item-main>
                      </q-item>
                    </q-list>
                  </div>
                </div>
                <div class="row" v-if="(settings.messageGroup.indexOf('custom') != -1)">
                  <div class="col-12">
                    <q-input v-model="settings.customMessage" float-label="Custom Message"
                             placeholder="Enter Custom Message"></q-input>
                  </div>
                </div>
              </q-card-main>
            </q-card>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>

  export default {
    name: 'Alerts',
    props: ['settings'],
    components: {
    },
    data () {
      return {
        beforeExamOpensOptions: [
          {
            label: 'Days',
            value: 'Days'
          },
          {
            label: 'Weeks',
            value: 'Weeks'
          }
        ],
        beforeExamClosesOptions: [
          {
            label: 'Days',
            value: 'Days'
          },
          {
            label: 'Weeks',
            value: 'Weeks'
          }
        ]
      }
    }
  }
</script>
<style lang="stylus">

</style>
