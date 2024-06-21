<template>
  <div class="chat-app">
    <ChatWindow :messages="localMessages" />
    <MessageInput @send-message="sendMessageToServer" />
  </div>
</template>

<script>
import ChatWindow from "./ChatWindow.vue";
import MessageInput from "./MessageInput.vue";
import axios from "axios";

export default {
  name: "ChatApp",
  components: {
    ChatWindow,
    MessageInput,
  },
  props: {
    messages: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      localMessages: [...this.messages],
      selectedChatId: null,
    };
  },
  watch: {
    messages(newMessages) {
      this.localMessages = [...newMessages];
    },
  },
  methods: {
    async sendMessageToServer({ user, text }) {
      const newMessage = {
        chat_id: this.selectedChatId,
        user: user,
        text: text,
      };
      this.localMessages.push(newMessage);

      try {
        await axios.post("http://localhost:5000/messages", newMessage);
        if (user === "You") {
          this.addBotResponse();
        }
      } catch (error) {
        console.error("Error sending message:", error);
      }
    },
    addBotResponse() {
      setTimeout(async () => {
        const botMessage = {
          chat_id: this.selectedChatId,
          user: "Bot",
          text: "This is an automatic response",
        };
        this.localMessages.push(botMessage);

        try {
          await axios.post("http://localhost:5000/messages", botMessage);
        } catch (error) {
          console.error("Error sending bot message:", error);
        }
      }, 1000);
    },
  },
};
</script>

<style scoped>
.chat-app {
  width: 100%;
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.chat-window {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  background-color: #f0f0f0;
  border-bottom: 1px solid #ccc;
}

.message-input {
  display: flex;
  padding: 10px;
  background-color: #ffffff;
  border-top: 1px solid #ccc;
}
</style>
