<template>
  <div id="app">
    <!-- 🔹 Top Bar -->


    <!-- 🔹 Top Bar -->
    <div class="top-bar">
      <div class="logo">
        <img src="" alt="Greenville University" class="logo-img" />
      </div>
      <div class="nav-links">
        <a href="#" style="padding-right: 20px">About Us</a>
        <i class="bi bi-info-circle" style="padding-right: 50px"></i>
      </div>
    </div>
    <!-- 🔹 Main Content Container -->
    <div class="main-container">
      <!-- 🔹 Sidebar -->
      <div class="sidebar">
        <!-- 用户信息（已登录时显示） -->
        <div v-if="isAuthenticated" class="user-profile">
          <img :src="user.avatar || defaultAvatar" alt="User Avatar" class="user-avatar" />
          <p class="username">{{ user.username }}</p>
        </div>

        <ul>
          <li>
            <router-link to="/home">
              <i class="bi bi-house-door-fill"></i> Home
            </router-link>
          </li>

          <!-- 未登录时显示 Login 和 Register -->
          <li v-if="!isAuthenticated">
            <router-link to="/login">
              <i class="bi bi-box-arrow-in-right"></i> Login
            </router-link>
          </li>
          <li v-if="!isAuthenticated">
            <router-link to="/register">
              <i class="bi bi-pencil-square"></i> Register
            </router-link>
          </li>
      <li v-if="!isAuthenticated">
            <router-link to="/reset_password">
              <i class="bi bi-pencil-square"></i> Find Password
            </router-link>
          </li>
          <!-- 登录后显示功能 -->
          <li v-if="isAuthenticated">
            <router-link to="/donation">
              <i class="bi bi-heart-fill"></i> Donation
            </router-link>
          </li>
          <li v-if="isAuthenticated">
            <router-link to="/post-merchandise">
              <i class="bi bi-plus-circle-fill"></i> Post Merchandise
            </router-link>
          </li>
          <li v-if="isAuthenticated">
            <router-link to="/like">
              <i class="bi bi-star-fill"></i> Favorite
            </router-link>
          </li>
          <li v-if="isAuthenticated">
            <router-link to="/my_merchandise">
              <i class="bi bi-box-seam"></i> My Merchandise
            </router-link>
          </li>
          <li v-if="isAuthenticated">
            <router-link to="/message">
              <i class="bi bi-envelope-fill"></i> Messages
            </router-link>
          </li>
          <li v-if="isAuthenticated">
            <router-link to="/setting">
              <i class="bi bi-gear-fill"></i> Settings
            </router-link>
          </li>

          <!-- 退出登录 -->
          <li v-if="isAuthenticated">
            <a href="#" @click.prevent="logout">
              <i class="bi bi-box-arrow-left"></i> Logout
            </a>
          </li>
        </ul>
      </div>

      <!-- 🔹 Content Area -->
      <div class="content">
        <router-view @login-success="updateSidebar" />
      </div>
    </div>

    <!-- 🔹 Footer -->
    <div class="footer">
      <p>&copy; 2025 Greenville University Resell</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { ref, watchEffect, onMounted } from 'vue';
import { useRouter } from 'vue-router';

axios.defaults.withCredentials = true;

export default {
  name: 'MainPageTemplate',
  setup() {
    const isAuthenticated = ref(localStorage.getItem('isAuthenticated') === 'true');
    const user = ref({ username: '', avatar: '' });
    const router = useRouter();
    const defaultAvatar = `${import.meta.env.VITE_API_URL}/media/avatars/default.jpeg`; // 默认头像

    // ✅ 获取当前用户信息
    const fetchUser = async () => {
      if (!isAuthenticated.value) return;
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/user/get_current_user/`);
        user.value = response.data;
      } catch (error) {
        console.error("Error fetching user data:", error);
      }
    };

    // ✅ 退出登录
    const logout = async () => {
      try {
        await axios.post(`${import.meta.env.VITE_API_URL}/user/logout/`, {}, { withCredentials: true });

        // ✅ 清除本地存储
        localStorage.removeItem('isAuthenticated');
        localStorage.removeItem('user');
        isAuthenticated.value = false;
        user.value = { username: '', avatar: '' };

        // ✅ 跳转到登录页面
        router.push('/login');
      } catch (error) {
        console.error("❌ Logout error:", error);
      }
    };

    // ✅ 登录后更新 Sidebar
    const updateSidebar = () => {
      isAuthenticated.value = localStorage.getItem('isAuthenticated') === 'true';
      fetchUser();
    };

    // ✅ 监听 `localStorage` 变化，自动更新 UI
    watchEffect(() => {
      isAuthenticated.value = localStorage.getItem('isAuthenticated') === 'true';
    });

    onMounted(fetchUser);

    return { isAuthenticated, user, defaultAvatar, logout, updateSidebar };
  }
};
</script>

<style scoped>
/* Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

#app {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: linear-gradient(to bottom, #f0f2f5, #e5e7eb);
  font-family: 'Roboto', sans-serif;
}
/* 🔹 顶部导航栏 */
.top-bar {
  background: #2E2E2E;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 35px 30px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.logo-img {
  height: 40px;
}

.nav-links {
  display: flex;
  align-items: center;
}

.nav-links a {
  color: white;
  margin-left: 20px;
  text-decoration: none;
  font-size: 16px;
  font-weight: bold;
}

.nav-links a:hover {
  color: #FF7F2A;
}

.nav-links i {
  color: white;
  font-size: 22px;
  margin-left: 15px;
  cursor: pointer;
}

.nav-links i:hover {
  color: #FF7F2A;
}

/* 🔹 Main Container */
.main-container {
  display: flex;
  flex: 1;
}

/* 🔹 Sidebar */
.sidebar {
  width: 260px;
  background: #2c3e50;
  padding: 25px;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  border-top-right-radius: 12px;
  border-bottom-right-radius: 12px;
  color: white;
}

/* 🔹 用户信息 */
.user-profile {
  text-align: center;
  margin-bottom: 20px;
}

.user-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #f1c40f;
}

.username {
  margin-top: 8px;
  font-size: 18px;
  font-weight: bold;
  color: #f1c40f;
}

/* 🔹 菜单列表 */
.sidebar ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar ul li {
  margin: 15px 0;
  font-size: 18px;
}

.sidebar ul li a {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: #ecf0f1;
  font-weight: 500;
  transition: transform 0.2s ease, color 0.2s ease;
}

.sidebar ul li a i {
  margin-right: 12px;
  font-size: 22px;
}

.sidebar ul li a:hover {
  transform: scale(1.05);
  color: #f1c40f;
}

/* 🔹 Content */
.content {
  flex: 1;
  padding: 40px;
  background: #eceff1;
  border-radius: 12px;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
}

/* 🔹 Footer */
.footer {
  background: #FFA07A;
  color: white;
  text-align: center;
  padding: 15px;
  font-weight: 600;
  border-top: 2px solid #FFDAB9;
}
</style>
