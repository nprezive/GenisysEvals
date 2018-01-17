<template>
  <div id="library" style="background-color: white;">
    <q-tabs align="justify" inverted>
      <q-tab default slot="title" name="Exams">Exams</q-tab>
      <q-tab slot="title" name="QuestionSets">Questionsets</q-tab>
      <q-tab-pane name="Exams">
        <exams></exams>
      </q-tab-pane>
      <q-tab-pane name="QuestionSets">
        <question-sets></question-sets>
      </q-tab-pane>
    </q-tabs>
  </div>
</template>

<script>
  import QuestionSets from './InstructorQuestionSets.vue'
  import Exams from './InstructorExams.vue'

  export default {
    name: 'Library',
    components: {
      QuestionSets,
      Exams
    }
  }
</script>
