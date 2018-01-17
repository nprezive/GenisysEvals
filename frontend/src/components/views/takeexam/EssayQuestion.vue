<template>
  <div class="examQuestion">
    <q-card style="background-color: white">
      <q-card-title>
        {{ index + 1 }}. {{ question.text }}
        <!--TODO add so that we get the question it was for the student-->
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
          <q-input
            v-model="response"
            type="textarea"
            placeholder="Enter response here"
            :min-rows="7"
            :max-height="400"
            :disable="review"
          ></q-input>
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
    computed: {
      answered () {
        let a = false
        if (this.response !== '') {
          a = true
        }
        return a
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
