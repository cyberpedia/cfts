import { defineStore } from 'pinia';
import { ref } from 'vue';
import apiClient from '../../services/api';

export const useAdminSettingsStore = defineStore('adminSettings', () => {
  // State
  const settings = ref(null);

  // Actions
  async function fetchSettings() {
    try {
      const response = await apiClient.get('/admin/settings/');
      settings.value = response.data;
    } catch (error) {
      console.error('Failed to fetch settings:', error);
      throw error;
    }
  }

  async function updateSettings(data) {
    try {
      const response = await apiClient.put('/admin/settings/', data);
      settings.value = response.data;
      return response.data;
    } catch (error) {
      console.error('Failed to update settings:', error);
      throw error.response.data;
    }
  }

  return { settings, fetchSettings, updateSettings };
});
