// src/store/index.js
import { createStore } from 'vuex';

const store = createStore({
  state: {
    isAuthenticated: false,  // 记录用户登录状态
  },
  mutations: {
    setAuthStatus(state, status) {
      state.isAuthenticated = status;
    },
  },
  actions: {
    checkAuth({ commit }) {
      // 假设你的后端提供了一个接口来检查用户是否登录
      fetch('user/login/')
        .then((response) => response.json())
        .then((data) => {
          commit('setAuthStatus', data.login);
        });
    },
  },
});

export default store;
