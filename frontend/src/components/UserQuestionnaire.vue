<template>
  <div class="questionnaire">
    <h2>Cuestionario</h2>
    <form @submit.prevent="submit">
      <div class="form-group">
        <label for="question1">¿Cómo te sientes hoy?</label>
        <input
          type="text"
          id="question1"
          v-model="answers.question1"
          class="form-control"
        />
      </div>
      <div class="form-group">
        <label for="question2">¿Cuál es tu color favorito?</label>
        <input
          type="text"
          id="question2"
          v-model="answers.question2"
          class="form-control"
        />
      </div>
      <button type="submit" class="btn btn-primary">Enviar</button>
    </form>
  </div>
</template>

<script>
export default {
  name: "UserQuestionnaire",
  data() {
    return {
      answers: {
        question1: "",
        question2: "",
      },
    };
  },
  methods: {
    submit() {
      this.$emit("complete", this.answers);
    },
  },
};
</script>

<style scoped>
.questionnaire {
  margin: auto;
  padding: 20px;
  width: 50%;
  background-color: #f9f9f9;
  border: 1px solid #ccc;
  border-radius: 5px;
}
</style>
