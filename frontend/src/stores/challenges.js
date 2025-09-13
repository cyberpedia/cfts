import { defineStore } from 'pinia';
import { ref } from 'vue';
import apiClient from '../services/api';
import { useAuthStore } from './auth';

export const useChallengesStore = defineStore('challenges', () => {
  const challenges = ref([]);
  const currentChallenge = ref(null);

  async function fetchChallenges() {
    try {
      const response = await apiClient.get('/challenges/');
      challenges.value = response.data;
    } catch (error) {
      console.error('Failed to fetch challenges:', error);
      throw error;
    }
  }

  async function fetchChallenge(id) {
    try {
      const response = await apiClient.get(`/challenges/${id}`);
      currentChallenge.value = response.data;
    } catch (error) {
      console.error(`Failed to fetch challenge ${id}:`, error);
      currentChallenge.value = null;
      throw error;
    }
  }

  async function submitFlag({ challengeId, flag }) {
    const authStore = useAuthStore();
    try {
      const response = await apiClient.post(`/challenges/${challengeId}/submit`, { flag });
      // On success, refresh the user's profile to get updated score and badges
      await authStore.refreshUserProfile();
      await fetchChallenge(challengeId); // Re-fetch challenge to show updated solve status
      return response.data;
    } catch (error) {
      console.error('Flag submission failed:', error);
      throw error.response.data;
    }
  }

  return { challenges, currentChallenge, fetchChallenges, fetchChallenge, submitFlag };
});
