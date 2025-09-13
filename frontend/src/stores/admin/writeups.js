import { defineStore } from 'pinia';
import { ref } from 'vue';
import apiClient from '../../services/api';

export const useAdminWriteupsStore = defineStore('adminWriteups', () => {
  // State
  const writeups = ref([]);

  // Actions
  async function fetchWriteups() {
    try {
      // NOTE: This assumes a GET /admin/writeups/ endpoint exists
      const response = await apiClient.get('/admin/writeups/');
      writeups.value = response.data;
    } catch (error) {
      console.error('Failed to fetch writeups:', error);
      throw error;
    }
  }

  async function moderateWriteup({ writeupId, status, points }) {
    try {
      // NOTE: This assumes a POST /admin/writeups/{id}/moderate endpoint exists
      const response = await apiClient.post(`/admin/writeups/${writeupId}/moderate`, { status, points });
      // Update the local state to reflect the change
      const index = writeups.value.findIndex(w => w.id === writeupId);
      if (index !== -1) {
        writeups.value[index] = response.data;
      }
    } catch (error) {
      console.error(`Failed to moderate writeup ${writeupId}:`, error);
      throw error.response.data;
    }
  }

  return { writeups, fetchWriteups, moderateWriteup };
});
