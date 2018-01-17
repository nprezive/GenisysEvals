<template>
  <div class="animated fadeIn row endExam h-100 bg-light" v-if="summary">
    <div class="mt-auto col-12 mb-auto">
      <div class="row">
        <div class="col-2 gt-sm"></div>
        <div class="col-md-8 col-sm-12">
          <q-card style="background-color: white;">
            <q-card-title class="bg-primary">Score Summary</q-card-title>
            <q-card-separator></q-card-separator>
            <q-card-main v-if="summary.canviewscores">
              <div>Of {{ summary.total }} questions on your exam, {{ summary.gradable
                }} could be automatically scored.<br><br>
                You received {{ summary.score }} out of {{ summary.totalscore
                }} points possible. (your instructor may have assigned more than one point per
                question). In percentage terms, you scored <b>{{ Math.round(((summary.score / summary.totalscore) * 100) * 100) / 100 }}%</b><br><br>
                There <span v-if="summary.total - summary.gradable > 1">are</span><span v-else>is</span>
                {{ summary.total - summary.gradable }}
                <span v-if="summary.total - summary.gradable > 1">questions</span><span v-else>question</span>
                that are not automatically scoreable. Your instructor may score these questions
                later. There is a total of {{ summary.unscoreablepoints
                }} points possible for these questions. (Questions that cannot be
                automatically scored include questions where the instructor has not specified a correct responses as well
                as all essay questions.)
              </div>
            </q-card-main>
            <q-card-main v-else>
              <div>
                Viewing scores of an attempt is not allowed for this exam.
              </div>
            </q-card-main>
          </q-card>
        </div>
        <div class="col-2 gt-sm"></div>
      </div>
      <div class="row">
        <div class="col-2 gt-sm"></div>
        <div class="col-md-8 col-sm-12">
          <q-card style="background-color: white;">
            <q-card-title class="bg-secondary text-white">Exam Review</q-card-title>
            <q-card-separator></q-card-separator>
            <q-card-main v-if="summary.reviewable">
              <div>Online reviewing of exam results is allowed for this exam, with the following limitations:<br>
                <div class="ml-1" v-if="summary.anyComputer">You can review at any computer.</div>
                <div class="ml-1" v-else>You will be allowed to review only at the sites where the exam was available.
                </div>
                <div class="ml-1" v-if="summary.onlyMissed">You will only be able to review missed questions.</div>
                <div class="ml-1" v-else>You will be able to review all of the questions.</div>
                <div class="ml-1" v-if="summary.when === 'any-time'">You can review anytime after you finish the exam.
                </div>
                <div class="ml-1" v-else>You can review anytime after the exam's close date.</div>
                <div v-if="summary.cantake"><b>You are currently allowed to review this exam.</b></div>
                <div v-else><b>You are not currently allowed to review this exam.</b></div>
              </div>
            </q-card-main>
            <q-card-main v-else>
              <div>
                Reviewing of exam results is not allowed for this exam.
              </div>
            </q-card-main>
            <q-card-separator></q-card-separator>
            <div>
              <div class="row m-2 pb-2">
                <div class="col-lg-6 col-md-12 m-auto row">
                  <div class="col-sm-12 col-md-5">
                    <q-btn color="primary" @click="home" class="full-width">
                      Home
                    </q-btn>
                  </div>
                  <div class="col-md-2 col-sm-12"></div>
                  <div class="col-sm-12 col-md-5">
                    <q-btn color="secondary" class="full-width" v-if="summary.cantake" @click="$router.push({path: '/review/' + resultID})">
                      Review Attempt
                    </q-btn>
                  </div>
                </div>
              </div>
            </div>
          </q-card>
        </div>
        <div class="col-2 gt-sm"></div>
      </div>
    </div>
  </div>
</template>
<script>
  import {
    Loading
  } from 'quasar'

  export default {
    name: 'EndExam',
    props: ['loadForbidden', 'resultID'],
    data () {
      return {
        summary: false
      }
    },
    mounted () {
      Loading.show({
        message: 'Retrieving Results for Attempt'
      })
      this.$http({
        method: 'get',
        url: '/api/result/' + this.resultID + '/summary/'
      }).then(response => {
        if (response.status === 250) {
          this.$router.error = response.data
          this.$router.push({path: '/error'})
        }
        if (response.status === 250) {
          Loading.hide()
          this.loadForbidden(response.data)
        } else {
          this.summary = response.data
          Loading.hide()
        }
      }).catch(error => {
        console.log(error)
      })
    },
    methods: {
      home: function () {
        this.$router.push({path: '/'})
      }
    }
  }
</script>
<style>
  .resultCard {
    max-width: 750px;
  }
</style>
