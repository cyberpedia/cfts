<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-900">
    <div class="w-full max-w-md p-8 space-y-6 bg-gray-800 rounded-lg shadow-md">
      <h1 class="text-2xl font-bold text-center text-white">Login</h1>
      
      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <label for="username" class="block text-sm font-medium text-gray-300">Username</label>
          <input
            v-model="username"
            type="text"
            id="username"
            required
            class="w-full px-3 py-2 mt-1 text-white bg-gray-700 border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>
        
        <div>
          <label for="password" class="block text-sm font-medium text-gray-300">Password</label>
          <input
            v-model="password"
            type="password"
            id="password"
            required
            class="w-full px-3 py-2 mt-1 text-white bg-gray-700 border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <div v-if="errorMessage" class="p-3 text-sm text-red-300 bg-red-800 bg-opacity-50 border border-red-500 rounded-md">
          {{ errorMessage }}
        </div>

        <button
          type="submit"
          class="w-full py-2 font-semibold text-white bg-indigo-600 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          Login
        </button>
      </form>
      
      <div class="text-sm text-center text-gray-400">
        Don't have an account? 
        <router-link to="/register" class="font-medium text-indigo-400 hover:underline">
          Register here
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const username = ref('');
const password = ref('');
const errorMessage = ref('');
const authStore = useAuthStore();
const router = useRouter();

const handleLogin = async () => {
  try {
    errorMessage.value = '';
    await authStore.login({ username: username.value, password: password.value });
    router.push({ name: 'home' });
  } catch (error) {
    errorMessage.value = error.detail || 'An unexpected error occurred.';
    console.error('Login failed:', error);
  }
};
</script>
