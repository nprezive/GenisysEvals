<template>
  <div class="examQuestion" v-if="isLoaded">
    <q-card style="background-color: white">
      <q-card-title>
        {{ index + 1 }}. {{ question.text }}
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
        <div v-for="(option, index) in options" :key="index">
          <matching-option :oldResponse="oldResponse" :ref="'match' + index" :option="option"
                           :questionOptions="questionOptions" :index="index" :review="review"></matching-option>
        </div>
      </q-card-main>
    </q-card>
  </div>
</template>

<script>
  import MatchingOption from './matching/MatchingOption.vue'

  export default {
    name: 'Question',
    props: ['index', 'question', 'result', 'review', 'questionresponse'],
    components: {
      MatchingOption
    },
    data () {
      return {
        questionid: this.question.id,
        questiontype: this.question.question_type_id,
        oldResponse: [],
        isLoaded: false,
        answered: false,
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
        if (response.data === '') {
          for (let i = 0; i < this.question.settings.options.length; i++) {
            this.oldResponse.push('')
          }
        } else {
          this.oldResponse = response.data['settings']['response']
          this.bookmarked = response.data['settings']['bookmarked']
          this.answered = true
        }
        this.isLoaded = true
      }).catch(error => {
        console.log(error)
      })
    },
    computed: {
      questionOptions () {
        let options = []
        for (let i = 0; i < this.question.settings.distractors.length; i++) {
          options.push({label: this.question.settings.distractors[i], value: i})
        }
        return options
      },
      response () {
        if (this.isLoaded) {
          let data = []
          let arrayFull = true
          for (let i = 0; i < this.options.length; i++) {
            data.push()
          }
          for (let i = 0; i < this.options.length; i++) {
            data[this.$refs['match' + i][0].option.answer] = this.$refs['match' + i][0]._data.response
            if (this.$refs['match' + i][0]._data.response === '') {
              arrayFull = false
            }
          }
          if (arrayFull) {
            this.answered = true
          }
          return data
        }
      },
      options () {
        let options = this.shuffle(this.question.settings.options)
        return options
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
      },
      shuffle (array) {
        let currentIndex = array.length, temporaryValue, randomIndex
        while (currentIndex !== 0) {
          randomIndex = Math.floor(Math.random() * currentIndex)
          currentIndex -= 1

          temporaryValue = array[currentIndex]
          array[currentIndex] = array[randomIndex]
          array[randomIndex] = temporaryValue
        }

        return array
      }
    }
  }
</script>
<style lang="stylus">
  .examQuestion
    max-width 750px
    min-height 500px

  .drop-box
    width: 100x
    height: 35px
</style>
