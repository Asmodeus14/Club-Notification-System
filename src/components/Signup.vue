<template >
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-r from-purple-600 to-blue-500">
    <div class="flex flex-col w-1/2 p-5 bg-opacity-10 bg-gray-600 rounded-xl shadow-lg border-3 border-transparent ">
      <h1 class="text-3xl font-semibold text-white text-center mb-8">Signup Form</h1>
      <form @submit.prevent="submitForm" class="space-y-6">
        
        <!-- ID -->
        <div class="form-group flex flex-col items-center w-full mb-4">
          <input 
            type="text" 
            v-model="id" 
            id="id" 
            name="id" 
            required 
            placeholder="ID" 
            class="w-3/5 p-4 rounded-3xl border-2 border-white text-aliceblue bg-transparent transition-all duration-500 ease-in-out"
          />
        </div>
        
        <!-- Email -->
        <div class="form-group flex flex-col items-center w-full mb-4">
          <input 
            type="email" 
            v-model="email" 
            id="Email" 
            name="Email" 
            required 
            placeholder="Email" 
            class="w-3/5 p-4 rounded-3xl border-2 border-white text-aliceblue bg-transparent transition-all duration-500 ease-in-out"
          />
        </div>
        
        <!-- Name -->
        <div class="form-group flex flex-col items-center w-full mb-4">
          <input 
            type="text" 
            v-model="name" 
            id="name" 
            name="name" 
            required 
            placeholder="Name" 
            class="w-3/5 p-4 rounded-3xl border-2 border-white text-aliceblue bg-transparent transition-all duration-500 ease-in-out"
          />
        </div>
        
        <!-- Club -->
        <div class="form-group flex flex-col items-center w-full mb-4">
          <input 
            type="text" 
            v-model="club" 
            id="club" 
            name="club" 
            required 
            placeholder="Club" 
            class="w-3/5 p-4 rounded-3xl border-2 border-white text-aliceblue bg-transparent transition-all duration-500 ease-in-out"
          />
        </div>
        
        <!-- Course -->
        <div class="form-group flex flex-col items-center w-full mb-4">
          <input 
            type="text" 
            v-model="course" 
            id="course" 
            name="course" 
            required 
            placeholder="Course" 
            class="w-3/5 p-4 rounded-3xl border-2 border-white text-aliceblue bg-transparent transition-all duration-500 ease-in-out"
          />
        </div>
        
        <!-- Password -->
        <div class="form-group flex flex-row justify-center w-full mb-4 relative">
          <input 
            type="password" 
            v-model="password" 
            id="password" 
            name="password" 
            required 
            placeholder="Password" 
            class="w-1/2 p-4 rounded-3xl border-2 border-white text-aliceblue bg-transparent transition-all duration-500 ease-in-out"
          />
          <img 
            :src="eyeIcon"
            alt="eye-icon"
            @click="togglePasswordVisibility" 
            class="relative top-4 -right-4 cursor-pointer w-6 h-6 "
          />
        </div>

        <!-- Position -->
        <div class="form-group flex flex-col items-center w-full mb-4">
          <select 
            v-model="position" 
            id="position" 
            name="position"
            
            required 
            class="w-3/5 p-4 rounded-3xl border-2 border-white text-aliceblue bg-transparent transition-all duration-500 ease-in-out  cursor-pointer placeholder-white"
          >
            <option value="" disabled selected>Position</option>
            <option value="Vetran-Coordinator">Vetran-Coordinator</option>
            <option value="Asistant-Coordinator">Asistant-Coordinator</option>
            <option value="Student-Coordinator">Student-Coordinator</option>
          </select>
        </div>
        <span v-if="submissionSuccess" class="text-white text-center  ">
        Form submitted successfully!
        </span>
        <!-- Submit Button -->
        <div class="form-group flex justify-center">
          <button
            id="submit"
            :disabled="isSubmitting"
            type="submit" 
            class="w-1/5 py-3 mt-5 text-white bg-transparent border-2 border-gray-300 rounded-3xl font-bold transition-all duration-500 ease-in-out hover:bg-purple-700 hover:border-purple-700"
          >
            Submit
          </button>
        </div>
      </form>
      

    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      id: "",
      email: "",
      name: "",
      club: "",
      course: "",
      password: "",
      position: "",
      isPasswordVisible: false,
      isSubmitting: false,
      submissionSuccess: false,
    };
  },
  name: "SignupForm",
  computed: {
    
    eyeIcon() {
      return this.isPasswordVisible 
        ? require('@/assets/eye-open.png') 
        : require('@/assets/eye-close.png');
    },
  },
  methods: {
    submitForm() {
      this.submit();
    },
    togglePasswordVisibility() {
      this.isPasswordVisible = !this.isPasswordVisible;
      const passwordField = document.getElementById('password');
      passwordField.type = this.isPasswordVisible ? 'text' : 'password';
    },
    async submit() {
      this.isSubmitting = true;
      try {
        
        console.log("Form submitted", this.$data);
      } catch (error) {
        console.error("Submission failed", error);
      } finally {
        this.isSubmitting = false;
        this.submissionSuccess = true;
        document.getElementById("submit").textContent="Login";
        document.getElementById("submit").addEventListener("click",()=>{
          this.$router.push("/");
        });
      }
    },
  },
};
</script>

<style scoped>

img {
  transition: transform 0.2s ease-in-out;
}
img:hover {
  transform: scale(1.2);
}

</style>
