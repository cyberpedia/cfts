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
import NavBar from './components/NavBar.vue';
import Footer from './components/Footer.vue';
</script>

<style>
/* Global styles remain the same */
body {
  background-color: #1a202c; /* Equivalent to bg-gray-900 */
}
</style>
