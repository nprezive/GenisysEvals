<template>
  <div class="matchingOption">
    <q-field>
      <q-select
        :float-label="option.text"
        v-model="response"
        :options="questionOptions"
        :disable="review"
      ></q-select>
    </q-field>
  </div>
</template>

<script>

  export default {
    name: 'MatchingOption',
    props: ['index', 'option', 'questionOptions', 'oldResponse', 'review'],
    data () {
      return {
        response: ''
      }
    },
    mounted () {
      this.response = this.oldResponse[this.option.answer]
    }
  }
</script>
<style lang="stylus">
</style>
