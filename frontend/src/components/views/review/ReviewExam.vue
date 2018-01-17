<template>
  <div class="h-100 w-100" v-if="results">
    <q-tabs class="h-100" inverted align="justify">
      <q-tab :default="isDefault(index)" v-for="(result, index) in results" slot="title" :name="'tab' + index" :key="index"> Attempt {{results.length - index}}
      </q-tab>
      <q-tab-pane v-for="(result, index) in results" :name="'tab' + index" class="p-0 h-100" :key="index">
        <result-summary :result="result.result" :loadForbidden="loadForbidden"></result-summary>
      </q-tab-pane>
    </q-tabs>
  </div>
</template>
<script>
  import {
    Loading
  } from 'quasar'
  import ResultSummary from './ResultSummary.vue'

  export default {
    name: 'EndExam',
    components: {
      ResultSummary
    },
    data () {
      return {
        results: false
      }
    },
    mounted () {
      Loading.show({
        message: 'Retrieving Results'
      })
      this.$http({
        method: 'get',
        url: '/api/exam/' + this.$route.params.id + '/examresults/'
      }).then(response => {
        if (response.status === 250) {
          this.$router.error = response.data
          this.$router.push({path: '/error'})
        }
        Loading.hide()
        this.results = response.data
        if (this.results.length === 0) {
          this.$router.push({path: '/'})
        }
      }).catch(error => {
        console.log(error)
      })
    },
    methods: {
      loadForbidden () {
        this.$router.push({path: '/'})
      },
      isDefault (i) {
        if (i === 0) {
          return true
        } else {
          return false
        }
      }
    }
  }
</script>
<style lang="stylus">
  .q-tabs-panes
    height: 100%
</style>
