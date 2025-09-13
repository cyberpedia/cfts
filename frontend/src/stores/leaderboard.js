import { defineStore } from 'pinia';
import { ref } from 'vue';
import apiClient from '../services/api';

export const useLeaderboardStore = defineStore('leaderboard', () => {
  // State
  const leaderboard = ref([]);

  // Actions
  async function fetchLeaderboard() {
    try {
      const response = await apiClient.get('/leaderboard/');
      leaderboard.value = response.data;
    } catch (error) {
      console.error('Failed to fetch leaderboard:', error);
      throw error;
    }
  }

  return { leaderboard, fetchLeaderboard };
});
