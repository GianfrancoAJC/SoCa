<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <a class="navbar-brand" href="#">SoCa</a>
      <button
        class="navbar-toggler"
        type="button"
        data-toggle="collapse"
        data-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ml-auto">
          <li class="nav-item">
            <router-link class="nav-link" to="/">Inicio</router-link>
          </li>
          <li class="nav-item" v-if="!userId">
            <router-link class="nav-link" to="/auth"
              >Iniciar Sesión / Registrarse</router-link
            >
          </li>
          <li class="nav-item" v-if="userId">
            <router-link class="nav-link" :to="{ name: 'questionnaire' }"
              >Cuestionario</router-link
            >
          </li>
          <li class="nav-item" v-if="userId">
            <router-link class="nav-link" :to="{ name: 'dashboard' }"
              >Dashboard</router-link
            >
          </li>
        </ul>
      </div>
    </nav>
    <router-view @login="handleLogin" />
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";

export default {
  name: "App",
  computed: {
    ...mapGetters(["getUserId"]),
    userId() {
      return this.getUserId;
    },
  },
  methods: {
    ...mapActions(["setUserId"]),
    handleLogin(userId) {
      this.setUserId(userId);
    },
    /*setupWebSocket() {
      // Reemplaza 'localhost' con la dirección IP o el nombre de host donde se ejecuta tu servidor WebSocket
      this.ws = new WebSocket("ws://190.236.203.37:8081/ws");

      this.ws.onopen = () => {
        console.log("Conectado al servidor WebSocket");
        // Puedes enviar un mensaje al servidor al establecer la conexión si es necesario
        this.ws.send("Hola desde Vue.js");
      };

      this.ws.onmessage = (event) => {
        console.log("Mensaje recibido del servidor:", event.data);
        // Procesa los mensajes recibidos del servidor WebSocket
      };

      this.ws.onclose = () => {
        console.log("Conexión cerrada");
        // Maneja la reconexión si es necesario
      };
    },*/
  },
  /*mounted() {
    this.setupWebSocket(); // Inicializa la conexión WebSocket al montar el componente
  },*/
};
</script>

<style>
body {
  font-family: "Arial", sans-serif;
}

#app {
  text-align: center;
}

.navbar {
  margin-bottom: 20px;
}
</style>
