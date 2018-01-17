<template>
  <div class="mb-3 mt-3">
    <canvas id="viewCanvas" width="1280" height="720"></canvas>
  </div>
</template>
<script>
  import {
    Loading
  } from 'quasar'

  export default {
    name: 'ViewCanvas',
    props: {
      updateComputerInfo: {
        type: Function
      },
      loadCanvas: {
        type: Function
      },
      fixCanvas: {
        type: Function
      },
      chosenSite: {
        type: Number
      }
    },
    data () {
      return {
        stations: [],
        updateTimer: null,
        viewCanvas: null
      }
    },
    mounted () {
      this.loadViewCanvas(this.chosenSite)
    },
    beforeDestroy () {
      window.clearInterval(this.updateTimer)
      this.viewCanvas.clear()
    },
    methods: {
      updateOccupied () {
        // APICall that gets all the stations to see if they are occupied or not
        this.$http({
          method: 'get',
          url: '/api/site/' + this.chosenSite + '/sitecomputers/'
        }).then(response => {
          if (response.status === 250) {
            this.$router.error = response.data
            this.$router.push({path: '/error'})
          }
          let APICall = response.data
          for (let i = 0; i < APICall.length; i++) {
            this.viewCanvas.forEachObject(function (o) {
              if (o.class === 'computer') {
                if (o.id === 'c' + APICall[i].id) {
                  if (APICall[i].occupied === true) {
                    o.occupied = true
                    o._objects[0].setColor('red')
                    o._objects[1].setColor('red')
                  }
                  if (APICall[i].occupied === false) {
                    o.occupied = false
                    o._objects[0].setColor('black')
                    o._objects[1].setColor('black')
                  }
                }
              }
            })
          }
          this.viewCanvas.renderAll()
        }).catch(error => {
          console.log(error)
        })
      },
      loadViewCanvas (id) {
        Loading.show({
          message: 'Loading Canvas'
        })
        window.clearInterval(this.updateTimer)
        if (this.viewCanvas === null) {
          this.viewCanvas = new window.fabric.Canvas('viewCanvas')
          // Opens Popover for clicking on computers
          let page = this
          this.viewCanvas.on('mouse:down', function (obj) {
            if (obj.target !== null) {
              if (obj.target.class === 'computer') {
                page.updateComputerInfo(obj.target)
              }
            }
          })
          this.viewCanvas.forEachObject(function (o) {
            o.selectable = false
          })
        } else {
          this.viewCanvas.clear()
        }
        this.viewCanvas.id = 'viewCanvas'
        // API Call to get the saved Canvas this.chosenSite
        this.$http({
          method: 'get',
          url: '/api/site/' + id + '/canvas/'
        }).then(response => {
          if (response.status === 250) {
            this.$router.error = response.data
            this.$router.push({path: '/error'})
          }
          Loading.hide()
          let apiCall = response.data
          if (apiCall === '') {
            apiCall = []
          }
          if (apiCall.length === 0) {
            this.loadCanvas(apiCall, this.viewCanvas)
          } else {
            this.loadCanvas(apiCall, this.viewCanvas)
          }
          this.updateOccupied()
          this.updateTimer = window.setInterval(() => this.updateOccupied(), 20000)
        }).catch(error => {
          console.log(error)
        })
      }
    }
  }
</script>
<style>
</style>
