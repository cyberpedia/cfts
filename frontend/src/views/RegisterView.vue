<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-900">
    <div class="w-full max-w-md p-8 space-y-6 bg-gray-800 rounded-lg shadow-md">
      <h1 class="text-2xl font-bold text-center text-white">Create an Account</h1>
      
      <div v-if="successMessage" class="p-3 text-sm text-green-300 bg-green-800 bg-opacity-50 border border-green-500 rounded-md">
        {{ successMessage }}
      </div>

      <form v-else @submit.prevent="handleRegister" class="space-y-6">
        <div>
          <label for="username" class="block text-sm font-medium text-gray-300">Username</label>
          <input
            v-model="form.username"
            type="text"
            id="username"
            required
            class="w-full px-3 py-2 mt-1 text-white bg-gray-700 border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>
        
        <div>
          <label for="email" class="block text-sm font-medium text-gray-300">Email</label>
          <input
            v-model="form.email"
            type="email"
            id="email"
            required
            class="w-full px-3 py-2 mt-1 text-white bg-gray-700 border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <div>
          <label for="password" class="block text-sm font-medium text-gray-300">Password</label>
          <input
            v-model="form.password"
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
          Register
        </button>
      </form>
      
      <div class="text-sm text-center text-gray-400">
        Already have an account? 
        <router-link to="/login" class="font-medium text-indigo-400 hover:underline">
          Login here
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const form = reactive({
  username: '',
  email: '',
  password: '',
});
const errorMessage = ref('');
const successMessage = ref('');
const authStore = useAuthStore();
const router = useRouter();

const handleRegister = async () => {
  try {
    errorMessage.value = '';
    await authStore.register(form);
    successMessage.value = 'Registration successful! Please check your email to verify your account.';
    
    // Optionally redirect after a few seconds
    setTimeout(() => {
      router.push({ name: 'login' });
    }, 3000);

  } catch (error) {
    errorMessage.value = error.detail || 'An unexpected error occurred during registration.';
    console.error('Registration failed:', error);
  }
};
</script>
