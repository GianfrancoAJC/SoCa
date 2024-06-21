<template>
  <div class="chat-list">
    <ul class="list-group">
      <li
        v-for="chat in chats"
        :key="chat.chat_id"
        class="list-group-item"
        @click="selectChat(chat.chat_id)"
      >
        Chat {{ chat.chat_id }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "ChatList",
  props: {
    chats: {
      type: Array,
      required: true,
    },
  },
  methods: {
    selectChat(chatId) {
      this.$emit("select-chat", chatId);
    },
  },
};
</script>

<style scoped>
.chat-list {
  width: 100%;
  padding: 10px;
  background-color: #f7f7f7;
}

.list-group-item {
  cursor: pointer;
}

.list-group-item:hover {
  background-color: #e6e6e6;
}
</style>
