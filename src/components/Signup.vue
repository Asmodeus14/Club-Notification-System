<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-r from-purple-600 to-blue-500 px-4">
    <div class="w-full max-w-md bg-white bg-opacity-10 p-8 rounded-2xl shadow-2xl backdrop-blur-lg">
      <h1 class="text-3xl font-bold text-white text-center mb-2">Create an Account</h1>
      <p class="text-white text-center mb-6">Join us today!</p>

      <form @submit.prevent="submitForm">
        <!-- ID -->
        <div class="relative mb-6">
          <input type="text" id="id" v-model="formdata.id" required
            class="peer w-full p-4 bg-transparent border border-white rounded-xl text-white placeholder-transparent focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
            placeholder="User ID" />
          <label for="id"
            class="absolute left-4 top-4 text-white text-opacity-0 transition-all peer-placeholder-shown:top-4 peer-placeholder-shown:text-lg peer-placeholder-shown:text-opacity-50 peer-focus:top-0 peer-focus:text-sm peer-focus:text-opacity-100">User
            ID</label>
        </div>

        <!-- Email -->
        <div class="relative mb-6">
          <input type="email" id="email" v-model="formdata.email" required
            class="peer w-full p-4 bg-transparent border border-white rounded-xl text-white placeholder-transparent focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
            placeholder="Email" />
          <label for="email"
            class="absolute left-4 top-4 text-white text-opacity-0 transition-all peer-placeholder-shown:top-4 peer-placeholder-shown:text-lg peer-placeholder-shown:text-opacity-50 peer-focus:top-0 peer-focus:text-sm peer-focus:text-opacity-100">Email</label>
        </div>

        <!-- Name -->
        <div class="relative mb-6">
          <input type="text" id="name" v-model="formdata.name" required
            class="peer w-full p-4 bg-transparent border border-white rounded-xl text-white placeholder-transparent focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
            placeholder="Name" />
          <label for="name"
            class="absolute left-4 top-4 text-white text-opacity-0 transition-all peer-placeholder-shown:top-4 peer-placeholder-shown:text-lg peer-placeholder-shown:text-opacity-50 peer-focus:top-0 peer-focus:text-sm peer-focus:text-opacity-100">Full
            Name</label>
        </div>

        <!-- Club -->
        <div class="relative mb-6">
          <select v-model="formdata.club" id="clubs" required
            class="w-full p-4 bg-stone-800 border border-white rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-blue-400 transition cursor-pointer">
            <option disabled selected value="">-- Select a Club --</option>

            <optgroup label="Art and Culture">
              <option v-for="club in artAndCultureClubs" :key="club" :value="club">{{ club }}</option>
            </optgroup>

            <optgroup label="Photography">
              <option v-for="club in photographyClubs" :key="club" :value="club">{{ club }}</option>
            </optgroup>

            <optgroup label="Music">
              <option v-for="club in musicClubs" :key="club" :value="club">{{ club }}</option>
            </optgroup>

            <optgroup label="Psychology">
              <option v-for="club in psychologyClubs" :key="club" :value="club">{{ club }}</option>
            </optgroup>

            <optgroup label="Business and Consultancy">
              <option v-for="club in businessClubs" :key="club" :value="club">{{ club }}</option>
            </optgroup>

            <optgroup label="Sports">
              <option v-for="club in sportsClubs" :key="club" :value="club">{{ club }}</option>
            </optgroup>

            <optgroup label="Social Initiatives">
              <option v-for="club in socialInitiativesClubs" :key="club" :value="club">{{ club }}</option>
            </optgroup>
          </select>
        </div>

        <!-- Course -->
        <div class="relative mb-6">

          <select v-model="formdata.course" id="courses" required 
            class="w-full p-4 bg-stone-800 border border-white rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-blue-400 transition cursor-pointer">
            <option disabled selected value="">--Select a Course--</option>

            <optgroup label="Undergraduate Programs">
              <option v-for="course in undergraduateCourses" :key="course" :value="course">{{ course }}</option>
            </optgroup>

            <optgroup label="Postgraduate Programs">
              <option v-for="course in postgraduateCourses" :key="course" :value="course">{{ course }}</option>
            </optgroup>

            <optgroup label="Diploma Programs">
              <option v-for="course in diplomaCourses" :key="course" :value="course">{{ course }}</option>
            </optgroup>
          </select>
        </div>

        <!-- Password with Toggle -->
        <div class="relative mb-6">
          <input :type="isPasswordVisible ? 'text' : 'password'" id="password" v-model="formdata.password" required
            class="peer w-full p-4 bg-transparent border border-white rounded-xl text-white placeholder-transparent focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
            placeholder="Password" />
          <label for="password"
            class="absolute left-4 top-4 text-white text-opacity-0 transition-all peer-placeholder-shown:top-4 peer-placeholder-shown:text-lg peer-placeholder-shown:text-opacity-50 peer-focus:top-0 peer-focus:text-sm peer-focus:text-opacity-100">Password</label>
          <img :src="eyeIcon" alt="eye-icon" @click="togglePasswordVisibility"
            class="absolute right-4 top-4 w-6 h-6 cursor-pointer opacity-80 hover:opacity-100 transition" />
        </div>

        <!-- Position -->
        <div class="relative mb-6">
          <select v-model="formdata.position" required
            class="w-full p-4 bg-stone-800 border border-white rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-blue-400 transition cursor-pointer">
            <option value="" disabled selected>--Select Your Postion--</option>
            <option value="Vetran-Coordinator">Veteran Coordinator</option>
            <option value="Assistant-Coordinator">Assistant Coordinator</option>
            <option value="Student-Coordinator">Student Coordinator</option>
          </select>
        </div>

        <!-- Submit Button -->
        <button type="submit" :disabled="isSubmitting"
          class="w-full py-3 bg-blue-600 text-white font-semibold rounded-xl shadow-md hover:bg-blue-700 transition-all">
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
      undergraduateCourses: [
        'B.Tech. in Computer Science Engineering',
        'B.Tech. in Electrical Engineering',
        'B.Tech. in Mechanical Engineering',
        'B.Tech. in Civil Engineering',
        'B.Tech. in Biotechnology',
        'B.Tech. in Biotechnology (Lateral Entry)',
        'B.Tech. in Biotechnology + M.B.A. (Integrated)',
        'BCA (Bachelor of Computer Applications)',
        'BBA (Bachelor of Business Administration)',
        'BBA with specialization in Business Analytics',
        'BBA with specialization in Digital Banking & Fintech',
        'B.Com. (Bachelor of Commerce)',
        'B.Com. (Hons.)',
        'BA + LLB (Integrated)',
        'BBA + LLB (Hons.) (Integrated)',
        'LLB (Bachelor of Law)',
        'B.Pharm. (Bachelor of Pharmacy)',
        'D.Pharm. (Diploma in Pharmacy)',
        'B.Sc. (Hons.) in Agriculture',
        'B.Sc. (Hons.) in Biotechnology',
        'B.Sc. (Hons.) in Microbiology',
        'B.Sc. (Hons.) in Food Technology',
        'B.A. (Hons.) in English',
        'B.A. (Hons.) in Political Science',
        'B.A. (Hons.) in Sociology',
        'B.A. (Hons.) in Applied Psychology',
        'B.A. (Hons.) in Economics',
        'B.A. (Hons.) in Journalism & Mass Communication',
        'B.Ed. (Bachelor of Education)',
      ],
      postgraduateCourses: [
        'MBA (Master of Business Administration)',
        'MBA with specialization in Business Analytics',
        'MBA with specialization in Healthcare and Hospital Management',
        'MBA with specialization in Agribusiness Management',
        'LLM in Corporate & Commercial Law',
        'LLM in Criminal & Security Law',
        'LLM in Constitutional & Administrative Law',
        'LLM in International & Comparative Law',
        'M.Sc. in Biotechnology',
        'M.Sc. in Environmental Science',
        'M.Sc. in IT',
        'M.Sc. in Mathematics',
        'M.Sc. in Chemistry',
        'M.Sc. in Physics',
        'MSW (Master in Social Work)',
        'Master in Public Health (MPH)',
      ],
      diplomaCourses: [
        'Diploma in Civil Engineering (Lateral Entry)',
        'Diploma in Mechanical Engineering (Production) (Lateral Entry)',
        'Diploma in Mechanical Engineering (Automobile) (Lateral Entry)',
      ],
      artAndCultureClubs: [
        'Srijan Club',
        'Expressions',
        'Spic Macay',
      ],
      photographyClubs: [
        'Snapshot',
      ],
      musicClubs: [
        'Sur Jhankar',
        'Beat the Beats',
      ],
      psychologyClubs: [
        'Positive Psychology',
      ],
      businessClubs: [
        'Business Consultancy',
        'Business Buzz',
      ],
      sportsClubs: [
        'Sportizz',
      ],
      socialInitiativesClubs: [
        'Power Angels',
        'Ozone',
        'Golden Pen',
        'Razzmatazz',
        'Manch',
      ],
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
        await axios
        .post('http://127.0.0.1:5000/api/register', new URLSearchParams(this.formdata), {
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        }).then(response => console.log(response))
        .catch(error => console.log(error.response));
        
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
