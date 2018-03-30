<template>
  <div class="row clearfix p-1">
              <!-- <div class="col-md-12 col-lg-4 clearfix">
                <q-card>
                  <q-card-main class="card-block pt-2">
                      <q-btn color="primary">Go to Course Evals</q-btn>
                  </q-card-main>
                </q-card>
              </div> -->
    <div class="col-md-12 col-lg-12 clearfix">
      <q-card>
        <q-card-main class="card-block pt-2">
          <p>Instructor can share their course and instructor evaluations with students.</p>
          <p>Below are evaluations that instructors have chosen to share.</p>
          <q-btn push color="primary">
            Filter By Instructor
            <q-popover
              :anchor="anchor"
              :self="self">
              <q-list link style="min-width: 100px">
                <q-item
                  v-for="n in semester"
                  :key="`b-${n}`"
                  v-close-overlay
                  @click.native="notify">
                  <q-item-main label="Instuctor Name" />
                </q-item>
              </q-list>
            </q-popover>
          </q-btn>
        </q-card-main>
      </q-card>
    </div>

    <div class="col-md-12 col-lg-12 clearfix">
      <q-list v-for="sem in semester">
        <q-collapsible :label="sem.semester">
          <q-card>
            <q-card-main class="card-block pt-2">
              <table style="width: 100%">
                <tr v-for="c in sem.classes">
                  <td><a :href="c.evalURL" target="_blank">{{c.className}}{{c.crn}}</a> ({{c.instructorLast}}, {{c.instructorFirst}})</td>
                </tr>
              </table>
            </q-card-main>
          </q-card>
        </q-collapsible>
      </q-list>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      sSemesterIndex: 0
    }
  },
  computed: {
    semester () {
      // APICall to get student's proctors
      let apiCall = [
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
              instructorFirst: 'FirstName',
              instructorLast: 'LastName',
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
              instructorFirst: 'FirstName',
              instructorLast: 'LastName',
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
              instructorFirst: 'FirstName',
              instructorLast: 'LastName',
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
              instructorFirst: 'FirstName',
              instructorLast: 'LastName',
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
              instructorFirst: 'FirstName',
              instructorLast: 'LastName',
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
              instructorFirst: 'FirstName',
              instructorLast: 'LastName',
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
              instructorFirst: 'FirstName',
              instructorLast: 'LastName',
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
              instructorFirst: 'FirstName',
              instructorLast: 'LastName',
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
              instructorFirst: 'FirstName',
              instructorLast: 'LastName',
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
              instructorFirst: 'FirstName',
              instructorLast: 'LastName',
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
              instructorFirst: 'FirstName',
              instructorLast: 'LastName',
              evalURL: 'www.weber.edu',
              isCourseEvaluated: true,
              isPublic: true,
              isSharedDeans: true
            }
          ]
        }
      ]
      return apiCall
    }
  },
  methods: {
    openModal (semesterID) {
      for (let i = 0; i < this.semester.length; i++) {
        if (this.semester[i].id === semesterID) {
          this.sSemesterIndex = semesterID
          this.$refs.basicModal.open()
          break
        }// end if
      }// end for
    }
  }
}
</script>
