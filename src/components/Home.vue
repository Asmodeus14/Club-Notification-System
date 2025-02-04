<template>
  <div
    class="max-w-full mx-auto p-6 min-h-screen bg-gradient-to-br from-gray-900 via-indigo-800 to-purple-900 flex flex-col items-center">
    <notification-permission></notification-permission>

    <!-- Navigation Bar -->
    <nav
      class="flex justify-between items-center bg-white bg-opacity-10 backdrop-blur-md text-white p-4 rounded-lg w-full max-w-5xl shadow-lg">
      <router-link to="/" class="text-2xl font-bold">Campus Connect</router-link>
      <div class="flex gap-4">
        <router-link to="/login" class="hover:opacity-80">Login</router-link>
        <router-link to="/signup" class="hover:opacity-80">Sign Up</router-link>
      </div>
    </nav>

    <!-- Hero Section -->
    <main
      class="text-center bg-white bg-opacity-10 backdrop-blur-md text-white py-16 rounded-lg mt-6 shadow-lg w-full max-w-5xl">
      <h1 class="text-4xl font-bold">Welcome to Campus Connect</h1>
      <p class="mt-2 text-lg">Your gateway to college events and announcements</p>
    </main>
    <!-- Notification Center -->
    <div class="bg-white bg-opacity-10 backdrop-blur-md p-6 rounded-lg mt-6 shadow-lg w-full max-w-5xl">
      <div class="flex justify-between items-center">
        <h2 class="text-xl font-semibold text-white">Recent Alerts</h2>
        <button @click="showNotifications = !showNotifications"
          class="bg-indigo-900 text-white px-4 py-2 rounded-lg hover:opacity-90">
          {{ showNotifications ? 'Hide' : 'Show' }} Notifications
        </button>
      </div>

      <transition name="slide-fade">
        <div v-if="showNotifications" class="mt-4 max-h-64 overflow-y-auto">
          <div v-for="(notification, index) in notifications" :key="index"
            class="flex items-center bg-white bg-opacity-20 backdrop-blur-md p-4 rounded-lg mb-2 shadow hover:shadow-md transition">
            <span class="text-2xl text-yellow-300">🔔</span>
            <div class="ml-4 text-white">
              <p>{{ notification.message }}</p>
              <small class="text-gray-300">{{ formatTimestamp(notification.timestamp) }}</small>
            </div>
          </div>
          <p v-if="!notifications.length" class="text-center text-gray-300 py-4">No new notifications</p>
        </div>
      </transition>
    </div>

    <!-- Floating Notification Indicator -->
    <div v-if="notifications.length" @click="showNotifications = true"
      class="fixed bottom-6 right-6 bg-white bg-opacity-20 backdrop-blur-md text-white p-4 rounded-full shadow-lg flex items-center cursor-pointer">
      <span class="bg-red-500 text-white text-xs font-bold px-2 py-1 rounded-full absolute -top-2 -right-2">{{
        notifications.length }}</span>
      <span class="text-2xl">🔔</span>
    </div>
    <!-- Slideshow Section -->
    <div class="relative w-full max-w-5xl mt-6 overflow-hidden rounded-lg shadow-lg h-96">
      <transition-group name="slide-fade" tag="div" class="relative h-full">
        <div v-for="(slide, index) in slides" :key="index" v-show="currentSlide === index"
          class="absolute inset-0 w-full h-full transition-opacity duration-1000 ease-in-out">
          <img :src="slide" class="object-cover w-full h-full" :alt="`Slide ${index + 1}`" />
        </div>
      </transition-group>

      <!-- Navigation Dots -->
      <div class="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex space-x-2">
        <button v-for="(slide, index) in slides" :key="index" @click="currentSlide = index"
          class="w-3 h-3 rounded-full transition-colors duration-300"
          :class="currentSlide === index ? 'bg-white' : 'bg-gray-400'"></button>
      </div>
    </div>


    <!-- Register for Clubs -->
    <div class="mt-6 text-center">
      <router-link to="/clubs" class="bg-indigo-900 text-white px-6 py-3 rounded-lg hover:opacity-90 shadow-lg">Register
        for Student
        Clubs</router-link>
    </div>

    
  </div>
</template>

<script>
import io from 'socket.io-client';
import NotificationPermission from './Notification.vue';

export default {
  name: 'HomePage',
  components: { NotificationPermission },
  data() {
    return {
      notifications: [],
      socket: null,
      showNotifications: false,
      slides: [
        new URL('@/assets/images/arts.jpg', import.meta.url).href,
        new URL('@/assets/images/sports.jpg', import.meta.url).href,
        new URL('@/assets/images/cultural.jpg', import.meta.url).href
      ],
      currentSlide: 0
    };
  },
  mounted() {
    this.socket = io('http://localhost:5000');

    this.socket.on('notification', (data) => {
      this.notifications.unshift({ ...data, timestamp: new Date() });
      this.showBrowserNotification(data.message);
    });

    this.startSlideShow();
  },
  methods: {
    showBrowserNotification(message) {
      if ("Notification" in window && Notification.permission === "granted") {
        new Notification(message);
      } else if (Notification.permission !== "denied") {
        Notification.requestPermission().then(permission => {
          if (permission === "granted") {
            new Notification(message);
          }
        });
      }
    },
    formatTimestamp(timestamp) {
      return new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    },
    startSlideShow() {
      this.slideInterval = setInterval(() => {
        this.currentSlide = (this.currentSlide + 1) % this.slides.length;
      }, 5000);
    }
  },
  beforeUnmount() {
    if (this.socket) this.socket.disconnect();
    if (this.slideInterval) {
      clearInterval(this.slideInterval);
    }
  }
};
</script>

<style>
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: opacity 1s ease-in-out;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  opacity: 0;
}
</style>