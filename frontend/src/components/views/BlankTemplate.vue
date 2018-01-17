<template>
  <div class="wrapper">
    <div class="animated fadeIn blank-template">
      <div class="row">
        <div class="col-12">
          <h1>Parent</h1>
          <blank-template-child :objectToPassDown="objectToPassDown"></blank-template-child>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import BlankTemplateChild from './BlankTemplateChild.vue'

  export default {
    name: 'BlankTemplate',
    components: {
      BlankTemplateChild
    },
    data () {
      return {
        someObject: {},
        objectToPassDown: {
          arr: [1, 2, 3, 4]
        }
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
