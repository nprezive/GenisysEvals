<template>
  <div class="animated fadeIn proctoring">
    <div class="row">
      <div class="col-12">
        <q-tabs align="justify" inverted
                style="background-color: white">
          <!--TODO at tab change call newProctor()-->
          <q-tab default label="Proctoring" slot="title"
                 name="tab-1"></q-tab>
          <q-tab-pane name="tab-1" class="p-0" v-if="proctors.length > 0">
            <q-toolbar inverted color="dark" class="bg-light">
              <q-toolbar-title>
                Proctor Tools
              </q-toolbar-title>
              <q-fab color="primary" active-icon="fa-times" icon="fa-cogs" direction="left">
                <q-fab-action color="negative" @click="toast('alarm')" icon="fa-question">
                  <q-tooltip anchor="center left" self="center right" :offset="[20, 0]">Need Help?</q-tooltip>
                </q-fab-action>
                <q-fab-action color="secondary" @click="toast('alarm')" icon="fa-globe">
                  <q-tooltip anchor="center left" self="center right" :offset="[20, 0]">Request Proctored Exam
                  </q-tooltip>
                </q-fab-action>
                <q-fab-action color="primary" @click="toast('alarm')" icon="fa-user">
                  <q-tooltip anchor="center left" self="center right" :offset="[20, 0]">Create A Proctor</q-tooltip>
                </q-fab-action>
              </q-fab>
            </q-toolbar>
            <div class="row clearfix p-1">
              <div class="col-md-12 col-lg-4 clearfix">
                <q-card>
                  <q-card-title class="bg-primary">
                    <b>What is Proctoring?</b>
                  </q-card-title>
                  <q-card-main class="card-block pt-2">
                    <p>
                      A proctor is a person who is in no way related to the student, nor are they a friend, roommate, neighbor, coach,
                      current teacher, employer, supervisor or co-worker. They supervise students as they take exams, thus ensuring a
                      secure environment free of distractions and/or resources that might compromise the integrity of the student.
                    </p>
                    <p>
                      Suitable proctors include college/university testing center staff, college/university librarians, college/university
                      distance learning staff, professional testing services, and in some cases military education officers.
                    </p>
                    <p>
                      Some proctors will provide their services at no cost. If the proctor or testing center charges a fee, it is the
                      responsibility of the student to pay. Students should find out about fees, prior to setting up a proctor.
                    </p>
                    <p>
                      Proctors must have a computer with internet access and be able to understand instructions written in English.
                    </p>
                    <p>
                      Only professional credentials of the proctor are allowed when entering his/her information. Personal email address,
                      street addresses and/or phone numbers will not be accepted.
                    </p>
                  </q-card-main>
                </q-card>
              </div>
              <div class="col-md-12 col-lg-8 clearfix">
                <q-card>
                  <q-card-title class="bg-primary">
                    <b>Proctor Locations</b>
                  </q-card-title>
                  <q-card-main>
                    <gmap-map id="proctorMap" class="card-block" :center="center" :zoom="10" style="height: 477px;">
                      <gmap-info-window :options="infoOptions" :position="infoWindowPos"
                                        :opened="infoWindowOpen" :content="infoContent"
                                        @closeclick="infoWindowOpen=false"></gmap-info-window>
                      <gmap-marker :key="index" v-for="(proctor, index) in allProctors"
                                   :position="{lat: proctor.latitude, lng: proctor.longitude}"
                                   :clickable="true" @click="proctorClick(proctor, index)"
                                   v-if="!proctor.donotuse && proctor.advertised && proctor.approved">
                      </gmap-marker>
                    </gmap-map>
                  </q-card-main>
                </q-card>
              </div>
            </div>
          </q-tab-pane>
          <q-tab label="My Proctors" slot="title"
                 name="tab-2"></q-tab>
          <q-tab-pane name="tab-2" class="p-0">
            <q-toolbar inverted color="dark" class="bg-light">
              <q-toolbar-title>
                Proctor Tools
              </q-toolbar-title>
              <q-fab color="primary" active-icon="fa-times" icon="fa-cogs" direction="left">
                <q-fab-action color="negative" @click="toast('alarm')" icon="fa-question">
                  <q-tooltip anchor="center left" self="center right" :offset="[20, 0]">Need Help?</q-tooltip>
                </q-fab-action>
                <q-fab-action color="secondary" @click="toast('alarm')" icon="fa-globe">
                  <q-tooltip anchor="center left" self="center right" :offset="[20, 0]">Request Proctored Exam
                  </q-tooltip>
                </q-fab-action>
                <q-fab-action color="primary" @click="toast('alarm')" icon="fa-user">
                  <q-tooltip anchor="center left" self="center right" :offset="[20, 0]">Create A Proctor</q-tooltip>
                </q-fab-action>
              </q-fab>
            </q-toolbar>
            <div class="row">
              <div class="col-2">
                <q-list no-border separator link>
                  <q-item :class="{active: index === setActiveProctor()}"
                          v-for="(proctor, index) in proctors"
                          :key="index" @click="changeProctor(proctor, index)">
                    <q-item-side color="primary" icon="fa-slideshare"></q-item-side>
                    <q-item-main>
                      <q-item-tile label class="font-sm">
                        {{proctor.firstname + " " + proctor.lastname}}
                      </q-item-tile>
                    </q-item-main>
                  </q-item>
                </q-list>
              </div>
              <div class="col-10">
                <q-card>
                  <Proctor :proctor="activeProctor" :setDefaultProctor="setDefaultProctor"></Proctor>
                </q-card>
              </div>
            </div>
          </q-tab-pane>
        </q-tabs>
      </div>
    </div>
  </div>
</template>
<script>
  import * as VueGoogleMaps from 'vue2-google-maps'
  import Vue from 'vue'
  import Proctor from './proctoring/proctor'

  Vue.use(VueGoogleMaps, {
    load: {
      key: 'AIzaSyDqB5cf-GgBvQl8sstOcsjbznysYsYPbow'
    }
  })
  export default {
    name: 'proctoring',
    components: {
      Proctor
    },
    data () {
      return {
        msg: 'Proctoring',
        center: {lat: 41.1924, lng: -111.9419},
        infoWindowPos: {lat: 0, lng: 0},
        infoWindowOpen: true,
        infoContent: '',
        infoOptions: {},
        size: 'small',
        statusText: '',
        currentMidx: null,
        activeProctor: {},
        activeProctorIndex: 0
      }
    },
    mounted: function () {
      this.newProctor()
      if (this.proctors) {
        this.activeProctorIndex = 0
        this.activeProctor = this.proctors[0]
      }
    },
    computed: {
      proctors () {
        // APICall to get student's proctors
        let apiCall = [
          {
            id: 1,
            firstname: 'Bob',
            lastname: 'Marley',
            position: 'Artist',
            institution: 'Music Industries',
            streetaddress: '1586 Rough Road, Salt Lake City, UT',
            zip: '84111',
            email: 'DoNotUse@gmail.com',
            phone: '(123) 456-7890',
            fee: 'Free',
            isDefault: false,
            registered: 'January 1, 2017'
          },
          {
            id: 2,
            firstname: 'Michael',
            lastname: 'Jackson',
            position: 'Artist',
            institution: 'Music Industries',
            streetaddress: '3600 W 1800 S, New York, NY',
            zip: '80879',
            email: 'DoNotUse@hotmail.com',
            phone: '(098) 765-4321',
            fee: 'Your First Born Child',
            isDefault: true,
            registered: 'February 1, 2016'
          }]
        return apiCall
      },
      allProctors () {
        let apiCall = [
          {
            id: 1,
            firstname: 'Bob',
            lastname: 'Marley',
            position: 'Artist',
            institution: 'Music Industries',
            streetaddress: '1586 Rough Road, Salt Lake City, UT',
            zip: '84111',
            email: 'DoNotUse@gmail.com',
            phone: '(123) 456-7890',
            fee: 'Free',
            latitude: 41.307729,
            longitude: -111.962700,
            approved: true,
            advertised: true,
            donotuse: false
          },
          {
            id: 2,
            firstname: 'Michael',
            lastname: 'Jackson',
            position: 'Artist',
            institution: 'Music Industries',
            streetaddress: '3600 W 1800 S, New York, NY',
            zip: '80879',
            email: 'DoNotUse@hotmail.com',
            phone: '(098) 765-4321',
            fee: 'Your First Born Child',
            latitude: 41.059680,
            longitude: -111.973000,
            approved: true,
            advertised: true,
            donotuse: false
          }]
        return apiCall
      },
      proctorTitle () {
        if (this.proctors.length < 2) {
          return 'My Proctor'
        } else {
          return 'My Proctors'
        }
      }
    },
    methods: {
      setActiveProctor () {
        return this.activeProctorIndex
      },
      changeProctor (proctor, index) {
        this.activeProctor = proctor
        this.activeProctorIndex = index
      },
      setDefaultProctor: function (proctorID) {
        for (let i = 0; i < this.proctors.length; i++) {
          if (this.proctors[i].isDefault === true) {
            this.proctors[i].isDefault = false
          }
        }
        for (let i = 0; i < this.proctors.length; i++) {
          if (this.proctors[i].id === proctorID) {
            this.proctors[i].isDefault = true
          }
        }
      },
      proctorClick: function (proctor, index) {
        this.center = {
          lat: proctor.latitude,
          lng: proctor.longitude
        }
        this.infoWindowPos = {
          lat: proctor.latitude,
          lng: proctor.longitude
        }
        this.infoContent = '<div class="mapName">' + proctor.firstname + ' ' + proctor.lastname + '</div>' +
          '<div class="mapInside"><span class="mapHeader">Institution: </span>' + proctor.institution + '</div>' +
          '<div class="mapInside"><span class="mapHeader">Phone: </span>' + proctor.phone + '</div>' +
          '<div class="mapInside"><span class="mapHeader">Email: </span>' + proctor.email + '</div>' +
          '<div class="mapInside"><span class="mapHeader">Address: </span>' + proctor.streetaddress + ' ' + proctor.zip + '</div>' +
          '<div class="mapInside"><span class="mapHeader">Fee: </span>' + proctor.fee + '</div><br>' +
          '<button type="button" class="btn btn-primary btn-sm">Use This Proctor</button>'
        if (this.currentMidx === index) {
          this.infoWindowOpen = !this.infoWindowOpen
        } else {
          this.infoWindowOpen = true
          this.currentMidx = index
        }
      },
      newProctor: function () {
        Vue.$gmapDefaultResizeBus.$emit('resize')
        // Try HTML5 geolocation.
        let pos = {
          lat: 41.1924,
          lng: -111.9419
        }
        let myDom = this
        this.infoWindowPos = pos
        this.infoContent = 'Weber State University'
        this.infoWindowOpen = true
        this.center = pos
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(function (position) {
            pos = {
              lat: position.coords.latitude,
              lng: position.coords.longitude
            }
            myDom.infoWindowPos = pos
            myDom.infoContent = 'You Are Here'
            myDom.infoWindowOpen = true
            myDom.center = pos
          }, function () {
            handleLocationError(true, myDom.center)
          })
        } else {
          // Browser doesn't support Geolocation
          handleLocationError(false, myDom.center)
        }

        function handleLocationError (browserHasGeolocation, pos) {
          myDom.infoWindowPos = pos
          myDom.infoContent = (browserHasGeolocation
            ? 'Error: The Geolocation service failed.'
            : 'Error: Your browser doesn\'t support geolocation.')
        }
      }
    }
  }
</script>
<style>
  *,
  *::before,
  *::after {
    box-sizing: border-box;
  }

  html {
    font-size: 100%;
  }

  .mapHeader {
    font-weight: bolder;
    font-size: 1.2em;
  }

  .mapName {
    color: darkblue;
    font-size: 1.2em;
    font-family: 'Signika', sans-serif;
    padding-bottom: 10px;
  }

  .mapInside {
    font-size: .8em;
  }
</style>
