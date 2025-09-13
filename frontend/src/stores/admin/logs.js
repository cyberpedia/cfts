import { defineStore } from 'pinia';
import { ref } from 'vue';
import apiClient from '../../services/api';

export const useAdminLogsStore = defineStore('adminLogs', () => {
  // State
  const logs = ref([]);
  const totalLogs = ref(0); // For pagination

  // Actions
  async function fetchLogs(page = 1, limit = 20) {
    try {
      const response = await apiClient.get('/admin/logs/', {
        params: {
          skip: (page - 1) * limit,
          limit: limit,
        },
      });
      logs.value = response.data;
      // NOTE: A real API would provide a total count for pagination.
      // We'll simulate it for now.
      if (response.headers['x-total-count']) {
          totalLogs.value = parseInt(response.headers['x-total-count'], 10);
      } else {
          // Fallback if the header isn't present
          totalLogs.value = response.data.length < limit ? (page - 1) * limit + response.data.length : page * limit + 1;
      }
    } catch (error) {
      console.error('Failed to fetch audit logs:', error);
      logs.value = [];
      totalLogs.value = 0;
      throw error;
    }
  }

  return { logs, totalLogs, fetchLogs };
});
