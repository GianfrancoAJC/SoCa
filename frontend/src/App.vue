<template>
  <div class="app">
    <UserQuestionnaire
      v-if="!questionnaireCompleted"
      @complete="handleQuestionnaireComplete"
    />
    <div v-else>
      <ChatList :chats="chats" @select-chat="selectChat" />
      <ChatApp :messages="messages" />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import UserQuestionnaire from "./components/UserQuestionnaire.vue";
import ChatList from "./components/ChatList.vue";
import ChatApp from "./components/ChatApp.vue";

export default {
  name: "App",
  components: {
    UserQuestionnaire,
    ChatList,
    ChatApp,
  },
  data() {
    return {
      questionnaireCompleted: false,
      chats: [],
      messages: [],
      selectedChatId: null,
    };
  },
  methods: {
    async handleQuestionnaireComplete(answers) {
      this.questionnaireCompleted = true;
      try {
        const response = await axios.post(
          "http://localhost:5000/generate_chats",
          answers
        );
        this.chats = response.data.chats;
        this.selectChat(this.chats[0].chat_id);
      } catch (error) {
        console.error("Error generating chats:", error);
      }
    },
    async selectChat(chatId) {
      this.selectedChatId = chatId;
      try {
        const response = await axios.get(
          `http://localhost:5000/messages/${chatId}`
        );
        this.messages = response.data;
      } catch (error) {
        console.error("Error fetching messages:", error);
      }
    },
  },
};
</script>

<style scoped>
.app {
  display: flex;
  height: 100vh;
}
</style>
