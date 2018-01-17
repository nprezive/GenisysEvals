<template>
  <div class="wrapper animated fadeIn">
    <q-modal minimized id="exam-actions-modal" ref="examActionsModal" class="text-center" @close="closeModal()">
      <div v-if="settings && exam.status" class="bg-light">
        <div class="bg-primary text-white">
          <h4 class="m-0 pt-3 pb-3">
            Actions For {{ settings.name }}</h4>
        </div>
        <div class="mt-2 ml-2 mr-2">
          <q-btn flat :disabled="exam.button" @click="startExam()">
            <div style="display:grid;">
              <q-icon size="2.5em" color="primary" name="fa-play-circle"></q-icon>
              {{ exam.status }}
              <q-tooltip :disable="exam.disableTooltip">{{ exam.tooltip }}</q-tooltip>
            </div>
          </q-btn>
          <q-btn flat @click="$refs.examActionsModal.close()">
            <div style="display:grid;">
              <q-icon size="2.5em" color="secondary" name="fa-globe"></q-icon>
              Request Proctored Exam
            </div>
          </q-btn>
          <q-btn flat :disabled="review.button" @click="reviewExam()">
            <div style="display:grid;">
              <q-icon size="2.5em" color="tertiary" name="fa-eye"></q-icon>
              Review Exam / See Score
              <q-tooltip :disable="review.disableTooltip">{{ review.tooltip }}</q-tooltip>
            </div>
          </q-btn>
        </div>
        <exam-information-card class="p-2" :settings="settings"
                               :showStartExamOptions="showStartExamOptions">
        </exam-information-card>
      </div>
    </q-modal>
  </div>
</template>

<script>

  import ExamInformationCard from './ExamInformationCard.vue'

  export default {
    name: 'ExamActionsModal',
    props: ['exam', 'review', 'settings', 'closeModal'],
    components: {
      ExamInformationCard
    },
    data () {
      return {
        showStartExamOptions: false
      }
    },
    methods: {
      click () {
        // do nothing
      },
      startExam () {
        this.$router.push({path: '/takeexam/start/' + this.settings.id})
      },
      reviewExam () {
        this.$router.push({path: '/takeexam/review/' + this.settings.id})
      },
      openModal () {
        this.$refs.examActionsModal.open()
      }
    }
  }
</script>
<style lang="stylus">

  .modal-content
    max-width: 60%
    border: none

</style>
