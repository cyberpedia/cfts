<template>
  <div class="flex flex-col min-h-screen bg-gray-900 text-gray-200">
    <NavBar />
    <main class="flex-grow container mx-auto px-4 py-8">
      <router-view />
    </main>
    <Footer />
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import NavBar from './components/NavBar.vue';
import Footer from './components/Footer.vue';
import { useSettingsStore } from './stores/settings';

const settingsStore = useSettingsStore();

// Fetch public settings when the application loads
onMounted(() => {
  settingsStore.fetchPublicSettings();
});
</script>

<style>
body {
  background-color: #1a202c;
}
</style>
