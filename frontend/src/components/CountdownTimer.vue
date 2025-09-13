<template>
  <div class="bg-gray-800 p-6 rounded-lg shadow-lg text-center mb-8">
    <div v-if="countdownMessage" class="text-2xl font-bold text-white">
      {{ countdownMessage }}
    </div>
    <div v-if="timerVisible" class="flex justify-center space-x-4 md:space-x-8 mt-4 text-white">
      <div>
        <div class="text-4xl md:text-6xl font-bold">{{ days }}</div>
        <div class="text-sm uppercase text-gray-400">Days</div>
      </div>
      <div>
        <div class="text-4xl md:text-6xl font-bold">{{ hours }}</div>
        <div class="text-sm uppercase text-gray-400">Hours</div>
      </div>
      <div>
        <div class="text-4xl md:text-6xl font-bold">{{ minutes }}</div>
        <div class="text-sm uppercase text-gray-400">Minutes</div>
      </div>
      <div>
        <div class="text-4xl md:text-6xl font-bold">{{ seconds }}</div>
        <div class="text-sm uppercase text-gray-400">Seconds</div>
      </div>
    </div>
    <div v-else class="text-2xl font-bold text-indigo-400 mt-4">
      {{ statusMessage }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue';
import { useSettingsStore } from '../stores/settings';

const settingsStore = useSettingsStore();

const days = ref('00');
const hours = ref('00');
const minutes = ref('00');
const seconds = ref('00');

const countdownMessage = ref('');
const statusMessage = ref('');
const timerVisible = ref(false);

let intervalId = null;

const targetDate = computed(() => {
  const now = new Date();
  const startTime = settingsStore.settings?.event_start_time ? new Date(settingsStore.settings.event_start_time) : null;
  const endTime = settingsStore.settings?.event_end_time ? new Date(settingsStore.settings.event_end_time) : null;

  if (startTime && now < startTime) {
    countdownMessage.value = "Event Starts In";
    return startTime;
  }
  if (endTime && now < endTime) {
    countdownMessage.value = "Event Ends In";
    return endTime;
  }
  return null;
});

const updateCountdown = () => {
  if (!targetDate.value) {
    timerVisible.value = false;
    const now = new Date();
    const startTime = settingsStore.settings?.event_start_time ? new Date(settingsStore.settings.event_start_time) : null;
    if (startTime && now >= startTime) {
        statusMessage.value = 'The Event is LIVE!';
    } else {
        statusMessage.value = 'The Event has ended.';
    }
    clearInterval(intervalId);
    return;
  }
  
  timerVisible.value = true;
  const now = new Date().getTime();
  const distance = targetDate.value.getTime() - now;

  if (distance < 0) {
    days.value = '00';
    hours.value = '00';
    minutes.value = '00';
    seconds.value = '00';
    // Recalculate state in the next tick
    settingsStore.fetchPublicSettings(); // Re-fetch to update status
    return;
  }

  days.value = String(Math.floor(distance / (1000 * 60 * 60 * 24))).padStart(2, '0');
  hours.value = String(Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))).padStart(2, '0');
  minutes.value = String(Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60))).padStart(2, '0');
  seconds.value = String(Math.floor((distance % (1000 * 60)) / 1000)).padStart(2, '0');
};

onMounted(() => {
  // Wait for settings to be available, then start the timer
  const stopWatch = watch(() => settingsStore.settings, (newSettings) => {
    if (newSettings) {
      updateCountdown();
      intervalId = setInterval(updateCountdown, 1000);
      stopWatch(); // Stop watching once the timer is set up
    }
  }, { immediate: true });
});

onUnmounted(() => {
  clearInterval(intervalId);
});
</script>
