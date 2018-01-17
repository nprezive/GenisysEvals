<template>
  <div class="animated fadeIn" id="CheckIn" v-if="checked && stations && sites && site">
    <div class="row">
      <div class="col-12">
        <!--<router-view :sites="sites" :clickSite="clickSite"></router-view>-->
        <q-tabs align="justify" @select="tabLeave(editCanvas)" v-model="selectedTab" inverted
                style="background-color: white;" class="">
          <q-tab default slot="title" name="Check-in Site">Check-in Site</q-tab>
          <q-tab slot="title" name="Edit Site">Edit Site</q-tab>

          <q-tab-pane name="Check-in Site">
            <div class="row">
              <q-toolbar inverted color="dark" class="bg-light col-12">
                <q-toolbar-title>
                  Check-In Tools
                </q-toolbar-title>
                <q-fab color="primary" active-icon="fa-times" icon="fa-cogs" direction="left">
                  <q-fab-action color="primary" @click="openModal('checkinStudent')" icon="fa-user-plus">
                    <q-tooltip anchor="center left" self="center right" :offset="[20, 0]">Check-In Student</q-tooltip>
                  </q-fab-action>
                </q-fab>
              </q-toolbar>
            </div>
            <div class="row">
              <div class="col-lg-2 col-md-12">
                <sites :sites="sites" :clickSite="clickSite" :chosenSite="chosenSite"></sites>
              </div>
              <div class="col-lg-10 col-md-12">
                <view-canvas ref="viewCanvas" :updateComputerInfo="updateComputerInfo" :loadCanvas="loadCanvas"
                             :fixCanvas="fixCanvas"
                             :viewCanvas="viewCanvas" :chosenSite="chosenSite"></view-canvas>
              </div>
            </div>
          </q-tab-pane>
          <q-tab-pane name="Edit Site">
            <div class="row">
              <q-toolbar inverted color="dark" class="bg-light col-12">
                <q-toolbar-title>
                  Edit Site Tools
                </q-toolbar-title>
                <q-fab ref="editToolbar" color="primary" active-icon="fa-times" icon="fa-cogs" direction="left">
                  <q-fab-action color="positive" @click="saveCanvas" icon="fa-download">
                    <q-tooltip anchor="center left" self="center right" :offset="[20, 0]">Save Canvas</q-tooltip>
                  </q-fab-action>
                  <q-fab-action color="warning" @click="openOptions" icon="fa-cog">
                    <q-tooltip anchor="center left" self="center right" :offset="[20, 0]">Site Options</q-tooltip>
                  </q-fab-action>
                  <q-fab-action color="red" @click="deleteObject" icon="fa-ban">
                    <q-tooltip anchor="center left" self="center right" :offset="[20, 0]">Delete Object</q-tooltip>
                  </q-fab-action>
                  <q-fab-action color="secondary" @click="" icon="fa-laptop">
                    <q-tooltip anchor="center left" self="center right" :offset="[20, 0]">Add Computer</q-tooltip>
                    <q-popover>
                      <q-list>
                        <q-item v-for="(station, index) in stations" :key="index" class="mt-1" :id="'c' + station.id"
                                :ref="'c' + station.id">
                          <q-btn color="primary" class="ml-auto mr-auto"
                                 @click="addComputer(station.name, station.id)">{{ station.name }}
                          </q-btn>
                        </q-item>
                      </q-list>
                      <div v-if="noComputers">
                        There are no more computers to add.
                      </div>
                      <div v-if="!noComputers" style="visibility: hidden; height: 0px;">
                        There are no more computers to add.
                      </div>
                    </q-popover>
                  </q-fab-action>
                  <q-fab-action color="primary" @click="addRoom" icon="fa-plus">
                    <q-tooltip anchor="center left" self="center right" :offset="[20, 0]">Create Room</q-tooltip>
                  </q-fab-action>
                </q-fab>
              </q-toolbar>
            </div>
            <div class="row">
              <div class="col-lg-2 col-md-4">
                <sites :sites="sites" :clickSite="clickSite" :chosenSite="chosenSite"></sites>
              </div>
              <div class="col-md-10 col-sm-12">
                <edit-canvas ref="editCanvas" :keepInBounds="keepInBounds" :loadCanvas="loadCanvas"
                             :fixCanvas="fixCanvas"
                             :editCanvas="editCanvas" :chosenSite="chosenSite"></edit-canvas>
              </div>
            </div>
          </q-tab-pane>
        </q-tabs>
        <q-modal @close="pickedStation = false; studentSelected = false; studentsMatched = false; studentExams = []; matchedStudents = []; matchedStudents = ''; studentW = ''; selectedExam = '';" ref="checkinStudent" minimized>
          <div class="m-3">
            <div v-if="!studentsMatched && !studentSelected">
              <q-field>
                <q-input v-on:keyup.enter="submitW" v-model="studentW" float-label="Enter Student's WildcatID"></q-input>
              </q-field>
              <q-btn class="mt-1" color="primary" @click="submitW" push>Submit</q-btn>
            </div>
            <div v-if="studentsMatched && !studentSelected">
              <q-field>
                <q-select @change="selectStudent" v-model="selectedStudent" float-label="Students" :options="matchedStudents"></q-select>
              </q-field>
              <q-btn class="mt-1" color="negative" @click="studentsMatched = false; matchedStudents = [];" push>Back</q-btn>
            </div>
            <div v-if="studentSelected && studentsMatched">
              <q-select v-model="selectedExam" float-label="Student's Exams" :options="studentExams"></q-select>
              <q-btn class="mt-1" color="negative" @click="studentSelected = false; selectedStudent = '';" push>Back</q-btn>
              <q-btn color="primary" @click="submitExam" :disabled="!studentSelected">Submit</q-btn>
            </div>
          </div>
        </q-modal>
        <q-modal minimized ref="computerInfo">
          <computer-info v-if="station" :station="station"></computer-info>
        </q-modal>
        <q-modal minimized ref="siteOptions" @close="saveOptions">
          <site-options ref="siteOption" :site="site" @update="updateStations" :stations="stations"></site-options>
        </q-modal>
      </div><!--/.col-->
    </div><!--/.row-->
  </div>
</template>

<script>
  import {
    Dialog,
    Toast,
    Loading
  } from 'quasar'
  import Sites from '../views/Sites.vue'
  import '../../statics/js/fabric.exec.js'
  import ComputerInfo from '../views/checkin/ComputerInfo'
  import SiteOptions from '../views/checkin/SiteOptions'
  import ViewCanvas from '../views/checkin/ViewCanvas.vue'
  import EditCanvas from '../views/checkin/EditCanvas.vue'

  export default {
    name: 'Checkin',
    components: {
      Sites,
      ComputerInfo,
      SiteOptions,
      ViewCanvas,
      EditCanvas
    },
    data () {
      return {
        checked: false,
        chosenSite: 1,
        editCanvas: null,
        viewCanvas: null,
        bounds: null,
        goodTop: null,
        goodLeft: null,
        noComputers: false,
        size: 'small',
        studentW: '',
        studentExams: [],
        selectedExam: '',
        studentSelected: false,
        station: false,
        pickedStation: false,
        needSave: false,
        selectedTab: 'Check-in Site',
        matchedStudents: [],
        selectedStudent: '',
        studentsMatched: false,
        sites: false,
        stations: false,
        site: false
      }
    },
    mounted () {
      this.$http({
        method: 'post',
        url: '/api/isloggedin/'
      }).then(response => {
        if (response.status === 200) {
          this.checked = true
        }
        if (response.status === 250) {
          this.$router.push({path: '/login'})
        }
      }).catch(error => {
        console.log(error)
      })

      Loading.show({
        message: 'Getting Site Info'
      })
      // API Call to get the sites
      this.$http({
        method: 'get',
        url: '/api/checkinsites/'
      }).then(response => {
        if (response.status === 250) {
          this.$router.error = response.data
          this.$router.push({path: '/error'})
        }
        this.$http({
          method: 'get',
          url: '/api/site/' + this.chosenSite + '/siteinfo/'
        }).then(response => {
          if (response.status === 250) {
            this.$router.error = response.data
            this.$router.push({path: '/error'})
          }
          Loading.hide()
          this.site = response.data
        }).catch(error => {
          console.log(error)
        })
        this.sites = response.data
      }).catch(error => {
        console.log(error)
      })
      // API Call to get the stations of teh site
      this.$http({
        method: 'get',
        url: '/api/site/' + this.chosenSite + '/sitecomputers/'
      }).then(response => {
        if (response.status === 250) {
          this.$router.error = response.data
          this.$router.push({path: '/error'})
        }
        this.stations = response.data
      }).catch(error => {
        console.log(error)
      })
    },
    methods: {
      saveOptions () {
        this.$http({
          method: 'post',
          url: '/api/site/' + this.chosenSite + '/siteoptions/',
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          },
          data: {
            options: this.$refs['siteOption'].siteOptions
          }
        }).then(response => {
          if (response.status === 250) {
            this.$router.error = response.data
            this.$router.push({path: '/error'})
          }
        }).catch(error => {
          console.log(error)
        })
      },
      clickSite: function (site) {
        Loading.show({
          message: 'Getting Site Info'
        })
        this.chosenSite = site.id
        this.$http({
          method: 'get',
          url: '/api/site/' + this.chosenSite + '/siteinfo/'
        }).then(response => {
          if (response.status === 250) {
            this.$router.error = response.data
            this.$router.push({path: '/error'})
          }
          Loading.hide()
          this.site = response.data
        }).catch(error => {
          console.log(error)
        })
        // API Call for Stations
        this.$http({
          method: 'get',
          url: '/api/site/' + this.chosenSite + '/sitecomputers/'
        }).then(response => {
          if (response.status === 250) {
            this.$router.error = response.data
            this.$router.push({path: '/error'})
          }
          Loading.hide()
          this.stations = response.data
        }).catch(error => {
          console.log(error)
        })
        this.$refs.siteOption.updateSiteOptions(site.id)
        if (this.$refs.viewCanvas) {
          this.$refs.viewCanvas.loadViewCanvas(site.id)
        }
        if (this.$refs.editCanvas) {
          this.$refs.editCanvas.loadEditCanvas(site.id)
        }
      },
      tabLeave (editCanvas) {
        if (this.needSave) {
          let that = this
          Dialog.create({
            title: 'Confirm',
            message: 'Save your changes?',
            buttons: [
              {
                label: 'Do not save.',
                handler () {
                  Toast.create('Not saved.')
                }
              },
              {
                label: 'Yes, save.',
                handler () {
                  that.forgotSave(editCanvas)
                  Toast.create('Saved!')
                }
              }
            ]
          })
          this.needSave = false
        }
      },
      updateStations (value) {
        this.stations[value.indx][value.type] = value.newValue
      },
      openOptions () {
        this.$refs.siteOptions.open()
      },
      submitExam () {
        let examInfo = {
          exam: this.selectedExam,
          user: this.selectedStudent
        }
        if (this.pickedStation === false) {
          let window = this
          setTimeout(function () {
            alert('Please pick a station')
            window.pickedStation = true
          }, 1000)
        } else {
          // Insert APICall that checks in student to computer based on this.pickedStation (This is the id)
          Loading.show({
            message: 'Checking in Student'
          })
          this.$http({
            method: 'post',
            url: '/api/sitecomputer/' + this.pickedStation + '/checkin/',
            headers: {
              'X-CSRFToken': this.getCookie('csrftoken')
            },
            data: {
              exam: examInfo.exam,
              user: examInfo.user
            }
          }).then(response => {
            if (response.status === 250) {
              this.$router.error = response.data
              this.$router.push({path: '/error'})
            }
            Loading.hide()
            this.$refs.checkinStudent.close()
            this.pickedStation = false
            this.$refs.viewCanvas.updateOccupied()
          }).catch(error => {
            console.log(error)
          })
        }
      },
      updateComputerInfo (obj) {
        if (this.pickedStation === false) {
          Loading.show({
            message: 'Retrieving Student Info'
          })
          // Get the Info for the Station
          this.$http({
            method: 'get',
            url: '/api/sitecomputer/' + obj.id.slice(1) + '/computerinfo/'
          }).then(response => {
            if (response.status === 250) {
              this.$router.error = response.data
              this.$router.push({path: '/error'})
            }
            Loading.hide()
            this.station = response.data
            let isTaken = false
            for (let i = 0; i < this.stations.length; i++) {
              if (obj.id === 'c' + this.stations[i].id) {
                if (obj.occupied) {
                  isTaken = true
                  break
                } else {
                  isTaken = false
                }
              }
            }
            if (isTaken) {
              this.openPopover()
            } else {
              this.pickedStation = obj.id
              this.$refs.checkinStudent.open()
            }
          }).catch(error => {
            console.log(error)
          })
        } else {
          let isTaken = false
          for (let i = 0; i < this.stations.length; i++) {
            if (obj.id === this.stations[i].id) {
              if (this.stations[i].occupied) {
                isTaken = true
                break
              } else {
                isTaken = false
              }
            }
          }
          if (isTaken) {
            alert('Please pick an unoccupied station.')
          } else {
            this.pickedStation = obj.id
            this.submitExam()
          }
        }
      },
      openPopover () {
        this.$refs.computerInfo.open()
      },
      deleteObject () {
        this.needSave = true
        let activeObject = this.editCanvas.getActiveObject()
        let activeId = activeObject.id
        if (confirm('Are you sure?')) {
          if (activeObject.class === 'computer') {
            this.$refs[activeId][0].style.display = 'inherit'
          }
          this.editCanvas.remove(this.editCanvas.getActiveObject())
        }
      },
      loadCanvas (canvasJson, canvas) {
        this.editCanvas = canvas
        if (canvasJson.length !== 0) {
          if (canvas.id === 'editCanvas') {
            let that = this
            canvas.loadFromJSON(canvasJson, function () {
            }, function (o) {
              if (o.class === 'computer') {
                that.$refs[o.id][0].style.display = 'none'
              }
            })
          } else {
            canvas.loadFromJSON(canvasJson, function () {
            }, function (o) {
            })
            this.editCanvas.forEachObject(function (o) {
              o.selectable = false
            })
          }
          canvas.renderAll.bind(this.editCanvas)
        }
        this.fixCanvas(canvas)
      },
      saveCanvas () {
        let canvasJson = JSON.stringify(this.editCanvas.toJSON(['id', 'name', 'text', 'originX', 'originY', 'fill', 'fontFamily', 'class', 'selectable', '_controlsVisibility', 'Zindex', 'id', 'lockMovementX', 'evented', 'hasBorders', 'lockMovementY', 'lockRotation', 'lockScalingX', 'lockScalingY', 'lockUniScaling', 'hasControls', 'strokeWidth', 'stroke']))
        Loading.show({
          message: 'Saving Canvas'
        })
        this.$http({
          method: 'post',
          url: '/api/site/' + this.chosenSite + '/canvas/',
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          },
          data: {
            canvas: canvasJson
          }
        }).then(response => {
          if (response.status === 250) {
            this.$router.error = response.data
            this.$router.push({path: '/error'})
          }
          Loading.hide()
        }).catch(error => {
          console.log(error)
        })
        this.needSave = false
      },
      forgotSave (canvas) {
        let canvasJson = JSON.stringify(canvas.toJSON(['id', 'name', 'text', 'originX', 'originY', 'fill', 'fontFamily', 'class', 'selectable', '_controlsVisibility', 'Zindex', 'id', 'lockMovementX', 'evented', 'hasBorders', 'lockMovementY', 'lockRotation', 'lockScalingX', 'lockScalingY', 'lockUniScaling', 'hasControls', 'strokeWidth', 'stroke']))
        Loading.show({
          message: 'Saving Canvas'
        })
        this.$http({
          method: 'post',
          url: '/api/site/' + this.chosenSite + '/canvas/',
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          },
          data: {
            canvas: canvasJson
          }
        }).then(response => {
          if (response.status === 250) {
            this.$router.error = response.data
            this.$router.push({path: '/error'})
          }
          Loading.hide()
        }).catch(error => {
          console.log(error)
        })
        this.needSave = false
      },
      getCookie (name) {
        let cookieValue = null
        if (document.cookie && document.cookie !== '') {
          let cookies = document.cookie.split(';')
          for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim()
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
              break
            }
          }
        }
        return cookieValue
      },
      submitW () {
        // API Call to get Users
        Loading.show({
          message: 'Searching for Students'
        })
        this.$http({
          method: 'post',
          url: '/api/userbylookup',
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          },
          data: {
            user: this.studentW
          }
        }).then(response => {
          if (response.status === 250) {
            this.$router.error = response.data
            this.$router.push({path: '/error'})
          }
          Loading.hide()
          this.matchedStudents = response.data
          this.studentsMatched = true
        }).catch(error => {
          console.log(error)
        })
      },
      selectStudent (v) {
        Loading.show({
          message: 'Searching for Exams'
        })
        this.$http({
          method: 'get',
          url: '/api/user/' + v + '/checkinexams/'
        }).then(response => {
          if (response.status === 250) {
            this.$router.error = response.data
            this.$router.push({path: '/error'})
          }
          Loading.hide()
          this.studentExams = response.data
          this.studentSelected = true
        }).catch(error => {
          console.log(error)
        })
      },
      openModal (ref) {
        this.$refs[ref].open()
      },
      closeModal (ref) {
        this.$refs[ref].close()
      },
      addRoom: function () {
        this.needSave = true
        let room = new window.fabric.Rect({
          top: 100,
          left: 100,
          width: 50,
          height: 50,
          fill: 'transparent',
          stroke: 'black',
          strokeWidth: 0.5,
          Zindex: -1,
          class: 'room',
          id: ''
        })
        room.setControlsVisibility({
          mtr: false
        })
        this.editCanvas.add(room)
        let keepCount = 0
        this.editCanvas.forEachObject(function (o) {
          if (o.Zindex === -2) {
            o.moveTo(keepCount)
            keepCount++
          }
        })
        this.editCanvas.forEachObject(function (o) {
          if (o.Zindex === -1) {
            o.moveTo(keepCount)
            keepCount++
          }
        })
        this.editCanvas.forEachObject(function (o) {
          if (o.Zindex === 0) {
            o.moveTo(keepCount)
            keepCount++
          }
        })
        this.editCanvas.forEachObject(function (o) {
          if (o.Zindex === 1) {
            o.moveTo(keepCount)
            keepCount++
          }
        })
      },
      addComputer: function (name, id) {
        this.needSave = true
        let text
        text = new window.fabric.IText('\uf108', {
          fill: 'black',
          originX: 'center',
          originY: 'center',
          left: 0,
          top: 0,
          fontSize: 40,
          fontFamily: 'FontAwesome',
          Zindex: 1
        })
        let cText
        if (name.length < 4) {
          cText = new window.fabric.Text(name, {
            originX: 'center',
            originY: 'center',
            left: 0,
            top: -8
          })
        }
        if (name.length >= 4) {
          cText = new window.fabric.Text(name.slice(0, 3), {
            originX: 'center',
            originY: 'center',
            left: 0,
            top: -8
          })
        }
        cText.scaleToHeight(15)
        let cGroup = new window.fabric.Group([text, cText], {
          top: 100,
          left: 100
        })
        cGroup.lockScalingY = true
        cGroup.lockScalingX = true
        cGroup.lockRotation = true
        cGroup.id = 'c' + id
        cGroup.class = 'computer'
        cGroup.Zindex = 1
        cGroup.name = name
        cGroup.setControlsVisibility({
          mt: false,
          mb: false,
          ml: false,
          mr: false,
          bl: false,
          br: false,
          tl: false,
          tr: false,
          mtr: false
        })
        document.getElementById('c' + id).style.display = 'none'
        for (let i = 0; i < this.stations.length; i++) {
          let tempID = this.stations[i].id
          if (document.getElementById('c' + tempID).style.display !== 'none') {
            this.noComputers = false
            break
          }
          this.noComputers = true
        }
        cGroup.Zindex = 1
        this.editCanvas.add(cGroup)
      },
      keepInBounds: function () {
        let obj
        if (this.editCanvas.getActiveObjects()[0] !== undefined) {
          obj = this.editCanvas.getActiveObjects()[0]
          obj.setCoords()
          if (!obj.isContainedWithinObject(this.bounds)) {
            obj.setTop(this.goodTop)
            obj.setLeft(this.goodLeft)
            obj.setCoords()
          } else {
            this.goodTop = obj.top
            this.goodLeft = obj.left
          }
        }
      },
      fixCanvas: function (canvas) {
        let keepCount = 0
        canvas.forEachObject(function (o) {
          if (o.Zindex === -2) {
            o.moveTo(keepCount)
            keepCount++
          }
        })
        canvas.forEachObject(function (o) {
          if (o.Zindex === -1) {
            o.moveTo(keepCount)
            keepCount++
          }
        })
        canvas.forEachObject(function (o) {
          if (o.Zindex === 0) {
            o.moveTo(keepCount)
            keepCount++
          }
        })
        canvas.forEachObject(function (o) {
          if (o.Zindex === 1) {
            o.moveTo(keepCount)
            keepCount++
          }
        })
        if (canvas.id === 'viewCanvas') {
          canvas.forEachObject(function (o) {
            o.selectable = false
          })
        }
        canvas.selection = false
      }
    }
  }
</script>

<style lang="stylus">
  #CheckIn .canvas-container {
    border: 1px solid black
  }

  #CheckIn .q-tabs-head {
    padding: 0 !important
  }

  #CheckIn .q-tab-pane {
    padding: 0
  }

  #CheckIn .q-list {
    padding: 0
  }

  #CheckIn .q-toolbar {
    box-shadow: 0 0 2px rgba(0, 0, 0, .12), 0 2px 2px rgba(0, 0, 0, .2)
    margin-bottom: 4px
  }
</style>
