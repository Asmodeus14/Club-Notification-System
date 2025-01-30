<template>
    <div class="min-h-screen bg-gray-100">
      <nav class="bg-blue-600 p-4 text-white shadow-md">
        <div class="container mx-auto flex justify-between items-center">
          <h1 class="text-xl font-bold">Admin Dashboard</h1>
          <button @click="toggleMenu" class="md:hidden text-white focus:outline-none">
            ☰
          </button>
          <ul :class="{'hidden': !menuOpen, 'flex': menuOpen}" class="md:flex md:space-x-4 absolute md:relative top-16 md:top-0 left-0 bg-blue-600 w-full md:w-auto md:bg-transparent p-4 md:p-0">
            <li><RouterLink to="/settings" class="block md:inline hover:underline">Settings</RouterLink></li>
          </ul>
        </div>
      </nav>
      
      <div class="p-6">
        <div class="bg-white shadow-lg rounded-lg p-6 overflow-x-auto">
          <h2 class="text-2xl font-semibold mb-4">Pending Approvals</h2>
          <table class="w-full border-collapse">
            <thead>
              <tr class="bg-gray-200">
                <th class="p-2 text-left">Name</th>
                <th class="p-2 text-left">Email</th>
                <th class="p-2 text-left">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="request in requests" :key="request.id" class="border-t">
                <td class="p-2">{{ request.name }}</td>
                <td class="p-2">{{ request.email }}</td>
                <td class="p-2 flex flex-col md:flex-row space-y-2 md:space-y-0 md:space-x-2">
                  <button @click="approveRequest(request.id)" class="bg-green-500 text-white px-4 py-1 rounded hover:bg-green-600">Approve</button>
                  <button @click="rejectRequest(request.id)" class="bg-red-500 text-white px-4 py-1 rounded hover:bg-red-600">Reject</button>
                </td>
              </tr>
              <tr v-if="requests.length === 0">
                <td colspan="3" class="p-4 text-center">No pending requests</td>
              </tr>
            </tbody>
          </table>
        </div>
        
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
              <tr v-for="request in processedRequests" :key="request.id" class="border-t">
                <td class="p-2">{{ request.name }}</td>
                <td class="p-2">{{ request.email }}</td>
                <td class="p-2">{{ request.status }}</td>
                <td class="p-2">
                  <button v-if="request.status === 'Approved'" @click="deleteApproved(request.id)" class="bg-yellow-500 text-white px-4 py-1 rounded hover:bg-yellow-600">Delete</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "AdministratorManager",
    data() {
      return {
        menuOpen: false,
        requests: [
          { id: 1, name: "John Doe", email: "john@example.com" },
          { id: 2, name: "Jane Smith", email: "jane@example.com" }
        ],
        processedRequests: []
      };
    },
    methods: {
      toggleMenu() {
        this.menuOpen = !this.menuOpen;
      },
      approveRequest(id) {
        const request = this.requests.find(req => req.id === id);
        if (request) {
          this.processedRequests.push({ ...request, status: "Approved" });
          this.requests = this.requests.filter(req => req.id !== id);
        }
      },
      rejectRequest(id) {
        const request = this.requests.find(req => req.id === id);
        if (request) {
          this.processedRequests.push({ ...request, status: "Rejected" });
          this.requests = this.requests.filter(req => req.id !== id);
        }
      },
      deleteApproved(id) {
        this.processedRequests = this.processedRequests.filter(req => req.id !== id);
      }
    }
  };
  </script>
  
  <style scoped>
  </style>
  