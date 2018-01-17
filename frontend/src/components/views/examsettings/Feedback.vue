<template>
  <div id="feedback">
    <div class="row">
      <div class="col-md-6">
        <div class="row">
          <div class="col-md-10 col-sm-12">
            <div class="q-if-label font-size-12">Receive Score</div>
            <q-list link dense no-border>
              <q-item tag="label" class="pl-0">
                <q-item-side>
                  <q-checkbox color="primary" v-model="settings.allowViewScore"></q-checkbox>
                </q-item-side>
                <q-item-main>
                  <q-item-tile label>Allow student's to view their score.</q-item-tile>
                </q-item-main>
              </q-item>
            </q-list>
          </div>
        </div>
        <div class="row">
          <div class="col-md-10 col-sm-12">
            <div class="q-if-label font-size-12">Show Question Feedback To Student Upon Answering Each Question</div>
            <q-list link dense no-border>
              <q-item tag="label" class="pl-0">
                <q-item-side>
                  <q-checkbox color="secondary" v-model="settings.duringReview"></q-checkbox>
                </q-item-side>
                <q-item-main>
                  <q-item-tile label>During exam review</q-item-tile>
                </q-item-main>
              </q-item>
              <q-item tag="label" class="pl-0">
                <q-item-side>
                  <q-checkbox color="negative" v-model="settings.duringExam"></q-checkbox>
                </q-item-side>
                <q-item-main>
                  <q-item-tile label>During the exam</q-item-tile>
                </q-item-main>
              </q-item>
            </q-list>
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <div class="row">
          <div class="col-12">
            <q-card>
              <q-card-title class="bg-primary">
                Placeholder Card
              </q-card-title>
              <q-card-main>
                To Be Determined
              </q-card-main>
            </q-card>
          </div>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-md-12">
        <q-collapsible icon="fa-globe" label="Score Feedback"
                       sublabel="Show one of the following messages upon completion of the exam, based on the students score">
          <div class="row">
            <div class="col-12">
              <table class="q-table striped-even width-100">
                <thead>
                <tr>
                  <th class="pb-0">If the points scored are at least</th>
                  <th class="pb-0">Feedback message to student</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="(item, index) in settings.scoreFeedback">
                  <td>
                    <q-field>
                      <q-input v-model="item.score" type="number" :min="0"></q-input>
                    </q-field>
                  </td>
                  <td>
                    <q-field>
                      <q-input
                        v-model="item.message"
                        type="textarea"
                        :max-height="100"
                        :min-rows="1"></q-input>
                    </q-field>
                  </td>
                </tr>
                </tbody>
              </table>
            </div>
          </div>
          <div class="row">
            <div class="col-12">
              <q-input v-model="settings.scoreLessThanAboveFeedback"
                       float-label="If the score is less than all the above, then show"></q-input>
            </div>
          </div>
        </q-collapsible>
      </div>
    </div>
  </div>
</template>
<script>

  export default {
    name: 'Feedback',
    props: ['settings'],
    components: {
    },
    data () {
      return {}
    },
    methods: {
    }
  }
</script>
<style lang="stylus">

  #feedback .width-100
    width: 100%

</style>
