<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const username = ref('');
const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const firstName = ref('');
const lastName = ref('');
const description = ref('');
const schoolYear = ref('');
const verificationCode = ref('');  // 用于存储验证码
const errorMessage = ref('');
const router = useRouter();

// 学年选项
const schoolYearOptions = [
  { value: 'Freshmen', label: 'Freshmen' },
  { value: 'Sophomore', label: 'Sophomore' },
  { value: 'Junior', label: 'Junior' },
  { value: 'Senior', label: 'Senior' },
];

const register = async () => {
  try {
    const response = await axios.post(`${import.meta.env.VITE_API_URL}/user/user_register/`,
      {
        username: username.value,
        password: password.value,
        email: email.value,
        first_name: firstName.value,
        last_name: lastName.value,
        description: description.value,
        school_year: schoolYear.value,
        verification_code: verificationCode.value
      },
      {
        headers: { "Content-Type": "application/json" },
        withCredentials: true
      }
    );

    if (response.status === 201) {
      router.push('/login'); // ✅ 注册成功后跳转
    }
  } catch (err) {
    // ✅ 如果后端返回了 ValidationError，就显示具体的错误信息
    errorMessage.value = err.response?.data?.error || "😞 An error occurred";
  }
};


// 发送验证码请求
const sendVerificationCode = async () => {
  try {
    await axios.post(`${import.meta.env.VITE_API_URL}/user/user_verification/`, { email: email.value },{headers:{"Content-Type":"application/json"},
    withCredentials:true});
    errorMessage.value = '✅ Verification code sent to your email.';
  } catch (error) {
    errorMessage.value = error.response?.data?.message || '😞 Failed to send verification code.';
  }
};
</script>

<template>

    <h2 class="mb-4 text-center">🚀 Register Account</h2>
    <form @submit.prevent="register" class="p-4 shadow-sm bg-light rounded">
      <div class="mb-3">
        <label for="username" class="form-label">
          <i class="fas fa-user"></i> Username:
        </label>
        <input type="text" id="username" v-model="username" required class="form-control" placeholder="Enter your username" />
      </div>
      <div class="mb-3">
        <label for="email" class="form-label">
          <i class="fas fa-envelope"></i> Email:
        </label>
        <div class="input-group">
          <input type="email" id="email" v-model="email" required class="form-control" placeholder="you@example.com" />
          <button type="button" @click="sendVerificationCode" class="btn btn-outline-secondary">
            📧 Send Code
          </button>
        </div>
      </div>
      <div class="mb-3">
        <label for="verification_code" class="form-label">
          <i class="fas fa-key"></i> Verification Code:
        </label>
        <input type="text" id="verification_code" v-model="verificationCode" required class="form-control" placeholder="Enter code" />
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">
          <i class="fas fa-lock"></i> Password:
        </label>
        <input type="password" id="password" v-model="password" required class="form-control" placeholder="Enter your password" />
      </div>
      <div class="mb-3">
        <label for="confirm_password" class="form-label">
          <i class="fas fa-lock"></i> Confirm Password:
        </label>
        <input type="password" id="confirm_password" v-model="confirmPassword" required class="form-control" placeholder="Re-enter your password" />
      </div>
      <div class="mb-3">
        <label for="first_name" class="form-label">
          <i class="fas fa-user-circle"></i> First Name:
        </label>
        <input type="text" id="first_name" v-model="firstName" required class="form-control" placeholder="Your first name" />
      </div>
      <div class="mb-3">
        <label for="last_name" class="form-label">
          <i class="fas fa-user-circle"></i> Last Name:
        </label>
        <input type="text" id="last_name" v-model="lastName" required class="form-control" placeholder="Your last name" />
      </div>
      <div class="mb-3">
        <label for="description" class="form-label">
          <i class="fas fa-comment-dots"></i> Description:
          <small class="text-muted">(Optional)</small>
        </label>
        <textarea id="description" v-model="description" class="form-control" rows="3" placeholder="Tell us about yourself"></textarea>
      </div>
     <!-- 下拉框部分 -->
<div class="mb-3">
  <label for="school_year" class="form-label">
    <i class="fas fa-graduation-cap"></i> School Year:
  </label>
  <select id="school_year" v-model="schoolYear" required class="form-select custom-select">
    <option value="">Select your school year...</option>
    <option v-for="option in schoolYearOptions" :key="option.value" :value="option.value">
      {{ option.label }}
    </option>
  </select>
</div>

      <div class="d-grid">
        <button type="submit" class="btn btn-primary btn-lg">
          <i class="fas fa-user-plus"></i> Register
        </button>
      </div>
    </form>
    <div v-if="errorMessage" class="mt-3 alert alert-danger text-center">
      {{ errorMessage }}
    </div>
</template>

<style scoped>
/* 自定义一些细节 */
h2 {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

input::placeholder,
textarea::placeholder {
  font-style: italic;
  color: #6c757d;
}

/* 轻微动画效果 */
button.btn-primary:hover {
  transform: scale(1.02);
  transition: transform 0.2s ease-in-out;
}
select.custom-select {
  border-radius: 8px;
  border: 1px solid #ced4da;
  background: linear-gradient(145deg, #ffffff, #f8f8f8);
  padding: 0.375rem 0.75rem;
  font-size: 1rem;
  transition: all 0.2s ease-in-out;
  box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.1);
  appearance: none; /* 隐藏默认箭头 */
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 120 120' xmlns='http://www.w3.org/2000/svg'%3E%3Cpolygon points='0,40 60,100 120,40' fill='%236c757d'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 0.75rem center;
  background-size: 1rem;
}

select.custom-select:focus {
  border-color: #FFA07A;
  box-shadow: 0 0 0 0.2rem rgba(255, 160, 122, 0.25);
  outline: none;
}
</style>
