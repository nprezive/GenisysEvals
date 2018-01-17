<template>
  <div class="sendfinalgrades">
    <h2>Submit Finals Grade for {{students.course}}</h2><br/>
    <h1>This tool will send final grades to Banner.</h1>

    <h1>Step 1. Select which Canvas column from your gradebook you would use - Current or Final.</h1>
    <ul>
      <li>Current Grade shows a total for only those assignments that you have graded so far.</li>
      <li>Final Grade assumes all ungraded assignments are given 0s.</li>
      <li>You must enable a <a>grading scheme</a> to see letter grades in these columns</li>
    </ul>
    <h1>Step 2. You can manually select which grade to send to Banner in the Banner Final Grade column.</h1>
    <ul>
      <li>Note: An I, E, or UW grade will prompt for additional information such as last date of attendance.</li>
    </ul>
    <h1>
      Step 3. Check the Verify box if everything looks good and then click Submit Final Grade at the bottom of the screen to send to Banner.</h1>
    <ul>
      <li>Only grades where you have checked the verify box will be sent.</li>
      <li>
        Grades are rolled to the academic transcript nightly. After a grade has rolled in Banner, you will not be able to make changes here. You will need to contact the <a>Records Office</a>.
      </li>
    </ul>
    <table class="table table-hover table-striped m-2" id="sendFinalGrades">
      <thead>
      <tr>
        <th>Student</th>
        <th>
          <div class="row text-center">
            <span class="col-12">Canvas</span>
          </div>
          <div class="row">
            <ui-button size="sm" @click="currentGrade" class="col-6">Current Grade</ui-button>
            <ui-button size="sm" @click="finalGrade" class="col-6">Final Grade</ui-button>
          </div>
        </th>
        <th>
          <div class="row text-center">
            <span class="col-12">Banner</span>
          </div>
          <div class="row">
            <span class="col-6">Final Grade <a>?</a></span>
            <span class="col-6">Last Attendance <a>?</a></span>
          </div>
        </th>
        <th>
          <div class="row">
            <ui-button size="sm" @click="verifyAll" class="col-12">Verify All</ui-button>
          </div>
        </th>
      </tr>
      </thead>
      <tbody class="cursor-pointer">
      <tr v-for="(student, index) in students.students" :key="index" :class="'tr_'+index%2">
        <td>
          <div class="row">
            {{index}}
            {{student.name}}
          </div>
          <div class="row">
            <span class="sNum">{{student.wnum}}</span>
          </div>
        </td>
        <td>
          <div class="row text-center">
            <span class="col-6">{{student.currentgrade}} ({{student.currentgrade}}%)</span>
            <span class="col-6">{{student.finalgrade}} ({{student.finalgrade}}%)</span>
          </div>
        </td>
        <td>
          <div class="row">
            <ui-select
              placeholder="Select Grade"
              :options="acceptableGrades"
              :keys="{label: 'value', value: 'value'}"
              v-model="finalStudents[index].grade"
              class="col-4"
            ></ui-select>
            <ui-datepicker :id="'date' + index" style="display:none;" class="col-8" placeholder="Last Day of Attendance" v-model="finalStudents[index].date"></ui-datepicker>
          </div>
        </td>
        <td class="float-right">
          <ui-checkbox v-model="finalStudents[index].verify"></ui-checkbox>
        </td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
  export default {
    name: 'Login',
    data () {
      return {
        acceptableGrades: [
          // Grades banner will accept. The incomplete attribute should only be true for one and the fail grade attribute should only be true for one.
          // The lastDate attribute should be set to true for grades that require last date of attendance.
          // The acceptableIncomplete attribute should be true for all grades that can be used with an Incomplete.
          {value: 'A', lastDate: false, incomplete: false, acceptableIncomplete: true, failGrade: false},
          {value: 'A-', lastDate: false, incomplete: false, acceptableIncomplete: true, failGrade: false},
          {value: 'B+', lastDate: false, incomplete: false, acceptableIncomplete: true, failGrade: false},
          {value: 'B', lastDate: false, incomplete: false, acceptableIncomplete: true, failGrade: false},
          {value: 'B-', lastDate: false, incomplete: false, acceptableIncomplete: true, failGrade: false},
          {value: 'C+', lastDate: false, incomplete: false, acceptableIncomplete: true, failGrade: false},
          {value: 'C', lastDate: false, incomplete: false, acceptableIncomplete: true, failGrade: false},
          {value: 'C-', lastDate: false, incomplete: false, acceptableIncomplete: true, failGrade: false},
          {value: 'D+', lastDate: false, incomplete: false, acceptableIncomplete: true, failGrade: false},
          {value: 'D', lastDate: false, incomplete: false, acceptableIncomplete: true, failGrade: false},
          {value: 'D-', lastDate: false, incomplete: false, acceptableIncomplete: true, failGrade: false},
          {value: 'E', lastDate: true, incomplete: false, acceptableIncomplete: true, failGrade: true},
          {value: 'UW', lastDate: true, incomplete: false, acceptableIncomplete: false, failGrade: false},
          {value: 'I', lastDate: false, incomplete: true, acceptableIncomplete: false, failGrade: false}
        ],
        finalStudents: [],
        FinalGrade: null,
        AllVerify: null
      }
    },
    mounted () {
      for (let i = 0; i < this.students.students.length; i++) {
        this.finalStudents.push({grade: '', date: null, verify: false})
      }
    },
    computed: {
      students () {
        let APICall = {
          'students': [
            {
              'name': 'Trevor',
              'wnum': '0000000',
              'currentgrade': 90,
              'currentlettergrade': 'A-',
              'finalgrade': 100,
              'finallettergrade': 'A',
              'rolled': false,
              'submitted': true
            },
            {
              'name': 'Caden',
              'wnum': '0000001',
              'currentgrade': 50,
              'currentlettergrade': 'E',
              'finalgrade': 60,
              'finallettergrade': 'D-',
              'rolled': false,
              'submitted': false
            },
            {
              'name': 'Collin',
              'wnum': '0000002',
              'currentgrade': 70,
              'currentlettergrade': 'C-',
              'finalgrade': 85,
              'finallettergrade': 'B',
              'rolled': true,
              'submitted': true
            }
          ],
          'course': 'CS3550 WSU Spr 17 35512'
        }
        return APICall
      }
    },
    watch: {
      finalStudents: {
        handler: function () {
          for (let i = 0; i < this.finalStudents.length; i++) {
            if (document.getElementById('date' + i) !== null) {
              if (this.finalStudents[i].grade.value === 'I' || this.finalStudents[i].grade.value === 'UW' || this.finalStudents[i].grade.value === 'E') {
                document.getElementById('date' + i).style.display = 'flex'
              } else {
                document.getElementById('date' + i).style.display = 'none'
              }
            }
          }
        },
        deep: true
      }
    },
    methods: {
      currentGrade () {
        for (let i = 0; i < this.finalStudents.length; i++) {
          this.finalStudents[i].grade = {value: this.students.students[i].currentlettergrade}
        }
        this.updateAttendance()
      },
      finalGrade () {
        for (let i = 0; i < this.finalStudents.length; i++) {
          this.finalStudents[i].grade = {value: this.students.students[i].finallettergrade}
        }
        this.updateAttendance()
      },
      verifyAll () {
        for (let i = 0; i < this.finalStudents.length; i++) {
          this.finalStudents[i].verify = true
        }
      },
      inputChange () {
      },
      dateChange () {
      }
    }
  }
</script>

<style scoped>
  body {
    font-size: 10px;
    margin: 10px;
  }

  .centered {
    text-align: center;
  }

  .sNum {
    font-size: 8px;
  }

  #sendFinalGrades {
    width: 1000px;
    margin: 50px;
  }

  h1 {
    font-size: 14px;
  }

  .firstRow {
    background-color: rgb(187, 199, 210);
  }

  .tr_1 {
    background-color: #f0f2f5;
  }

  .submittedtrue {
    background: #ccffcc;
  }
</style>
