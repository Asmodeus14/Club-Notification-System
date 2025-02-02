<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-r from-purple-600 to-blue-500 px-4">
    <div class="w-full max-w-md bg-white bg-opacity-10 p-8 rounded-2xl shadow-2xl backdrop-blur-lg">
      <h1 class="text-3xl font-bold text-white text-center mb-2">Welcome Back</h1>
      <p class="text-white text-center mb-6">Login to continue</p>

      <form @submit.prevent="handleLogin">
        <!-- ID Input -->
        <div class="relative mb-6">
          <input type="text" id="ID" v-model="formData.user_id" required
            class="peer w-full p-4 bg-transparent border border-white rounded-xl text-white placeholder-transparent focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
            placeholder="User ID" />
          <label for="ID"
            class="absolute left-4 top-4 text-white text-opacity-0 transition-all peer-placeholder-shown:top-4 peer-placeholder-shown:text-lg peer-placeholder-shown:text-opacity-50 peer-focus:top-0 peer-focus:text-sm peer-focus:text-opacity-100">
            User ID
          </label>
        </div>

        <!-- Password Input with Toggle -->
        <div class="relative mb-6">
          <input :type="isPasswordVisible ? 'text' : 'password'" id="password" v-model="formData.password" required
            class="peer w-full p-4 bg-transparent border border-white rounded-xl text-white placeholder-transparent focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
            placeholder="Password" />
          <label for="password"
            class="absolute left-4 top-4 text-white text-opacity-0 transition-all peer-placeholder-shown:top-4 peer-placeholder-shown:text-lg peer-placeholder-shown:text-opacity-50 peer-focus:top-0 peer-focus:text-sm peer-focus:text-opacity-100">
            Password
          </label>
          <img :src="eyeIcon" alt="eye-icon" @click="togglePasswordVisibility"
            class="absolute right-4 top-4 w-6 h-6 cursor-pointer opacity-80 hover:opacity-100 transition" />
        </div>

        <!-- Forgot Password -->
        <div class="text-right mb-6">
          <router-link to="/forgotpassword" class="text-white text-sm hover:underline">
            Forgot Password?
          </router-link>
        </div>

        <!-- Login Button -->
        <button type="submit"
          class="w-full py-3 bg-blue-600 text-white font-semibold rounded-xl shadow-md hover:bg-blue-700 transition-all">
          Login
        </button>

        <!-- Divider -->
        <div class="flex items-center my-6">
          <div class="flex-1 border-t border-white opacity-30"></div>
          <p class="mx-4 text-white text-sm opacity-80">OR</p>
          <div class="flex-1 border-t border-white opacity-30"></div>
        </div>

        <!-- Social Login Buttons -->
        <div class="flex gap-4">
          <button
            class="flex-1 flex items-center justify-center py-3 bg-white bg-opacity-20 rounded-xl hover:bg-opacity-30 transition">
            <img src="@/assets/google.svg" alt="Google" class="w-6 h-6 mr-2" />
            <span class="text-white">Google</span>
          </button>
        </div>

        <!-- Signup Link -->
        <p class="text-center text-white text-sm mt-6">
          Don't have an account?
          <router-link to="/signup" class="underline">Sign up</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "LoginForm",
  data() {
    return {
      formData: {
        user_id: '', // Changed from ID to user_id for consistency with backend
        password: '',
      },
      isPasswordVisible: false,
      loginError: null, // Added for error handling
    };
  },
  computed: {
    eyeIcon() {
      return this.isPasswordVisible
        ? require('@/assets/eye-open.png')
        : require('@/assets/eye-close.png');
    },
  },
  methods: {
    togglePasswordVisibility() {
      this.isPasswordVisible = !this.isPasswordVisible;
    },
    async handleLogin() {
      this.loginError = null; // Reset error message

      try {
        const response = await axios.post(
          'http://127.0.0.1:5000/api/login',
          new URLSearchParams(this.formData),
          {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          }
        );

        if (response.status === 200 && response.data.user_id) {
          // Redirect to dashboard with user_id
          this.$router.push(`/dashboard/${response.data.user_id}`);
        } else {
          this.loginError = "Invalid credentials, please try again.";
        }
      } catch (error) {
        console.error("Login failed:", error);
        this.loginError = error.response?.data?.error || "An unexpected error occurred. Please try again.";
      }
    },
  },
};
</script>

<style scoped>
/* Add custom styles here if needed */
</style>