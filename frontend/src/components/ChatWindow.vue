<template>
  <div class="chat-window">
    <div class="messages">
      <div v-for="(message, index) in messages" :key="index" class="message">
        <span class="user">{{ message.user }}:</span>
        <span class="text">{{ message.text }}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ChatWindow",
  props: {
    messages: {
      type: Array,
      required: true,
    },
  },
};
</script>

<style scoped>
.chat-window {
  border: 1px solid #ccc;
  padding: 10px;
  height: 300px;
  overflow-y: auto;
}

.message {
  margin: 5px 0;
}

.user {
  font-weight: bold;
  margin-right: 5px;
}

.text {
  word-wrap: break-word;
}
</style>
