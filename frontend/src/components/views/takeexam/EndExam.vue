<template>
  <div class="h-100 w-100">
    <result-summary :resultID="$route.params.id" :loadForbidden="loadForbidden"></result-summary>
  </div>
</template>
<script>
  import ResultSummary from '../review/ResultSummary.vue'

  export default {
    name: 'EndExam',
    props: ['error', 'loadForbidden'],
    components: {
      ResultSummary
    }
  }
</script>
<style>
  .resultCard {
    max-width: 750px;
  }
</style>
