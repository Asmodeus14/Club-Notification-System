<template>
  <div class="min-h-screen bg-gradient-to-br from-purple-700 via-blue-600 to-indigo-900 flex flex-col items-center">
    <nav class="backdrop-blur-lg bg-white/10 p-4 text-white shadow-lg w-full">
      <div class="container mx-auto flex justify-between items-center">
        <h1 class="text-2xl font-bold flex items-center space-x-2">
          <span>{{ position(userdata.position) }}</span>
          <span class="text-sm text-gray-300">|</span>
          <span class="text-lg">{{ userdata.club }}</span>
        </h1>
      </div>
    </nav>

    <div class="flex flex-col items-center text-lg mt-6">
      <h1 class="text-4xl font-bold text-center text-gray-200">
        Welcome <span class="text-blue-400">{{ userdata.name }}</span>
      </h1>
    </div>

    <div class="p-6 w-full max-w-5xl">
      <div class="backdrop-blur-lg bg-white/10 shadow-lg rounded-2xl p-6 overflow-hidden hover:overflow-auto">
        <h2 class="text-2xl font-semibold text-white mb-4">Pending Approvals</h2>
        <!-- <input v-model="searchQuery" type="text" placeholder="Search..." class="p-2 border rounded-md w-full mb-4 bg-gray-800 text-white"> -->
        <table class="w-full text-white">
          <thead>
            <tr class="bg-white/20">
              <th class="p-2 text-left">Name</th>
              <th class="p-2 text-left">Email</th>
              <th class="p-2 text-left">Position</th>
              <th class="p-2 text-left">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="request in requests" :key="request.user_id" class="border-t border-white/20">
              <td class="p-2">{{ request.name }}</td>
              <td class="p-2">{{ request.email }}</td>
              <td class="p-2">{{ request.position }}</td>
              <td class="p-2 flex space-x-2">
                <button @click="approveRequest(request)"
                  class="bg-green-500 px-4 py-1 rounded-lg hover:bg-green-600">Approve</button>
                <button @click="rejectRequest(request)"
                  class="bg-red-500 px-4 py-1 rounded-lg hover:bg-red-600">Reject</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <!-- Approved & Rejected Requests -->
      <div class="p-6 w-full max-w-5xl">
        <div class="backdrop-blur-lg bg-white/10 shadow-lg rounded-2xl p-6 overflow-hidden hover:overflow-auto">
          <h2 class="text-2xl font-semibold text-white mb-4">Approved - Rejected Requests</h2>
          <table class="w-full text-white">
            <thead>
              <tr class="bg-white/20">
                <th class="p-2 text-left">Name</th>
                <th class="p-2 text-left">Email</th>
                <th class="p-2 text-left">Status</th>
                <th class="p-2 text-left">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="request in processedRequests" :key="request.user_id" class="border-t border-white/20">
                <td class="p-2">{{ request.name }}</td>
                <td class="p-2">{{ request.email }}</td>
                <td class="p-2">{{ request.status }}</td>
                <td class="p-2">
                  <button v-if="request.status === 'Approved'" @click="deleteApproved(request)"
                    class="bg-yellow-500 text-white px-4 py-1 rounded-lg hover:bg-yellow-600">Delete</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="mt-6 backdrop-blur-lg bg-white/10 shadow-lg rounded-2xl p-6">
        <h2 class="text-2xl font-semibold text-white mb-4">Send a Message</h2>
        <div class="flex flex-col md:flex-row md:space-x-4 ">
          <select v-model="selectedRole"
            class="p-2 border rounded-md w-full md:w-1/3 bg-transparent text-white overflow:hidden" required multiple>
            <option value="Veteran Coordinator">Veteran Coordinator</option>
            <option value="Assistant Coordinator">Assistant Coordinator</option>
            <option value="Student Coordinator">Student Coordinator</option>
            <option value="Club Members">Club Members</option>
          </select>
          <textarea v-model="messageText" placeholder="Enter message..." rows="4"
            class="p-2 border rounded-md flex-1 bg-transparent text-white"></textarea>
        </div>
        <div class="flex justify-center mt-4">
          <button @click="sendMessage"
            class=" max-w-72 flex-1 flex items-center justify-center py-3 bg-white bg-opacity-20 rounded-xl hover:bg-opacity-30 transition">Send</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { url } from './data/url';

export default {
  name: "AdministratorManager",
  props: ['user_id'],
  data() {
    return {
      user_id_local: this.user_id || this.$route.params.user_id,
      userdata: {},
      menuOpen: false,
      requests: [],
      processedRequests: [],
      messageText: "",
      selectedRole: [],
    };
  },
  created() {
    console.log("Route params:", this.$route.params);

    if (this.user_id_local) {
      this.fetchUserData();
    } else {
      console.error("User ID is missing!", this.user_id, this.$route.params.user_id);
    }
  },
  methods: {
    async fetchUserData() {
      try {
        const response = await axios.get(`${url}/api/get_user/${this.user_id_local}`);
        this.userdata = response.data;
        this.fetchRequests();
      } catch (error) {
        console.error("Error fetching user data:", error);
      }
    },
    toggleMenu() {
      this.menuOpen = !this.menuOpen;
    },
    async fetchRequests() {
      if (!this.userdata.position) return;
      try {
        const response = await axios.get(`${url}/api/approvals/${this.userdata.position}-${this.userdata.club}`);
        this.requests = response.data.pending || {};
        this.processedRequests = response.data.processed || {};
        console.log("Requests:", this.requests, "Processed:", this.processedRequests);
      } catch (error) {
        console.error("Error fetching requests:", error);
      }
    },
    async approveRequest(request) {
      try {
        console.log("Approving User ID:", request.user_id);
        await axios.post(`${url}/api/approve/${request.user_id}`);
        this.fetchRequests();
      } catch (error) {
        console.error("Error approving request:", error);
        alert("Failed to approve request.");
      }
    },

    async rejectRequest(request) {
      try {
        console.log("Rejecting User ID:", request.user_id);
        await axios.post(`${url}/api/reject/${request.user_id}`);
        this.fetchRequests();
      } catch (error) {
        console.error("Error rejecting request:", error);
        alert("Failed to reject request.");
      }
    },

    async deleteApproved(request) {
      if (this.userdata.position === 'Admin') {
        try {
          await axios.delete(`${url}/api/delete/${request.user_id}`);
          this.fetchRequests();
        } catch (error) {
          console.error("Error deleting approved request:", error);
          alert("Failed to delete request.");
        }
      } else {
        alert("You do not have permission to delete this.");
      }
    },
    async sendMessage() {
      if (!this.selectedRole || !this.messageText.trim()) {
        alert("Please select a role and enter a message.");
        
        return;
      }
      if(this.selectedRole.length==0){
        alert("Select who to send")
        return;
      }

      try {

        await axios.post(`${url}/api/send_message`, {
          role: this.selectedRole,
          message: this.messageText,
          postion:this.userdata['position'],
          club:this.userdata['club']
        })

        // Reset the input fields after successful message send
        this.messageText = "";
        this.selectedRole = [];  // Reset to an empty array
        alert("Message sent successfully!");

      } catch (error) {
        console.error("Error sending message:", error);
        alert("Failed to send message.");
      }
    },
    position(user) {
        if (user && typeof user=== "string") {
          user = user.replace("-", " ").toUpperCase();
        }
        return user;
      },
  }


};


</script>
<style scoped>
/* For WebKit browsers (Chrome, Safari, Opera) */
.select-no-scrollbar::-webkit-scrollbar {
  display: none;
}

/* For Firefox */
.select-no-scrollbar {
  scrollbar-width: none;
}

/* For IE and Edge */
.select-no-scrollbar {
  -ms-overflow-style: none;
}
</style>
