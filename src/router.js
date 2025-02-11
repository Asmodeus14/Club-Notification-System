// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';

// Import your components (views)
import LoginForm from "@/components/LoginForm.vue";
import SignupForm from './components/Signup.vue';
import Forgotpassword from './components/Forgotpassword.vue';
import AdministratorManager from './components/Dashboard.vue';
import ResetPassword from './components/ResetPassword.vue';
import HomePage from './components/Home.vue';
import ClubsPage from './components/Clubs.vue';
import ClubSignFrom from './components/ClubSignFrom.vue';
import MainPage from './components/Main.vue';
import ChatRoom from './components/ChatRoom.vue';

const routes = [
    {
        path:'/',
        name:'Home-Page',
        component:HomePage,
    },
    {
        path:'/main',
        name:'Main-Page',
        component:MainPage,
    },
    {
        path:'/chatroom',
        name:'ChatRoom',
        component:ChatRoom,
    },
    {
        path: '/login',
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
    },
    {
        path:'/dashboard/:user_id',  // Route expects u_id
        props:true,
        name:'Dashboard',
        component:AdministratorManager,
    },
    {
        path:'/reset-password',
        props:true,
        name:'ResetPassword',
        component:ResetPassword,
        
    },
    {
        path:'/Clubs',
        name:"ClubPage",
        component:ClubsPage
    },
    {
        path:'/ClubFrom',
        name:"ClubForm",
        component:ClubSignFrom
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
