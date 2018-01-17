import Vue from 'vue'
import Vuex from 'vuex'
import examModule from './modules/exam'
import enrollmentModule from './modules/enrollment'

Vue.use(Vuex)

const store = new Vuex.Store({
  modules: {
    examModule,
    enrollmentModule
  }
})

export default store
