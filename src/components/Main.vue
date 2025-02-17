<template>
    <div class="min-h-screen bg-gray-100" @dblclick="toggleChat">
        <!-- Header with Chat Icon -->
        <header class="bg-white shadow-sm fixed w-full top-0 z-50">
            <div class="container mx-auto px-4 py-3 flex justify-between items-center">
                <h1
                    class="text-2xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                    Campus Connect
                </h1>

                <!-- Chat Icon -->
                <button @click="toggleChat" class="relative p-2 hover:bg-gray-100 rounded-full transition-colors">
                    <i class="fas fa-comment-dots text-2xl text-purple-600"></i>
                    <span v-if="unreadMessages"
                        class="absolute -top-1 -right-1 bg-red-500 text-white rounded-full w-5 h-5 text-xs flex items-center justify-center animate-bounce">
                        {{ unreadMessages }}
                    </span>
                </button>
            </div>
        </header>

        <!-- Main Feed -->
        <main class="container mx-auto px-4 pt-20 pb-8">
            <!-- Post Creation -->
            <div class="mb-6 bg-white rounded-xl shadow-md p-4">
                <div class="flex items-center space-x-3">
                    <img :src="currentUser.avatar"
                        class="w-10 h-10 rounded-full object-cover border-2 border-purple-200">
                    <input v-model="newPost" placeholder="What's happening on campus?"
                        class="flex-1 p-2 bg-gray-50 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-200"
                        @keyup.enter="createPost">
                    <button @click="createPost"
                        class="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition-colors">
                        Post
                    </button>
                </div>
            </div>

            <!-- Posts Grid -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <div v-for="post in posts" :key="post.id"
                    class="bg-white rounded-xl shadow-md overflow-hidden transform transition hover:scale-105 post">
                    <!-- Post Header -->
                    <div class="flex items-center p-4 border-b">
                        <img :src="post.user.avatar" class="w-8 h-8 rounded-full mr-3">
                        <span class="font-semibold">{{ post.user.name }}</span>
                    </div>

                    <!-- Post Image -->
                    <img :src="post.image" class="w-full h-64 object-cover">

                    <!-- Post Actions -->
                    <div class="p-4">
                        <div class="flex space-x-4 mb-2">
                            <button @click="toggleLike(post)"
                                class="flex items-center space-x-1 text-red-500 like-button">
                                <i :class="post.liked ? 'fas fa-heart' : 'far fa-heart'" class="text-xl"></i>
                                <span>{{ post.likes }}</span>
                            </button>
                            <button class="flex items-center space-x-1 text-gray-600">
                                <i class="far fa-comment text-xl"></i>
                                <span>{{ post.comments.length }}</span>
                            </button>
                        </div>

                        <!-- Post Caption -->
                        <p class="text-gray-800">
                            <span class="font-semibold">{{ post.user.name }}</span>
                            {{ post.caption }}
                        </p>
                    </div>
                </div>
            </div>
        </main>

        <!-- Chat Sidebar -->
        <div v-show="showChat" ref="chatSidebar" class="fixed right-0 top-0 h-screen w-80 bg-white shadow-xl z-50">
            <div class="p-4 border-b">
                <h2 class="text-xl font-semibold">Chats</h2>
            </div>

            <!-- Chat List -->
            <div class="overflow-y-auto h-full">
                <div v-for="chat in chats" :key="chat.id" class="p-4 hover:bg-gray-50 cursor-pointer border-b">
                    <div class="flex items-center space-x-3" @click="chatroom">
                        <img :src="chat.user.avatar" class="w-10 h-10 rounded-full">
                        <div>
                            <h3 class="font-semibold">{{ chat.user.name }}</h3>
                            <p class="text-sm text-gray-500 truncate">{{ chat.lastMessage }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import anime from "animejs";
// import axios from "axios";
// import { url1 } from "./data/url";

export default {
    name: "MainPage",
    data() {
        return {
            showChat: false,
            unreadMessages: 0,
            newPost: "",
            currentUser: {
                name: "Abhay Singh",
                avatar: "https://source.unsplash.com/random/100x100/?face"
            },
            posts: [
                {
                    id: 1,
                    user: {
                        name: "TechFusion Club",
                        avatar: "https://source.unsplash.com/random/100x100/?face"
                    },
                    image: "https://source.unsplash.com/random/800x600/?campus",
                    caption: "Amazing tech fest happening this weekend!",
                    likes: 42,
                    liked: false,
                    comments: []
                },
                {
                    id: 2,
                    user: {
                        name: "TechFusion Club",
                        avatar: "https://source.unsplash.com/random/100x100/?face"
                    },
                    image: "https://source.unsplash.com/random/800x600/?college",
                    caption: "HAckathon coming soon!",
                    likes: 28,
                    liked: true,
                    comments: []
                }
            ],
            chats: [
                {
                    id: 1,
                    user: {
                        name: "CLub",
                        avatar: "https://source.unsplash.com/random/100x100/?face"
                    },
                    lastMessage: "Click ME! to enter the chatroom",
                    messages: []
                }
            ]
        };
    },
    methods: {
        createPost() {
            if (this.newPost.trim()) {
                this.posts.unshift({
                    id: Date.now(),
                    user: this.currentUser,
                    image: "https://source.unsplash.com/random/800x600/?campus",
                    caption: this.newPost,
                    likes: 0,
                    liked: false,
                    comments: []
                });
                this.newPost = "";
                this.animatePosts();
            }
        },
        checkmesseage() {
            for (let i = 0; i < this.chats.length; i++) {
                this.unreadMessages = this.unreadMessages + 1;
            }
        },
        chatroom() {
            this.$router.push("/chatroom");
        },
        toggleLike(post) {
            post.liked = !post.liked;
            post.likes += post.liked ? 1 : -1;
            anime({
                targets: ".like-button",
                scale: [1, 1.2, 1],
                duration: 300,
                easing: "easeOutElastic"
            });
        },
        toggleChat() {
            this.showChat = !this.showChat;
            anime({
                targets: this.$refs.chatSidebar,
                translateX: this.showChat ? [300, 0] : [0, 300],
                duration: 500,
                easing: "easeInOutQuad"
            });
        },
        animatePosts() {
            anime({
                targets: ".post",
                opacity: [0, 1],
                translateY: [50, 0],
                duration: 500,
                easing: "easeOutExpo",
                delay: anime.stagger(100)
            });
        },
        // getchats(){
        //     axios.post(`${url1}/chats${this.currentUser}`).then((response) => {
        //         this.chats = response.data;
        //     });
        // }
    },
    mounted() {
        this.animatePosts();
        this.checkmesseage();
        // this.getchats();
    }
};
</script>

<style>
/* Custom scrollbar */
::-webkit-scrollbar {
    width: 6px;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
    background: #888;
    border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
    background: #555;
}
</style>