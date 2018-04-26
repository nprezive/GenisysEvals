<template>
  <div class="row clearfix p-1">
    <div class="col-md-12 col-lg-12 clearfix">
      <!-- <q-card>
        <q-card-main class="card-block pt-2"> -->
          <p>Instructor can share their course and instructor evaluations with students.</p>
          <p>Below are evaluations that instructors have chosen to share.</p>
          <input type="text" v-model="search" placeholder="Filter Instructor"/>
          <!-- filteredSemesters() -->
          <div v-for="sem in courses">
            <br/>
            <div class="col-md-12 col-lg-12 clearfix">
              <q-collapsible :label="sem.semester" opened>
                <!-- <q-card> -->
                  <!-- <q-card-main class="card-block pt-2"> -->
                    <table style="width: 100%">
                      <tr v-for="c in filteredClasses(sem.classes)">
                        <td><a :href="c.evalURL" target="_blank">{{c.className}}</a> ({{c.instructorName}})</td>
                      </tr>
                    </table>
                  <!-- </q-card-main> -->
                <!-- </q-card> -->
              </q-collapsible>
              <hr style="width:98%;"/>
            </div>
          </div>
        <!-- </q-card-main>
      </q-card> -->
    </div>
  </div>
</template>

<script>
export default {
  data: function () {
    return {
      search: '',
      searchInstructor: '',
      courses: [
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
              instructorName: 'Smith, Kevin',
              evalURL: 'www.weber.edu',
              isCourseEvaluated: true,
              isPublic: true,
              isSharedDeans: true
            },
            {
              id: 1233,
              crn: '22145',
              className: 'CS1410',
              taken: '19',
              total: '25',
              instructorName: 'Hart, Michelle',
              evalURL: 'www.google.com',
              isCourseEvaluated: false,
              isPublic: true,
              isSharedDeans: true
            },
            {
              id: 12334,
              crn: '22323',
              className: 'CS3100',
              taken: '18',
              total: '22',
              instructorName: 'Vase, Nancy',
              evalURL: 'www.utah.edu',
              isCourseEvaluated: true,
              isPublic: true,
              isSharedDeans: true
            },
            {
              id: 12334,
              crn: '22323',
              className: 'CS4110',
              taken: '9',
              total: '22',
              instructorName: 'Adams, Clark',
              evalURL: 'www.weber.edu',
              isCourseEvaluated: true,
              isPublic: true,
              isSharedDeans: true
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
              instructorName: 'Adams, Clark',
              evalURL: 'www.weber.edu',
              isCourseEvaluated: true,
              isActive: true,
              isPublic: true,
              isSharedDeans: true
            },
            {
              id: 1233,
              crn: '22145',
              className: 'CS1410',
              taken: '19',
              total: '25',
              instructorName: 'Adams, Clark',
              evalURL: 'www.weber.edu',
              isCourseEvaluated: false,
              isPublic: true,
              isSharedDeans: true
            },
            {
              id: 12334,
              crn: '22323',
              className: 'CS3100',
              taken: '18',
              total: '22',
              instructorName: 'Adams, Clark',
              evalURL: 'www.weber.edu',
              isCourseEvaluated: true,
              isPublic: true,
              isSharedDeans: true
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
              instructorName: 'Adams, Clark',
              evalURL: 'www.weber.edu',
              isCourseEvaluated: true,
              isActive: true,
              isPublic: true,
              isSharedDeans: true
            },
            {
              id: 1233,
              crn: '22145',
              className: 'CS1410',
              taken: '19',
              total: '25',
              instructorName: 'Adams, Clark',
              evalURL: 'www.weber.edu',
              isCourseEvaluated: false,
              isPublic: true,
              isSharedDeans: true
            },
            {
              id: 12334,
              crn: '22323',
              className: 'CS3100',
              taken: '18',
              total: '22',
              instructorName: 'Adams, Clark',
              evalURL: 'www.weber.edu',
              isCourseEvaluated: true,
              isPublic: true,
              isSharedDeans: true
            },
            {
              id: 123343,
              crn: '223232',
              className: 'CS3110',
              taken: '13',
              total: '22',
              instructorName: 'Adams, Clark',
              evalURL: 'www.weber.edu',
              isCourseEvaluated: true,
              isPublic: true,
              isSharedDeans: true
            }
          ]
        }
      ]
    }
  },
  computed: {

  },
  methods: {
    filteredSemesters: function () {
      var self = this
      return this.courses.filter(function (sem) {
        return sem.semester.toLowerCase().indexOf(self.search.toLowerCase()) >= 0
      })
    },

    filteredClasses: function (classes) {
      var self = this
      return classes.filter(function (classes) {
        var values = classes.instructorName.toLowerCase().indexOf(self.search.toLowerCase()) >= 0
        values += classes.className.toLowerCase().indexOf(self.search.toLowerCase()) >= 0
        return values
      })
    }
  }
}
</script>
