<template>
  <div class="settings-container">
    <!-- 🔹 左侧: 用户编辑表单 -->
    <div class="settings">
      <h2>⚙️ User Settings</h2>

      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
      <div v-if="successMessage" class="success-message">{{ successMessage }}</div>

      <form @submit.prevent="updateProfile" class="settings-form">
        <!-- 头像上传 -->
        <div class="avatar-container">
          <img :src="user.avatar || defaultAvatar" alt="User Avatar" class="avatar" />
          <input type="file" accept="image/*" @change="handleFileUpload" class="upload-btn" />
        </div>

        <!-- 用户名 -->
        <label>👤 Username:</label>
        <input type="text" v-model="user.username" required />

        <!-- 学年 -->
        <label>🏫 School Year:</label>
        <select v-model="user.school_year">
          <option value="Freshmen">Freshmen</option>
          <option value="Sophomore">Sophomore</option>
          <option value="Junior">Junior</option>
          <option value="Senior">Senior</option>
        </select>

        <!-- 个人简介 -->
        <label>📝 Description:</label>
        <textarea v-model="user.description"></textarea>

        <!-- 提交按钮 -->
        <button type="submit" class="save-btn">💾 Save Changes</button>
      </form>
    </div>

    <!-- 🔹 右侧: 个人名片 -->
    <div class="profile-card">
      <h3>📌 Profile Overview</h3>
      <div class="profile-header">
        <img :src="user.avatar || defaultAvatar" alt="User Avatar" class="profile-avatar" />
      </div>
      <div class="profile-info">
        <p><strong>👤 Username:</strong> <span>{{ user.username }}</span></p>
        <p><strong>📧 Email:</strong> <span>{{ user.email }}</span></p>
        <p><strong>🏫 School Year:</strong> <span>{{ user.school_year }}</span></p>
        <p><strong>📝 Description:</strong> <span>{{ user.description || "No description provided." }}</span></p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

axios.defaults.withCredentials = true;

const user = ref({
  username: '',
  email: '',
  school_year: '',
  description: '',
  avatar: ''
});

const defaultAvatar = `${import.meta.env.VITE_API_URL}/media/avatars/default.jpeg/`; // 默认头像路径
const selectedAvatar = ref(null);
const errorMessage = ref('');
const successMessage = ref('');

// ✅ 获取当前用户信息
const fetchUser = async () => {
  try {
    const response = await axios.get(`${import.meta.env.VITE_API_URL}/user/get_current_user/`);
    user.value = response.data;
  } catch (error) {
    console.error("Error fetching user data:", error);
    errorMessage.value = "⚠️ Failed to load user data.";
  }
};

// ✅ 处理头像上传
const handleFileUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    selectedAvatar.value = file;
    const reader = new FileReader();
    reader.onload = (e) => {
      user.value.avatar = e.target.result; // 预览头像
    };
    reader.readAsDataURL(file);
  }
};

// ✅ 提交修改
const updateProfile = async () => {
  const formData = new FormData();
  formData.append("username", user.value.username);
  formData.append("school_year", user.value.school_year);
  formData.append("description", user.value.description);

  if (selectedAvatar.value) {
    formData.append("avatar", selectedAvatar.value);
  }

  try {
    await axios.put(`${import.meta.env.VITE_API_URL}/user/update_user/`, formData, {
      headers: {'Content-Type': 'multipart/form-data'}
    });

    successMessage.value = "✅ Profile updated successfully!";
    await fetchUser(); // 更新 UI
    user.value.avatar = `${user.value.avatar}?t=${new Date().getTime()}`;
  } catch (error) {
    console.error("Error updating profile:", error);
    errorMessage.value = error.response?.data?.error || "❌ Failed to update profile.";
  }
};

onMounted(fetchUser);
</script>

<style scoped>
/* ✅ 页面布局 */
.settings-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 30px;
  max-width: 1000px;
  margin: 40px auto;
}

/* ✅ 左侧: 设置表单 */
.settings {
  flex: 1;
  min-width: 450px;
  padding: 25px;
  background: white;
  border-radius: 10px;
  box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
}

.error-message, .success-message {
  text-align: center;
  margin-bottom: 10px;
  font-weight: bold;
}

.success-message {
  color: green;
}

.error-message {
  color: red;
}

.settings-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

input, select, textarea {
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.save-btn {
  padding: 12px;
  background: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  border-radius: 8px;
}

.avatar-container {
  text-align: center;
}

.avatar {
  width: 110px;
  height: 110px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 10px;
}

/* ✅ 右侧: 个人名片 */
.profile-card {
  flex: 0.4;
  min-width: 400px;
  padding: 20px;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.15);
  text-align: center;
  transition: transform 0.2s ease-in-out;
}

.profile-card:hover {
  transform: scale(1.03);
}

.profile-header {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.profile-avatar {
  width: 140px;
  height: 140px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid #4CAF50;
  margin-bottom: 15px;
}

.profile-info p {
  margin: 10px 0;
  font-size: 16px;
  font-weight: bold;
  color: #444;
}

.profile-info span {
  font-weight: normal;
  color: #666;
  font-size: 15px;
}

/* ✅ 响应式设计 */
@media (max-width: 768px) {
  .settings-container {
    flex-direction: column;
    align-items: center;
  }

  .profile-card {
    width: 100%;
    max-width: 450px;
  }
}
</style>
