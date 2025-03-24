import axios from "axios";

axios.defaults.withCredentials = true;
axios.defaults.baseURL = import.meta.env.VITE_API_URL;

// ✅ 获取 CSRF Token
async function fetchCsrfToken() {
    try {
        const response = await axios.get("/csrf/");
        console.log("✅ CSRF Token 已获取:", response.data.csrfToken);
    } catch (error) {
        console.error("❌ 获取 CSRF Token 失败:", error);
    }
}
fetchCsrfToken();

// ✅ 拦截所有请求，自动加上 CSRF Token
axios.interceptors.request.use(config => {
    const csrfToken = document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];

    if (csrfToken) {
        config.headers['X-CSRFToken'] = csrfToken;  // ✅ 发送 X-CSRFToken
    }
    return config;
}, error => Promise.reject(error));

export default axios;
