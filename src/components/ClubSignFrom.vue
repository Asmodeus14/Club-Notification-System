<template>
    <div
        class="min-h-screen bg-gradient-to-br from-gray-900 via-indigo-900 to-purple-900 flex items-center justify-center p-4">
        <form @submit.prevent="handleSubmit" class="glass-form w-full max-w-2xl">
            <h2 class="form-title">Club Registration Form</h2>

            <!-- Name Input -->
            <div class="form-group">
                <label>Full Name</label>
                <input v-model="formData.name" type="text" placeholder="Enter your full name" @blur="v$.name.$touch">
                <span v-if="v$.name.$error" class="error-message">
                    Please enter your full name
                </span>
            </div>

            <!-- ID Number Input -->
            <div class="form-group">
                <label>Student ID Number</label>
                <input v-model="formData.studentId" type="text" placeholder="Enter your student ID"
                    @blur="v$.studentId.$touch">
                <span v-if="v$.studentId.$error" class="error-message">
                    Valid student ID is required
                </span>
            </div>

            <!-- Email Input -->
            <div class="form-group">
                <label>Email Address</label>
                <input v-model="formData.email" type="email" placeholder="student@college.edu" @blur="v$.email.$touch">
                <span v-if="v$.email.$error" class="error-message">
                    Valid email address is required
                </span>
            </div>

            <!-- Year of Study -->
            <div class="form-group">
                <label>Year of Study</label>
                <select v-model="formData.year" @change="v$.year.$touch">
                    <option value="" disabled>Select your current year</option>
                    <option v-for="year in academicYears" :key="year" :value="year">
                        {{ year }} Year
                    </option>
                </select>
                <span v-if="v$.year.$error" class="error-message">
                    Please select your current year
                </span>
            </div>

            <!-- Club Selection -->
            <div class="form-group">
                <label>Select Club</label>
                <select v-model="formData.club" @change="v$.club.$touch" class="capitalize">
                    <option value="" disabled>Choose a club</option>
                    <optgroup v-for="(clubs, category) in clubCategories" :key="category"
                        :label="formatCategory(category)">
                        <option v-for="club in clubs" :key="club" :value="club">
                            {{ club }}
                        </option>
                    </optgroup>
                </select>
                <span v-if="v$.club.$error" class="error-message">
                    Please select a club to join
                </span>
            </div>

            <!-- Notification Consent -->
            <div class="form-group checkbox-group">
                <label class="checkbox-label">
                    <input type="checkbox" v-model="formData.notificationConsent" class="checkbox-input">
                    <span class="checkmark"></span>
                    I agree to receive notifications via email
                </label>
            </div>

            <!-- Form Actions -->
            <div class="form-actions">
                <button type="submit" class="submit-btn" :disabled="v$.$invalid || !formData.notificationConsent">
                    Register
                </button>
               
            </div>
        </form>
    </div>
</template>

<script>
import { useVuelidate } from '@vuelidate/core'
import { required, email, numeric } from '@vuelidate/validators'
import { clubCategories } from './data/club';
export default {
    name:"ClubFrom",
    setup() {
        return { v$: useVuelidate() }
    },
    data() {
        return {
            formData: {
                name: '',
                studentId: '',
                email: '',
                year: '',
                club: '',
                notificationConsent: false
            },
            academicYears: ['1st', '2nd', '3rd', '4th'],
            clubCategories:clubCategories
        }
    },
    validations() {
        return {
            formData: {
                name: { required },
                studentId: { required, numeric },
                email: { required, email },
                year: { required },
                club: { required }
            }
        }
    },
    methods: {
        formatCategory(category) {
            return category
                .replace(/([A-Z])/g, ' $1')
                .replace(/^./, str => str.toUpperCase())
                .replace(' Clubs', '')
        },
        handleSubmit() {
            if (!this.v$.$invalid && this.formData.notificationConsent) {
                console.log('Form Data:', this.formData)
                this.$router.push('/')
            }
        }
    }
}
</script>

<style scoped>
.glass-form {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    @apply p-8 rounded-2xl shadow-2xl;
}

.form-title {
    @apply text-3xl font-bold text-center text-white mb-8;
}

.form-group {
    @apply mb-6;
}

.form-group label {
    @apply block text-white mb-2 text-sm font-medium;
}

.form-group input,
.form-group select {
    @apply w-full px-4 py-3 bg-white bg-opacity-10 border border-white border-opacity-20 rounded-lg text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-400 transition-all;
}

.error-message {
    @apply text-red-400 text-sm mt-1 block;
}

.checkbox-group {
    @apply mt-8;
}

.checkbox-label {
    @apply flex items-center space-x-3 cursor-pointer text-white;
}

.checkbox-input {
    @apply hidden;
}

.checkmark {
    @apply w-5 h-5 border border-white border-opacity-30 rounded-sm flex items-center justify-center transition-all;
}

.checkbox-input:checked+.checkmark {
    @apply bg-indigo-500 border-indigo-500;
}

.checkbox-input:checked+.checkmark:after {
    content: '✓';
    @apply text-white text-sm;
}

.form-actions {
    @apply mt-8 space-y-4;
}

.submit-btn {
    @apply w-full py-3 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed;
}

.login-link {
    @apply block text-center text-gray-300 hover:text-white text-sm transition-colors mt-4;
}

/* Animations */
.glass-form {
    animation: slideUp 0.6s ease-out;
}

@keyframes slideUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>