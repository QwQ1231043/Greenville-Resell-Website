<template>
  <div class="chat-list-container">
    <h2>💬 Messages</h2>

    <!-- 🔍 搜索区域 -->
    <div class="search-container">
      <input v-model="searchQuery" @input="searchUsers" placeholder="🔍 Search by username or email..." class="search-box" />

      <div v-if="searchResults.length > 0" class="search-results">
        <div v-for="user in searchResults" :key="user.id" class="search-item">
          <img :src="user.avatar" alt="Avatar" class="chat-avatar" />
          <div @click="openChat(user.id, user.username)">
            <h3>{{ user.username }}</h3>
            <p class="user-email">{{ user.email }}</p>
          </div>
          <button class="start-chat-btn" @click="startChat(user.username)">✉️ Chat</button>
        </div>
      </div>
    </div>

    <!-- 📩 最近聊天列表 -->
    <div class="chat-list">
      <h3>📩 Recent Chats</h3>
      <div v-for="chat in chats" :key="chat.id" class="chat-item" @click="openChat(chat.id, chat.username)">
        <img :src="chat.avatar" alt="Avatar" class="chat-avatar" />
        <div class="chat-info">
          <h3>{{ chat.username }}</h3>
          <p class="latest-message">{{ chat.latest_message }}</p>
        </div>
        <div class="chat-meta">
          <span class="timestamp">{{ formatTime(chat.timestamp) }}</span>
          <span v-if="chat.unread > 0" class="unread-badge">{{ chat.unread }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const chats = ref([]);
const searchQuery = ref("");
const searchResults = ref([]);
const fetchInterval = ref(null);

// ✅ 获取聊天列表
const fetchChats = async () => {
  try {
    const response = await axios.get(`${import.meta.env.VITE_API_URL}/messages/get_recent_chats/`);
    chats.value = response.data;

  } catch (error) {
    console.error("Error fetching chat list:", error);
  }
};

// ✅ 进入聊天详情页
const openChat = (userId, username) => {
  router.push({ name: "MessageDetail", params: { id: userId, username: username } });
};

// ✅ 搜索用户
const searchUsers = async () => {
  if (searchQuery.value.length < 2) {
    searchResults.value = [];

    return;
  }

  try {
    const response = await axios.get(`${import.meta.env.VITE_API_URL}/user/search/?query=${searchQuery.value}`);
    searchResults.value = response.data;
  } catch (error) {
    console.error("Error searching users:", error);
  }
};

const startChat = async (receiverUsername) => {
  try {
    const response = await axios.get(`${import.meta.env.VITE_API_URL}/user/get_current_user/`, {
      params: { username: receiverUsername },
    });

    const user = response.data;
    if (!user || !user.id) {
      console.error("User ID not found for:", receiverUsername);
      return;
    }

    router.push({
      name: "MessageDetail",
      params: {id: user.id, username: receiverUsername},
    });

  } catch (error) {
    console.error("Error fetching user ID:", error);
  }
};

// ✅ 格式化时间
const formatTime = (timestamp) => {
  const date = new Date(timestamp);
  return date.toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'});
};

// ✅ 组件挂载：每 5 秒刷新一次
onMounted(() => {
  fetchChats();
  fetchInterval.value = setInterval(fetchChats, 50000);
});

onUnmounted(() => {
  if (fetchInterval.value) {
    clearInterval(fetchInterval.value);
    fetchInterval.value = null;
  }
});
</script>

<style scoped>
/* ✅ 整体容器 */
.chat-list-container {
  width: 100%;
  max-width: 600px;
  margin: 20px auto;
  padding: 15px;
  background: white;
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
}

/* 🔍 搜索区域 */
.search-container {
  margin-bottom: 15px;
}

.search-box {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

/* 🔽 搜索结果 */
.search-results {
  background: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
  margin-top: 5px;
}

.search-item {
  display: flex;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #ddd;
  cursor: pointer;
}

.search-item:hover {
  background: #f1f1f1;
}

.chat-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 15px;
}

/* 🔹 发送消息按钮 */
.start-chat-btn {
  margin-left: auto;
  background: #4CAF50;
  color: white;
  padding: 8px 12px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.start-chat-btn:hover {
  background: #45a049;
}

/* 🔹 聊天列表 */
.chat-list {
  margin-top: 10px;
  padding: 10px;
  border-top: 1px solid #ddd;
}

.chat-item {
  display: flex;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #ddd;
  cursor: pointer;
  transition: background 0.2s;
}

.chat-item:hover {
  background: #f8f8f8;
}

.chat-info {
  flex-grow: 1;
}

.latest-message {
  font-size: 14px;
  color: #666;
  margin-top: 3px;
}

.chat-meta {
  text-align: right;
}

.timestamp {
  font-size: 12px;
  color: #aaa;
}

.unread-badge {
  display: inline-block;
  background: red;
  color: white;
  padding: 5px 10px;
  border-radius: 20px;
  font-size: 12px;
  margin-left: 5px;
}
</style>
