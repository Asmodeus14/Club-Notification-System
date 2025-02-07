<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-700 via-blue-600 to-indigo-900 px-4">
    <div class="w-full max-w-md bg-white bg-opacity-10 p-6 rounded-2xl shadow-lg backdrop-blur-md border border-white border-opacity-20">
      <h1 class="text-3xl font-semibold text-white text-center mb-4">Forgot Password</h1>
      <p class="text-white text-center text-sm mb-6">Enter your email and ID to reset your password</p>

      <form @submit.prevent="handleForgotPassword" class="flex flex-col space-y-5">
        <!-- Email Input -->
        <div class="relative">
          <input
            type="email"
            placeholder="Enter your email"
            class="w-full p-3 rounded-xl border border-white text-white bg-transparent placeholder-white focus:ring-2 focus:ring-blue-300 focus:outline-none transition-all duration-300"
            v-model="formData.email"
            required
          />
          <span v-if="errors.email" class="text-red-400 text-sm absolute -bottom-5 left-2">{{ errors.email }}</span>
        </div>

        <!-- ID Input -->
        <div class="relative">
          <input
            type="text"
            placeholder="Enter your ID"
            class="w-full p-3 rounded-xl border border-white text-white bg-transparent placeholder-white focus:ring-2 focus:ring-blue-300 focus:outline-none transition-all duration-300"
            v-model="formData.user_id"
            required
          />
          <span v-if="errors.user_id" class="text-red-400 text-sm absolute -bottom-5 left-2">{{ errors.user_id }}</span>
        </div>

        <!-- Submit Button -->
        <button
          type="submit"
          class="w-full py-3 bg-white text-blue-900 font-semibold rounded-xl shadow-md hover:bg-blue-200 transition-all duration-300"
          :disabled="isLoading"
        >
          <span v-if="!isLoading">Reset Password</span>
          <span v-else>Processing...</span>
        </button>
      </form>

      <!-- Back to Login -->
      <div class="text-center text-white mt-4 text-sm">
        <p>Remember your password? <router-link to="/login" class="underline hover:text-blue-300">Login</router-link></p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { url } from './data/url';

export default {
  name: "ForgotPassword",
  data() {
    return {
      formData: {
        email: '',
        user_id: '', // Changed from 'id' to 'user_id' for consistency with backend
      },
      errors: {
        email: '',
        user_id: '',
      },
      isLoading: false, // Added for loading state
    };
  },
  methods: {
    async handleForgotPassword() {
      this.errors = {}; // Reset errors

      // Basic validation
      if (!this.formData.email.includes('@')) {
        this.errors.email = "Enter a valid email address";
      }
      if (this.formData.user_id.length < 3) {
        this.errors.user_id = "ID must be at least 3 characters long";
      }

      // If validation fails, stop request
      if (Object.keys(this.errors).length > 0) return;

      this.isLoading = true; // Start loading

      try {
        const response = await axios.post(
          `${url}/api/forgot`,
          new URLSearchParams(this.formData),
          {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          }
        );

        if (response.status === 200) {
          alert("A password reset link has been sent to your email!");
        } else {
          alert("Failed to process your request. Please try again.");
        }
      } catch (error) {
        console.error("Error:", error);
        alert(error.response?.data?.error || "An unexpected error occurred. Please try again.");
      } finally {
        this.isLoading = false; // Stop loading
      }
    },
  },
};
</script>

<style scoped>
/* Add custom styles here if needed */
</style>