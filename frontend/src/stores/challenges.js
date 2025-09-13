import { defineStore } from 'pinia';
import { ref } from 'vue';
import apiClient from '../services/api';

export const useChallengesStore = defineStore('challenges', () => {
  // State
  const challenges = ref([]);
  const currentChallenge = ref(null);

  // Actions
  async function fetchChallenges() {
    try {
      const response = await apiClient.get('/challenges/');
      challenges.value = response.data;
    } catch (error) {
      console.error('Failed to fetch challenges:', error);
      // Handle the error appropriately in the UI
      throw error;
    }
  }

  async function fetchChallenge(id) {
    try {
      const response = await apiClient.get(`/challenges/${id}`);
      currentChallenge.value = response.data;
    } catch (error) {
      console.error(`Failed to fetch challenge ${id}:`, error);
      currentChallenge.value = null; // Clear on error
      throw error;
    }
  }

  async function submitFlag({ challengeId, flag }) {
    try {
      const response = await apiClient.post(`/challenges/${challengeId}/submit`, { flag });
      // Optionally, re-fetch challenge data to update solve status
      await fetchChallenge(challengeId);
      return response.data; // e.g., { message: "Correct flag!" }
    } catch (error) {
      console.error('Flag submission failed:', error);
      throw error.response.data; // e.g., { detail: "Incorrect flag." }
    }
  }

  return { challenges, currentChallenge, fetchChallenges, fetchChallenge, submitFlag };
});
