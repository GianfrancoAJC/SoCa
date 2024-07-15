<template>
  <div class="auth">
    <h2>{{ isLogin ? "Iniciar Sesión" : "Registrarse" }}</h2>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="user">Usuario</label>
        <input
          type="string"
          v-model="user"
          class="form-control"
          required
          placeholder="Ingresa tu usuario"
          id="user"
        />
      </div>
      <div class="form-group">
        <label for="password">Contraseña</label>
        <input
          type="password"
          v-model="password"
          class="form-control"
          required
          placeholder="Ingresa tu contraseña"
          id="password"
        />
      </div>
      <button type="submit" class="btn btn-primary">
        {{ isLogin ? "Iniciar Sesión" : "Registrarse" }}
      </button>
    </form>
    <button @click="toggleMode" class="btn btn-link">
      {{
        isLogin
          ? "¿No tienes cuenta? Regístrate"
          : "¿Ya tienes cuenta? Inicia sesión"
      }}
    </button>
  </div>
</template>

<script>
import axios from "axios";
import { mapActions } from "vuex";

export default {
  name: "UserAuth",
  data() {
    return {
      user: "",
      password: "",
      isLogin: true,
    };
  },
  methods: {
    ...mapActions(["setUserId"]),
    toggleMode() {
      this.isLogin = !this.isLogin;
    },
    async submitForm() {
      try {
        const endpoint = this.isLogin ? "user" : "users";
        const response = await axios.post(`http://localhost:5001/${endpoint}`, {
          username: this.user,
          password: this.password,
        });
        const userId = response.data.user_id;
        console.log("Autenticación exitosa, user_id:", userId); // Asegúrate de ver este log en la consola
        this.setUserId(userId); // Almacena userId en Vuex
        this.$router.push({
          name: "questionnaire",
        });
      } catch (error) {
        console.error("Error en la autenticación:", error);
      }
    },
  },
};
</script>

<style scoped>
.auth {
  max-width: 400px;
  margin: auto;
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
</style>
