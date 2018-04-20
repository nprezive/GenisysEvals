<template>
  <div>
    <q-toolbar inverted color="dark" class="bg-light">
      <q-toolbar-title>
        My Evals - Click on a section to generate an evaluations report.
      </q-toolbar-title>
      <q-btn row inline color="primary" @click="openModal()">Promotion and Tenure</q-btn>
    </q-toolbar>
    <div class="row clearfix p-1">
      <div class="col-md-12 col-lg-12 clearfix">
          <div v-for="sem in semData.s">
            <div class="col-md-12 col-lg-12 clearfix">
            <q-collapsible :label="sem.semester">
                <q-card-main class="card-block pt-2">
                  <div class="row">
                  <div class="col-md-8 col-lg-8 clearfix">
                    <div class="row">
                      <div class="col-md-3 col-lg-3 col-sm-3 col-xs-3 clearfix" style="text-align:center;">
                        <h6>Course</h6>
                      </div>
                      <div class="col-md-3 col-lg-3 col-sm-3 col-xs-3 clearfix" style="text-align:center;">
                        <h6>Evaluate</h6>
                      </div>
                      <div class="col-md-3 col-lg-3 col-sm-3 col-xs-3 clearfix" style="text-align:center;">
                        <h6>Dean/Chair Access</h6>
                      </div>
                      <div class="col-md-3 col-lg-3 col-sm-3 col-xs-3 clearfix" style="text-align:center;">
                        <h6>Public</h6>
                      </div>
                    </div>
                    <div class="row" v-for="c in sem.classes">
                      <div class="col-md-3 col-lg-3 col-sm-3 col-xs-3 clearfix" style="text-align:center;">
                        {{c.className}} <br>
                        <i v-if="!c.isCourseEvaluated">Course is not evaluated</i>
                        <i v-else-if="c.taken > 10">{{c.taken}}/{{c.total}} Have Responded</i>
                        <i v-else-if="c.taken < 10">Less than 10 Students Responded</i>
                      </div>
                      <div class="col-md-3 col-lg-3 col-sm-3 col-xs-3 clearfix" style="text-align:center;">
                        <q-checkbox v-model="c.isCourseEvaluated"/>
                      </div>
                      <div class="col-md-3 col-lg-3 col-sm-3 col-xs-3 clearfix" style="text-align:center;">
                        <q-checkbox v-if="c.isCourseEvaluated" v-model="c.isSharedDeans"/>
                      </div>
                      <div class="col-md-3 col-lg-3 col-sm-3 col-xs-3 clearfix" style="text-align:center;">
                        <q-checkbox v-if="c.isSharedDeans" v-model="c.isPublic"/>
                      </div>
                    </div>
                  </div>
                <div class="col-md-4 col-lg-4 clearfix">
                  <p>By selecting the button below, you are agreeing to send the settings configured for this semester to the Dean or Chair for review.</p>
                  <q-btn inline color="primary">Lock</q-btn>
                </div>
                  </div>
                </q-card-main>
            </q-collapsible>
              <hr style="width:98%;">
            </div>
          </div>
      </div>
        <q-modal ref="basicModal" :content-css="{padding: '50px'}">
          <div id="boxwhisker">
          </div>
          <q-btn color="primary" @click="$refs.basicModal.close()">Close</q-btn>
        </q-modal>
    </div>
  </div>
</template>
<script>
  export default {
    name: 'mydefaults',
    created () {
      let recaptchaScript = document.createElement('script')
      recaptchaScript.setAttribute('src', 'https://cdn.plot.ly/plotly-latest.min.js')
      document.head.appendChild(recaptchaScript)
    },
    mounted:function(){
      var y = ['Semester', 'Semester', 'Semester', 'Semester', 'Semester', 'Semester',
        'Semester', 'Semester', 'Semester', 'Semester', 'Semester', 'Semester']

      var trace1 = {
        x: [0.2, 0.2, 0.6, 1.0, 0.5, 0.4, 0.2, 0.7, 0.9, 0.1, 0.5, 0.3],
        y: y,
        boxpoints: 'all',
        name: 'Spring 2018',
        marker: {color: '#3D9970'},
        type: 'box',
        boxmean: false,
        orientation: 'h'
      }

      var trace2 = {
        x: [0.6, 0.7, 0.3, 0.6, 0.0, 0.5, 0.7, 0.9, 0.5, 0.8, 0.7, 0.2],
        y: y,
        boxpoints: 'all',
        name: 'Fall 2017',
        marker: {color: '#FF4136'},
        type: 'box',
        boxmean: false,
        orientation: 'h'
      }

      var trace3 = {
        x: [0.1, 0.3, 0.1, 0.9, 0.6, 0.6, 0.9, 1.0, 0.3, 0.6, 0.8, 0.5],
        y: y,
        boxpoints: 'all',
        name: 'Summer 2017',
        marker: {color: '#FF851B'},
        type: 'box',
        boxmean: false,
        orientation: 'h'
      }

      var data = [trace1, trace2, trace3]

      var layout = {
        title: 'Evaluations',
        xaxis: {
          title: 'Percentage',
          zeroline: false
        },
        boxmode: 'group'
      }
       while (!Plotly === true){
         var a
       }
       Plotly.newPlot('boxwhisker', data, layout)
    },
    data () {
      return {
        msg: 'Proctoring',
        semData: {
          s: [
            {
              id: 12,
              semester: 'Spring 2018',
              isActive: true,
              classes: [
                {
                  id: 1234,
                  crn: '22325',
                  className: 'CS1400',
                  taken: '22',
                  total: '35',
                  isCourseEvaluated: false,
                  isPublic: false,
                  isSharedDeans: false
                },
                {
                  id: 1233,
                  crn: '22145',
                  className: 'CS1410',
                  taken: '19',
                  total: '25',
                  isCourseEvaluated: false,
                  isPublic: false,
                  isSharedDeans: false
                },
                {
                  id: 12334,
                  crn: '22323',
                  className: 'CS3100',
                  taken: '18',
                  total: '22',
                  isCourseEvaluated: false,
                  isPublic: false,
                  isSharedDeans: false
                },
                {
                  id: 12334,
                  crn: '22323',
                  className: 'CS4110',
                  taken: '9',
                  total: '22',
                  isCourseEvaluated: false,
                  isPublic: false,
                  isSharedDeans: false
                }
              ]
            },
            {
              id: 13,
              semester: 'Fall 2017',
              isActive: false,
              classes: [
                {
                  id: 1234,
                  crn: '22325',
                  className: 'CS1400',
                  taken: '22',
                  total: '35',
                  isCourseEvaluated: false,
                  isPublic: false,
                  isSharedDeans: false
                },
                {
                  id: 1233,
                  crn: '22145',
                  className: 'CS1410',
                  taken: '19',
                  total: '25',
                  isCourseEvaluated: false,
                  isPublic: false,
                  isSharedDeans: false
                },
                {
                  id: 12334,
                  crn: '22323',
                  className: 'CS3100',
                  taken: '18',
                  total: '22',
                  isCourseEvaluated: false,
                  isPublic: false,
                  isSharedDeans: false
                }
              ]
            },
            {
              id: 14,
              semester: 'Spring 2017',
              isActive: false,
              classes: [
                {
                  id: 1234,
                  crn: '22325',
                  className: 'CS1400',
                  taken: '22',
                  total: '35',
                  isCourseEvaluated: false,
                  isPublic: false,
                  isSharedDeans: false
                },
                {
                  id: 1233,
                  crn: '22145',
                  className: 'CS1410',
                  taken: '19',
                  total: '25',
                  isCourseEvaluated: false,
                  isPublic: false,
                  isSharedDeans: false
                },
                {
                  id: 12334,
                  crn: '22323',
                  className: 'CS3100',
                  taken: '18',
                  total: '22',
                  isCourseEvaluated: false,
                  isPublic: false,
                  isSharedDeans: false
                },
                {
                  id: 123343,
                  crn: '223232',
                  className: 'CS3110',
                  taken: '13',
                  total: '22',
                  isCourseEvaluated: false,
                  isPublic: false,
                  isSharedDeans: false
                }
              ]
            }
          ]
        }
      }
    },
    methods: {
      openModal () {
        this.$refs.basicModal.open()
      }
    }
  }
</script>
