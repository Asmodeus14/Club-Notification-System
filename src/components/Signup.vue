<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-r from-purple-600 to-blue-500 px-4">
    <div class="w-full max-w-md bg-white bg-opacity-10 p-8 rounded-2xl shadow-2xl backdrop-blur-lg">
      <h1 class="text-3xl font-bold text-white text-center mb-2">Create an Account</h1>
      <p class="text-white text-center mb-6">Join us today!</p>

      <form @submit.prevent="submitForm">
        <!-- ID -->
        <div class="relative mb-6">
          <input 
            type="text" 
            id="id"
            v-model="formdata.id"
            required
            class="peer w-full p-4 bg-transparent border border-white rounded-xl text-white placeholder-transparent focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
            placeholder="User ID"
          />
          <label 
            for="id"
            class="absolute left-4 top-4 text-white text-opacity-80 transition-all peer-placeholder-shown:top-5 peer-placeholder-shown:text-lg peer-placeholder-shown:text-opacity-50 peer-focus:top-2 peer-focus:text-sm peer-focus:text-opacity-100"
          >User ID</label>
        </div>

        <!-- Email -->
        <div class="relative mb-6">
          <input 
            type="email" 
            id="email"
            v-model="formdata.email"
            required
            class="peer w-full p-4 bg-transparent border border-white rounded-xl text-white placeholder-transparent focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
            placeholder="Email"
          />
          <label 
            for="email"
            class="absolute left-4 top-4 text-white text-opacity-80 transition-all peer-placeholder-shown:top-5 peer-placeholder-shown:text-lg peer-placeholder-shown:text-opacity-50 peer-focus:top-2 peer-focus:text-sm peer-focus:text-opacity-100"
          >Email</label>
        </div>

        <!-- Name -->
        <div class="relative mb-6">
          <input 
            type="text" 
            id="name"
            v-model="formdata.name"
            required
            class="peer w-full p-4 bg-transparent border border-white rounded-xl text-white placeholder-transparent focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
            placeholder="Name"
          />
          <label 
            for="name"
            class="absolute left-4 top-4 text-white text-opacity-80 transition-all peer-placeholder-shown:top-5 peer-placeholder-shown:text-lg peer-placeholder-shown:text-opacity-50 peer-focus:top-2 peer-focus:text-sm peer-focus:text-opacity-100"
          >Full Name</label>
        </div>

        <!-- Club -->
        <div class="relative mb-6">
          <input 
            type="text" 
            id="club"
            v-model="formdata.club"
            required
            class="peer w-full p-4 bg-transparent border border-white rounded-xl text-white placeholder-transparent focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
            placeholder="Club"
          />
          <label 
            for="club"
            class="absolute left-4 top-4 text-white text-opacity-80 transition-all peer-placeholder-shown:top-5 peer-placeholder-shown:text-lg peer-placeholder-shown:text-opacity-50 peer-focus:top-2 peer-focus:text-sm peer-focus:text-opacity-100"
          >Club</label>
        </div>

        <!-- Course -->
        <div class="relative mb-6">
          <input 
            type="text" 
            id="course"
            v-model="formdata.course"
            required
            class="peer w-full p-4 bg-transparent border border-white rounded-xl text-white placeholder-transparent focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
            placeholder="Course"
          />
          <label 
            for="course"
            class="absolute left-4 top-4 text-white text-opacity-80 transition-all peer-placeholder-shown:top-5 peer-placeholder-shown:text-lg peer-placeholder-shown:text-opacity-50 peer-focus:top-2 peer-focus:text-sm peer-focus:text-opacity-100"
          >Course</label>
        </div>

        <!-- Password with Toggle -->
        <div class="relative mb-6">
          <input 
            :type="isPasswordVisible ? 'text' : 'password'" 
            id="password"
            v-model="formdata.password"
            required
            class="peer w-full p-4 bg-transparent border border-white rounded-xl text-white placeholder-transparent focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
            placeholder="Password"
          />
          <label 
            for="password"
            class="absolute left-4 top-4 text-white text-opacity-80 transition-all peer-placeholder-shown:top-5 peer-placeholder-shown:text-lg peer-placeholder-shown:text-opacity-50 peer-focus:top-2 peer-focus:text-sm peer-focus:text-opacity-100"
          >Password</label>
          <img 
            :src="eyeIcon" 
            alt="eye-icon" 
            @click="togglePasswordVisibility" 
            class="absolute right-4 top-4 w-6 h-6 cursor-pointer opacity-80 hover:opacity-100 transition"
          />
        </div>

        <!-- Position -->
        <div class="relative mb-6">
          <select 
            v-model="formdata.position"
            required
            class="w-full p-4 bg-transparent border border-white rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-blue-400 transition cursor-pointer"
          >
            <option value="" disabled selected>Position</option>
            <option value="Vetran-Coordinator">Veteran Coordinator</option>
            <option value="Assistant-Coordinator">Assistant Coordinator</option>
            <option value="Student-Coordinator">Student Coordinator</option>
          </select>
        </div>

        <!-- Submit Button -->
        <button 
          type="submit"
          :disabled="isSubmitting"
          class="w-full py-3 bg-blue-600 text-white font-semibold rounded-xl shadow-md hover:bg-blue-700 transition-all"
        >
          {{ isSubmitting ? "Submitting..." : "Sign Up" }}
        </button>

        <!-- Success Message -->
        <p v-if="submissionSuccess" class="text-white text-center mt-4">Form submitted successfully! Redirecting...</p>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "SignupForm",
  data() {
    return {
      formdata: {
        id: "",
        email: "",
        name: "",
        club: "",
        course: "",
        password: "",
        position: "",
      },
      isPasswordVisible: false,
      isSubmitting: false,
      submissionSuccess: false,
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
    async submitForm() {
      this.isSubmitting = true;
      try {
        await axios.post('http://127.0.0.1:5000/api/register', new URLSearchParams(this.formdata), {
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        });
        this.submissionSuccess = true;
        setTimeout(() => {
          this.$router.push("/");
        }, 2000);
      } catch (error) {
        console.error("Submission failed", error);
      } finally {
        this.isSubmitting = false;
      }
    },
  },
};
</script>
