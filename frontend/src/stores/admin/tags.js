import { defineStore } from 'pinia';
import { ref } from 'vue';
import apiClient from '../../services/api';

export const useAdminTagsStore = defineStore('adminTags', () => {
  // State
  const tags = ref([]);

  // Actions
  async function fetchTags() {
    try {
      // NOTE: Assumes a GET /admin/tags/ endpoint exists
      const response = await apiClient.get('/admin/tags/');
      tags.value = response.data;
    } catch (error) {
      console.error('Failed to fetch tags:', error);
      throw error;
    }
  }

  async function createTag(tagName) {
    try {
      const response = await apiClient.post('/admin/tags/', { name: tagName });
      tags.value.push(response.data);
      return response.data;
    } catch (error) {
      console.error('Failed to create tag:', error);
      throw error.response.data;
    }
  }

  return { tags, fetchTags, createTag };
});
