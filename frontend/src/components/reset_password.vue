<script setup>
import {ref} from "vue";
import axios from "axios";

const email = ref("");  // ✅ 记录用户输入的 email
const verificationCode = ref("");  // ✅ 记录用户输入的验证码
const newPassword = ref("");  // ✅ 记录用户输入的新密码
const step = ref(1);  // ✅ 记录当前步骤 (1: 发送验证码, 2: 输入验证码和新密码)
const message = ref("");  // ✅ 提示信息

// ✅ 发送验证码到用户邮箱
const sendVerificationCode = async () => {
  try {
    const response = await axios.post("http://localhost:8000/user/user_verification/", {email: email.value});
    message.value = response.data.message;
    step.value = 2;  // ✅ 进入下一步
  } catch (error) {
    message.value = "Failed to send verification code.";
  }
};

// ✅ 验证验证码 + 重置密码
const verifyAndResetPassword = async () => {
  try {
    const response = await axios.post("http://localhost:8000/user/verify_and_reset_password/", {
      email: email.value,  // ✅ 直接使用用户输入的 email
      code: verificationCode.value,
      new_password: newPassword.value,
    });

    message.value = response.data.message;
    step.value = 3;  // ✅ 完成
  } catch (error) {
    message.value = "Failed to reset password.";
  }
};
</script>

<template>
  <div class="reset-container">
    <h2>🔑 Reset Password</h2>

    <div v-if="step === 1">
      <p>Enter your email to receive a verification code:</p>
      <input type="email" v-model="email" placeholder="📧 Enter your email"/>
      <button @click="sendVerificationCode">📩 Send Code</button>
    </div>

    <div v-if="step === 2">
      <p>Enter the verification code sent to your email:</p>
      <input type="text" v-model="verificationCode" placeholder="🔢 Enter code"/>

      <p>Enter your new password:</p>
      <input type="password" v-model="newPassword" placeholder="🔒 Enter new password"/>

      <button @click="verifyAndResetPassword">✅ Reset Password</button>
    </div>

    <div v-if="step === 3">
      <p>🎉 Password reset successful! You can now login.</p>
    </div>

    <p class="message">{{ message }}</p>
  </div>
</template>

<style scoped>
.reset-container {
  max-width: 400px;
  margin: auto;
  text-align: center;
  background: #f8f8f8;
  padding: 20px;
  border-radius: 10px;
}

input {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border-radius: 5px;
}

button {
  width: 100%;
  padding: 10px;
  background: #007BFF;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background: #0056b3;
}

.message {
  margin-top: 10px;
  color: red;
}
</style>
