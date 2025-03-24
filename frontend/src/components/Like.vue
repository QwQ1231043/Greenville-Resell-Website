<template>
  <div class="liked-container">
    <h2>❤️ Liked Merchandise</h2>

    <div v-if="likedMerchandise.length > 0" class="merchandise-grid">
      <div v-for="item in likedMerchandise" :key="item.id" class="merchandise-card"@click="goToDetail(item.id)">

        <!-- 📷 商品图片 -->
        <div class="image-container">
          <img v-if="item.pictures.length > 0" :src="item.pictures[0].picture" alt="Merchandise Image" />
        </div>

        <!-- 📜 商品信息 -->
        <div class="info">
          <h3 class="title">{{ item.name }}</h3>

          <!-- 💰 价格 -->
          <p class="price">
            💰 {{ item.price }}
            <span v-if="item.is_negotiated" class="negotiable-tag">💬 Negotiable</span>
          </p>

          <!-- 📜 描述 -->
          <p class="description">{{ item.description }}</p>

          <!-- 👤 卖家 -->
          <p class="user">👤 Seller: {{ item.username }}</p>

          <!-- ❌ 取消收藏按钮 -->
          <button class="cancel-btn" @click.stop="toggleLike(item)">❌ Remove Merchandise from Like List</button>
             <!-- ✉️ Chat 按钮 -->
          <button class="chat-btn" @click.stop="startChat(item.username)">✉️ Chat</button>
        </div>
      </div>
    </div>

    <div v-else>
      <p>😞 No liked merchandise found.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
axios.defaults.withCredentials = true;

const router = useRouter();
const likedMerchandise = ref([]);

// ✅ 进入聊天
const startChat = async (sellerUsername) => {
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
// ✅ 获取收藏的商品
const fetchLikedMerchandise = async () => {
  try {
    const response = await axios.get(`${import.meta.env.VITE_API_URL}/merchandise/get-liked-merchandise/`);
    likedMerchandise.value = response.data.map(item => ({
      ...item,
      pictures: item.pictures || [],
      liked: true  // ✅ 这些商品都是喜欢的
    }));
  } catch (error) {
    console.error("Error fetching liked merchandise:", error);
  }
};

// ✅ 处理取消收藏（Unlike）
const toggleLike = async (item) => {
  const isAuthenticated = localStorage.getItem("isAuthenticated") === "true"; // ✅ 检查是否已登录

  if (!isAuthenticated) {
    alert("⚠️ You need to login first! Redirecting to login page...");
    router.push("/login"); // ✅ 跳转到登录页面
    return;
  }

  try {
    const response = await axios.post(`${import.meta.env.VITE_API_URL}/merchandise/${item.id}/like/`, {}, {
      withCredentials: true,
    });

    // ✅ 取消收藏后，前端 UI 立即移除商品
    if (!response.data.liked) {
      likedMerchandise.value = likedMerchandise.value.filter(m => m.id !== item.id);
    }
  } catch (error) {
    console.error("Error toggling like:", error.response?.data || error);
  }
};

onMounted(fetchLikedMerchandise);

const goToDetail = (id) => {
  router.push({ name: "MerchandiseDetail", params: { id:id.toString() } });
};
</script>

<style scoped>

/* ✅ Chat 按钮 */
.chat-btn {
  margin-top: 10px;
  background: #007BFF;
  color: white;
  padding: 8px 12px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  width: 100%;
  font-weight: bold;
  z-index: 2;
}

.chat-btn:hover {
  background: #0056b3;
}
/* ✅ 页面整体优化 */
.liked-container {
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

/* ✅ 商品卡片 */
.merchandise-card {
  background: white;
  border: 2px solid #ff7e5f; /* ✅ 明显的边框 */
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

/* ✅ 取消收藏按钮 */
.cancel-btn {
  width: 100%;
  background: #ff3b3b;
  color: white;
  font-size: 14px;
  font-weight: bold;
  padding: 8px 10px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s ease-in-out;
  margin-top: 10px;
  z-index: 2;
}

.cancel-btn:hover {
  background: #e63946;
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
