<template>
  <div class="p-8">
    <h1 class="text-4xl font-bold text-white mb-8">Challenges</h1>
    <div v-if="loading" class="text-center text-gray-400">Loading challenges...</div>
    <div v-else-if="error" class="text-center text-red-400">{{ error }}</div>
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      <router-link
        v-for="challenge in challenges"
        :key="challenge.id"
        :to="{ name: 'challenge-detail', params: { id: challenge.id } }"
        :class="[
          'block p-6 rounded-lg shadow-lg transition-transform transform hover:-translate-y-1',
          challenge.is_locked ? 'bg-gray-800 border border-gray-700 cursor-not-allowed' : 'bg-gray-700 hover:bg-gray-600'
        ]"
      >
        <div class="flex justify-between items-center">
          <h2 class="text-xl font-semibold text-white truncate">{{ challenge.name }}</h2>
          <div v-if="challenge.is_locked" class="text-gray-500">
            <!-- Simple lock icon using text or SVG -->
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
          </div>
        </div>
        <p class="mt-2 text-indigo-400 font-medium">{{ challenge.points }} Points</p>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useChallengesStore } from '../stores/challenges';
import { storeToRefs } from 'pinia';

const challengesStore = useChallengesStore();
const { challenges } = storeToRefs(challengesStore);
const loading = ref(true);
const error = ref('');

onMounted(async () => {
  try {
    await challengesStore.fetchChallenges();
  } catch (err) {
    error.value = 'Failed to load challenges. Please try again later.';
  } finally {
    loading.value = false;
  }
});
</script>
