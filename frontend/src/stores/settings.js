import { defineStore } from 'pinia';
import { ref } from 'vue';
import apiClient from '../services/api';

export const useSettingsStore = defineStore('settings', () => {
  // State
  const settings = ref(null);

  // Action
  async function fetchPublicSettings() {
    try {
      const response = await apiClient.get('/settings/public');
      settings.value = response.data;
    } catch (error) {
      console.error('Failed to fetch public settings:', error);
      // It's okay to fail silently here, defaults will apply
    }
  }

  return { settings, fetchPublicSettings };
});
