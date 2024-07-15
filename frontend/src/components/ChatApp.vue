<template>
  <div class="chat-app">
    <h2>Chat Simulado</h2>
    <div class="chat-list">
      <ul>
        <li
          v-for="chat in chats"
          :key="chat.id"
          :class="{ active: selectedChat && selectedChat.id === chat.id }"
          @click="selectChat(chat)"
        >
          {{ chat.chat_name }}
        </li>
      </ul>
    </div>
    <div class="chat-window" v-if="selectedChat">
      <h3>{{ selectedChat.chat_name }}</h3>
      <div class="messages">
        <div v-for="message in messages" :key="message.id" class="message">
          <div
            v-if="message.sender_type === 'user'"
            :class="{ user: message.sender_type === 'user' }"
          >
            {{ message.message }}
          </div>
          <div v-if="message.sender_type === 'auto'" class="response">
            Respuesta automática: {{ message.message }}
          </div>
        </div>
      </div>
      <div class="input-area">
        <input
          v-model="newMessage"
          @keyup.enter="sendMessage"
          placeholder="Escribe un mensaje..."
        />
        <button @click="sendMessage">Enviar</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { mapState } from "vuex";

export default {
  name: "ChatApp",
  computed: {
    ...mapState(["userId"]),
  },
  data() {
    return {
      chats: [],
      selectedChat: null,
      messages: [],
      newMessage: "",
    };
  },
  async created() {
    console.log("Componente ChatApp creado, user_id:", this.userId); // Depuración
    try {
      const response = await axios.post(`http://localhost:5001/chat`, {
        user_id: this.userId,
      });
      this.chats = response.data.chats;
    } catch (error) {
      console.error("Error al obtener los chats:", error);
    }
  },
  methods: {
    async selectChat(chat) {
      this.selectedChat = chat;
      try {
        const response = await axios.post(`http://localhost:5001/message`, {
          chat_id: chat.id,
        });
        this.messages = response.data.messages;
      } catch (error) {
        console.error("Error al obtener los mensajes:", error);
      }
    },
    async sendMessage() {
      if (this.newMessage.trim()) {
        try {
          const response = await axios.post("http://localhost:5001/messages", {
            chat_id: this.selectedChat.id,
            user_id: this.userId,
            message: this.newMessage,
          });
          this.messages.push(response.data.message);
          this.messages.push(response.data.amessage);
          this.newMessage = "";
        } catch (error) {
          console.error("Error al enviar el mensaje:", error);
        }
      }
    },
  },
};
</script>

<style scoped>
.chat-app {
  display: flex;
  max-width: 800px;
  margin: auto;
  flex-direction: column;
}
.chat-list {
  border-bottom: 1px solid #ddd;
  padding: 10px 0;
}
.chat-list ul {
  list-style: none;
  padding: 0;
}
.chat-list li {
  padding: 10px;
  cursor: pointer;
}
.chat-list li.active {
  background-color: #007bff;
  color: white;
}
.chat-window {
  padding: 20px;
}
.messages {
  border: 1px solid #ddd;
  padding: 10px;
  max-height: 400px;
  overflow-y: auto;
}
.message {
  margin-bottom: 10px;
}
.message.user {
  text-align: right;
}
.input-area {
  display: flex;
  margin-top: 10px;
}
.input-area input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
.input-area button {
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.response {
  font-style: italic;
  color: #888;
}
</style>
