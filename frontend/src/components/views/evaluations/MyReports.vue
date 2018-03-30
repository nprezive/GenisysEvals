<template>
  <div>
    <q-toolbar inverted color="dark" class="bg-light">
      <q-toolbar-title>
        My Reports - Click on a section to generate an evaluations report.
      </q-toolbar-title>
      <q-btn row inline color="primary">Promotion and Tenure</q-btn>
    </q-toolbar>
    <div class="row clearfix p-1">
      <div class="col-md-12 col-lg-12 clearfix">
        <q-list  v-for="sem in courses">
          <q-collapsible :label="sem.semester">
            <q-card>
              <q-card-main class="card-block pt-2">
                <table style="width: 80%; display:inline;">
                  <tr>
                    <th style="width: 25%">Course</th>
                    <th style="width: 25%; text-align:center">Should This Class be Evaluated</th>
                    <th style="width: 25%; text-align:center">Share with Dean/Chair</th>
                    <th style="width: 25%; text-align:center">Public Access</th>
                  </tr>
                  <tr v-for="c in sem.courses">
                    <td>{{c.title}}<br><i>25/30 Have Responded</i></td>
                    <td align="center"><input type="checkbox"></td>
                    <td align="center"><input type="checkbox"></td>
                    <td align="center"><input type="checkbox"></td>
                  </tr>
                </table>
                <div style="float:right; width:20%;">
                  <p>By selecting the button below, you are agreeing to send the settings configured for this semester to the Dean or Chair for review.</p>
                  <q-btn inline color="primary">Lock</q-btn>
                </div>
              </q-card-main>
            </q-card>
          </q-collapsible>
        </q-list>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name:'mydefaults',
  computed: {
    courses() {
      let apicall = [
        {
          semester: 'Spring 2017',
          courses:
            [
              {
                title: 'CS 2420',
                description: "blah blah blah"
              },
              {
                title: 'CS 3000',
                description: "blah blah blah"
              },
              {
                title: 'CS 3100',
                description: "blah blah blah"
              },
              {
                title: 'CS 3200',
                description: "blah blah blah"
              },
              {
                title: 'CS 4110',
                description: "blah blah blah"
              }
            ]
        },
        {
          semester: 'Summer 2017',
          courses:
            [
              {
                title: 'CS 2420',
                description: "blah blah blah"
              },
              {
                title: 'CS 3000',
                description: "blah blah blah"
              },
              {
                title: 'CS 3100',
                description: "blah blah blah"
              },
              {
                title: 'CS 3200',
                description: "blah blah blah"
              },
              {
                title: 'CS 4110',
                description: "blah blah blah"
              }
            ]
        },
        {
          semester: 'Fall 2017',
          courses:
            [
              {
                title: 'CS 2420',
                description: "blah blah blah"
              },
              {
                title: 'CS 3000',
                description: "blah blah blah"
              },
              {
                title: 'CS 3100',
                description: "blah blah blah"
              },
              {
                title: 'CS 3200',
                description: "blah blah blah"
              },
              {
                title: 'CS 4110',
                description: "blah blah blah"
              }
            ]
        },
        {
          semester: 'Spring 2018',
          courses:
            [
              {
                title: 'CS 2420',
                description: "blah blah blah"
              },
              {
                title: 'CS 3000',
                description: "blah blah blah"
              },
              {
                title: 'CS 3100',
                description: "blah blah blah"
              },
              {
                title: 'CS 3200',
                description: "blah blah blah"
              },
              {
                title: 'CS 4110',
                description: "blah blah blah"
              }
            ]
        }
      ]
      return apicall
    }
  }
}
</script>
