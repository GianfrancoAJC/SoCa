<template>
  <div class="dashboard">
    <h2>Dashboard</h2>
    <div v-if="analytics">
      <h3>Estadísticas de la Simulación</h3>
      <div class="stats">
        <div class="stat">
          <h4>Total de Mensajes</h4>
          <p>{{ analytics.total_messages }}</p>
        </div>
        <div class="stat">
          <h4>Tiempo de Conexión</h4>
          <p>{{ analytics.connection_time }}</p>
        </div>
        <div class="stat">
          <h4>Tiempo en el Chat</h4>
          <p>{{ analytics.chat_time }}</p>
        </div>
        <div class="stat">
          <h4>Tiempo Promedio de Respuesta</h4>
          <p>{{ analytics.average_response_time }}</p>
        </div>
        <div class="stat">
          <h4>Tiempo Promedio de Espera</h4>
          <p>{{ analytics.average_await_time }}</p>
        </div>
        <div class="stat">
          <h4>Tiempo Promedio en el Chat</h4>
          <p>{{ analytics.average_chat_time }}</p>
        </div>
        <div class="stat">
          <h4>Tiempo Promedio de Mensaje</h4>
          <p>{{ analytics.average_message_time }}</p>
        </div>
      </div>
    </div>
    <canvas id="chart"></canvas>
  </div>
</template>

<script>
import axios from "axios";
import { Chart } from "chart.js";
import { mapGetters } from "vuex";

export default {
  name: "UserDashboard",
  computed: {
    ...mapGetters(["getUserId"]),
    userId() {
      return this.getUserId;
    },
  },
  data() {
    return {
      analytics: null,
    };
  },
  async mounted() {
    try {
      const response = await axios.post(`http://localhost:5001/analytics`, {
        user_id: this.userId,
      });
      this.analytics = response.data;
      this.renderChart();
    } catch (error) {
      console.error("Error al obtener las estadísticas:", error);
    }
  },
  methods: {
    renderChart() {
      const ctx = document.getElementById("chart").getContext("2d");
      new Chart(ctx, {
        type: "bar",
        data: {
          labels: [
            "Total de Mensajes",
            "Tiempo de Conexión",
            "Tiempo en el Chat",
            "Tiempo Promedio de Respuesta",
            "Tiempo Promedio de Espera",
            "Tiempo Promedio en el Chat",
            "Tiempo Promedio de Mensaje",
          ],
          datasets: [
            {
              label: "Estadísticas de la Simulación",
              data: [
                this.analytics.total_messages,
                this.analytics.connection_time,
                this.analytics.chat_time,
                this.analytics.average_response_time,
                this.analytics.average_await_time,
                this.analytics.average_chat_time,
                this.analytics.average_message_time,
              ],
              backgroundColor: [
                "#007bff",
                "#28a745",
                "#dc3545",
                "#ffc107",
                "#17a2b8",
                "#6c757d",
                "#f8f9fa",
              ],
            },
          ],
        },
      });
    },
  },
};
</script>

<style scoped>
.dashboard {
  max-width: 800px;
  margin: auto;
  text-align: center;
  padding: 20px;
}
.stats {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
  margin-top: 20px;
}
.stat {
  flex: 1;
  margin: 10px;
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
canvas {
  margin-top: 20px;
}
</style>
