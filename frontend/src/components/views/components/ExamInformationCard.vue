<template>
  <div v-if="settings" class="wrapper">
    <div class="exam-information-card">
      <q-card class="bg-white">
        <q-card-title v-if="showStartExamOptions" class="bg-primary">
          <h4 class="text-center">Hey! Did You Study?</h4>
        </q-card-title>
        <q-card-main>
          <div>
            <q-list no-border class="row">
              <q-list-header class="col-12 text-center" v-if="showStartExamOptions">
                Are you sure you want to start {{ settings.name }}?
              </q-list-header>
              <q-item class="col-lg-4 col-sm-6">
                <q-item-side color="primary" icon="fa-desktop"></q-item-side>
                <q-item-main>
                  <q-item-tile label class="font-sm">
                    <div v-if="settings.sites.length > 0">
                  <span v-for="(site, index) in settings.sites">
                    <span>{{ site }}</span><span v-if="index + 2 < settings.sites.length">, </span><span
                    v-if="index === settings.sites.length - 2">, and </span>
                  </span>
                    </div>
                    <div v-else>
                      None
                    </div>
                  </q-item-tile>
                  <q-item-tile sublabel class="font-xs">This exam is available at the following sites</q-item-tile>
                </q-item-main>
              </q-item>
              <q-item class="col-lg-4 col-sm-6">
                <q-item-side color="positive" icon="fa-calendar"></q-item-side>
                <q-item-main>
                  <q-item-tile label class="font-sm">{{ settings.daterange.from }} to {{ settings.daterange.to }}
                  </q-item-tile>
                  <q-item-tile sublabel class="font-xs">The exam is available anytime between</q-item-tile>
                </q-item-main>
              </q-item>
              <q-item v-if="settings.timelimit !== ''" class="col-lg-4 col-sm-6">
                <q-item-side color="info" icon="fa-clock-o"></q-item-side>
                <q-item-main>
                  <q-item-tile label class="font-sm">Time Limit</q-item-tile>
                  <q-item-tile sublabel class="font-xs">This exam has a time limit of {{ settings.timelimit }} minutes
                  </q-item-tile>
                </q-item-main>
              </q-item>
              <q-item v-if="settings.timelimit === ''" class="col-lg-4 col-sm-6">
                <q-item-side color="info" icon="fa-clock-o"></q-item-side>
                <q-item-main>
                  <q-item-tile label class="font-sm">Time Limit</q-item-tile>
                  <q-item-tile sublabel class="font-xs">There is no time limit for this exam
                  </q-item-tile>
                </q-item-main>
              </q-item>
              <q-item v-if="settings.materials.includes('open-book')" class="col-lg-4 col-sm-6">
                <q-item-side color="secondary" icon="fa-book"></q-item-side>
                <q-item-main>
                  <q-item-tile label class="font-sm">Open Book</q-item-tile>
                  <q-item-tile sublabel class="font-xs">You may use the book: {{ settings.openbookname }} on this exam
                  </q-item-tile>
                </q-item-main>
              </q-item>
              <q-item v-if="settings.materials.includes('keep-notes') || settings.materials.includes('cue-sheets')"
                      class="col-lg-4 col-sm-6">
                <q-item-side color="warning" icon="fa-sticky-note"></q-item-side>
                <q-item-main>
                  <q-item-tile label class="font-sm" v-if="settings.materials.includes('keep-notes')">Notes
                  </q-item-tile>
                  <q-item-tile sublabel class="font-xs" v-if="settings.materials.includes('keep-notes')">
                    You may have {{ settings.personalnotes }}
                  </q-item-tile>
                  <q-item-tile label class="font-sm" v-if="settings.materials.includes('cue-sheets')">Cue Sheets
                  </q-item-tile>
                  <q-item-tile sublabel class="font-xs" v-if="settings.materials.includes('cue-sheets')">
                    You may have {{ settings.cuesheets }}
                  </q-item-tile>
                  <q-item-tile label class="font-sm" v-if="settings.materials.includes('scratch-paper')">Scratch Paper
                  </q-item-tile>
                  <q-item-tile sublabel class="font-xs" v-if="settings.materials.includes('scratch-paper')">
                    You may use scratch paper
                  </q-item-tile>
                  <q-item-tile label class="font-sm" v-if="settings.keepnotes">Keep Notes</q-item-tile>
                  <q-item-tile sublabel class="font-xs" v-if="settings.keepnotes">
                    Student is allowed to keep their notes
                  </q-item-tile>
                </q-item-main>
              </q-item>
              <q-item v-if="settings.calculators.length !== 0" class="col-lg-4 col-sm-6">
                <q-item-side color="dark" icon="fa-calculator"></q-item-side>
                <q-item-main>
                  <q-item-tile label class="font-sm">You are allowed to use these calculators for this exam
                  </q-item-tile>
                  <q-item-tile sublabel class="font-xs">
                    <span v-for="(calculator, index) in settings.calculators" :key="index">
                      <span v-if="calculator === 'other'">
                        <span>{{ settings.othercalculator }}</span><span v-if="index + 2 < settings.calculators.length">, </span><span
                        v-if="index === settings.calculators.length - 2">, and </span>
                      </span>
                      <span v-else>
                        <span>{{ calculator }}</span><span
                        v-if="index + 2 < settings.calculators.length">, </span><span
                        v-if="index === settings.calculators.length - 2">, and </span>
                      </span>
                    </span>
                  </q-item-tile>
                </q-item-main>
              </q-item>
              <q-item v-if="settings.restroombreak" class="col-lg-4 col-sm-6">
                <q-item-side color="negative" icon="fa-file-text-o"></q-item-side>
                <q-item-main>
                  <q-item-tile label class="font-sm">Instructions To Students</q-item-tile>
                  <q-item-tile sublabel class="font-xs">{{ settings.instructionsToStudents }}
                  </q-item-tile>
                </q-item-main>
              </q-item>
              <q-item v-if="settings.restroombreak" class="col-lg-4 col-sm-6">
                <q-item-side color="faded" icon="fa-sign-out"></q-item-side>
                <q-item-main>
                  <q-item-tile label class="font-sm">Restroom Break</q-item-tile>
                  <q-item-tile sublabel class="font-xs">You may take a restroom break on this exam
                  </q-item-tile>
                </q-item-main>
              </q-item>
              <q-item v-if="settings.dictionaries.length !== 0" class="col-lg-4 col-sm-6">
                <q-item-side color="secondary" icon="fa-book"></q-item-side>
                <q-item-main>
                  <q-item-tile label class="font-sm">You are allowed to use these dictionaries for this exam
                  </q-item-tile>
                  <q-item-tile sublabel class="font-xs">
                    <span v-for="(dictionary, index) in settings.dictionaries" :key="index">
                        <span>{{ dictionary }}</span><span
                      v-if="index + 2 < settings.dictionaries.length">, </span><span
                      v-if="index === settings.dictionaries.length - 2">, and </span>
                    </span>
                  </q-item-tile>
                </q-item-main>
              </q-item>
            </q-list>
          </div>
          <div>
            <div v-if="showStartExamOptions" class="row m-2">
              <div class="col-lg-6 col-md-12 m-auto row">
                <div class="col-sm-12 col-md-5">
                  <q-btn color="primary" @click="goBack" class="full-width">
                    Home
                  </q-btn>
                </div>
                <div class="col-md-2 col-sm-12"></div>
                <div class="col-sm-12 col-md-5">
                  <q-btn color="secondary" class="full-width" @click="startExam">
                    {{ examStatus }}
                    <q-tooltip :disable="disableTooltip">
                      {{ tooltipText }}
                    </q-tooltip>
                  </q-btn>
                </div>
              </div>
            </div>
          </div>
        </q-card-main>
      </q-card>
    </div>
  </div>
</template>

<script>

  export default {
    name: 'ExamInformationCard',
    props: ['settings', 'showStartExamOptions', 'examStatus', 'startExam'],
    data () {
      return {
        disableTooltip: true,
        tooltipText: ''
      }
    },
    methods: {
      goBack () {
        this.$router.push({path: '/'})
      }
    }
  }
</script>
<style lang="stylus">

  .q-item-label > span
    color: initial;

  /*override quasar q-item-label > span { color: #757575; }*/

  .q-list-header
    line-height: 25px
    padding-top: 5px
    padding-bottom: 10px

  /*remove gap in q-list-header*/


</style>
