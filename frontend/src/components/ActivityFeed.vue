<template>
  <div class="bg-gray-800 p-6 rounded-lg shadow-lg">
    <h2 class="text-2xl font-bold text-white mb-4">Live Activity Feed</h2>
    <div class="space-y-3 h-96 overflow-y-auto pr-2">
      <div v-if="!messages.length" class="text-gray-400 text-center pt-16">
        Waiting for activity...
      </div>
      <div
        v-for="(message, index) in messages"
        :key="index"
        class="bg-gray-700 p-3 rounded-md animate-fade-in"
      >
        <p class="text-sm text-gray-300">
          <span class="font-bold text-indigo-400">{{ message.team_name || message.username }}</span>
          solved
          <span class="font-bold text-green-400">{{ message.challenge_name }}</span>
        </p>
        <p class="text-xs text-gray-500 text-right">{{ formatTime(message.timestamp) }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import websocketService from '../services/websocket';

const messages = ref([]);
const MAX_MESSAGES = 15; // Keep the feed from growing indefinitely

const handleNewMessage = (event) => {
  try {
    const data = JSON.parse(event.data);
    // Add new message to the top
    messages.value.unshift(data);
    // Trim the array if it gets too long
    if (messages.value.length > MAX_MESSAGES) {
      messages.value.pop();
    }
  } catch (error) {
    console.error('Error parsing WebSocket message:', error);
  }
};

const formatTime = (isoString) => {
  const date = new Date(isoString);
  return date.toLocaleTimeString();
};

onMounted(() => {
  websocketService.subscribe(handleNewMessage);
});

onUnmounted(() => {
  websocketService.unsubscribe(handleNewMessage);
});
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.5s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
