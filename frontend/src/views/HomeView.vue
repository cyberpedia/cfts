<template>
  <div class="p-4 md:p-8">
    <div class="text-center mb-12">
      <h1 class="text-5xl font-extrabold text-white mb-4">
        {{ settingsStore.settings?.event_title || 'Welcome to the CTF' }}
      </h1>
      <p class="text-lg text-gray-400">The competition is on. Good luck, have fun!</p>
    </div>

    <!-- Countdown Timer -->
    <CountdownTimer />

    <!-- Activity Feed -->
    <div class="max-w-4xl mx-auto">
      <ActivityFeed />
    </div>
  </div>
</template>

<script setup>
import ActivityFeed from '../components/ActivityFeed.vue';
import CountdownTimer from '../components/CountdownTimer.vue';
import { useSettingsStore } from '../stores/settings';

const settingsStore = useSettingsStore();
</script>
