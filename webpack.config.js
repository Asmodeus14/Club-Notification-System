module.exports = {
  devServer: {
    host: "0.0.0.0", // Allow external access
    port: 8080,
    client: {
      webSocketURL: {
        hostname: "club-notification-backend.vercel.app", // Your backend domain
        port: 443, // HTTPS WebSocket
        pathname: "/socket.io/",
        protocol: "wss:", // Secure WebSocket
      },
    },
    proxy: {
      "/socket.io/": {
        target: "https://club-notification-backend.vercel.app", // Backend URL
        ws: true, // Enable WebSocket proxying
        changeOrigin: true,
      },
    },
    server: "https", // Enable HTTPS
  },
};
