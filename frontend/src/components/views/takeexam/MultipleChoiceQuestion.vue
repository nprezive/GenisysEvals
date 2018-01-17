<template>
  <div class="examQuestion">
    <q-card style="background-color: white">
      <q-card-title>
        {{ index+1 }}. {{ question.text }}
        <div slot="right">
          <q-toggle v-if="!review" icon="bookmark" v-model="bookmarked"></q-toggle>
          <span v-if="review">
            <span v-if="questionresponse.graded">{{ questionresponse.score }} / {{ question.weight }} ( {{ Math.round(((questionresponse.score / question.weight) * 100) * 100) / 100 }}% )</span>
            <span v-if="!questionresponse.graded">Has not been graded.</span>
          </span>
          <div v-if="review"> For you this was question: {{  }}</div>
        </div>
      </q-card-title>
      <q-card-separator></q-card-separator>
      <q-card-main>
        <q-field>
          <q-option-group
            v-model="response"
            :options="questionOptions"
            :disable="review"
          ></q-option-group>
        </q-field>
      </q-card-main>
    </q-card>
  </div>
</template>

<script>

  export default {
    name: 'Question',
    props: ['index', 'question', 'result', 'review', 'questionresponse'],
    data () {
      return {
        response: '',
        questionid: this.question.id,
        questiontype: this.question.question_type_id,
        bookmarked: false
      }
    },
    mounted () {
      this.$http({
        method: 'get',
        url: '/api/result/' + this.result + '/' + this.questionid + '/',
        headers: {
          'X-CSRFToken': this.getCookie('csrftoken')
        }
      }).then(response => {
        if (response.status === 250) {
          this.$router.error = response.data
          this.$router.push({path: '/error'})
        }
        this.response = response.data['settings']['response']
        this.bookmarked = response.data['settings']['bookmarked']
      }).catch(error => {
        console.log(error)
      })
    },
    computed: {
      questionOptions () {
        let options = []
        for (let i = 0; i < this.question.settings.distractors.length; i++) {
          options.push({label: this.question.settings.distractors[i].text, value: this.question.settings.distractors[i].sequence})
        }
        return options
      },
      answered () {
        let a = false
        if (this.response !== '') {
          a = true
        }
        return a
      }
    },
    methods: {
      getResponse () {
        return this.response
      },
      getCookie (name) {
        let cookieValue = null
        if (document.cookie && document.cookie !== '') {
          let cookies = document.cookie.split(';')
          for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim()
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
              break
            }
          }
        }
        return cookieValue
      }
    }
  }
</script>
<style lang="stylus">
  .examQuestion
    max-width 750px
    min-height 500px
</style>
