<template>
  <div class="questionnaire">
    <h2>Cuestionario Inicial</h2>
    <form @submit.prevent="submitForm">
      <div v-for="(chat, index) in chats" :key="index" class="form-group">
        <label :for="'chat' + index">Nombre del Chat {{ index + 1 }}</label>
        <input type="text" :id="'chat' + index" v-model="chat.name" class="form-control" required />
      </div>
      <div class="form-group">
        <label for="numChats">Número de chats:</label>
        <input type="number" id="numChats" v-model="numChats" @change="updateChats" min="1" max="20" class="form-control" required />
      </div>
      <button type="submit" class="btn btn-primary">Iniciar Simulación</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Questionnaire',
  data() {
    return {
      numChats: 1,
      chats: [{ name: '' }],
      user_id: 'some_user_id' // This should be dynamic
    };
  },
  methods: {
    updateChats() {
      const newChats = [];
      for (let i = 0; i < this.numChats; i++) {
        newChats.push({ name: '' });
      }
      this.chats = newChats;
    },
    async submitForm() {
      try {
        const chatNames = this.chats.map(chat => chat.name);
        await axios.post('http://localhost:5000/chats', {
          user_id: this.user_id,
          chat_name: chatNames,
          n: this.numChats
        });
        this.$router.push({ name: 'ChatApp' });
      } catch (error) {
        console.error('Error creating chats:', error);
      }
    }
  }
};
</script>

<style scoped>
.questionnaire {
  max-width: 600px;
  margin: auto;
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
</style>
