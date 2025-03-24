<template>
  <div class="my-merchandise-container">
    <h2>📦 My Merchandise</h2>

    <div v-if="myMerchandise.length > 0" class="merchandise-grid">
      <div v-for="item in myMerchandise" :key="item.id" class="merchandise-card" @click="goToDetail(item.id)">
        <div class="image-container">
          <img v-if="item.pictures.length > 0" :src="item.pictures[0].picture" alt="Merchandise Image" />
        </div>

        <div class="info">
          <h3 class="title">{{ item.name }}</h3>
          <p class="description">{{ item.description }}</p>
          <p class="price">💰 {{ item.price }}</p>

          <!-- ✅ 永久可见的 Edit 和 Delete 按钮 -->
          <div class="actions">
            <button class="edit-btn" @click.stop="editMerchandise(item.id)">✏️ Edit</button>
            <button class="delete-btn" @click.stop="deleteMerchandise(item.id)">🗑️ Delete</button>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="empty-state">
      <p>😞 You haven't posted any merchandise yet.</p>
      <router-link to="/post-merchandise" class="add-btn">➕ Post New Merchandise</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

axios.defaults.withCredentials = true;

const myMerchandise = ref([]);
const router = useRouter();

const goToDetail = (id) => {
  router.push({ name: "MerchandiseDetail", params: { id:id.toString() } });
};
// ✅ 获取当前用户发布的商品
const fetchMyMerchandise = async () => {
  try {
    const response = await axios.get(`${import.meta.env.VITE_API_URL}/merchandise/my-merchandise/`);
    myMerchandise.value = response.data;
  } catch (error) {
    console.error("Error fetching user merchandise:", error);
  }
};

// ✅ 删除商品
const deleteMerchandise = async (itemId) => {
  if (!confirm("⚠️ Are you sure you want to delete this item?")) return;
  try {
    await axios.delete(`${import.meta.env.VITE_API_URL}/merchandise/${itemId}/`);
    myMerchandise.value = myMerchandise.value.filter(item => item.id !== itemId);
  } catch (error) {
    console.error("Error deleting merchandise:", error);
  }
};

// ✅ 点击商品，进入编辑页面
const editMerchandise = (itemId) => {
  router.push(`/edit-merchandise/${itemId}`);
};

onMounted(fetchMyMerchandise);
</script>

<style scoped>
/* ✅ 页面整体 */
.my-merchandise-container {
  max-width: 1200px;
  margin: 20px auto;
  padding: 20px;
  text-align: center;
  background: #ffffff;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

/* ✅ 网格布局 */
.merchandise-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

/* ✅ 商品卡片 */
.merchandise-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
  position: relative;
  padding-bottom: 15px; /* 增加底部间距，避免按钮贴着卡片边缘 */
  cursor:pointer;
}

.merchandise-card:hover {
  transform: scale(1.03);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}

/* ✅ 商品图片 */
.image-container {
  position: relative;
  width: 100%;
  height: 200px;
  background: #f8f8f8;
}

.image-container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* ✅ 商品信息 */
.info {
  padding: 15px;
  text-align: left;
}

.title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 5px;
}

.price {
  font-size: 16px;
  font-weight: bold;
  color: #ff5733;
}

/* ✅ Edit 和 Delete 按钮 */
.actions {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
  z-index: 2;
}

.edit-btn,
.delete-btn {
  flex: 1;
  padding: 10px 15px;
  border: none;
  color: white;
  cursor: pointer;
  border-radius: 5px;
  font-size: 14px;
  transition: background 0.2s ease-in-out;
  font-weight: bold;
}

.edit-btn {
  background-color: #4CAF50;
  margin-right: 5px;
}

.edit-btn:hover {
  background-color: #388E3C;
}

.delete-btn {
  background-color: #e57373;
  margin-left: 5px;
}

.delete-btn:hover {
  background-color: #d32f2f;
}

/* ✅ 空状态 */
.empty-state {
  margin-top: 40px;
}

.add-btn {
  display: inline-block;
  padding: 10px 20px;
  background: #007BFF;
  color: white;
  font-weight: bold;
  border-radius: 8px;
  text-decoration: none;
  margin-top: 10px;
}

.add-btn:hover {
  background: #0056b3;
}
</style>
