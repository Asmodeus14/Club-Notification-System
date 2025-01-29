<template>
    <div class="min-h-screen min-w-screen flex items-center justify-center bg-gradient-to-r from-purple-600 to-blue-500">
        <div
            class="w-96 h-96 bg-white bg-opacity-10 p-5 rounded-lg shadow-lg backdrop-blur-lg "
            >
            <h1 class="text-3xl font-semibold text-white text-center mb-8">Forgot Password</h1>
            <form action="" method="post" class="  flex flex-col items-center p-9">

                <div class="form flex flex-col items-center w-full space-y-6">
                    <input type="text"
                        class=" w-full p-4 rounded-3xl border-2 border-white text-aliceblue bg-transparent transition-all duration-500 ease-in-out"
                        placeholder="Enter your email">

                    <input type="text"
                        class="w-full p-4 rounded-3xl border-2 border-white text-aliceblue bg-transparent transition-all duration-500 ease-in-out"
                        placeholder="Enter your ID">
                </div>

                <button
                    class="mt-8 w-1/3 py-2 bg-transparent border-2 border-white text-white rounded-3xl hover:bg-black hover:bg-opacity-20 transition duration-300">
                    Check
                </button>
            </form>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Forgotpassword-1',
};
</script>

<style scoped></style>