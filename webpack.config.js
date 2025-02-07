module.exports = {
    devServer: {
      host: '0.0.0.0',  // Allow external access
      port: 8080,
      client: {
        webSocketURL: {
          hostname: '755e-103-176-170-230.ngrok-free.app', // Replace with your actual hostname
          port: 443, // Use HTTPS port
          pathname: '/ws',
          protocol: 'wss:', // Secure WebSocket
        },
      },
      server: 'https', // Enable HTTPS
    },
  };
  