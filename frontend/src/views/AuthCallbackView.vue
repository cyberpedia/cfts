<template>
  <div class="flex flex-col items-center justify-center min-h-screen text-white bg-gray-900">
    <div v-if="error" class="text-center p-8 bg-gray-800 rounded-lg">
      <h1 class="text-2xl font-bold text-red-400 mb-4">Authentication Failed</h1>
      <p class="text-gray-300">{{ error }}</p>
      <router-link to="/login" class="mt-6 inline-block bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-4 rounded-md">
        Return to Login
      </router-link>
    </div>
    <div v-else class="text-center">
      <h1 class="text-2xl font-bold">Authenticating...</h1>
      <p class="text-gray-400 mt-2">Please wait while we log you in.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const error = ref('');

onMounted(async () => {
  const token = route.query.token;

  if (!token) {
    error.value = 'No authentication token was provided. The login process may have failed.';
    return;
  }

  try {
    await authStore.handleSocialLogin(token);
    router.push({ name: 'home' });
  } catch (err) {
    console.error('Failed to handle social login:', err);
    error.value = 'There was a problem verifying your identity. Please try again.';
    // Clear any potentially bad token
    authStore.logout();
  }
});
</script>
