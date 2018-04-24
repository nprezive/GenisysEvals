<template>
  <div class="animated fadeIn proctoring">
    <div class="row">
      <div class="col-12">
        <q-tabs align="justify" inverted
                style="background-color: white">

          <q-tab default label="My Evals" slot="title" name="tab-1"></q-tab>
          <q-tab-pane name="tab-1" class="p-0">
            <MyReports></MyReports>
          </q-tab-pane>

          <!--
          <q-tab label="My Completion Lists" slot="title"
                 name="tab-2"></q-tab>
          <q-tab-pane name="tab-2" class="p-0">
            <q-toolbar inverted color="dark" class="bg-light">
              <q-toolbar-title>
              </q-toolbar-title>
            </q-toolbar>
            <CompletionLists></CompletionLists>
          </q-tab-pane>
          -->

          <q-tab label="Public Evals" slot="title"
                 name="tab-2"></q-tab>
          <q-tab-pane name="tab-2" class="p-0">
            <q-toolbar inverted color="dark" class="bg-light">
              <q-toolbar-title>
                Public Evaluations
              </q-toolbar-title>
              <q-fab color="primary" active-icon="fa-times" icon="fa-cogs" direction="left">
                <q-fab-action color="negative" @click="toast('alarm')" icon="fa-question">
                  <q-tooltip anchor="center left" self="center right" :offset="[20, 0]">Need Help?</q-tooltip>
                </q-fab-action>
                <q-fab-action color="primary" @click="toast('alarm')" icon="fa-user">
                  <q-tooltip anchor="center left" self="center right" :offset="[20, 0]">Create A Evaluation</q-tooltip>
                </q-fab-action>
              </q-fab>
            </q-toolbar>
            <PublicEvals></PublicEvals>
          </q-tab-pane>

          <q-tab label="Reports" slot="title"
                 name="tab-3"></q-tab>
          <q-tab-pane name="tab-3" class="p-0">
            <q-toolbar inverted color="dark" class="bg-light">
              <q-toolbar-title>
                Reports
              </q-toolbar-title>
              <q-fab color="primary" active-icon="fa-times" icon="fa-cogs" direction="left">
                <q-fab-action color="negative" @click="toast('alarm')" icon="fa-question">
                  <q-tooltip anchor="center left" self="center right" :offset="[20, 0]">Need Help?</q-tooltip>
                </q-fab-action>
                <q-fab-action color="primary" @click="toast('alarm')" icon="fa-user">
                  <q-tooltip anchor="center left" self="center right" :offset="[20, 0]">Create A Evaluation</q-tooltip>
                </q-fab-action>
              </q-fab>
            </q-toolbar>
            <MyRankings></MyRankings>
          </q-tab-pane>



          <q-tab label="Administration" slot="title"
                 name="tab-4"></q-tab>
          <q-tab-pane name="tab-4" class="p-0">
            <!-- <q-toolbar inverted color="dark" class="bg-light">
              <q-toolbar-title>
                User Roles
              </q-toolbar-title>
              <q-fab color="primary" active-icon="fa-times" icon="fa-cogs" direction="left">
                <q-fab-action color="negative" @click="toast('alarm')" icon="fa-question">
                  <q-tooltip anchor="center left" self="center right" :offset="[20, 0]">Need Help?</q-tooltip>
                </q-fab-action>
                <q-fab-action color="primary" @click="toast('alarm')" icon="fa-user">
                  <q-tooltip anchor="center left" self="center right" :offset="[20, 0]">Create A Evaluation</q-tooltip>
                </q-fab-action>
              </q-fab>
            </q-toolbar> -->
            <q-tabs align="justify" inverted
                style="background-color: white">
              <q-tab default label="User Roles" slot="title" name="tab-1"></q-tab>
              <q-tab-pane name="tab-1" class="p-0">
                <UserRoles></UserRoles>
              </q-tab-pane>

              <q-tab default label="Semester Review" slot="title" name="tab-2"></q-tab>
              <q-tab-pane name="tab-2" class="p-0">
                <SemesterReview></SemesterReview>
              </q-tab-pane>
            </q-tabs>

          </q-tab-pane>
        </q-tabs>
      </div>
    </div>
  </div>
</template>
<script>
  import UserRoles from './evaluations/UserRoles'
  import MyRankings from './evaluations/MyRankings'
  import MyReports from './evaluations/MyReports'
  import PublicEvals from './evaluations/PublicEvals'
  import CompletionLists from './evaluations/CompletionLists'
  import SemesterReview from './evaluations/SemesterReview'

  export default {
    name: 'evaluations',
    components: {
      UserRoles,
      MyRankings,
      MyReports,
      PublicEvals,
      CompletionLists,
      SemesterReview
    }
  }
</script>
<style>
  *,
  *::before,
  *::after {
    box-sizing: border-box;
  }

  html {
    font-size: 100%;
  }
</style>
