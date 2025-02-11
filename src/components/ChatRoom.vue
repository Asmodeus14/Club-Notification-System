<template>
    <div class="min-h-screen bg-gray-900 text-gray-100 flex">
      <!-- Server List -->
      <div class="w-20 bg-gray-800 flex flex-col items-center py-4 space-y-4">
        <div 
          v-for="server in servers" 
          :key="server.id"
          class="server-icon"
          @mouseenter="hoverServer(server.id)"
          @mouseleave="resetServer(server.id)"
          @click="selectServer(server.id)"
        >
          <img 
            :src="server.icon" 
            class="w-12 h-12 rounded-full cursor-pointer transition-transform"
            :class="{ 'rounded-xl': server.id === activeServer }"
          >
        </div>
      </div>
  
      <!-- Channel List -->
      <div class="w-64 bg-gray-800 flex flex-col">
        <div class="p-4 border-b border-gray-700">
          <h2 class="font-bold text-xl">{{ activeServerName }}</h2>
        </div>
        <div class="flex-1 overflow-y-auto">
          <div 
            v-for="channel in channels" 
            :key="channel.id"
            class="channel-item px-4 py-2 hover:bg-gray-700 cursor-pointer"
            :class="{ 'bg-gray-700': channel.id === activeChannel }"
            @click="selectChannel(channel.id)"
          >
            # {{ channel.name }}
          </div>
        </div>
      </div>
  
      <!-- Chat Area -->
      <div class="flex-1 flex flex-col bg-gray-900">
        <!-- Messages -->
        <div class="flex-1 overflow-y-auto p-4 space-y-4" ref="messagesContainer">
          <div 
            v-for="message in messages"
            :key="message.id"
            class="message animate-in"
          >
            <div class="flex items-start space-x-4">
              <img :src="message.author.avatar" class="w-10 h-10 rounded-full">
              <div>
                <div class="flex items-center space-x-2">
                  <span class="font-bold text-purple-400">{{ message.author.name }}</span>
                  <span class="text-xs text-gray-400">{{ message.timestamp }}</span>
                </div>
                <p class="text-gray-100">{{ message.content }}</p>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Message Input -->
        <div class="p-4 border-t border-gray-800">
          <div class="flex space-x-4">
            <input
              v-model="newMessage"
              @keyup.enter="sendMessage"
              placeholder="Message #general"
              class="flex-1 bg-gray-800 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
            >
            <button 
              @click="sendMessage"
              class="bg-purple-600 px-4 py-2 rounded-lg hover:bg-purple-700 transition-colors"
            >
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import anime from 'animejs';
  
  export default {
    name:"ChatRoom",
    data() {
      return {
        activeServer: 1,
        activeChannel: 1,
        newMessage: '',
        servers: [
          { id: 1, name: "Campus Hub", icon: "https://source.unsplash.com/random/100x100/?campus" },
          { id: 2, name: "CS Dept", icon: "https://source.unsplash.com/random/100x100/?code" },
          { id: 3, name: "Sports", icon: "https://source.unsplash.com/random/100x100/?sports" }
        ],
        channels: [
          { id: 1, serverId: 1, name: "general" },
          { id: 2, serverId: 1, name: "announcements" },
          { id: 3, serverId: 1, name: "events" }
        ],
        messages: [
          {
            id: 1,
            content: "Welcome to Campus Connect! 🎉",
            author: { name: "Admin", avatar: "https://source.unsplash.com/random/100x100/?admin" },
            timestamp: "Today at 10:00 AM"
          }
        ]
      }
    },
    computed: {
      activeServerName() {
        return this.servers.find(s => s.id === this.activeServer)?.name || ''
      }
    },
    methods: {
      hoverServer(serverId) {
        anime({
          targets: `.server-icon[data-server="${serverId}"] img`,
          scale: 1.1,
          duration: 300,
          easing: 'easeOutQuad'
        });
      },
      resetServer(serverId) {
        anime({
          targets: `.server-icon[data-server="${serverId}"] img`,
          scale: 1,
          duration: 300,
          easing: 'easeOutQuad'
        });
      },
      selectServer(serverId) {
        this.activeServer = serverId;
        this.animateChannelList();
      },
      selectChannel(channelId) {
        this.activeChannel = channelId;
        this.animateMessages();
      },
      sendMessage() {
        if (this.newMessage.trim()) {
          const newMsg = {
            id: Date.now(),
            content: this.newMessage,
            author: {
              name: "You",
              avatar: "https://source.unsplash.com/random/100x100/?user"
            },
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
          };
          
          this.animateMessageEntry(newMsg);
          this.newMessage = '';
        }
      },
      animateChannelList() {
        anime({
          targets: '.channel-item',
          opacity: [0, 1],
          translateX: [-20, 0],
          delay: anime.stagger(50),
          duration: 300,
          easing: 'easeOutQuad'
        });
      },
      animateMessages() {
        anime({
          targets: '.message',
          opacity: [0, 1],
          translateY: [20, 0],
          delay: anime.stagger(50),
          duration: 400,
          easing: 'easeOutExpo'
        });
      },
      animateMessageEntry(message) {
        const timeline = anime.timeline({
          easing: 'easeOutExpo',
          duration: 400
        });
  
        timeline.add({
          targets: this.$refs.messagesContainer,
          scrollTop: this.$refs.messagesContainer.scrollHeight,
          duration: 300
        });
  
        timeline.add({
          targets: [message],
          begin: () => {
            this.messages.push(message);
          },
          opacity: [0, 1],
          translateY: [20, 0],
          easing: 'easeOutExpo'
        });
      }
    },
    mounted() {
      // Initialize WebSocket connection
      this.websocket = new WebSocket('ws://your-backend-url/chat');
      
      this.websocket.onmessage = (event) => {
        const message = JSON.parse(event.data);
        this.animateMessageEntry(message);
      };
  
      // Initial animations
      this.animateChannelList();
      this.animateMessages();
    }
  }
  </script>
  
  <style>
  /* Custom Scrollbar */
  ::-webkit-scrollbar {
    width: 8px;
  }
  
  ::-webkit-scrollbar-track {
    background: #2d2d2d;
  }
  
  ::-webkit-scrollbar-thumb {
    background: #4a4a4a;
    border-radius: 4px;
  }
  
  ::-webkit-scrollbar-thumb:hover {
    background: #5a5a5a;
  }
  
  /* Message Animation */
  .animate-in {
    animation: messageIn 0.4s ease-out forwards;
  }
  
  @keyframes messageIn {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  </style>