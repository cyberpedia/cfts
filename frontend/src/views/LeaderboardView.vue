<template>
  <div class="p-8">
    <h1 class="text-4xl font-bold text-white mb-8">Leaderboard</h1>
    <div v-if="loading" class="text-center text-gray-400">Loading leaderboard...</div>
    <div v-else-if="error" class="text-center text-red-400">{{ error }}</div>
    <div v-else class="bg-gray-800 rounded-lg shadow-lg overflow-hidden">
      <table class="min-w-full text-white">
        <thead class="bg-gray-700">
          <tr>
            <th class="py-3 px-6 text-left text-sm font-semibold uppercase tracking-wider">Rank</th>
            <th class="py-3 px-6 text-left text-sm font-semibold uppercase tracking-wider">Team</th>
            <th class="py-3 px-6 text-right text-sm font-semibold uppercase tracking-wider">Score</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-700">
          <tr v-for="entry in leaderboard" :key="entry.team_id" class="hover:bg-gray-700/50">
            <td class="py-4 px-6 font-medium">{{ entry.rank }}</td>
            <td class="py-4 px-6">{{ entry.team_name }}</td>
            <td class="py-4 px-6 text-right font-semibold text-indigo-400">{{ entry.total_score }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useLeaderboardStore } from '../stores/leaderboard';
import { storeToRefs } from 'pinia';

const leaderboardStore = useLeaderboardStore();
const { leaderboard } = storeToRefs(leaderboardStore);
const loading = ref(true);
const error = ref('');

onMounted(async () => {
  try {
    await leaderboardStore.fetchLeaderboard();
  } catch (err) {
    error.value = 'Failed to load leaderboard. Please try again.';
  } finally {
    loading.value = false;
  }
});
</script>
