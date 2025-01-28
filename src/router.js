// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';

// Import your components (views)
import LoginForm from "@/components/LoginForm.vue";
import SignupForm from './components/Signup.vue';
import Forgotpassword from './components/Forgotpassword.vue';

const routes = [
    {
        path: '/',
        name: 'login',
        component: LoginForm,
    },
    {
        path: '/signup',
        name: 'signup',
        component: SignupForm,
    },
    {
        path:'/forgotpassword',
        name:'forgotpassword',
        component:Forgotpassword,
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
