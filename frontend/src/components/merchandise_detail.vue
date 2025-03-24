<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

axios.defaults.withCredentials = true;

const route = useRoute();
const router = useRouter();
const merchandise = ref(null);
const isLoading = ref(true);
const isAuthenticated = ref(localStorage.getItem('isAuthenticated') === 'true');

// ✅ 获取商品详情
const fetchMerchandiseDetail = async () => {
  try {
    const response = await axios.get(`${import.meta.env.VITE_API_URL}/merchandise/merchandiseDetail/${route.params.id}/`);
    merchandise.value = response.data;
    isLoading.value = false;
  } catch (error) {
    console.error("Error fetching merchandise details:", error);
    isLoading.value = false;
  }
};

// ✅ 处理收藏（Like/Unlike）
const toggleLike = async () => {
  if (!isAuthenticated.value) {
    alert("⚠️ You need to login first! Redirecting to login page...");
    router.push("/login");
    return;
  }

  try {
    const response = await axios.post(
      `${import.meta.env.VITE_API_URL}/merchandise/${merchandise.value.id}/like/`,
      {},
      { withCredentials: true }
    );
    merchandise.value.liked = response.data.liked;
  } catch (error) {
    console.error("Error toggling like:", error);
  }
};

// ✅ 发送消息（打开聊天）
const startChat = async () => {
  if (!isAuthenticated.value) {
    alert("⚠️ You need to login first! Redirecting to login page...");
    router.push("/login");
    return;
  }

  try {
    const response = await axios.get(`${import.meta.env.VITE_API_URL}/user/get_by_username/`, {
      params: { username: merchandise.value.seller.username },
    });

    const seller = response.data;
    if (!seller || !seller.id) {
      console.error("User ID not found for:", merchandise.value.seller.username);
      return;
    }

    router.push({
      name: "MessageDetail",
      params: { id: seller.id, username: merchandise.value.seller.username },
    });

  } catch (error) {
    console.error("Error fetching user ID:", error);
  }
};

onMounted(fetchMerchandiseDetail);
</script>


<template>
  <div class="merchandise-detail-container" v-if="!isLoading && merchandise">
    <div class="merchandise-header">
      <h2>🛍️ {{ merchandise.name }}</h2>
    </div>

    <div class="merchandise-content">
      <!-- ✅ 左侧：商品图片 + 商品信息 -->
      <div class="left-section">
        <!-- 商品图片 -->
        <div class="image-gallery">
          <img
            v-for="pic in merchandise.pictures"
            :key="pic.id"
            :src="pic.picture"
            alt="Merchandise Image"
          />
        </div>

        <!-- 商品信息 -->
        <div class="product-info">
          <h3 class="title">{{ merchandise.name }}</h3>
          <p class="price">
            💰 <span class="price-amount">{{ merchandise.price }}</span>
            <span v-if="merchandise.is_negotiated" class="negotiable-tag">💬 Negotiable</span>
            <span v-if="merchandise.is_donation" class="donation-tag">🎁 Donation</span>
          </p>
          <p class="description">{{ merchandise.description }}</p>

          <!-- ❤️ 收藏按钮 -->
          <button class="like-btn" @click="toggleLike">
            <i :class="merchandise.liked ? 'bi bi-heart-fill liked' : 'bi bi-heart'"></i>
            <span v-if="merchandise.liked">Liked</span>
            <span v-else>Like</span>
          </button>
        </div>
      </div>

      <!-- ✅ 右侧：用户信息 -->
      <div class="right-section">
        <div class="seller-info">
          <h3>👤 Seller Info</h3>
          <div class="seller-profile">
            <img :src="merchandise.seller.avatar" alt="Seller Avatar" class="avatar" />
            <p class="username">{{ merchandise.seller.username }}</p>
            <p class="school-year">🎓 {{ merchandise.seller.school_year }}</p>
            <p class="seller-description">📝 {{ merchandise.seller.description }}</p>
            <p class="email">📧 {{ merchandise.seller.email }}</p>
          </div>
          <button class="chat-btn" @click="startChat">✉️ Chat with Seller</button>
        </div>
      </div>
    </div>
  </div>

  <div v-else-if="isLoading">
    <p class="loading-text">⏳ Loading merchandise details...</p>
  </div>

  <div v-else>
    <p class="error-text">⚠️ Merchandise not found.</p>
  </div>
</template>

<style scoped>
/* ✅ 页面整体 */
.merchandise-detail-container {
  max-width: 1200px;
  margin: 20px auto;
  padding: 20px;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
}

/* ✅ 标题 */
.merchandise-header {
  background: linear-gradient(45deg, #ff7e5f, #feb47b);
  color: white;
  padding: 15px;
  border-radius: 12px;
  text-align: center;
  font-size: 24px;
  font-weight: bold;
}

/* ✅ 商品内容：两列布局 */
.merchandise-content {
  display: flex;
  gap: 25px;
  align-items: flex-start;
  margin-top: 20px;
}

/* ✅ 左侧：商品图片 + 商品信息 */
.left-section {
  width: 65%;
}

/* ✅ 右侧：用户信息 */
.right-section {
  width: 35%;
}

/* ✅ 商品图片 */
.image-gallery {
  display: flex;
  gap: 10px;
  overflow-x: auto;
  padding: 10px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
}

.image-gallery img {
  height: 280px;
  width: auto;
  border-radius: 8px;
  transition: transform 0.3s ease-in-out;
}

.image-gallery img:hover {
  transform: scale(1.08);
}

/* ✅ 商品信息 */
.product-info {
  margin-top: 20px;
  background: #ffffff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
}

.title {
  font-size: 22px;
  font-weight: bold;
  margin-bottom: 10px;
}

.price {
  font-size: 20px;
  font-weight: bold;
  color: #ff5733;
  display: flex;
  align-items: center;
  gap: 8px;
}

.price-amount {
  font-size: 22px;
  font-weight: bold;
  color: #d35400;
}

/* ✅ 议价 & 捐赠标签 */
.negotiable-tag {
  background: #ffeb3b;
  color: #333;
  font-size: 14px;
  padding: 6px 12px;
  border-radius: 5px;
}

.donation-tag {
  background: #4CAF50;
  color: white;
  font-size: 14px;
  padding: 6px 12px;
  border-radius: 5px;
}

/* ✅ 卖家信息 */
.seller-info {
  padding: 20px;
  background: #ffffff;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
  width: 100%;
}

.seller-profile {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 15px;
}

.avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid #ddd;
}

.username {
  font-size: 20px;
  font-weight: bold;
  margin-top: 8px;
}

.school-year,
.seller-description,
.email {
  font-size: 16px;
  color: #555;
  margin-top: 8px;
}

/* ✅ 按钮样式 */
.chat-btn,
.like-btn {
  display: block;
  width: 100%;
  margin-top: 15px;
  padding: 12px 20px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: transform 0.2s ease-in-out;
}

.chat-btn {
  background: #007BFF;
  color: white;
}

.chat-btn:hover {
  transform: scale(1.05);
  background: #0056b3;
}

.like-btn {
  background: #ff3b3b;
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
}

.like-btn:hover {
  transform: scale(1.05);
  background: #d32f2f;
}

.like-btn i {
  font-size: 18px;
}

.liked {
  color: white;
}

/* ✅ 加载 & 错误消息 */
.loading-text,
.error-text {
  font-size: 18px;
  color: #888;
  text-align: center;
  margin-top: 20px;
}
</style>

