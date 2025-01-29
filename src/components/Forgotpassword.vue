<template>
    <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-700 via-blue-600 to-indigo-900 px-4">
      <div class="w-full max-w-md bg-white bg-opacity-10 p-6 rounded-2xl shadow-lg backdrop-blur-md border border-white border-opacity-20">
        <h1 class="text-3xl font-semibold text-white text-center mb-4">Forgot Password</h1>
        <p class="text-white text-center text-sm mb-6">Enter your email and ID to reset your password</p>
  
        <form @submit.prevent="forgotpassword" class="flex flex-col space-y-5">
          <!-- Email Input -->
          <div class="relative">
            <input 
              type="email"
              placeholder="Enter your email"
              class="w-full p-3 rounded-xl border border-white text-white bg-transparent placeholder-white focus:ring-2 focus:ring-blue-300 focus:outline-none transition-all duration-300"
              v-model="formdata.email"
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
              v-model="formdata.id"
              required
            />
            <span v-if="errors.id" class="text-red-400 text-sm absolute -bottom-5 left-2">{{ errors.id }}</span>
          </div>
  
          <!-- Submit Button -->
          <button 
            type="submit"
            class="w-full py-3 bg-white text-blue-900 font-semibold rounded-xl shadow-md hover:bg-blue-200 transition-all duration-300">
            Reset Password
          </button>
        </form>
  
        <!-- Back to Login -->
        <div class="text-center text-white mt-4 text-sm">
          <p>Remember your password? <router-link to="/" class="underline hover:text-blue-300">Login</router-link></p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: "ForgotPassword",
    data() {
      return {
        formdata: {
          email: '',
          id: '',
        },
        errors: {
          email: '',
          id: '',
        },
      };
    },
    methods: {
      forgotpassword() {
        this.errors = {}; // Reset errors
  
        // Basic validation
        if (!this.formdata.email.includes('@')) {
          this.errors.email = "Enter a valid email address";
        }
        if (this.formdata.id.length < 3) {
          this.errors.id = "ID must be at least 3 characters long";
        }
  
        // If validation fails, stop request
        if (Object.keys(this.errors).length > 0) return;
  
        axios
          .post('http://127.0.0.1:5000/api/forgot', new URLSearchParams(this.formdata), {
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded'
            }
          })
          .then((response) => {
            console.log("Success:", response);
            alert("A password reset link has been sent to your email!");
          })
          .catch((error) => {
            console.error("Error:", error);
            alert("Failed to process your request. Please try again.");
          });
      },
    },
  };
  </script>
