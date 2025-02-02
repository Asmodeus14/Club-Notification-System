<template>
  <div class="min-h-screen bg-gray-100">
    <nav class="bg-blue-600 p-4 text-white shadow-md">
      <div class="container mx-auto flex justify-between items-center">
        <!-- Logo and Dashboard Name -->
        <h1 class="text-xl font-bold flex items-center space-x-2">
          <span>{{ userdata.name }}</span>
          <span class="text-sm text-gray-300">|</span>
          <span class="text-lg">{{ userdata.club }}</span>
          
        </h1>
      </div>
    </nav>
    <div class="flex justify-center text-lg">
      <h1>
        -----welcome to dashboard
        {{ userdata.position }}-----
      </h1>
      
    </div>
    <div class="p-6">
      <!-- Pending Approvals -->
      <div class="bg-white shadow-lg rounded-lg p-6 overflow-x-auto">
        <h2 class="text-2xl font-semibold mb-4">Pending Approvals</h2>
        <table class="w-full border-collapse">
          <thead>
            <tr class="bg-gray-200">
              <th class="p-2 text-left">Name</th>
              <th class="p-2 text-left">Email</th>
              <th class="p2 text-left">Position</th>
              <th class="p-2 text-left">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="request in requests" :key="request.user_id" class="border-t">
              <td class="p-2">{{ request.name }}</td>
              <td class="p-2">{{ request.email }}</td>
              <td class="p-2">{{ request.position }}</td>
              <td class="p-2 flex flex-col md:flex-row space-y-2 md:space-y-0 md:space-x-2">
                <!-- Change request.id to request.user_id -->
                <button @click="approveRequest(request)"
                  class="bg-green-500 text-white px-4 py-1 rounded hover:bg-green-600">Approve</button>
                <button @click="rejectRequest(request)"
                  class="bg-red-500 text-white px-4 py-1 rounded hover:bg-red-600">Reject</button>
              </td>
            </tr>

            <tr v-if="requests?.length === 0">
              <td colspan="3" class="p-4 text-center">No pending requests</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Approved & Rejected Requests -->
      <div class="mt-6 bg-white shadow-lg rounded-lg p-6 overflow-x-auto">
        <h2 class="text-2xl font-semibold mb-4">Approved & Rejected Requests</h2>
        <table class="w-full border-collapse">
          <thead>
            <tr class="bg-gray-200">
              <th class="p-2 text-left">Name</th>
              <th class="p-2 text-left">Email</th>
              <th class="p-2 text-left">Status</th>
              <th class="p-2 text-left">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="request in processedRequests" :key="request.user_id" class="border-t">
              <td class="p-2">{{ request.name }}</td>
              <td class="p-2">{{ request.email }}</td>
              <td class="p-2">{{ request.status }}</td>
              <td class="p-2">
                <button v-if="request.status === 'Approved'" @click="deleteApproved(request)"
                  class="bg-yellow-500 text-white px-4 py-1 rounded hover:bg-yellow-600">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Message Input & Role Selection -->
      <div class="mt-6 bg-white shadow-lg rounded-lg p-6">
        <h2 class="text-2xl font-semibold mb-4">Send a Message</h2>
        <div class="flex flex-col md:flex-row md:space-x-4">
          <select v-model="selectedRole" class="p-2 border rounded-md w-full md:w-1/3" multiple>
            <option value="Veteran Coordinator">Veteran Coordinator</option>
            <option value="Assistant Coordinator">Assistant Coordinator</option>
            <option value="Student Coordinator">Student Coordinator</option>
            <option value="Club Members">Club Members</option>
          </select>
            <textarea v-model="messageText" placeholder="Enter message..." rows="4"
            class="p-2 border rounded-md flex-1"></textarea>
          
        </div>
        <div class="flex justify-center mt-4">
          <button @click="sendMessage" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Send</button>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import axios from 'axios';

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
        const response = await axios.get(`http://127.0.0.1:5000/api/get_user/${this.user_id_local}`);
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
        const response = await axios.get(`http://127.0.0.1:5000/api/approvals/${this.userdata.position}-${this.userdata.club}`);
        this.requests = response.data.pending || [];
        this.processedRequests = response.data.processed || [];
        console.log("Requests:", this.requests, "Processed:", this.processedRequests);
      } catch (error) {
        console.error("Error fetching requests:", error);
      }
    },
    async approveRequest(request) {
      try {
        console.log("Approving User ID:", request.user_id);
        await axios.post(`http://127.0.0.1:5000/api/approve/${request.user_id}`);
        this.fetchRequests();
      } catch (error) {
        console.error("Error approving request:", error);
        alert("Failed to approve request.");
      }
    },

    async rejectRequest(request) {
      try {
        console.log("Rejecting User ID:", request.user_id);
        await axios.post(`http://127.0.0.1:5000/api/reject/${request.user_id}`);
        this.fetchRequests();
      } catch (error) {
        console.error("Error rejecting request:", error);
        alert("Failed to reject request.");
      }
    },

    async deleteApproved(request) {
      if (this.userdata.position === 'Admin') {
        try {
          await axios.delete(`http://127.0.0.1:5000/api/delete/${request.user_id}`);
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

      try {
        
        await axios.post('http://127.0.0.1:5000/api/send_message', {
          role: this.selectedRole,
          message: this.messageText
        });

        // Reset the input fields after successful message send
        this.messageText = "";
        this.selectedRole = [];  // Reset to an empty array
        alert("Message sent successfully!");

      } catch (error) {
        console.error("Error sending message:", error);
        alert("Failed to send message.");
      }
    }

  }
};


</script>
