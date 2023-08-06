import Vue from 'vue'
import Vuex from 'vuex'
import * as actions from '@/store/actions'
import alarms from '@/store/modules/alarms'
import light from '@/store/modules/light'

Vue.use(Vuex)

const debug = process.env.NODE_ENV !== 'production'

export default new Vuex.Store({
  actions,
  modules: {
    alarms,
    light
  },
  strict: debug,
})
