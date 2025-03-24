import { createStore } from 'vuex';  // 只需要从 vuex 导入 createStore
import axios from 'axios';

export default createStore({
  state: {
    isAuthenticated: false,  // 用户登录状态
  },
  mutations: {
    setAuthentication(state, status) {
      state.isAuthenticated = status;  // 更新登录状态
    },
  },
  actions: {
async checkAuth({ commit }) {
  try {
    const response = await axios.get(`${import.meta.env.VITE_API_URL}/user/login/`, {
      withCredentials: true  // ✅ 让浏览器携带 sessionid
    });
    commit('setAuthentication', response.data.login);
  } catch (error) {
    console.error('Error checking login status:', error);
    commit('setAuthentication', false);
  }
},

  },
  getters: {
    isAuthenticated: (state) => state.isAuthenticated,  // 获取用户的登录状态
  },
});
