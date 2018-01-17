<template>
  <div class="app flex-row align-items-center login" v-if="checked">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-8">
          <div class="row">
            <q-card color="white" class="col-7 m-0 p-3">
              <q-card-title><img src="statics/img/logo.svg" class="mx-auto d-block p-3" style="width: 75%; height: 75%;"></q-card-title>
              <q-card-main>
                <q-field
                  icon="fa-user"
                  :error="hasError"
                >
                  <q-input type="text" @keyup.enter="login" v-model="username" float-label="Username"></q-input>
                </q-field>
                <q-field
                  icon="fa-lock"
                  :error="hasError"
                  :error-label="error"
                >
                  <q-input type="password" @keyup.enter="login" v-model="password" float-label="Password"></q-input>
                </q-field>
                <div class="row">
                  <div class="col-12 row mt-2">
                    <q-btn color="primary" class="col-12" @click="login">Login</q-btn>
                  </div>
                  <div class="col-12 text-right mt-2">
                    <q-btn color="black" flat small>Forgot password?</q-btn>
                  </div>
                </div>
              </q-card-main>
            </q-card>
            <q-card color="primary" class="text-center col-5 m-0 p-3">
              <q-card-title>Welcome!</q-card-title>
              <q-card-separator></q-card-separator>
              <q-card-main>
                <p>
                  Solvio is a secure online platform for students to take exams. To continue please login with your username and password that was provided to you.</p>
                <q-btn small color="secondary">Need Help?</q-btn>
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
    name: 'Login',
    components: {
    },
    data () {
      return {
        username: '',
        password: '',
        checked: false,
        error: '',
        hasError: false
      }
    },
    mounted () {
      this.$http({
        method: 'post',
        url: '/api/isloggedin/'
      }).then(response => {
        if (response.status === 200) {
          this.$router.push({ path: '/courses' })
        }
        if (response.status === 250) {
          this.checked = true
        }
      }).catch(error => {
        console.log(error)
      })
    },
    methods: {
      login () {
        this.hasError = false
        this.$http({
          method: 'post',
          url: '/api/login/',
          data: {
            username: this.username,
            password: this.password
          }
        }).then(response => {
          if (response.status === 250) {
            this.error = response.data
            this.hasError = true
          } else {
            this.$router.push({ path: '/courses' })
          }
        }).catch(error => {
          console.log(error)
        })
      }
    }
  }
</script>
