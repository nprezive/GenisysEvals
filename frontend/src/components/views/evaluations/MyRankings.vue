new Vue({
el: '#root',
data: {
picked: 'b'
}
});

<template>
  <div class="row clearfix p-1">
    <div class="col-md-12 col-lg-4 clearfix">
      <q-card class="center">
        <q-card-title class="bg-primary">

          <b>My Reports</b>
        </q-card-title>
        <q-card-main class="card-block pt-2">

          <q-list>

            <q-collapsible group="somegroup"  label="Terms" ref="mycollapse" >
              <div class="center">

                <select class="center" size="4" style="width: 250px;" font-size="24px;">
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
                <select class="center" size="4" style="width: 250px;" font-size="24px;">
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
                <select class="center" size="4" style="width: 250px;" font-size="24px;">
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

              <div class="center" v-if="picked === 'Instructor'">
                Select to include
                <br></br>
                <select size="4" style="width: 250px;" font-size="24px;">
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
    </div>
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
    data() {
      return{
        picked: ''
      }
    }
  }

</script>

