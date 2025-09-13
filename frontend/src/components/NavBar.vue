<template>
  <nav class="bg-gray-800 shadow-lg">
    <div class="container mx-auto px-4">
      <div class="flex justify-between items-center py-4">
        <router-link to="/" class="text-2xl font-bold text-white hover:text-indigo-400">
          CTF Platform
        </router-link>

        <div class="flex items-center space-x-6">
          <template v-if="authStore.accessToken">
            <router-link to="/challenges" class="text-gray-300 hover:text-white transition-colors">
              Challenges
            </router-link>
            <router-link to="/leaderboard" class="text-gray-300 hover:text-white transition-colors">
              Leaderboard
            </router-link>
            <router-link v-if="settingsStore.settings?.allow_teams" to="/teams" class="text-gray-300 hover:text-white transition-colors">
              Teams
            </router-link>
            
            <div class="flex items-center space-x-4">
              <!-- Notifications Icon -->
              <router-link to="/notifications" class="relative text-gray-300 hover:text-white">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                </svg>
                <span v-if="unreadCount > 0" class="absolute -top-2 -right-2 flex h-5 w-5 items-center justify-center rounded-full bg-red-500 text-xs text-white">
                  {{ unreadCount }}
                </span>
              </router-link>

              <!-- User Profile Link -->
              <router-link to="/profile" class="text-white hover:text-indigo-400">
                Hello, {{ authStore.user?.username }}
              </router-link>
              <button @click="handleLogout" class="bg-red-600 hover:bg-red-700 text-white font-semibold py-2 px-4 rounded-md transition-colors">
                Logout
              </button>
            </div>
          </template>

          <template v-else>
            <router-link to="/login" class="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-4 rounded-md transition-colors">
              Login
            </router-link>
            <router-link to="/register" class="text-gray-300 hover:text-white transition-colors">
              Register
            </router-link>
          </template>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { computed, onMounted, watch } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useSettingsStore } from '../stores/settings';
import { useNotificationsStore } from '../stores/notifications';

const authStore = useAuthStore();
const settingsStore = useSettingsStore();
const notificationsStore = useNotificationsStore();

const unreadCount = computed(() => notificationsStore.unreadCount);

const handleLogout = () => {
  authStore.logout();
};

// Fetch notifications when the user logs in
watch(() => authStore.accessToken, (newToken) => {
  if (newToken) {
    notificationsStore.fetchNotifications();
  }
}, { immediate: true });

onMounted(() => {
    // Also fetch on mount in case of a page refresh
    if (authStore.accessToken) {
        notificationsStore.fetchNotifications();
    }
});
</script>
