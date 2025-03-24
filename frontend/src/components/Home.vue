<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
axios.defaults.withCredentials = true;

const router = useRouter();
const merchandise = ref([]);
const searchQuery=ref("");
// ✅ 处理收藏（Like/Unlike）
const toggleLike = async (item) => {
  const isAuthenticated = localStorage.getItem("isAuthenticated") === "true"; // ✅ 检查是否已登录

  if (!isAuthenticated) {
    alert("⚠️ You need to login first! Redirecting to login page...");
    router.push("/login"); // ✅ 跳转到登录页面
    return;
  }

  try {
    const response = await axios.post(
      `${import.meta.env.VITE_API_URL}/merchandise/${item.id}/like/`,
      {},
      { withCredentials: true }
    );

    // ✅ 更新前端 `liked` 状态
    item.liked = response.data.liked;
  } catch (error) {
    console.error("Error toggling like:", error.response?.data || error);
  }
};
const goToDetail = (id) => {
  router.push({ name: "MerchandiseDetail", params: { id:id.toString() } });
};
// ✅ 获取所有商品
const fetchMerchandise = async () => {
  try {
    const response = await axios.get(`${import.meta.env.VITE_API_URL}/merchandise/`);
    merchandise.value = response.data.map(item => ({
      ...item,
      pictures: item.pictures || [],
      liked: item.liked || false
    }));
  } catch (error) {
    console.error("Error fetching merchandise:", error);
  }
};

onMounted(fetchMerchandise);

// ✅ 开启聊天
const startChat = async (sellerUsername) => {
    const isAuthenticated = localStorage.getItem("isAuthenticated") === "true"; // ✅ 检查是否已登录

  if (!isAuthenticated) {
    alert("⚠️ You need to login first! Redirecting to login page...");
    router.push("/login"); // ✅ 跳转到登录页面
    return;
  }

  try {
    const response = await axios.get(`${import.meta.env.VITE_API_URL}/user/get_by_username/`, {
      params: { username: sellerUsername },
    });

    const seller = response.data;
    if (!seller || !seller.id) {
      console.error("User ID not found for:", sellerUsername);
      return;
    }

    router.push({
      name: "MessageDetail",
      params: { id: seller.id, username: sellerUsername },
    });

  } catch (error) {
    console.error("Error fetching user ID:", error);
  }
};
// ✅ 搜索商品
const searchMerchandise = async () => {
  if (searchQuery.value.length < 2) {
    fetchMerchandise(); // 如果输入少于 2 个字符，返回所有商品
    return;
  }

  try {
    const response = await axios.get(`${import.meta.env.VITE_API_URL}/merchandise/search/?query=${searchQuery.value}`);
    merchandise.value = response.data;
  } catch (error) {
    console.error("Error searching merchandise:", error);
  }
};

onMounted(fetchMerchandise);
</script>

<template>
    <!-- 🔍 搜索栏 -->
    <div class="search-container">
      <input v-model="searchQuery" @input="searchMerchandise" placeholder="🔍 Search for merchandise..." class="search-box" />
    </div>
  <div class="merchandise-container">
    <h2>🛍️ Available Merchandise</h2>

    <div v-if="merchandise.length > 0" class="merchandise-grid">
      <div v-for="item in merchandise" :key="item.id" class="merchandise-card" @click="goToDetail(item.id)">

        <!-- 📷 商品图片 -->
        <div class="image-container">
          <img v-if="item.pictures.length > 0" :src="item.pictures[0].picture" alt="Merchandise Image"/>


        </div>

        <!-- 📜 商品信息 -->
        <div class="info">
                    <!-- ❤️ Like 按钮 -->
          <button class="like-btn" @click.stop="toggleLike(item)">
            <i :class="item.liked ? 'bi bi-heart-fill liked' : 'bi bi-heart'"></i>
          </button>
          <h3 class="title">{{ item.name }}</h3>

          <!-- 💰 价格 + 议价 -->
          <p class="price">
            💰 {{ item.price }}
            <span v-if="item.is_negotiated" class="negotiable-tag">💬 Negotiable</span>
            <span v-if="item.is_donation" class="donation-tag">💬 Donation</span>
          </p>

          <p class="description">{{ item.description }}</p>

          <!-- 👤 用户名 -->
          <p class="user">👤 {{ item.username || "Unknown Seller" }}</p>
          <button class="chat-btn" @click.stop="startChat(item.username)">✉️ Chat</button>
        </div>
      </div>
    </div>

    <div v-else>
      <p>😞 No merchandise available.</p>
    </div>
  </div>
</template>

<style scoped>
/* 🔍 搜索栏 */
.search-container {
  text-align: center;
  margin-bottom: 20px;
}

.search-box {
  width: 100%;
  max-width: 400px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 16px;
}
/* 🎁 赠送标签 */
.donation-tag {
  background: #4CAF50;
  color: white;
  font-size: 14px;
  font-weight: bold;
  padding: 5px 10px;
  border-radius: 5px;
  margin-right: 8px;
}
/* ✅ 页面整体优化 */
.merchandise-container {
  max-width: 1200px;
  margin: 20px auto;
  padding: 20px;
  text-align: center;
}

/* ✅ 网格布局 */
.merchandise-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); /* ✅ 调整列宽 */
  gap: 20px;
  margin-top: 20px;
}

/* ✅ Chat 按钮 */
.chat-btn {
  margin-top: 10px;
  background: #007BFF;
  color: white;
  padding: 8px 12px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  width: 35%;
  font-weight: bold;
  z-index: 2;
}

.chat-btn:hover {
  background: #0056b3;
}
/* ✅ 让整个卡片可点击 */
.merchandise-card {
  background: white;
  border: 2px solid #ff7e5f;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
  position: relative;
  cursor: pointer; /* 变为可点击 */
}

.merchandise-card:hover {
  transform: scale(1.04);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}

/* ✅ 收藏按钮 */
.like-btn {
  position: absolute;
  bottom: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 22px;
  cursor: pointer;
  transition: transform 0.2s ease-in-out;
    z-index: 2;
}

.like-btn .bi-heart {
  color: #aaa;
  transition: color 0.2s ease-in-out;
}

.like-btn .bi-heart-fill {
  color: #ff3b3b; /* ❤️ 变红 */
  transform: scale(1.2);
}

/* ❤️ 动画效果 */
.like-btn:active {
  transform: scale(0.9);
}

/* ✅ 图片容器 */
.image-container {
  width: 100%;
  height: 200px;
  overflow: hidden;
  background: #f8f8f8;
  position: relative;
}

.image-container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: opacity 0.3s ease-in-out;
}

.image-container:hover img {
  opacity: 0.8;
}

/* ✅ 商品信息 */
.info {
  padding: 15px;
  text-align: left;
}

/* ✅ 标题 */
.title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 8px;
}

/* ✅ 价格 + 议价 */
.price {
  font-size: 16px;
  font-weight: bold;
  color: #ff5733;
  display: flex;
  align-items: center;
  gap: 8px;
}

/* ✅ 议价标签 */
.negotiable-tag {
  background: #ffeb3b;
  color: #333;
  font-size: 12px;
  font-weight: bold;
  padding: 4px 8px;
  border-radius: 5px;
}

/* ✅ 描述 */
.description {
  font-size: 14px;
  color: #666;
  height: 40px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* ✅ 用户名 */
.user {
  font-size: 14px;
  color: #555;
  font-style: italic;
}
</style>
