<template>
  <div class="home">
    <h1>Bienvenido a SoCa</h1>
    <p>
      Explora las funcionalidades de nuestra aplicación web para manejar el
      FOMO.
    </p>
    <div class="features">
      <div class="feature">
        <h3>Simulaciones de Chat</h3>
        <p>
          Interactúa con nuestro simulador para entender mejor tu comportamiento
          en redes sociales.
        </p>
      </div>
      <div class="feature">
        <h3>Estadísticas Detalladas</h3>
        <p>
          Obtén estadísticas detalladas sobre tu uso de las redes sociales y
          consejos para mejorar.
        </p>
      </div>
      <div class="feature">
        <h3>Regístrate o Inicia Sesión</h3>
        <p>
          Regístrate o inicia sesión para comenzar tu simulación personalizada.
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "UserHome",
};
</script>

<style scoped>
.home {
  max-width: 800px;
  margin: auto;
  text-align: center;
  padding: 20px;
}
.features {
  display: flex;
  justify-content: space-around;
  margin-top: 20px;
}
.feature {
  flex: 1;
  margin: 0 10px;
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
</style>
