<template>
  <div class="row clearfix p-1">
    <div class="col-md-12 col-lg-4 clearfix">
      <q-card class="center">
        <q-card-title class="bg-primary">

          <b>My Reports</b>
        </q-card-title>
        <q-card-main class="card-block pt-2">

          <q-list>

            <q-collapsible group="somegroup"  label="Terms" ref="mycollapse">
              <div class="center">
                <select multiple >
                  <option value="volvo">Fall 2016</option>
                  <option value="saab">Fall 2017</option>
                  <option value="opel">Fall 2018</option>
                  <option value="audi">Fall 2019</option>
                </select>
                <br></br>
                <q-btn text-color="black" label="Standard">Next</q-btn>

              </div>

            </q-collapsible>
            <q-collapsible group="somegroup" label="Department" ref="departCollapse">
              <div class="center">
                Select Departments to include
                <select multiple>
                  <option value="volvo">Computer Science</option>
                  <option value="saab">Engineering</option>
                  <option value="opel">Math</option>
                  <option value="audi">Science</option>
                </select>
                <br></br>
                <q-btn text-color="black" label="Standard">Next</q-btn>

              </div>
            </q-collapsible>
            <q-collapsible group="somegroup" label="Course/Insturctor">
              <div class="center">
                Select to include
                <br></br>
                <select multiple>
                  <option value="volvo">CS2420</option>
                  <option value="saab">CS2550</option>
                  <option value="opel">CS2559</option>
                  <option value="audi">CS2690</option>
                </select>
                <br></br>
                <q-btn text-color="black" label="Standard">Next</q-btn>

              </div>
            </q-collapsible>
            <q-collapsible group="somegroup"  label="Sort By">
              <div class="center">
                Sort By
                <br></br>
                <q-radio v-model="radio1" val="opt1" checked-icon="visibility" label="Instructor" />
                <q-radio v-model="radio1" val="opt2" checked-icon="visibility" label="Course" />
                <br></br>
                <q-btn text-color="black" label="Standard">Next</q-btn>

              </div>
            </q-collapsible>

            <q-collapsible group="somegroup" label="Report Selection">
              <div class="center">
                Report Options:
                <br></br>
                <q-radio v-model="radio1" val="opt1" checked-icon="visibility" label="Sort per term" />
                <q-radio v-model="radio1" val="opt2" checked-icon="visibility" label="Sort per department" />
                <q-radio v-model="radio1" val="opt1" checked-icon="visibility" label="Sort per instructor/course" />
                <q-radio v-model="radio1" val="opt2" checked-icon="visibility" label="Display all as eval reports" />
                <q-radio v-model="radio1" val="opt2" checked-icon="visibility" label="Display all as one report" />
                <br></br>
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
  }
</style>
<script>

  export default {
    data () {
      return {
        radio1: 'two',
        radio2: 'one',
        radio3: 'three',
        group: 'upload',
        list: ''
      }
    }
  }

</script>

