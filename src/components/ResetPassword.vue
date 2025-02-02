<template>
    <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-700 via-blue-600 to-indigo-900 px-4">
      <div class="w-full max-w-md bg-white bg-opacity-10 p-6 rounded-2xl shadow-lg backdrop-blur-md border border-white border-opacity-20">
        <h1 class="text-3xl font-semibold text-white text-center mb-4">Reset Password</h1>
        <p class="text-white text-center text-sm mb-6">Enter your new password below</p>
  
        <form @submit.prevent="handleResetPassword" class="flex flex-col space-y-5">
          <!-- New Password Input -->
          <div class="relative">
            <input
              type="password"
              placeholder="New Password"
              v-model="newPassword"
              required
              class="w-full p-3 rounded-xl border border-white text-white bg-transparent placeholder-white focus:ring-2 focus:ring-blue-300 focus:outline-none transition-all duration-300"
            />
            <span v-if="errors.newPassword" class="text-red-400 text-sm absolute -bottom-5 left-2">{{ errors.newPassword }}</span>
          </div>
  
          <!-- Confirm Password Input -->
          <div class="relative">
            <input
              type="password"
              placeholder="Confirm New Password"
              v-model="confirmPassword"
              required
              class="w-full p-3 rounded-xl border border-white text-white bg-transparent placeholder-white focus:ring-2 focus:ring-blue-300 focus:outline-none transition-all duration-300"
            />
            <span v-if="errors.confirmPassword" class="text-red-400 text-sm absolute -bottom-5 left-2">{{ errors.confirmPassword }}</span>
          </div>
  
          <!-- Submit Button -->
          <button
            type="submit"
            class="w-full py-3 bg-white text-blue-900 font-semibold rounded-xl shadow-md hover:bg-blue-200 transition-all duration-300"
            :disabled="isLoading"
          >
            <span v-if="!isLoading">Reset Password</span>
            <span v-else>Resetting...</span>
          </button>
        </form>
  
        <!-- Error Message -->
        <div v-if="errorMessage" class="text-center text-red-400 mt-4 text-sm">
          {{ errorMessage }}
        </div>
  
        <!-- Success Message -->
        <div v-if="successMessage" class="text-center text-green-400 mt-4 text-sm">
          {{ successMessage }}
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: "ResetPassword",
    data() {
      return {
        newPassword: '',
        confirmPassword: '',
        errors: {
          newPassword: '',
          confirmPassword: '',
        },
        errorMessage: '',
        successMessage: '',
        isLoading: false,
        resetToken: '',
      };
    },
    created() {
      // Extract the reset token from the URL query parameters
      this.resetToken = this.$route.query.token;
      if (!this.resetToken) {
        this.errorMessage = "Invalid reset link. Please check your email for the correct link.";
      }
    },
    methods: {
      validateForm() {
        this.errors = {};
  
        if (this.newPassword.length < 8) {
          this.errors.newPassword = "Password must be at least 8 characters long.";
        }
        if (this.newPassword !== this.confirmPassword) {
          this.errors.confirmPassword = "Passwords do not match.";
        }
  
        return Object.keys(this.errors).length === 0;
      },
      async handleResetPassword() {
        if (!this.validateForm()) return;
  
        this.isLoading = true;
        this.errorMessage = '';
        this.successMessage = '';
  
        try {
          const response = await axios.post(
            'http://127.0.0.1:5000/api/reset-password',
            {
              token: this.resetToken,
              new_password: this.newPassword,
            }
          );
  
          if (response.status === 200) {
            this.successMessage = "Password reset successfully! You can now login with your new password.";
          } else {
            this.errorMessage = "Failed to reset password. Please try again.";
          }
        } catch (error) {
          console.error("Error resetting password:", error);
          this.errorMessage = error.response?.data?.error || "An unexpected error occurred. Please try again.";
        } finally {
          this.isLoading = false;
        }
      },
    },
  };
  </script>
  
  <style scoped>
  </style>