<template>
    <div v-if="showPrompt" class="fixed inset-0 z-50 flex items-center justify-center bg-black/30 backdrop-blur-sm">
      <!-- Modal Container with Enter/Leave Animation -->
      <transition
        enter-active-class="transition-all duration-300 ease-out"
        leave-active-class="transition-all duration-200 ease-in"
        enter-from-class="opacity-0 scale-95"
        leave-to-class="opacity-0 scale-95"
      >
        <!-- Modal Card -->
        <div class="w-full max-w-md mx-4 bg-white rounded-xl shadow-2xl overflow-hidden transform transition-all">
          <!-- Gradient Header -->
          <div class="bg-gradient-to-r from-blue-500 to-purple-600 p-6">
            <div class="flex items-center justify-center space-x-3">
              <!-- Animated Bell Icon -->
              <svg class="h-12 w-12 text-white animate-ring" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                      d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
              </svg>
              <h3 class="text-2xl font-bold text-white font-poppins">Stay Updated!</h3>
            </div>
          </div>
  
          <!-- Content Area -->
          <div class="p-6 space-y-6">
            <p class="text-gray-600 text-center text-lg leading-relaxed">
              Never miss important updates from our community! 
              Enable notifications to receive real-time alerts about 
              events, announcements, and special opportunities.
            </p>
  
            <!-- Action Buttons -->
            <div class="flex flex-col space-y-4 sm:flex-row sm:space-y-0 sm:space-x-4">
              <button
                @click="requestPermission"
                class="flex-1 bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 text-white font-semibold py-3 px-6 rounded-lg transform transition-all duration-200 hover:scale-105 shadow-lg"
              >
                Allow Notifications
              </button>
              <button
                @click="dismissPrompt"
                class="flex-1 border-2 border-gray-200 text-gray-600 hover:text-gray-800 hover:border-gray-300 font-semibold py-3 px-6 rounded-lg transition-colors duration-200"
              >
                Later
              </button>
            </div>
          </div>
  
          <!-- Footer Note -->
          <p class="text-center text-sm text-gray-400 pb-4">
            You can always change this in browser settings
          </p>
        </div>
      </transition>
    </div>
  </template>
  
  <script>
  export default {
    name: "NotificationPermission",
    data() {
      return {
        showPrompt: false,
      };
    },
    mounted() {
      if (typeof Notification !== "undefined" && Notification.permission === "default") {
        setTimeout(() => {
          this.showPrompt = true;
        }, 1500); // Slight delay for better UX
      }
    },
    methods: {
      async requestPermission() {
        try {
          const permission = await Notification.requestPermission();
          if (permission === "granted") {
            new Notification("🔔 You're all set!", {
              body: "Thanks for enabling notifications! We'll keep you updated.",
              icon: "@/assets/favicon.svg"
            });
          }
        } finally {
          this.showPrompt = false;
        }
      },
      dismissPrompt() {
        this.showPrompt = false;
        // Optional: Store dismissal in localStorage to prevent reappearance
      },
    },
  };
  </script>
  
  <style>
  @keyframes ring {
    0% { transform: rotate(0deg); }
    25% { transform: rotate(15deg); }
    50% { transform: rotate(-15deg); }
    75% { transform: rotate(5deg); }
    100% { transform: rotate(0deg); }
  }
  
  .animate-ring {
    animation: ring 1.5s ease-in-out;
  }
  
  .font-poppins {
    font-family: 'Poppins', sans-serif;
  }
  
  .backdrop-blur-sm {
    backdrop-filter: blur(4px);
  }
  </style>