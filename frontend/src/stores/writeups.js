import { defineStore } from 'pinia';
import apiClient from '../services/api';

export const useWriteupsStore = defineStore('writeups', () => {
  // There's no state to manage, just an action
  async function submitWriteup({ challengeId, content }) {
    try {
      // NOTE: This assumes a /writeups/ endpoint exists on the backend.
      // Based on the project spec, this is a reasonable assumption.
      const response = await apiClient.post('/writeups/', {
        challenge_id: challengeId,
        content: content,
      });
      return response.data;
    } catch (error) {
      console.error('Write-up submission failed:', error);
      throw error.response.data;
    }
  }

  return { submitWriteup };
});
