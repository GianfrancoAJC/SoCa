const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    port: 8081,
    client: {
      webSocketURL: "ws://localhost:8081/ws",
    },
  },
});
