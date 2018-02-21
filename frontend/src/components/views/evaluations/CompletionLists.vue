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
                           <q-item-tile sublabel lines="2">
                              {{c.taken}}/{{c.total}} Students Have Responded
                          </q-item-tile>
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
                          <q-item-tile label><q-btn @click="$refs.basicModal.open()">{{cSemester.semester}} ({{cSemester.classes.length}} Courses)</q-btn></q-item-tile>
                        </q-item-main>
                       </q-item>
                       <!--
                       <q-item>
                        <q-item-main>
                          <q-item-tile label><q-btn @click="$refs.basicModal.open()">Fall 2017 (3 Courses)</q-btn></q-item-tile>
                        </q-item-main>
                      </q-item>
                      <q-item>
                        <q-item-main>
                          <q-item-tile label @click="$refs.basicModal2.open()"><q-btn>Summer 2017 (2 Courses)</q-btn></q-item-tile>
                        </q-item-main>
                      </q-item>
                       -->
                    </q-list>
                  </q-card-main>
                </q-card>
              </div>

              <q-modal ref="basicModal" :content-css="{padding: '50px'}">
                <h4>Fall 2017</h4>
                <q-list no-border>
                          <q-item>
                            <q-item-main>
                              <q-item-tile label>CS1400 ONL Fall 17</q-item-tile>
                               <q-item-tile sublabel lines="2">
                                  30/33 Students Have Responded
                              </q-item-tile>
                            </q-item-main>
                          </q-item>
                          <q-item>
                            <q-item-main>
                              <q-item-tile label>CS1410 WSD Fall 17 (this course is not being evaluated)</q-item-tile>
                              <q-item-tile sublabel lines="2">
                                  No Students Have Responded
                              </q-item-tile>
                            </q-item-main>
                          </q-item>
                        </q-list>
                <q-btn color="primary" @click="$refs.basicModal.close()">Close</q-btn>
              </q-modal>

              <q-modal ref="basicModal2" :content-css="{padding: '50px'}">
                <h4>Summer 2017</h4>
                <q-list no-border>
                          <q-item>
                            <q-item-main>
                              <q-item-tile label>CS1400 ONL Summer 17</q-item-tile>
                               <q-item-tile sublabel lines="2">
                                  30/33 Students Have Responded
                              </q-item-tile>
                            </q-item-main>
                          </q-item>
                          <q-item>
                            <q-item-main>
                              <q-item-tile label>CS1410 WSD Summer 17 (this course is not being evaluated)</q-item-tile>
                              <q-item-tile sublabel lines="2">
                                  No Students Have Responded
                              </q-item-tile>
                            </q-item-main>
                          </q-item>
                        </q-list>
                <q-btn color="primary" @click="$refs.basicModal2.close()">Close</q-btn>
              </q-modal>
            </div>
</template>

<script>
export default {
  computed: {
    semester() {
      // APICall to get student's proctors
      let apiCall = [
        {
          id: 1111,
          semester: 'Spring 2018',
          isActive: true,
          classes : [
            {
              id: 1234,
              crn: '22325',
              className: 'CS1400',
              taken: '22',
              total: '35',
              isCourseEvaluated: true
            },
            {
              id: 1233,
              crn: '22145',
              className: 'CS1410',
              taken: '19',
              total: '25',
              isCourseEvaluated: false
            },
            {
              id: 12334,
              crn: '22323',
              className: 'CS3100',
              taken: '18',
              total: '22',
              isCourseEvaluated: true
            }
          ]
        },
                {
          id: 1111,
          semester: 'Fall 2017',
          isActive: false,
          classes : [
            {
              id: 1234,
              crn: '22325',
              className: 'CS1400',
              taken: '22',
              total: '35',
              isCourseEvaluated: true,
              isActive: true
            },
            {
              id: 1233,
              crn: '22145',
              className: 'CS1410',
              taken: '19',
              total: '25',
              isCourseEvaluated: false
            },
            {
              id: 12334,
              crn: '22323',
              className: 'CS3100',
              taken: '18',
              total: '22',
              isCourseEvaluated: true
            }
          ]
        },
        {
          id: 1111,
          semester: 'Spring 2017',
          isActive: false,
          classes : [
            {
              id: 1234,
              crn: '22325',
              className: 'CS1400',
              taken: '22',
              total: '35',
              isCourseEvaluated: true,
              isActive: true
            },
            {
              id: 1233,
              crn: '22145',
              className: 'CS1410',
              taken: '19',
              total: '25',
              isCourseEvaluated: false
            },
            {
              id: 12334,
              crn: '22323',
              className: 'CS3100',
              taken: '18',
              total: '22',
              isCourseEvaluated: true
            }
          ]
        }
      ]
      return apiCall
    }
  }
}
</script>
