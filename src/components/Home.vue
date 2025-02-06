<template>
  <div class="max-w-full p-6 min-h-screen bg-gradient-to-r from-purple-600 to-blue-500 px-4 flex flex-col items-center">
    <notification-permission></notification-permission>

    <!-- Navigation Bar -->
    <nav
      class="flex justify-between items-center bg-white bg-opacity-10 backdrop-blur-md text-white p-4 rounded-lg w-full max-w-full shadow-lg">
      <router-link to="/" class="text-2xl font-bold hover:scale-105 transition-transform">Campus Connect</router-link>
      <div class="flex gap-4">
        <router-link to="/login" class="hover:opacity-80 hover:text-indigo-300 transition">Login</router-link>
        <router-link to="/signup" class="hover:opacity-80 hover:text-indigo-300 transition">Sign Up</router-link>
      </div>
    </nav>

    <!-- Hero Section -->
    <main
      class="text-center bg-white bg-opacity-10 backdrop-blur-md text-white py-16 rounded-lg mt-6 shadow-lg w-full max-w-full">
      <h1 class="text-4xl font-bold animate-fade-in">Welcome to Campus Connect</h1>
      <p class="mt-2 text-lg">Your gateway to college events and announcements</p>
    </main>

    <!-- Notification Center -->
    <div class="bg-white bg-opacity-10 backdrop-blur-md p-6 rounded-lg mt-6 shadow-lg w-full max-w-6xl">
      <div class="flex justify-between items-center">
        <h2 class="text-xl font-semibold text-white">Recent Alerts</h2>
        <button @click="showNotifications = !showNotifications"
          class="bg-indigo-900 text-white px-4 py-2 rounded-lg hover:scale-105 transition-transform">
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

    <!-- Events Section -->
    <div class="bg-white bg-opacity-10 backdrop-blur-md p-6 rounded-lg mt-6 shadow-lg w-full max-w-6xl">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-semibold text-white">Upcoming Events</h2>
        <button @click="fetchEvents"
          class="bg-indigo-900 text-white px-4 py-2 rounded-lg hover:scale-105 transition-transform">
          Refresh Events
        </button>
      </div>

      <div v-if="loadingEvents" class="text-center text-white py-4">
        Loading events...
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div v-for="event in events" :key="event.id"
          class="bg-white bg-opacity-20 backdrop-blur-md p-4 rounded-lg hover:shadow-md transition">
          <div class="text-yellow-300 text-sm mb-2">
            {{ formatDate(event.date_time) }}
          </div>
          <h3 class="text-white font-semibold mb-2">{{ event.message }}</h3>
          <div class="text-gray-300 text-sm">
            Organized by: {{ event.club }}
          </div>
        </div>
        <div v-if="!events.length" class="text-center text-gray-300 col-span-full py-4">
          No upcoming events found
        </div>
      </div>
    </div>

    <!-- Slideshow Section -->
    <div class="relative w-full max-w-5xl mt-6 overflow-hidden rounded-lg shadow-lg h-96">
      <transition-group name="slide-fade" tag="div" class="relative h-full">
        <div v-for="(slide, index) in slides" :key="index" v-show="currentSlide === index"
          class="absolute inset-0 w-full h-full transition-opacity duration-1000 ease-in-out">
          <img :src="slide" class="object-cover w-full h-full" :alt="`Slide ${index + 1}`" />
        </div>
      </transition-group>
      <div class="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex space-x-2">
        <button v-for="(slide, index) in slides" :key="index" @click="currentSlide = index"
          class="w-3 h-3 rounded-full transition-colors duration-300"
          :class="currentSlide === index ? 'bg-white' : 'bg-gray-400'">
        </button>
      </div>
    </div>

    <!-- Register for Clubs -->
    <div class="mt-6 text-center">
      <router-link to="/clubs"
        class="bg-indigo-900 text-white px-6 py-3 rounded-lg hover:scale-105 transition-transform shadow-lg">
        Register for Student Clubs
      </router-link>
    </div>


  </div>
  <!-- Footer -->
  <footer class="bg-gray-800 text-white text-center py-4  w-full">
    <p>&copy; 2025 Campus Connect. All rights reserved.</p>
    <div class="flex justify-center gap-4 mt-2">
      <a href="#" class="hover:text-indigo-400 transition">Privacy Policy</a>
      <a href="#" class="hover:text-indigo-400 transition">Terms of Service</a>
      <a href="#" class="hover:text-indigo-400 transition">Contact Us</a>
    </div>
  </footer>
</template>

<script>
import io from 'socket.io-client';
import NotificationPermission from './Notification.vue';
import axios from 'axios'
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
        new URL('@/assets/images/cultural.jpg', import.meta.url).href,
        new URL('@/assets/images/tech-club.jpg', import.meta.url).href,
        new URL('@/assets/images/sports-club.jpg', import.meta.url).href,
        new URL('@/assets/images/techfest.jpg', import.meta.url).href,
      ],
      currentSlide: 0,
      events: [],
      loadingEvents: false,
    };
  },
  mounted() {
    this.socket = io('http://localhost:5000'); // Use socket.io-client here instead of WebSocket
    this.socket.on('notification', (data) => {
      this.notifications.unshift({ ...data, timestamp: new Date() });
      this.showBrowserNotification(data.message);
    });
    this.startSlideShow();
    this.fetchEvents();
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
    },
    async fetchEvents() {
      this.loadingEvents = true;
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/events');
        this.events = response.data;
      } catch (error) {
        console.error('Error fetching events:', error);
      } finally {
        this.loadingEvents = false;
      }
    },
    formatDate(dateString) {
    const options = {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    };
    return new Date(dateString).toLocaleDateString(undefined, options);
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
