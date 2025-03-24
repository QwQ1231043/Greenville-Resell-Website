<template>
  <div class="chat-container">
    <h2>💬 Chat with {{ receiver.username }}</h2>

    <!-- 消息列表 -->
    <div class="messages" ref="messageContainer">
      <div v-for="msg in messages" :key="msg.id"
           :class="{'sent': msg.sender_id === userId, 'received': msg.sender_id !== userId}">

        <!-- 发送者用户名 -->
        <p class="username">{{ msg.sender_id === userId ? 'You' : receiver.username }}</p>

        <!-- 消息气泡 -->
        <div class="message-bubble">
          <p>{{ msg.message }}</p>
          <span class="timestamp">{{ formatTime(msg.timestamp) }}</span>
        </div>
      </div>
    </div>

    <!-- 输入框 -->
    <div class="input-container">
      <input v-model="newMessage" @keyup.enter="sendMessage" placeholder="Type a message..." />
      <button @click="sendMessage">Send</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const userId = parseInt(localStorage.getItem('userId')); // 当前用户 ID
const receiver = ref({ username: route.params.username }); // 对方的用户名
const messages = ref([]);
const newMessage = ref("");
const messageContainer = ref(null);
let intervalId = null;

// ✅ 格式化时间
const formatTime = (timestamp) => {
  if (!timestamp) return "Unknown time";
  return new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
};

// ✅ 获取聊天记录
const fetchMessages = async () => {
  try {
    const response = await axios.get(`${import.meta.env.VITE_API_URL}/messages/get_chat_messages/${route.params.id}/`);
    messages.value = response.data;
    await nextTick();
    scrollToBottom();
  } catch (error) {
    console.error("Error fetching messages:", error);
  }
};

// ✅ 发送消息
const sendMessage = async () => {
  if (!newMessage.value.trim()) return;

  try {
    const response = await axios.post(`${import.meta.env.VITE_API_URL}/messages/send_message/`, {
      receiver: receiver.value.username,
      message: newMessage.value,
    });

    messages.value.push(response.data);
    newMessage.value = "";

    await nextTick();
    scrollToBottom();
  } catch (error) {
    console.error("Error sending message:", error);
  }
};

// ✅ 让消息窗口自动滚动到底部
const scrollToBottom = () => {
  if (messageContainer.value) {
    messageContainer.value.scrollTop = messageContainer.value.scrollHeight;
  }
};

// ✅ 监听 `visibilitychange`，减少 API 请求
const handleVisibilityChange = () => {
  if (!document.hidden) {
    fetchMessages();
    intervalId = setInterval(fetchMessages, 10000);
  } else {
    clearInterval(intervalId);
  }
};

// ✅ 组件挂载时启动自动刷新
onMounted(() => {
  fetchMessages();
  intervalId = setInterval(fetchMessages, 10000);
  document.addEventListener("visibilitychange", handleVisibilityChange);
});

// ✅ 组件卸载时清除自动刷新
onUnmounted(() => {
  if (intervalId) clearInterval(intervalId);
  document.removeEventListener("visibilitychange", handleVisibilityChange);
});
</script>

<style scoped>
/* ✅ 让聊天框整体更大 */
.chat-container {
  padding: 20px;
  max-width: 900px; /* ✅ 聊天框变宽 */
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  height: 85vh;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
}

/* ✅ 让消息列表占满整个高度 */
.messages {
  flex-grow: 1;
  overflow-y: auto;
  padding: 10px;
  display: flex;
  flex-direction: column;
}

/* ✅ 发送者用户名 */
.username {
  font-size: 12px;
  color: #666;
  margin-bottom: 5px;
  font-weight: bold;
}


/* ✅ 消息气泡优化 */
.message-bubble {
  display: inline-block; /* ✅ 避免 flex 压缩 */
  min-width: 100px; /* ✅ 确保第一行有最小宽度 */
  max-width: 100%; /* ✅ 让消息不会太长 */
  padding: 12px 15px;
  border-radius: 12px;
  word-wrap: break-word;
  word-break: break-word; /* ✅ 避免单词断得太碎 */
  white-space: normal; /* ✅ 允许自然换行 */
  font-size: 15px;
  line-height: 1.4;
}

/* ✅ 发送的消息（右侧） */
.sent {
  align-self: flex-end;
  text-align: right;
}

.sent .message-bubble {
  background: #007BFF;
  color: white;
  border-radius: 12px 12px 0 12px;
}

/* ✅ 接收的消息（左侧） */
.received {
  align-self: flex-start;
  text-align: left;
}

.received .message-bubble {
  background: #E5E5EA;
  color: black;
  border-radius: 12px 12px 12px 0;
}

/* ✅ 时间戳优化 */
.timestamp {
  font-size: 12px;
  color: #555;
  display: block;
  margin-top: 5px;
  text-align: right;
}

/* ✅ 输入框优化 */
.input-container {
  display: flex;
  align-items: center;
  padding: 12px;
  background: white;
  border-top: 1px solid #ddd;
}

.input-container input {
  flex-grow: 1;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 16px;
}

.input-container button {
  margin-left: 10px;
  padding: 12px 15px;
  border: none;
  background: #007BFF;
  color: white;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
}

.input-container button:hover {
  background: #0056b3;
}
</style>
