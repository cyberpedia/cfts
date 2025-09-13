import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import apiClient from '../services/api';

export const useNotificationsStore = defineStore('notifications', () => {
  // State
  const notifications = ref([]);

  // Getters
  const unreadCount = computed(() => notifications.value.filter(n => !n.is_read).length);

  // Actions
  async function fetchNotifications() {
    try {
      const response = await apiClient.get('/notifications/');
      notifications.value = response.data;
    } catch (error) {
      console.error('Failed to fetch notifications:', error);
      notifications.value = []; // Clear on error
    }
  }

  async function markAsRead(notificationId) {
    try {
      const response = await apiClient.post(`/notifications/${notificationId}/read`);
      // Find the notification in the local state and update it
      const index = notifications.value.findIndex(n => n.id === notificationId);
      if (index !== -1) {
        notifications.value[index] = response.data;
      }
    } catch (error) {
      console.error(`Failed to mark notification ${notificationId} as read:`, error);
      throw error;
    }
  }

  return { notifications, unreadCount, fetchNotifications, markAsRead };
});
