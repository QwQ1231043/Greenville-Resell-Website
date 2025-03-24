<template>
  <div class="post-merchandise">
    <h2>📦 Post Your Merchandise</h2>

    <!-- 成功 & 失败消息 -->
    <div class="messages">
      <transition name="fade">
        <div v-if="successMessage" class="success">{{ successMessage }}</div>
      </transition>
      <transition name="fade">
        <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
      </transition>
    </div>

    <form @submit.prevent="submitPost">
      <!-- 🔹 标题 + 描述 -->
      <div class="form-row">
        <div class="form-group">
          <label for="title">📌 Title</label>
          <input id="title" v-model="title" type="text" placeholder="Enter title" required />
        </div>

        <div class="form-group">
          <label for="description">📝 Description</label>
          <textarea id="description" v-model="description" placeholder="Enter description" required></textarea>
        </div>
      </div>

      <!-- 🔹 价格 + 议价 + 捐赠 -->
      <div class="form-row">
        <div class="form-group">
          <label for="price">💰 Price</label>
          <input id="price" v-model.number="price" type="number" min="0" placeholder="Enter price" :disabled="is_donation" required />
        </div>

        <div class="checkbox-group">
          <input type="checkbox" id="negotiable" v-model="is_negotiated" class="custom-checkbox" />
          <label for="negotiable">💬 Price Negotiable</label>
        </div>

        <div class="checkbox-group">
          <input type="checkbox" id="donation" v-model="is_donation" @change="handleDonationChange" class="custom-checkbox" />
          <label for="donation">🎁 Offer as Donation (Free)</label>
        </div>
      </div>

      <!-- 🔹 拖拽上传区域 -->
      <div class="form-group">
        <label>📷 Upload Images (up to 5):</label>
        <div class="drop-zone" @dragover.prevent @dragenter.prevent @drop="handleDrop" @click="triggerFileInput">
          <p v-if="selectedImages.length === 0">Drag & Drop or Click to Select Images</p>
          <p v-else>Drop more images to upload</p>
        </div>
        <input id="images" type="file" multiple accept="image/*" ref="fileInput" @change="onFileChange" hidden />
      </div>

      <!-- 🔹 图片预览 -->
      <div v-if="selectedImages.length > 0" class="image-preview">
        <div v-for="(image, index) in selectedImages" :key="index" class="image-item">
          <img :src="image.preview" alt="Preview" />
          <button class="remove-btn" @click="removeImage(index)">❌</button>
        </div>
      </div>

      <!-- 🔹 提交按钮 -->
      <button type="submit" class="submit-btn">🚀 Post Merchandise</button>
    </form>
  </div>
</template>

<script>
import axios from "axios";
import { ref } from "vue";
import { useRouter } from "vue-router";

export default {
  name: "PostMerchandise",
  setup() {
    const router = useRouter();
    const title = ref("");
    const description = ref("");
    const price = ref(null);
    const is_negotiated = ref(false);
    const is_donation = ref(false);
    const selectedImages = ref([]);
    const successMessage = ref("");
    const errorMessage = ref("");

    // ✅ 处理文件上传
    const onFileChange = (event) => {
      addFiles(event.target.files);
    };

    // ✅ 处理拖拽上传
    const handleDrop = (event) => {
      event.preventDefault();
      addFiles(event.dataTransfer.files);
    };

    // ✅ 触发文件选择框
    const triggerFileInput = () => {
      document.getElementById("images").click();
    };

    // ✅ 处理文件添加
    const addFiles = (files) => {
      const fileArray = Array.from(files);
      if (selectedImages.value.length + fileArray.length > 5) {
        errorMessage.value = "⚠️ You can upload up to 5 images only.";
        return;
      }

      fileArray.forEach((file) => {
        if (file.type.startsWith("image/")) {
          const reader = new FileReader();
          reader.onload = (e) => {
            selectedImages.value.push({ file, preview: e.target.result });
          };
          reader.readAsDataURL(file);
        }
      });

      errorMessage.value = "";
    };

    // ✅ 删除图片
    const removeImage = (index) => {
      selectedImages.value.splice(index, 1);
    };

    // ✅ 处理捐赠选项
    const handleDonationChange = () => {
      if (is_donation.value) {
        price.value = 0;
      }
    };

    // ✅ 提交商品信息到 API
    const submitPost = async () => {
      successMessage.value = "";
      errorMessage.value = "";

      try {
        const formData = new FormData();
        formData.append("name", title.value);
        formData.append("description", description.value);
        formData.append("price", price.value !== null ? price.value : "");
        formData.append("is_negotiated", is_negotiated.value ? "true" : "false");
        formData.append("is_donation", is_donation.value ? "true" : "false");

        selectedImages.value.forEach((imageObj) => {
          formData.append("pictures", imageObj.file);
        });

        await axios.post(`${import.meta.env.VITE_API_URL}/merchandise/`, formData, {
          headers: { "Content-Type": "multipart/form-data" },
          withCredentials: true,
        });

        successMessage.value = "🎉 Item posted successfully!";
        setTimeout(() => {
          router.push("/home"); // ✅ 成功后跳转回主页
        }, 2000);
      } catch (error) {
        errorMessage.value = "❌ Failed to post item. Please try again.";
        console.error("Error posting merchandise:", error);
      }
    };

    return {
      title,
      description,
      price,
      is_negotiated,
      is_donation,
      selectedImages,
      successMessage,
      errorMessage,
      onFileChange,
      handleDrop,
      triggerFileInput,
      removeImage,
      handleDonationChange,
      submitPost, // ✅ 确保 submitPost() 方法存在
    };
  },
};
</script>


<style scoped>
/* ✅ 页面整体优化 */
.post-merchandise {
  max-width: 900px;
  margin: 20px auto;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

/* ✅ 表单行 */
.form-row {
  display: flex;
  gap: 20px;
  margin-bottom: 15px;
}

/* ✅ 输入框优化 */
.form-group {
  flex: 1;
}

input,
textarea {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 5px;
  transition: all 0.2s ease-in-out;
}

input:focus,
textarea:focus {
  border-color: #ff7e5f;
  box-shadow: 0 0 5px rgba(255, 126, 95, 0.5);
}

/* ✅ 勾选框美化 */
.checkbox-group {
  display: flex;
  align-items: center;
  gap: 5px;
}

.custom-checkbox {
  width: 18px;
  height: 18px;
  appearance: none;
  border: 2px solid #ff7e5f;
  border-radius: 5px;
  cursor: pointer;
  position: relative;
}

.custom-checkbox:checked {
  background: #ff7e5f;
}

.custom-checkbox:checked::before {
  content: "✔";
  font-size: 14px;
  color: white;
  position: absolute;
  left: 3px;
  top: 1px;
}

/* ✅ 拖拽上传区域 */
.drop-zone {
  border: 2px dashed #ff7e5f;
  padding: 20px;
  text-align: center;
  border-radius: 8px;
  cursor: pointer;
}

.drop-zone:hover {
  background: rgba(255, 127, 95, 0.1);
}

/* ✅ 统一图片预览大小 & 自动换行 */
.image-preview {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
}

.image-item {
  position: relative;
  width: 100px;
  height: 100px;
  border-radius: 8px;
  overflow: hidden;
}

.image-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.remove-btn {
  position: absolute;
  top: 5px;
  right: 5px;
  background: red;
  color: white;
  border: none;
  cursor: pointer;
}

/* ✅ 提交按钮 */
.submit-btn {
  width: 100%;
  padding: 12px;
  background: #ff7e5f;
  color: white;
  font-size: 18px;
  border-radius: 8px;
}

.submit-btn:hover {
  background: #e65c4f;
}
</style>
