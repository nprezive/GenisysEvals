<template>
  <div class="mb-3 mt-3">
    <canvas id="editCanvas" width="1280" height="720"></canvas>
  </div>
</template>
<script>
  import {
    Loading
  } from 'quasar'

  export default {
    name: 'EditCanvas',
    props: {
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
        bounds: null,
        editCanvas: null
      }
    },
    mounted () {
      this.loadEditCanvas(this.chosenSite)
    },
    methods: {
      loadEditCanvas (id) {
        Loading.show({
          message: 'Loading Canvas'
        })
        let grid = 40
        if (this.editCanvas === null) {
          this.editCanvas = new window.fabric.Canvas('editCanvas')
          // Clips stuff to Grid
          this.editCanvas.on('object:moving', function (options) {
            options.target.set({
              left: Math.round(options.target.left / grid) * grid,
              top: Math.round(options.target.top / grid) * grid
            })
          })
          // Keeps Adjustable objects in mutiples of grid
          this.editCanvas.on('object:modified', function (options) {
            if (options.target.class === 'room') {
              options.target.set({opacity: 1})
              let newWidth = (Math.round(options.target.getWidth() / grid)) * grid
              let newHeight = (Math.round(options.target.getHeight() / grid)) * grid
              if (options.target.getWidth() !== newWidth) {
                options.target.set({width: newWidth, height: newHeight, scaleX: 1, scaleY: 1})
              }
            }
          })
          // Keeps Objects within Canvas
          let that = this
          this.editCanvas.on('object:moving', function (obj) {
            obj = obj.target
            obj.setCoords()
            if (!obj.isContainedWithinObject(that.bounds)) {
              obj.setTop(that.goodTop)
              obj.setLeft(that.goodLeft)
              obj.setCoords()
            } else {
              that.goodTop = obj.top
              that.goodLeft = obj.left
            }
          })
        } else {
          this.editCanvas.clear()
        }
        this.editCanvas.id = 'editCanvas'
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
            this.editCanvas.setHeight(720)
            this.editCanvas.setWidth(1280)
            this.editCanvas.selection = false

            this.bounds = new window.fabric.Rect({
              top: -10,
              left: -10,
              width: this.editCanvas.getWidth() + 20,
              height: this.editCanvas.getHeight() + 20,
              fill: 'transparent',
              hasBorders: false,
              hasControls: false,
              lockMovementX: true,
              lockMovementY: true,
              selectable: false,
              evented: false,
              id: 'bounds',
              Zindex: -2,
              class: 'bounds'
            })
            this.editCanvas.add(this.bounds)

            for (let i = 0; i < (this.editCanvas.getWidth() / grid); i++) {
              this.editCanvas.add(new window.fabric.Line([i * grid, 0, i * grid, this.editCanvas.getHeight()], {
                stroke: 'transparent',
                selectable: false,
                strokeWidth: 0,
                Zindex: -1,
                class: 'grid'
              }))
            }
            for (let i = 0; i < (this.editCanvas.getHeight() / grid); i++) {
              this.editCanvas.add(new window.fabric.Line([0, i * grid, this.editCanvas.getWidth(), i * grid], {
                stroke: 'transparent',
                selectable: false,
                strokeWidth: 0,
                Zindex: -1,
                class: 'grid'
              }))
            }
            this.loadCanvas(JSON.stringify(this.editCanvas.toJSON(['certificate', 'name', 'text', 'originX', 'originY', 'fill', 'fontFamily', 'class', 'selectable', '_controlsVisibility', 'Zindex', 'id', 'lockMovementX', 'evented', 'hasBorders', 'lockMovementY', 'lockRotation', 'lockScalingX', 'lockScalingY', 'lockUniScaling', 'hasControls', 'strokeWidth', 'stroke'])), this.editCanvas)
          } else {
            this.loadCanvas(apiCall, this.editCanvas)
            let that = this
            this.editCanvas.forEachObject(function (o) {
              if (o.id === 'bounds') {
                that.bounds = o
              }
            })
          }
        }).catch(error => {
          console.log(error)
        })
      }
    }
  }
</script>
<style>
</style>
