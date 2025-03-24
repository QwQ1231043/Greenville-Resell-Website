import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import axios from 'axios';

// ✅ 让 Axios 自动携带 `withCredentials`
axios.defaults.withCredentials = true;

// ✅ 获取 CSRF Token（Vue 3 `onMounted()` 只能在组件 `setup()` 里用，不能在 `main.js` 用）
async function fetchCsrfToken() {
    try {
        await axios.get(`${import.meta.env.VITE_API_URL}/csrf/`, { withCredentials: true });
        console.log("✅ CSRF Token 已获取");
    } catch (error) {
        console.error("❌ 获取 CSRF Token 失败:", error);
    }
}

// ✅ 全局拦截请求，自动加上 `X-CSRFToken`
axios.interceptors.request.use(config => {
    const csrfToken = document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];

    if (csrfToken) {
        config.headers['X-CSRFToken'] = csrfToken;
    }
    return config;
}, error => Promise.reject(error));

// ✅ 创建 Vue 应用实例
const app = createApp(App);

// ✅ 让 `this.$axios` 可用（Vue 组件可以用 `this.$axios.get()` ）
app.config.globalProperties.$axios = axios;

// ✅ 使用 Vuex store
app.use(store);

// ✅ 使用 Vue Router
app.use(router);

// ✅ 挂载 Vue 应用
app.mount('#app');

// ✅ 先获取 CSRF Token
fetchCsrfToken();
