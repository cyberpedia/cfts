<template>
  <div class="p-8 text-white">
    <div v-if="loading" class="text-center">Loading challenge...</div>
    <div v-else-if="error" class="text-center text-red-400">{{ error }}</div>
    <div v-else-if="challenge" class="max-w-4xl mx-auto space-y-8">
      <!-- Challenge Header -->
      <div>
        <h1 class="text-4xl font-bold mb-2">{{ challenge.name }}</h1>
        <p class="text-xl text-indigo-400 mb-6">{{ challenge.points }} points</p>
      </div>

      <!-- Locked Challenge -->
      <div v-if="challenge.is_locked" class="bg-gray-800 p-6 rounded-lg border border-gray-700">
        <h2 class="text-2xl font-semibold mb-4">Challenge Locked</h2>
        <p class="text-gray-400">You must solve all prerequisite challenges before accessing this one.</p>
      </div>

      <!-- Unlocked Challenge -->
      <div v-else class="space-y-8">
        <div class="bg-gray-800 p-6 rounded-lg border border-gray-700">
          <h2 class="text-xl font-semibold mb-3">Description</h2>
          <p class="text-gray-300 whitespace-pre-wrap">{{ challenge.description }}</p>
        </div>
        
        <!-- Flag Submission Form -->
        <form @submit.prevent="handleFlagSubmit" class="bg-gray-800 p-6 rounded-lg border border-gray-700">
          <h2 class="text-xl font-semibold mb-4">Submit Flag</h2>
          <div class="flex items-center space-x-4">
            <input v-model="flag" type="text" placeholder="CTF{...}" required class="flex-grow px-4 py-2 text-white bg-gray-700 border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"/>
            <button type="submit" class="py-2 px-6 font-semibold text-white bg-indigo-600 rounded-md hover:bg-indigo-700">Submit</button>
          </div>
          <p v-if="submissionStatus.message" :class="submissionStatus.isError ? 'text-red-400' : 'text-green-400'" class="mt-4 text-sm">{{ submissionStatus.message }}</p>
        </form>

        <!-- Write-up Form -->
        <div v-if="hasSolved" class="bg-gray-800 p-6 rounded-lg border border-gray-700">
          <h2 class="text-xl font-semibold mb-4">Submit a Write-up</h2>
          <form @submit.prevent="handleWriteupSubmit">
            <textarea v-model="writeupContent" rows="5" placeholder="Share your solution..." class="w-full p-3 text-white bg-gray-700 border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"></textarea>
            <p v-if="writeupStatus.message" :class="writeupStatus.isError ? 'text-red-400' : 'text-green-400'" class="mt-2 text-sm">{{ writeupStatus.message }}</p>
            <button type="submit" class="mt-4 py-2 px-6 font-semibold text-white bg-green-600 rounded-md hover:bg-green-700">Submit Write-up</button>
          </form>
        </div>
      </div>
    </div>
    <div v-else class="text-center">Challenge not found.</div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, reactive, watch } from 'vue';
import { useChallengesStore } from '../stores/challenges';
import { useSolvesStore } from '../stores/solves';
import { useWriteupsStore } from '../stores/writeups';
import { useAuthStore } from '../stores/auth';
import { storeToRefs } from 'pinia';

const props = defineProps({ id: { type: String, required: true } });

const challengesStore = useChallengesStore();
const solvesStore = useSolvesStore();
const writeupsStore = useWriteupsStore();
const authStore = useAuthStore();

const { currentChallenge: challenge } = storeToRefs(challengesStore);
const { solvedChallengeIds } = storeToRefs(solvesStore);

const loading = ref(true);
const error = ref('');
const flag = ref('');
const writeupContent = ref('');

const submissionStatus = reactive({ message: '', isError: false });
const writeupStatus = reactive({ message: '', isError: false });

const hasSolved = computed(() => solvedChallengeIds.value.has(parseInt(props.id)));

onMounted(async () => {
  try {
    // Fetch solves first to know the solved status
    if (authStore.user) {
        solvesStore.populateUserSolves(authStore.user.solves || []);
    }
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
    submissionStatus.message = 'Submitting...';
    const response = await challengesStore.submitFlag({ challengeId: props.id, flag: flag.value });
    submissionStatus.message = response.message || 'Correct flag!';
  } catch (err) {
    submissionStatus.isError = true;
    submissionStatus.message = err.detail || 'An error occurred.';
  }
};

const handleWriteupSubmit = async () => {
    if (!writeupContent.value.trim()) {
        writeupStatus.isError = true;
        writeupStatus.message = 'Write-up content cannot be empty.';
        return;
    }
    try {
        writeupStatus.isError = false;
        writeupStatus.message = 'Submitting write-up...';
        await writeupsStore.submitWriteup({ challengeId: props.id, content: writeupContent.value });
        writeupStatus.message = 'Write-up submitted for review!';
        writeupContent.value = ''; // Clear form
    } catch (err) {
        writeupStatus.isError = true;
        writeupStatus.message = err.detail || 'Could not submit write-up.';
    }
}
</script>
