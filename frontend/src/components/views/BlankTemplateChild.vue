<template>
  <div class="wrapper">
    <div class="animated fadeIn blank-template-child">
      <div class="row">
        <div class="col-md-3">
          <h2>Child</h2>
          <div v-for="(item, index) in objectToPassDown.arr">
            {{ item }}
          </div>
          </div>
        </div>
      </div>
    </div>
</template>

<script>

  export default {
    name: 'BlankTemplateChild',
    props: ['objectToPassDown'],
    data () {
      return {
        someObject: {}
      }
    },
    computed: {
      // api calls go here
      anApiCall () {
        // APICall to get something
        let apiCall = []
        return apiCall
      }
    },
    methods: {
      aFunction () {
        // do nothing
      }
    }
  }
</script>
