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
        <q-card v-for="sem in courses">
          <q-card-title class="bg-primary">
            <b>{{sem.semester}}</b>
          </q-card-title>
          <q-card-main class="card-block pt-2">
            <table style="width: 100%">
              <tr>
                <th style="width: 20%">Course</th>
                <th style="width: 40%; text-align:center">Share with Wildcat Account holders</th>
                <th style="width: 40%; text-align:center">Share with Chairs and Deans</th>
              </tr>
              <tr v-for="c in sem.courses">
                <td>{{c.title}}</td>
                <td align="center"><input type="checkbox"></td>
                <td align="center"><input type="checkbox"></td>
              </tr>
            </table>
          </q-card-main>
        </q-card>
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
    // columns() {
    //   let apicall = [
    //     {
    //       name: "course",

    //     }
    //   ]
    // }
  }
}
</script>
