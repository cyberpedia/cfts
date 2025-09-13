import { defineStore } from 'pinia';
import { ref } from 'vue';
import apiClient from '../../services/api';

export const useAdminUsersStore = defineStore('adminUsers', () => {
  // State
  const users = ref([]);
  const currentUser = ref(null);

  // Actions
  async function fetchUsers() {
    try {
      // NOTE: This assumes a GET /admin/users endpoint. We'll need to add it.
      // For now, let's assume it exists.
      const response = await apiClient.get('/admin/users/');
      users.value = response.data;
    } catch (error) {
      console.error('Failed to fetch users:', error);
      throw error;
    }
  }

  async function fetchUser(userId) {
    try {
      const response = await apiClient.get(`/admin/users/${userId}`);
      currentUser.value = response.data;
    } catch (error) {
      console.error(`Failed to fetch user ${userId}:`, error);
      currentUser.value = null;
      throw error;
    }
  }

  async function updateUser({ userId, data }) {
    try {
      const response = await apiClient.put(`/admin/users/${userId}`, data);
      // Update the user in the local list if it exists
      const index = users.value.findIndex(u => u.id === userId);
      if (index !== -1) {
        users.value[index] = response.data;
      }
      return response.data;
    } catch (error) {
      console.error(`Failed to update user ${userId}:`, error);
      throw error.response.data;
    }
  }

  async function deleteUser(userId) {
    try {
      await apiClient.delete(`/admin/users/${userId}`);
      // Remove the user from the local list
      users.value = users.value.filter(u => u.id !== userId);
    } catch (error) {
      console.error(`Failed to delete user ${userId}:`, error);
      throw error.response.data;
    }
  }

  return { users, currentUser, fetchUsers, fetchUser, updateUser, deleteUser };
});
