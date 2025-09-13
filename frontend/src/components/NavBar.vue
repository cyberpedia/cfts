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
            <!-- Conditionally render Teams link based on settings -->
            <router-link v-if="settingsStore.settings?.allow_teams" to="/teams" class="text-gray-300 hover:text-white transition-colors">
              Teams
            </router-link>
            
            <div class="flex items-center space-x-4">
              <span class="text-white">Hello, {{ authStore.user?.username }}</span>
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
import { useAuthStore } from '../stores/auth';
import { useSettingsStore } from '../stores/settings';

const authStore = useAuthStore();
const settingsStore = useSettingsStore();

const handleLogout = () => {
  authStore.logout();
};
</script>
