<template>
  <div class="questionnaire">
    <h2>Cuestionario Inicial</h2>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="numChats">Número de chats:</label>
        <input
          type="number"
          id="numChats"
          v-model="numChats"
          @change="updateChats"
          min="1"
          max="20"
          class="form-control"
          required
        />
      </div>
      <div v-for="(chat, index) in chats" :key="index" class="form-group">
        <label :for="'chat' + index">Nombre del Chat {{ index + 1 }}</label>
        <input
          type="text"
          :id="'chat' + index"
          v-model="chat.name"
          class="form-control"
          required
        />
        <label :for="'relationship' + index">Parentesco {{ index + 1 }}</label>
        <input
          type="text"
          :id="'relationship' + index"
          v-model="chat.relationship"
          class="form-control"
          required
        />
      </div>
      <button type="submit" class="btn btn-primary">Iniciar Simulación</button>
    </form>
  </div>
</template>

<script>
import axios from "axios";
import { mapState } from "vuex";

export default {
  name: "UserQuestionnaire",
  computed: {
    ...mapState(["userId"]),
  },
  data() {
    return {
      numChats: 1,
      chats: [{ name: "", relationship: "" }],
    };
  },
  created() {
    console.log("Componente UserQuestionnaire creado, user_id:", this.userId); // Depuración
  },
  methods: {
    updateChats() {
      const newChats = [];
      for (let i = 0; i < this.numChats; i++) {
        newChats.push({ name: "", relationship: "" });
      }
      this.chats = newChats;
    },
    async submitForm() {
      try {
        console.log("Enviando cuestionario, user_id:", this.userId); // Depuración
        await axios.post("http://localhost:5001/chats", {
          n: this.numChats,
          user_id: this.userId,
          chats: this.chats,
        });
        this.$router.push({ name: "chat" });
      } catch (error) {
        console.error("Id_dinamico:", this.userId);
        console.error("Error al enviar el cuestionario:", error);
      }
    },
  },
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
