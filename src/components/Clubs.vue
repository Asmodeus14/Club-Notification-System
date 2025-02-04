<template>
    <div class="min-h-screen bg-gradient-to-br from-gray-900 via-indigo-900 to-purple-900 p-6">
        <!-- Animated Header -->
        <h1
            class="text-5xl font-bold text-center text-transparent bg-clip-text bg-gradient-to-r from-yellow-400 to-orange-500 mb-12 animate-fade-in-down">
            Explore Our Clubs
        </h1>

        <!-- Club Categories Grid -->
        <div class="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-8">
            <!-- Category Card -->
            <div v-for="(clubs, category) in clubCategories" :key="category" class="group relative animate-fade-in-up">
                <!-- Category Header -->
                <div class="flex items-center mb-6 border-l-4 border-indigo-400 pl-4">
                    <div class="flex-1">
                        <h2 class="text-2xl font-bold text-white">
                            {{ formatCategory(category) }}
                        </h2>
                        <div class="h-1 bg-gradient-to-r from-indigo-500 to-purple-500 w-24 mt-2 rounded-full"></div>
                    </div>
                    <div class="ml-4 p-3 bg-white bg-opacity-10 rounded-full">
                        <i class="fas fa-users text-indigo-400 text-xl"></i>
                    </div>
                </div>

                <!-- Club Cards -->
                <div v-for="club in clubs" :key="club"
                    class="glass-card transform transition-all duration-300 hover:-translate-y-2 hover:shadow-2xl mb-4">
                    <div class="p-6">
                        <h3 class="text-xl font-semibold text-white mb-2">{{ club }}</h3>
                        <p class="text-gray-300 text-sm mb-4">Explore exciting opportunities with {{ club }}</p>
                        <button
                            class="club-button bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg transition-all"
                            @click="joinClub(club)">
                            Join Now
                            <i
                                class="fas fa-arrow-right ml-2 transform group-hover:translate-x-1 transition-transform"></i>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ClubPage',
    data() {
        return {
            clubCategories: {
                'artAndCultureClubs': ['Srijan Club', 'Expressions', 'Spic Macay'],
                'photographyClubs': ['Snapshot'],
                'musicClubs': ['Sur Jhankar', 'Beat the Beats'],
                'psychologyClubs': ['Positive Psychology'],
                'businessClubs': ['Business Consultancy', 'Business Buzz'],
                'sportsClubs': ['Sportizz'],
                'socialInitiativesClubs': ['Power Angels', 'Ozone', 'Golden Pen', 'Razzmatazz', 'Manch']
            }
        };
    },
    methods: {
        formatCategory(category) {
            return category
                .replace(/([A-Z])/g, ' $1')
                .replace(/^./, str => str.toUpperCase())
                .replace(' Clubs', '');
        },
        joinClub(club) {
            console.log(`Joining ${club}`);
            this.$router.push('/ClubFrom')
        }
    }
};
</script>

<style>
/* Glassmorphism Effect */
.glass-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
}

/* Animations */
@keyframes fade-in-down {
    0% {
        opacity: 0;
        transform: translateY(-20px);
    }

    100% {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes fade-in-up {
    0% {
        opacity: 0;
        transform: translateY(20px);
    }

    100% {
        opacity: 1;
        transform: translateY(0);
    }
}

.animate-fade-in-down {
    animation: fade-in-down 0.6s ease-out;
}

.animate-fade-in-up {
    animation: fade-in-up 0.6s ease-out;
}

/* Hover Effects */
.glass-card:hover {
    box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
}

.club-button:hover i {
    transform: translateX(3px);
}

.group:hover .fa-users {
    transform: rotate(360deg);
    transition: transform 0.6s ease;
}
</style>