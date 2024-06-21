<template>
  <div class="message-input">
    <select v-model="selectedUser">
      <option v-for="(user, index) in users" :key="index" :value="user">
        {{ user }}
      </option>
    </select>
    <input
      v-model="newMessage"
      @keyup.enter="sendMessage"
      type="text"
      placeholder="Type your message..."
    />
    <button @click="sendMessage">Send</button>
  </div>
</template>

<script>
export default {
  name: "MessageInput",
  props: {
    users: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      newMessage: "",
      selectedUser: this.users[0],
    };
  },
  methods: {
    sendMessage() {
      if (this.newMessage.trim() !== "") {
        this.$emit("send-message", {
          user: this.selectedUser,
          text: this.newMessage,
        });
        this.newMessage = "";
      }
    },
  },
};
</script>

<style scoped>
.message-input {
  display: flex;
  align-items: center;
}

.message-input select {
  margin-right: 10px;
}

.message-input input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin-right: 10px;
}

.message-input button {
  padding: 10px 20px;
  border: none;
  background-color: #007bff;
  color: white;
  cursor: pointer;
  border-radius: 4px;
}

.message-input button:hover {
  background-color: #0056b3;
}
</style>
