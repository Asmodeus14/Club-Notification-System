<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-r from-purple-600 to-blue-500">
    <div class="w-96 bg-white bg-opacity-10 p-8 rounded-lg shadow-lg backdrop-blur-lg">
      <h1 class="text-3xl text-white text-center mb-4">Welcome Back</h1>
      <p class="text-white text-center mb-2">Login | Signup</p>

      <form @submit.prevent="createpost">
        <input type="text" id="ID" placeholder="ID"
          class="w-full p-4 mb-4 bg-transparent border border-white rounded-xl text-white placeholder-white focus:outline-none"
          v-model="formdata.ID">

        <div class="flex items-center mb-4">
          <input type="password" id="password" placeholder="Password"
            class="w-full p-4 mr-2 bg-transparent border border-white rounded-xl text-white placeholder-white focus:outline-none"
            v-model="formdata.password">
          <img :src="eyeIcon" alt="eye-icon" @click="togglePasswordVisibility" class="w-8 h-8 cursor-pointer">
        </div>


        <span class="text-white block text-center mb-4">
          <router-link to="/forgotpassword" class="text-white">Forgot Password?</router-link>
        </span>

        <div class="flex justify-center space-x-4 mb-4">
          <button
            class="w-1/2 py-2 bg-transparent border-2 border-white text-white rounded-xl hover:bg-black hover:bg-opacity-20 transition duration-300">Login</button>
          <button
            class="w-1/2 py-2 bg-transparent border-2 border-white text-white rounded-xl hover:bg-black hover:bg-opacity-20 transition duration-300">
            <router-link to="/signup" class="text-white">Signup</router-link>
          </button>
        </div>
      </form>

      <div class="text-center text-white">
        <p>For registering in <a href="https://srmu.ac.in/clubs" class="underline">Clubs</a></p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: "LoginForm",
  data() {
    return {
      formdata: {
        ID: '',
        password: '',
      },
      isPasswordVisible: false,
    }
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
      const passwordField = document.getElementById('password');
      passwordField.type = this.isPasswordVisible ? 'text' : 'password';
    },
    createpost() {
  axios
    .post('http://127.0.0.1:5000/api/login', new URLSearchParams(this.formdata), {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
    .then((response) => {
      console.log(response);
    })
    .catch((error) => {
      console.log(error);
    });
}

    
  },
};

</script>
