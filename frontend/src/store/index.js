import { createStore } from "vuex";

export default createStore({
  state: {
    userId: null, // Estado inicial para almacenar el userId
  },
  getters: {
    getUserId(state) {
      return state.userId;
    },
  },
  mutations: {
    setUserId(state, userId) {
      state.userId = userId;
    },
  },
  actions: {
    setUserId({ commit }, userId) {
      commit("setUserId", userId);
    },
  },
  modules: {},
});
