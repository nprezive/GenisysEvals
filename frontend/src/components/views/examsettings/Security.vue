<template>
  <div id="security">
    <div class="row">
      <div class="col-md-6">
        <div class="row">
          <div class="col-md-10 col-sm-12">
            <q-list link dense no-border>
              <div class="q-if-label font-size-12 pb-2">Who Can Take This Exam</div>
              <q-item tag="label" class="pl-0">
                <q-item-side>
                  <q-radio color="negative" v-model="settings.audienceGroup" val="any"></q-radio>
                </q-item-side>
                <q-item-main>
                  <q-item-tile title>Anyone</q-item-tile>
                </q-item-main>
              </q-item>
              <q-item tag="label" class="pl-0">
                <q-item-side>
                  <q-radio color="secondary" v-model="settings.audienceGroup" val="ud"></q-radio>
                </q-item-side>
                <q-item-main>
                  <q-item-tile label>User With Exam ID</q-item-tile>
                </q-item-main>
              </q-item>
              <q-item tag="label" class="pl-0">
                <q-item-side>
                  <q-radio color="primary" v-model="settings.audienceGroup" val="aud"></q-radio>
                </q-item-side>
                <q-item-main>
                  <q-item-tile label>Users Targeted in Audience</q-item-tile>
                </q-item-main>
              </q-item>
            </q-list>
          </div>
        </div>
        <div class="row">
          <div class="col-md-10 col-sm-12">
            <q-field>
              <q-input v-model="settings.password" float-label="Exam Password" type="password" clearable></q-input>
            </q-field>

          </div>
        </div>
        <div class="row">
          <div class="col-md-10 col-sm-12">
            <q-field helper="Leave blank for unlimited attempts">
              <q-input v-model="settings.attempts" float-label="Attempts" type="number" :min="0" clearable></q-input>
            </q-field>
          </div>
        </div>
        <div class="row">
          <div class="col-md-10 col-sm-12">
            <q-field helper="Once checked, only an administrator can disable this">
              <q-checkbox v-model="settings.privacy" label="Keep respondents identities anonymous" color="negative"></q-checkbox>
            </q-field>
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <div class="row">
          <div class="col-12">
            <q-card>
              <q-card-title class="bg-primary">
                Release Options
              </q-card-title>
              <q-list separator>
                <q-collapsible icon="fa-unlock" label="Security Exceptions">
                  <div>
                    Lorem ipsum dolor sit amet...
                  </div>
                </q-collapsible>

                <q-collapsible icon="fa-check-square-o" label="Exam Pre-requisites">
                  <div>
                    Lorem ipsum dolor sit amet...
                  </div>
                </q-collapsible>
              </q-list>
            </q-card>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>

  export default {
    name: 'Security',
    props: ['settings'],
    components: {
    },
    data () {
      return {
      }
    }
  }
</script>
<style lang="stylus">

</style>
