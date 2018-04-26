new Vue({
el: '#root',
data: {
picked: 'b'
}
});

<template>
  <div class="row clearfix p-1">
    <div class="col-md-12 col-lg-12 clearfix">
      <q-card class="center">
        <q-card-main class="card-block pt-2">

          <q-list>

            <q-collapsible group="somegroup"  label="Terms" ref="mycollapse" >
              <div class="center">

                <select multiple class="center" size="4" style="width: 250px;" font-size="24px;">
                  <option >Fall 2016</option>
                  <option >Fall 2017</option>
                  <option >Fall 2018</option>
                  <option >Fall 2019</option>
                  <option >Fall 2020</option>
                  <option >Fall 2021</option>
                  <option >Fall 2022</option>
                  <option >Fall 2017</option>
                  <option >Fall 2018</option>
                  <option >Fall 2019</option>
                  <option >Fall 2020</option>
                  <option >Fall 2021</option>
                  <option >Fall 2022</option>
                </select>

                <br></br>

              </div>

            </q-collapsible>

            <q-collapsible group="somegroup" label="Department" ref="departCollapse" >
              <div class="center">
                Select Departments to include
                <br>
                <select multiple class="center" size="4" style="width: 250px;" font-size="24px;">
                  <option >Computer Science</option>
                  <option >Engineering</option>
                  <option >Math</option>
                  <option >Science</option>
                  <option >Computer Science</option>
                  <option >Engineering</option>
                  <option >Math</option>
                  <option >Science</option>
                </select>
                <br></br>

              </div>

            </q-collapsible>
            <q-collapsible group="somegroup"  label="Sort By">
              <div class="center">
                Sort By
                <br>
                <div id="demo">
                  <input type="radio" id="picked" v-model="picked" name="picked" v-bind:value="'Instructor'" value="Instructor" > Instructor
                  <br>
                  <input type="radio" id="picked" v-model="picked" name="picked" v-bind:value="'Course'" value="Course" > Course
                  <br>
                  <!--<span>Picked: {{ picked }}</span>-->
                </div>

              </div>
            </q-collapsible>
            <q-collapsible group="somegroup" label="Course/Insturctor">
              <div class="center" v-if="picked === 'Course'">
                Select to include
                <br></br>
                <select multiple class="center" size="4" style="width: 250px;" font-size="24px;">
                  <option >CS2420</option>
                  <option >CS2550</option>
                  <option >CS2559</option>
                  <option >CS2690</option>
                  <option >CS2550</option>
                  <option >CS2559</option>
                  <option >CS2690</option>
                  <option >CS2550</option>
                  <option >CS2559</option>
                  <option >CS2690</option>
                  <option >CS2550</option>
                  <option >CS2559</option>
                  <option >CS2690</option>
                </select>
                <br></br>

              </div>

              <div  v-if="picked === 'Instructor'">
                Select to include
                <br>
                <select multiple size="4" style="width: 250px;" font-size="24px;">
                  <option >John Smith</option>
                  <option >Jane Doe</option>
                  <option >Sam Smith</option>
                  <option >John Smith</option>
                  <option >Sam Adams</option>
                  <option >Jake Adams</option>
                  <option >John Smith</option>
                  <option >John Smith</option>
                  <option >John Smith</option>
                  <option >John Smith</option>
                  <option >John Smith</option>
                  <option >John Smith</option>
                  <option >John Smith</option>
                </select>
                <br></br>

              </div>
            </q-collapsible>


            <q-collapsible group="somegroup" label="Report Selection">

              <div class="center">
                Report Options:
                <br></br>
                <input type="radio" id="report" v-model="report" name="report" v-bind:value="'report'" value="report" > Sort per term
                <br>
                <input type="radio" id="report" v-model="report" name="report" v-bind:value="'report'" value="report" > Sort per department
                <br>
                <input type="radio" id="report" v-model="report" name="report" v-bind:value="'report'" value="report" > Sort per instructor/course
                <br>
                <input type="radio" id="report" v-model="report" name="report" v-bind:value="'report'" value="report" > Display all as eval reports
                <br>
                <input type="radio" id="report" v-model="report" name="report" v-bind:value="'report'" value="report" > Display all as one report
                <br>
                <q-btn text-color="black" label="Standard">Build Report</q-btn>

              </div>

            </q-collapsible>

          </q-list>

        </q-card-main>
      </q-card>

            <!--<div>"the value for number is: " + values</div>-->
      <q-card class="center">
        <q-card-title>
          <b>Charts</b>
        </q-card-title>
         <q-card-main class="card-block pt-2">
            <q-btn row inline color="primary" @click="openModal()">Box and Whisker Plot</q-btn>
            <q-btn row inline color="primary" @click="openModal()">Pin Graph</q-btn>
         </q-card-main>
      </q-card>

    </div>
    <q-modal ref="basicModal" :content-css="{padding: '50px'}">
        <div id="boxwhisker"></div>
      <div id="boxwhisker1"></div>
      <q-btn color="primary" @click="$refs.basicModal.close()">Close</q-btn>
    </q-modal>
    <q-modal ref="basicModal" :content-css="{padding: '50px'}">
        <div id="pinGraph"></div>
      <div id="pinGraph1"></div>
      <q-btn color="primary" @click="$refs.basicModal.close()">Close</q-btn>
    </q-modal>
  </div>
</template>
<style>
  .center {
    text-align: center;
    font-size: large;
  }
</style>
<script>




  export default {
    created () {
      let recaptchaScript = document.createElement('script')
      recaptchaScript.setAttribute('src', 'https://cdn.plot.ly/plotly-latest.min.js')
      document.head.appendChild(recaptchaScript)
    },mounted: function (){
      var trace1 = {
        x: [0.2, 0.2, 0.6, 1.0, 0.5, 0.4, 0.2, 0.7, 0.9, 0.1, 0.5, 0.3],
        boxpoints: 'all',
        name: 'Spring 2018',
        marker: {color: '#3D9970'},
        type: 'box',
        boxmean: false,
        orientation: 'h'
      }

      var trace2 = {
        x: [0.6, 0.7, 0.3, 0.6, 0.0, 0.5, 0.7, 0.9, 0.5, 0.8, 0.7, 0.2],
        boxpoints: 'all',
        name: 'Fall 2017',
        marker: {color: '#FF4136'},
        type: 'box',
        boxmean: false,
        orientation: 'h'
      }

      var trace3 = {
        x: [0.1, 0.3, 0.1, 0.9, 0.6, 0.6, 0.9, 1.0, 0.3, 0.6, 0.8, 0.5],
        boxpoints: 'all',
        name: 'Summer 2017',
        marker: {color: '#FF851B'},
        type: 'box',
        boxmean: false,
        orientation: 'h'
      }

      var trace4 = {
        x: [0.24, 0.2, 0.65, 1.0, 0.56, 0.43, 0.2, 0.72, 0.93, 0.18, 0.5, 0.34],
        boxpoints: 'all',
        name: 'Brad Peterson',
        marker: {color: '#3D9970'},
        type: 'box',
        boxmean: false,
        orientation: 'h'
      }

      var trace5 = {
        x: [0.64, 0.76, 0.31, 0.6, 0.0, 0.56, 0.7, 0.99, 0.57, 0.8, 0.74, 0.22],
        boxpoints: 'all',
        name: 'Ted Cowan',
        marker: {color: '#FF4136'},
        type: 'box',
        boxmean: false,
        orientation: 'h'
      }

      var trace6 = {
        x: [0.1, 0.35, 0.1, 0.92, 0.6, 0.6, 0.9, 1.0, 0.3, 0.62, 0.8, 0.53],
        boxpoints: 'all',
        name: 'Josh Jensen',
        marker: {color: '#FF851B'},
        type: 'box',
        boxmean: false,
        orientation: 'h'
      }

      var data = [trace1, trace2, trace3]
      var data2 = [trace4, trace5, trace6]

      var layout = {
        title: '1 Teacher by Semesters',
        xaxis: {
          title: 'Percentage',
          zeroline: false
        },
        boxmode: 'group'
      }
      var layout2 = {
        title: 'Many Teachers to 1 Class',
        annotations: [{
          text: 'CS2420',
            font: {
            size: 13,
            color: 'rgb(116, 101, 130)',
          },
          showarrow: false,
          align: 'center',
          x: 0.5,
          y: 1,
          xref: 'paper',
          yref: 'paper',
        }],
        xaxis: {
          title: 'Percentage',
          zeroline: false
        },
        boxmode: 'group'
      }
      while (!Plotly === true){}
      Plotly.newPlot('boxwhisker', data, layout)
      Plotly.newPlot('boxwhisker1', data2, layout2)
    },
    data () {
      return {
        picked: '',
        counter: 0,
        radio1: 'two',
        radio2: 'one',
        radio3: 'three',
        group: 'upload',
        list: ''
      }
    }, methods: {
      openModal () {
        this.$refs.basicModal.open()
      }
    }
  }
  // var values = $('#select-meal-type').val();
</script>
