<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-r from-purple-600 to-blue-500 px-4">
    <form @submit.prevent="handleSubmit" class="w-full max-w-2xl p-8 rounded-2xl shadow-2xl 
            bg-white bg-opacity-10 backdrop-blur-lg border border-white border-opacity-20 animate-slide-up">

      <h2 class="text-3xl font-bold text-center text-white mb-8">Club Registration Form</h2>

      <!-- Name Input -->
      <div class="mb-6">
        <label class="block text-white mb-2 text-sm font-medium">Full Name</label>
        <input v-model="formData.name" type="text" placeholder="Enter your full name"
          class="w-full px-4 py-3 bg-white bg-opacity-10 border border-white border-opacity-20 rounded-lg text-white 
                              placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-400 transition-all" @blur="v$.name.$touch">
        <span v-if="v$.name.$error" class="text-red-400 text-sm mt-1 block">Please enter your full name</span>
      </div>

      <!-- ID Number Input -->
      <div class="mb-6">
        <label class="block text-white mb-2 text-sm font-medium">Student ID Number</label>
        <input v-model="formData.studentId" type="text" placeholder="Enter your student ID"
          class="w-full px-4 py-3 bg-white bg-opacity-10 border border-white border-opacity-20 rounded-lg text-white 
                              placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-400 transition-all" @blur="v$.studentId.$touch">
        <span v-if="v$.studentId.$error" class="text-red-400 text-sm mt-1 block">Valid student ID is required</span>
      </div>

      <!-- Email Input -->
      <div class="mb-6">
        <label class="block text-white mb-2 text-sm font-medium">Email Address</label>
        <input v-model="formData.email" type="email" placeholder="student@college.edu"
          class="w-full px-4 py-3 bg-white bg-opacity-10 border border-white border-opacity-20 rounded-lg text-white 
                              placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-400 transition-all" @blur="v$.email.$touch">
        <span v-if="v$.email.$error" class="text-red-400 text-sm mt-1 block">Valid email address is required</span>
      </div>

      <!-- Year of Study -->
      <div class="mb-6">
        <label class="block text-white mb-2 text-sm font-medium">Year of Study</label>
        <select v-model="formData.year"
          class="w-full px-4 py-3 bg-white bg-opacity-10 border border-white border-opacity-20 rounded-lg text-white 
                               placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-400 transition-all" @change="v$.year.$touch">
          <option value="" disabled>Select your current year</option>
          <option v-for="year in academicYears" :key="year" :value="year" class="text-black">{{ year }} Year</option>
        </select>
        <span v-if="v$.year.$error" class="text-red-400 text-sm mt-1 block">Please select your current year</span>
      </div>

      <!-- Club Selection -->
      <div class="mb-6">
        <label class="block text-white mb-2 text-sm font-medium">Select Club</label>
        <select v-model="formData.club"
          class="w-full px-4 py-3 bg-white bg-opacity-10 border border-white border-opacity-20 rounded-lg text-white 
                               placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-400 transition-all capitalize"
          @change="v$.club.$touch">
          <option value="" disabled>Choose a club</option>
          <optgroup v-for="(clubs, category) in clubCategories" :key="category" class="text-black"
            :label="formatCategory(category)">
            <option v-for="club in clubs" :key="club" :value="club" class="text-black">
              {{ club }}
            </option>
          </optgroup>
        </select>
        <span v-if="v$.club.$error" class="text-red-400 text-sm mt-1 block">Please select a club to join</span>
      </div>

      <!-- Notification Consent -->
      <div class="mt-8 flex items-center space-x-3 cursor-pointer text-white">
        <input type="checkbox" v-model="formData.notificationConsent" id="notificationConsent" class="hidden">
        <label for="notificationConsent" class="flex items-center">
          <span
            class="w-5 h-5 border border-white border-opacity-30 rounded-sm flex items-center justify-center transition-all"
            :class="{ 'bg-indigo-500 border-indigo-500': formData.notificationConsent }">
            <span v-if="formData.notificationConsent" class="text-white text-sm">✓</span>
          </span>
          <span class="ml-2">I agree to receive notifications via email</span>
        </label>
      </div>

      <!-- Form Actions -->
      <div class="mt-8">
        <button type="submit" class="w-full py-3 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 transition-colors 
                               disabled:opacity-50 disabled:cursor-not-allowed"
          :disabled="v$.$invalid ">
          Register
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import { reactive } from 'vue'
import { useVuelidate } from '@vuelidate/core'
import { required, email, numeric } from '@vuelidate/validators'
import { clubCategories } from './data/club'
import axios from 'axios';

export default {
  name: "ClubForm",
  setup() {
    const formData = reactive({
      name: '',
      studentId: '',
      email: '',
      year: '',
      club: '',
      notificationConsent: false
    })

    const rules = {
      name: { required },
      studentId: { required, numeric },
      email: { required, email },
      year: { required },
      club: { required }
    }

    const v$ = useVuelidate(rules, formData)

    return {
      formData,
      v$,
      academicYears: ['1st', '2nd', '3rd', '4th'],
      clubCategories
    }
  },
  methods: {
    formatCategory(category) {
      return category
        .replace(/([A-Z])/g, ' $1')
        .replace(/^./, str => str.toUpperCase())
        .replace(' Clubs', '')
    },
    async handleSubmit() {
      const isValid = await this.v$.$validate();
      if (isValid ) {
        try {
          const response = await axios.post("http://127.0.0.1:5000/api/ClubForm", this.formData);
  
          if (response.status==200){
            this.$router.push('/');}
          
        } catch (error) {
          console.error('Error submitting form:', error);
          // Handle the error appropriately (e.g., show an error message)
        }
      } else {
        console.log("Validation failed or notification consent not provided.");
      }
    }
  }
}
</script>

<style scoped>
@keyframes slide-up {
  from {
    opacity: 0;
    transform: translateY(20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-slide-up {
  animation: slide-up 0.6s ease-out;
}
</style>
