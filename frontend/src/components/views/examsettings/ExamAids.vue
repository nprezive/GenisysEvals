<template>
  <div id="exam-aids">
    <div class="row">
      <div class="col-md-6">
        <div class="row">
          <div class="col-md-10 col-sm-12">
            <q-select
              multiple
              chips
              color="primary"
              float-label="Exam Materials"
              v-model="settings.materials"
              :options="materialsOptions"></q-select>
          </div>
        </div>
        <div class="row"
             v-if="(settings.materials.indexOf('personal-notes') != -1) || (settings.materials.indexOf('cue-sheets') != -1)">
          <div class="col-md-10 col-sm-12">
            <q-list link dense no-border class="pb-0">
              <q-item tag="label" class="pl-0 pb-0 mb-0">
                <q-item-side>
                  <q-checkbox v-model="settings.keepNotes"></q-checkbox>
                </q-item-side>
                <q-item-main>
                  <q-item-tile label>Allow students to keep their notes and cue sheets</q-item-tile>
                </q-item-main>
              </q-item>
            </q-list>
          </div>
        </div>
        <div class="row"
             v-if="(settings.materials.indexOf('personal-notes') != -1) || (settings.materials.indexOf('cue-sheets') != -1)">
          <div class="col-md-10 col-sm-12">
            <q-field v-if="settings.materials.indexOf('personal-notes') != -1">
              <q-input v-model="settings.personalNotes" float-label="Number or size of notes" type="text"
                       placeholder="'index card', '3'"></q-input>
            </q-field>
            <q-field v-if="settings.materials.indexOf('cue-sheets') != -1">
              <q-input v-model="settings.cueSheets" float-label="Number or size of sheets" type="text"
                       placeholder="'periodic table on index card'"></q-input>
            </q-field>
          </div>
        </div>
        <div class="row" v-if="(settings.materials.indexOf('open-book') != -1)">
          <div class="col-md-10 col-sm-12">
            <q-field>
              <q-input v-model="settings.openBookName" float-label="Name of book" type="text"
                       placeholder="Book Title"></q-input>
            </q-field>
          </div>
        </div>
        <div class="row">
          <div class="col-md-10 col-sm-12">
            <q-select
              multiple
              chips
              color="secondary"
              float-label="Dictionary Options"
              v-model="settings.dictionaries"
              :options="dictionaryOptions"></q-select>
          </div>
        </div>
        <div class="row">
          <div class="col-md-10 col-sm-12">
            <q-select
              multiple
              chips
              color="negative"
              float-label="Calculator Options"
              v-model="settings.calculators"
              :options="calculatorOptions"></q-select>
          </div>
        </div>
        <div class="row" v-if="settings.calculators.indexOf('other') != -1">
          <div class="col-md-10 col-sm-12">
            <q-field
              helper="You may choose a calculator that is more advanced than the calculator options normally allowed by the Testing Centers. The Testing Centers will allow the exact listed model, with no variations or exceptions. Be advised that even if specified, calculators with WiFi capability or full alphabetic keyboards will not be permitted in the WSU Testing Centers. Any questions regarding this policy should be directed to the Testing Center(s) where the students will be taking the exam">
              <q-input v-model="settings.otherCalculator" float-label="Other Calculator Type" type="text"></q-input>
            </q-field>
          </div>
        </div>
        <div class="row">
          <div class="col-md-10 col-sm-12">
            <q-list link dense no-border>
              <q-item tag="label" class="pl-0">
                <q-item-side>
                  <q-checkbox v-model="settings.restroomBreak"></q-checkbox>
                </q-item-side>
                <q-item-main>
                  <q-item-tile label>Allow a restroom break if exam is over two hours</q-item-tile>
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
        <q-collapsible icon="fa-globe" label="Whitelisted Websites"
                       sublabel="Allow a student to visit specified addresses on the Web while taking a exam">
          <div class="row">
            <div class="col-12 font-xs">
              Web sites that are listed in this section will be made available to students while they are taking their exams. Students will not be allowed to navigate outside the web address listed. This feature may be used for items such as online calculators, tables, images, or articles that you wish students to use as reference during the exam or for other purposes such as allowing students to listen to music.
            </div>
          </div>
          <div class="row">
            <div class="col-md-6 col-xs-12">
              <div class="row">
                <div class="col-md-10 col-xs-12">
                  <div class="row pt-2">
                    <div class="col-md-5 col-xs-5">Web Address</div>
                    <div class="col-md-5 col-xs-5">Name or Abbreviation</div>
                  </div>
                  <div class="row" v-for="(site, index) in settings.whitelistedSites">
                    <div class="col-md-5 col-xs-5">
                      <q-field>
                        <q-input v-model="site.webAddress"></q-input>
                      </q-field>
                    </div>
                    <div class="col-md-5 col-xs-5">
                      <q-field>
                        <q-input v-model="site.abbreviation"></q-input>
                      </q-field>
                    </div>
                    <div class="col-md-2 col-xs-1 pt-2">
                      <q-btn flat icon="fa-times" color="negative" @click=""></q-btn>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </q-collapsible>
      </div>
    </div>
  </div>
</template>
<script>

  export default {
    name: 'ExamAids',
    props: ['settings'],
    components: {
    },
    data () {
      return {
        materialsOptions: [
          {
            label: 'Scratch Paper',
            value: 'scratch-paper'
          },
          {
            label: 'Open Book',
            value: 'open-book'
          },
          {
            label: 'Personal Notes',
            sublabel: 'Notes that students have written themselves',
            value: 'personal-notes'
          },
          {
            label: 'Cue Sheets',
            sublabel: 'Documents like a periodic table, a log table, or a chronological time line - usually purchased items',
            value: 'cue-sheets'
          }
        ],
        dictionaryOptions: [
          {
            label: 'English',
            value: 'english'
          },
          {
            label: 'Paper Foreign',
            value: 'paper-foreign'
          }
        ],
        calculatorOptions: [
          {
            label: 'Four Function',
            value: 'four-function'
          },
          {
            label: 'Scientific',
            value: 'scientific'
          },
          {
            label: 'Graphing',
            value: 'graphing'
          },
          {
            label: 'Financial',
            value: 'financial'
          },
          {
            label: 'Other',
            value: 'other'
          },
          {
            label: 'Provided',
            value: 'provided',
            sublabel: 'Examination personnel provides calculator, please contact them to ensure they are able to do so'
          }
        ]
      }
    }
  }
</script>
