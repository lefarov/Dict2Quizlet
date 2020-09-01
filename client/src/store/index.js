import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    translation: [],
  },
  getters: {},
  mutations: {
    updateTranslation(state, payload) {
      state.translation = payload.translation;
    },
  },
  actions: {},
});
