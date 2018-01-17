<template>
  <div id="questions">
    <div class="row">
      <div class="col-md-6">
        <div class="row">
          <div class="col-md-10 col-sm-12">
            <div class="pb-2" v-if="noQuestionSets">
              This exam has no questions assigned to it, to assign questions go to the Exam Editor
            </div>
            <div class="q-if-label font-size-12">Each Student Will Receive</div>
            <q-list link dense no-border>
              <q-item tag="label" class="pl-0">
                <q-item-side>
                  <q-radio color="primary" v-model="settings.receiveQuestionGroup" val="all"
                           :disable="noQuestionSets"></q-radio>
                </q-item-side>
                <q-item-main>
                  <q-item-tile label>
                    All {{ totalQuestionCount }} questions
                  </q-item-tile>
                </q-item-main>
              </q-item>
              <q-item tag="label" class="pl-0">
                <q-item-side>
                  <q-radio color="secondary" v-model="settings.receiveQuestionGroup" val="randomly"
                           :disable="noQuestionSets"></q-radio>
                </q-item-side>
                <q-item-main>
                  <q-item-tile label>
                    <div class="row">
                      <div class="col-1">
                        <q-field>
                          <q-input class="p-0 m-0" v-model="settings.numQuestionsRandomlySelected" type="number"
                                   :min="0" :disable="noQuestionSets"></q-input>
                        </q-field>

                      </div>
                      <div class="col-11 pl-2 pt-2">
                        randomly selected from the total {{ totalQuestionCount }} questions
                      </div>
                    </div>
                  </q-item-tile>
                </q-item-main>
              </q-item>
              <q-item tag="label" class="pl-0" :disabled="noQuestionSets">
                <q-item-side>
                  <q-radio color="negative" v-model="settings.receiveQuestionGroup" val="questionset"
                           :disable="noQuestionSets"></q-radio>
                </q-item-side>
                <q-item-main>
                  <q-item-tile label>Questions selected randomly from question sets</q-item-tile>
                  <q-item-tile sublabel v-if="!noQuestionSets && settings.receiveQuestionGroup !== 'questionset'">
                    Additional settings are required for this option
                  </q-item-tile>
                  <q-item-tile sublabel v-else-if="settings.receiveQuestionGroup === 'questionset'"></q-item-tile>
                  <q-item-tile sublabel v-else>This exam has no question sets</q-item-tile>
                </q-item-main>
              </q-item>
            </q-list>
          </div>
        </div>
        <div class="row" v-if="settings.receiveQuestionGroup === 'questionset'">
          <div class="col-10">
            <div class="q-if-label font-size-12 pb-2">
              Please specify how many questions from each question set should be randomly selected below.
              Note that questions in the exam will be grouped in the order shown below, which can be rearranged by dragging and dropping within Proofread and Edit.
              You can randomize the order of question by checking the Randomization option below. The questions will be randomized within each question set
            </div>
            <span v-for="(questionSetValue, aindex) in settings.questionSets" :key="aindex">
              <span v-for="(questionSetInfo, bindex) in questionSets" :key="bindex">
                <span v-if="questionSetValue.id === questionSetInfo.id">
                  <div class="q-if-label font-size-12">{{ questionSetInfo.name }}: {{ questionSetValue.value
                    }} out of {{ questionSetInfo.question_count
                    }}</div>
                  <q-slider @change="updateTotalQuestionSetsCount" label v-model="questionSetValue.value" :min="0"
                        :max="questionSetInfo.question_count" :step="1" snap></q-slider>
                </span>
              </span>
            </span>
            <q-field class="mt-0 pb-2"
                     :helper="totalQuestionSetQuestionsSelected + ' questions out of ' + totalQuestionCount + ' will be delivered'"></q-field>
          </div>
        </div>
        <div class="row">
          <div class="col-md-10 col-sm-12">
            <div class="q-if-label font-size-12">Presentation</div>
            <q-list link dense no-border>
              <q-item tag="label" class="pl-0" @click="oneAtATime">
                <q-item-side>
                  <q-radio color="primary" v-model="settings.presentationGroup" val="one" @focus="oneAtATime"></q-radio>
                </q-item-side>
                <q-item-main>
                  <q-item-tile label>One at a time</q-item-tile>
                </q-item-main>
              </q-item>
              <q-item tag="label" class="pl-0" @click="allAtOnce">
                <q-item-side>
                  <q-radio color="secondary" v-model="settings.presentationGroup" val="all"
                           @focus="allAtOnce"></q-radio>
                </q-item-side>
                <q-item-main>
                  <q-item-tile label>
                    All questions at once
                  </q-item-tile>
                </q-item-main>
              </q-item>
              <q-item tag="label" class="pl-0" :disabled="questionSets.length === 0" @click="allPerQuestionSet">
                <q-item-side>
                  <q-radio color="negative" v-model="settings.presentationGroup" val="questionset"
                           :disable="questionSets.length === 0" @focus="allPerQuestionSet"></q-radio>
                </q-item-side>
                <q-item-main>
                  <q-item-tile label>All questions per question set at once</q-item-tile>
                  <q-item-tile sublabel v-if="questionSets.length === 0">This exam has no question sets
                  </q-item-tile>
                </q-item-main>
              </q-item>
            </q-list>
          </div>
        </div>
        <div class="row">
          <div class="col-md-10 col-sm-12">
            <q-select
              multiple
              chips
              color="primary"
              float-label="Additional Options"
              @change="additionalOptionsChange"
              v-model="settings.additional"
              :options="additionalOptions"></q-select>
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <div class="row">
          <div class="col-12">
            <q-card>
              <q-card-title class="bg-primary">
                Question Delivery
              </q-card-title>
              <q-card-main>
                <q-select
                  v-if="multipleChoiceSelect"
                  stack-label="Multiple Choice Questions"
                  separator
                  v-model="multipleChoiceSelect"
                  :options="multipleChoiceQuestions"></q-select>
                <q-select
                  v-if="multipleResponseSelect"
                  stack-label="Multiple Response Questions"
                  separator
                  v-model="multipleResponseSelect"
                  :options="multipleResponseQuestions"></q-select>
                <q-select
                  v-if="matchingSelect"
                  stack-label="Matching Questions"
                  separator
                  v-model="matchingSelect"
                  :options="matchingQuestions"></q-select>
                <q-select
                  v-if="shortAnswerSelect"
                  stack-label="Short Answer Questions"
                  separator
                  v-model="shortAnswerSelect"
                  :options="shortAnswerQuestions"></q-select>
                <q-select
                  v-if="essaySelect"
                  stack-label="Essay Questions"
                  separator
                  v-model="essaySelect"
                  :options="essayQuestions"></q-select>
              </q-card-main>
            </q-card>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>

  export default {
    name: 'Questions',
    props: ['settings', 'questionSets'],
    components: {},
    data () {
      return {
        noQuestionSets: true,
        totalQuestionCount: 0,
        totalQuestionSetQuestionsSelected: 0,
        additionalOptions: [
          {
            label: 'Randomize',
            sublabel: 'Randomize question order',
            value: 'randomize'
          },
          {
            label: 'Go Back',
            sublabel: 'Allow students to go back and change responses to questions already answered',
            value: 'go-back'
          },
          {
            label: 'Retake',
            sublabel: 'When retaking the exam, show only questions that were missed on previous attempt',
            value: 'retake'
          },
          {
            label: 'Spaces',
            sublabel: 'Ignore spaces in response when scoring short answer',
            value: 'spaces'
          },
          {
            label: 'Case Sensitive',
            sublabel: 'Case sensitive when scoring short answer',
            value: 'caseSensitive'
          }
        ],
//        TODO figure out way to get which questions are on the exam (for card) to this component
        multipleChoiceSelect: ' ',
        multipleResponseSelect: false,
        matchingSelect: false,
        shortAnswerSelect: ' ',
        essaySelect: ' ',
        multipleChoiceQuestions: [
          {
            label: 'Question 1',
            value: 'one'
          },
          {
            label: 'Question 2',
            value: 'two'
          },
          {
            label: 'Question 4',
            value: 'three'
          }
        ],
        multipleResponseQuestions: [],
        matchingQuestions: [],
        shortAnswerQuestions: [
          {
            label: 'Question 5',
            value: 'one'
          },
          {
            label: 'Question 6',
            value: 'two'
          }
        ],
        essayQuestions: [
          {
            label: 'Question 3',
            value: 'one'
          }
        ]
      }
    },
    mounted: function () {
      this.totalQuestionCount = 0
      this.totalQuestionSetQuestionsSelected = 0
      this.getQuestionSets()
    },
    methods: {
      updateTotalQuestionSetsCount (newVal) {
        this.totalQuestionSetQuestionsSelected = 0
        for (let i = 0; i < this.settings.questionSets.length; i++) {
          this.totalQuestionSetQuestionsSelected += this.settings.questionSets[i].value
        }
      },
      oneAtATime () {
        this.additionalOptions[1].sublabel = 'Allow students to go back and change responses to questions already answered'
        this.additionalOptions[0].sublabel = 'Randomize question order'
      },
      allAtOnce () {
        this.additionalOptions[0].sublabel = 'Randomize question order'
        this.enableGoBack()
      },
      allPerQuestionSet () {
        if (this.questionSets.length !== 0) {
          this.enableGoBack()
          this.disableRandomize()
        }
      },
      additionalOptionsChange (newValue) {
        if (this.settings.presentationGroup === 'all') {
          this.enableGoBack()
        }
        if (this.settings.presentationGroup === 'questionset') {
          this.enableGoBack()
          this.disableRandomize()
        }
      },
      enableGoBack () {
        if (this.settings.additional.indexOf('go-back') === -1) {
          this.settings.additional.push('go-back')
        }
        this.additionalOptions[1].sublabel = 'Allow students to go back and change responses to questions already answered' +
          '<br/><span class="text-red">This must be enabled if all questions are presented at once or all questions per question set at once</span>'
      },
      disableRandomize () {
        if (this.settings.additional.indexOf('randomize') !== -1) {
          this.settings.additional.splice(this.settings.additional.indexOf('randomize'), 1)
        }
        this.additionalOptions[0].sublabel = 'Randomize question order' +
          '<br/><span class="text-red">This option cannot be enabled if all questions per question set are presented at once</span>'
      },
      getQuestionSets () {
        if (this.questionSets.length < 1) {
          this.noQuestionSets = true
        } else {
          this.noQuestionSets = false
          for (let i = 0; i < this.settings.questionSets.length; i++) {
            this.totalQuestionSetQuestionsSelected += this.settings.questionSets[i].value
          }
          for (let j = 0; j < this.questionSets.length; j++) {
            this.totalQuestionCount += this.questionSets[j].question_count
          }
        }
      }
    }
  }
</script>
<style lang="stylus">

</style>
