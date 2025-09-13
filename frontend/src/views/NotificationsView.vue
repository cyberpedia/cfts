<template>
  <div class="p-8 max-w-4xl mx-auto">
    <h1 class="text-4xl font-bold text-white mb-8">Notifications</h1>
    <div v-if="loading" class="text-center text-gray-400">Loading...</div>
    <div v-else-if="!notifications.length" class="text-center text-gray-400 bg-gray-800 p-8 rounded-lg">
      You have no notifications.
    </div>
    <div v-else class="space-y-4">
      <div 
        v-for="notification in notifications" 
        :key="notification.id"
        :class="[
          'p-4 rounded-lg flex items-center justify-between transition-colors',
          notification.is_read ? 'bg-gray-800 text-gray-400' : 'bg-gray-700 text-white border-l-4 border-indigo-500'
        ]"
      >
        <div>
          <h2 class="font-bold">{{ notification.title }}</h2>
          <p class="text-sm">{{ notification.body }}</p>
          <p class="text-xs text-gray-500 mt-1">{{ new Date(notification.created_at).toLocaleString() }}</p>
        </div>
        <button
          v-if="!notification.is_read"
          @click="handleMarkAsRead(notification.id)"
          class="bg-blue-600 hover:bg-blue-700 text-white font-semibold text-xs py-1 px-3 rounded-md ml-4"
        >
          Mark as Read
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useNotificationsStore } from '../stores/notifications';
import { storeToRefs } from 'pinia';

const notificationsStore = useNotificationsStore();
const { notifications } = storeToRefs(notificationsStore);
const loading = ref(true);

onMounted(async () => {
  await notificationsStore.fetchNotifications();
  loading.value = false;
});

const handleMarkAsRead = async (id) => {
  try {
    await notificationsStore.markAsRead(id);
  } catch (error) {
    // Handle error in UI if necessary
    console.error("Failed to mark as read from component");
  }
};
</script>
