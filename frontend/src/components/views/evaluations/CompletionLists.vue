<template>
  <div class="row clearfix p-1">
    <div class="col-md-12 col-lg-6 clearfix">
      <q-card>
        <q-card-title class="bg-primary">
          <b>Current Semester</b>
        </q-card-title>
        <q-card-main class="card-block pt-2">
          <q-list no-border>
            <template v-for="cSemester in semester" v-if="cSemester.isActive">
              <q-item v-for="c in cSemester.classes">
                <q-item-main>
                  <q-item-tile label v-if="c.isCourseEvaluated">{{ c.className }} {{cSemester.semester}}</q-item-tile>
                  <q-item-tile label v-else>{{ c.className }} {{cSemester.semester}} (this course is not being evaluated)</q-item-tile>
                   <q-item-tile sublabel lines="2" v-if="c.taken > 10 && c.isCourseEvaluated">{{c.taken}}/{{c.total}} Students Have Responded</q-item-tile>
                   <q-item-tile sublabel lines="2" v-else-if="c.taken < 10 && c.isCourseEvaluated">Less than 10 Students Have Responded</q-item-tile>
                </q-item-main>
              </q-item>
            </template>
          </q-list>
        </q-card-main>

      </q-card>
    </div>
    <div class="col-md-12 col-lg-6 clearfix">
      <q-card>
        <q-card-title class="bg-primary">
          <b>Previous Semesters</b>
        </q-card-title>
        <q-card-main class="card-block pt-2">
           <q-list no-border>
             <q-item v-for="cSemester in semester" v-if="!cSemester.isActive">
               <q-item-main>
                <q-item-tile label><q-btn @click="openModal(cSemester.id)">{{cSemester.semester}} ({{cSemester.classes.length}} Courses)</q-btn></q-item-tile>
              </q-item-main>
             </q-item>
          </q-list>
        </q-card-main>
      </q-card>
    </div>
    <q-modal ref="basicModal" :content-css="{padding: '50px'}">
      <template v-for="cSemester in semester" v-if="cSemester.id == sSemesterIndex">
      <h4>{{cSemester.semester}}</h4>
      <q-list no-border>
        <q-item v-for="c in cSemester.classes">
          <q-item-main>
            <q-item-tile label v-if="c.isCourseEvaluated">{{ c.className }} {{cSemester.semester}}</q-item-tile>
            <q-item-tile label v-else>{{ c.className }} {{cSemester.semester}} (this course is not being evaluated)</q-item-tile>
             <q-item-tile sublabel lines="2" v-if="c.taken > 10  && c.isCourseEvaluated">{{c.taken}}/{{c.total}} Students Have Responded</q-item-tile>
             <q-item-tile sublabel lines="2" v-else-if="c.taken < 10  && c.isCourseEvaluated">Less than 10 Students Have Responded</q-item-tile>
          </q-item-main>
        </q-item>
      </q-list>
      </template>
      <q-btn color="primary" @click="$refs.basicModal.close()">Close</q-btn>
    </q-modal>
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
