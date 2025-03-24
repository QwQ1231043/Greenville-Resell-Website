<script setup>
import { ref, onMounted, watch } from 'vue';
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router';

axios.defaults.withCredentials = true;

const route = useRoute();
const router = useRouter();
const merchandiseId = route.params.id;

const merchandise = ref({
  name: '',
  description: '',
  price: '',
  is_negotiated: false,
  is_donation: false,
  pictures: [],
});

const selectedImages = ref([]);
const errorMessage = ref('');
const successMessage = ref('');

// ✅ 获取商品详情
const fetchMerchandise = async () => {
  try {
    const response = await axios.get(`${import.meta.env.VITE_API_URL}/merchandise/${merchandiseId}/`);
    merchandise.value = response.data;
  } catch (error) {
    console.error("Error fetching merchandise details:", error);
    errorMessage.value = "⚠️ Failed to load merchandise details.";
  }
};

// ✅ 处理文件上传
const onFileChange = (event) => {
  const files = event.target.files;
  selectedImages.value = [...files];
};

// ✅ 监听 is_donation 变化，强制 price = 0 并禁用价格输入框
watch(() => merchandise.value.is_donation, (newVal) => {
  if (newVal) {
    merchandise.value.price = 0;
  }
});

// ✅ 提交修改
const updateMerchandise = async () => {
  const formData = new FormData();
  formData.append("name", merchandise.value.name);
  formData.append("description", merchandise.value.description);
  formData.append("price", merchandise.value.price);
  formData.append("is_negotiated", merchandise.value.is_negotiated);
  formData.append("is_donation", merchandise.value.is_donation);

  selectedImages.value.forEach(file => {
    formData.append("pictures", file);
  });

  try {
    await axios.put(
      `${import.meta.env.VITE_API_URL}/merchandise/${merchandiseId}/`,
      formData,
      { headers: { 'Content-Type': 'multipart/form-data' } }
    );

    successMessage.value = "✅ Merchandise updated successfully!";
    setTimeout(() => router.push('/my_merchandise'), 1500);
  } catch (error) {
    console.error("Error updating merchandise:", error);
    errorMessage.value = "❌ Failed to update merchandise.";
  }
};

// 组件挂载时获取商品数据
onMounted(fetchMerchandise);
</script>

<template>
  <div class="edit-container">
    <h2>✏️ Edit Merchandise</h2>

    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    <div v-if="successMessage" class="success-message">{{ successMessage }}</div>

    <form @submit.prevent="updateMerchandise" class="edit-form">
      <label>📌 Name:</label>
      <input type="text" v-model="merchandise.name" required/>

      <label>📝 Description:</label>
      <textarea v-model="merchandise.description" required></textarea>

      <label>💰 Price:</label>
      <input type="number" v-model="merchandise.price" min="0" :disabled="merchandise.is_donation" required/>

      <div class="checkbox-group">
        <input type="checkbox" id="negotiable" v-model="merchandise.is_negotiated" :disabled="merchandise.is_donation"/>
        <label for="negotiable">💬 Price Negotiable</label>
      </div>

      <div class="checkbox-group">
        <input type="checkbox" id="donation" v-model="merchandise.is_donation"/>
        <label for="donation">🎁 Offer as Donation (Free)</label>
      </div>

      <label>📷 Upload New Images:</label>
      <input type="file" multiple accept="image/*" @change="onFileChange"/>

      <button type="submit" class="save-btn">💾 Save Changes</button>
    </form>
  </div>
</template>

<style scoped>
.edit-container {
  max-width: 500px;
  margin: 30px auto;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
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

.edit-form {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

input, textarea {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.checkbox-group {
  display: flex;
  align-items: center;
  gap: 5px;
}

.save-btn {
  padding: 10px;
  background: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
  font-size: 16px;
  border-radius: 5px;
}

.save-btn:hover {
  background: #388E3C;
}

input:disabled {
  background: #f0f0f0;
  cursor: not-allowed;
}
</style>
