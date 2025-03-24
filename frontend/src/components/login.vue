<script setup>
import { ref, defineEmits } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const email = ref('');
const password = ref('');
const errorMessage = ref('');
const router = useRouter();
const emit = defineEmits(["login-success"]); // ✅ 定义事件，通知 `mainpage_template.vue`

// ✅ 登录函数
const login = async () => {
  if (!email.value.trim() || !password.value.trim()) {
    errorMessage.value = '⚠️ Email and password are required!';
    return;
  }

  try {
    const response = await axios.post(
      `${import.meta.env.VITE_API_URL}/user/login/`,
      { email: email.value, password: password.value },
      { withCredentials: true }
    );

    if (response.status === 200) {
      console.log("✅ 登录成功");

      // ✅ 存储登录状态
      localStorage.setItem('isAuthenticated', 'true');
      localStorage.setItem('user', JSON.stringify(response.data.user));

      // ✅ 触发事件，通知 `mainpage_template.vue` 更新 Sidebar
      emit("login-success");

      // ✅ 跳转到主页
      router.push("/home");
    }
  } catch (error) {
    errorMessage.value = error.response?.data?.error || '😞 Login failed!';
    console.error("❌ 登录失败:", error);
  }
};
</script>

<template>
  <div class="login-container">
    <h2 class="text-center">🔐 Login</h2>
    <form @submit.prevent="login" class="p-4 shadow-sm bg-light rounded">
      <div class="mb-3">
        <label for="email" class="form-label">📧 Email:</label>
        <input type="email" id="email" v-model="email" required class="form-control" placeholder="Enter your email"/>
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">🔑 Password:</label>
        <input type="password" id="password" v-model="password" required class="form-control"
               placeholder="Enter your password"/>
      </div>
      <div class="d-grid">
        <button type="submit" class="btn btn-primary btn-lg">🚀 Login</button>
      </div>
    </form>
    <div v-if="errorMessage" class="mt-3 alert alert-danger text-center">
      {{ errorMessage }}
    </div>
  </div>
</template>


<style scoped>
.login-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
}
</style>
