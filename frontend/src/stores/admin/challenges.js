import { defineStore } from 'pinia';
import { ref } from 'vue';
import apiClient from '../../services/api';

export const useAdminChallengesStore = defineStore('adminChallenges', () => {
  // State
  const challenges = ref([]);
  const currentChallenge = ref(null);

  // Actions
  async function fetchChallenges() {
    try {
      // NOTE: Assumes a GET /admin/challenges/ endpoint exists
      const response = await apiClient.get('/admin/challenges/');
      challenges.value = response.data;
    } catch (error) {
      console.error('Failed to fetch challenges:', error);
      throw error;
    }
  }

  async function fetchChallenge(challengeId) {
    try {
      const response = await apiClient.get(`/admin/challenges/${challengeId}`);
      currentChallenge.value = response.data;
    } catch (error) {
      console.error(`Failed to fetch challenge ${challengeId}:`, error);
      currentChallenge.value = null;
      throw error;
    }
  }

  async function createChallenge(data) {
    try {
      const response = await apiClient.post('/admin/challenges/', data);
      challenges.value.push(response.data);
      return response.data;
    } catch (error) {
      console.error('Failed to create challenge:', error);
      throw error.response.data;
    }
  }

  async function updateChallenge({ challengeId, data }) {
    try {
      const response = await apiClient.put(`/admin/challenges/${challengeId}`, data);
      const index = challenges.value.findIndex(c => c.id === challengeId);
      if (index !== -1) {
        challenges.value[index] = response.data;
      }
      return response.data;
    } catch (error) {
      console.error(`Failed to update challenge ${challengeId}:`, error);
      throw error.response.data;
    }
  }

  async function deleteChallenge(challengeId) {
    try {
      await apiClient.delete(`/admin/challenges/${challengeId}`);
      challenges.value = challenges.value.filter(c => c.id !== challengeId);
    } catch (error) {
      console.error(`Failed to delete challenge ${challengeId}:`, error);
      throw error.response.data;
    }
  }

  return { challenges, currentChallenge, fetchChallenges, fetchChallenge, createChallenge, updateChallenge, deleteChallenge };
});
