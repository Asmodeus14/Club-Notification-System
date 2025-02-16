module.exports = {
    devServer: {
      host: '0.0.0.0',  // Allow external access
      port: 8080,
      client: {
        webSocketURL: {
          hostname: 'https://club-notification-backend.vercel.app', // Replace with your actual hostname
          port: 443, // Use HTTPS port
          pathname: '/ws',
          protocol: 'wss:', // Secure WebSocket
        },
      },
      server: 'https', // Enable HTTPS
    },
  };
  