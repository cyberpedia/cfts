<template>
  <div class="p-8 text-white">
    <div v-if="loading" class="text-center">Loading challenge...</div>
    <div v-else-if="error" class="text-center text-red-400">{{ error }}</div>
    <div v-else-if="challenge" class="max-w-4xl mx-auto">
      <h1 class="text-4xl font-bold mb-2">{{ challenge.name }}</h1>
      <p class="text-xl text-indigo-400 mb-6">{{ challenge.points }} points</p>
      
      <!-- Locked Challenge View -->
      <div v-if="challenge.is_locked" class="bg-gray-800 p-6 rounded-lg border border-gray-700">
        <h2 class="text-2xl font-semibold mb-4">Challenge Locked</h2>
        <p class="text-gray-400">
          You must solve all prerequisite challenges before accessing this one.
        </p>
      </div>

      <!-- Unlocked Challenge View -->
      <div v-else>
        <div class="bg-gray-800 p-6 rounded-lg border border-gray-700 mb-8">
          <h2 class="text-xl font-semibold mb-3">Description</h2>
          <p class="text-gray-300 whitespace-pre-wrap">{{ challenge.description }}</p>
        </div>
        
        <!-- Flag Submission Form -->
        <form @submit.prevent="handleFlagSubmit" class="bg-gray-800 p-6 rounded-lg border border-gray-700">
          <h2 class="text-xl font-semibold mb-4">Submit Flag</h2>
          
          <div class="flex items-center space-x-4">
            <input
              v-model="flag"
              type="text"
              placeholder="CTF{...}"
              required
              class="flex-grow px-4 py-2 text-white bg-gray-700 border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
            <button
              type="submit"
              class="py-2 px-6 font-semibold text-white bg-indigo-600 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Submit
            </button>
          </div>
          
          <p v-if="submissionStatus.message" :class="submissionStatus.isError ? 'text-red-400' : 'text-green-400'" class="mt-4 text-sm">
            {{ submissionStatus.message }}
          </p>
        </form>
      </div>
    </div>
    <div v-else class="text-center">Challenge not found.</div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, reactive } from 'vue';
import { useChallengesStore } from '../stores/challenges';
import { storeToRefs } from 'pinia';

const props = defineProps({
  id: {
    type: String,
    required: true,
  },
});

const challengesStore = useChallengesStore();
const { currentChallenge: challenge } = storeToRefs(challengesStore);
const loading = ref(true);
const error = ref('');
const flag = ref('');

const submissionStatus = reactive({
  message: '',
  isError: false,
});

onMounted(async () => {
  try {
    await challengesStore.fetchChallenge(props.id);
  } catch (err) {
    error.value = 'Could not load challenge details.';
  } finally {
    loading.value = false;
  }
});

const handleFlagSubmit = async () => {
  try {
    submissionStatus.isError = false;
    submissionStatus.message = '';
    const response = await challengesStore.submitFlag({ challengeId: props.id, flag: flag.value });
    submissionStatus.message = response.message || 'Correct flag!';
  } catch (err) {
    submissionStatus.isError = true;
    submissionStatus.message = err.detail || 'An error occurred.';
  }
};
</script>
