<template>
  <div>
    <h1 class="text-4xl font-bold mb-6">Write-up Moderation</h1>
    <div v-if="loading" class="text-center">Loading write-ups...</div>
    <div v-else-if="!pendingWriteups.length" class="text-center bg-gray-800 p-8 rounded-lg text-gray-400">
      There are no pending write-ups to review.
    </div>
    <div v-else class="space-y-6">
      <div v-for="writeup in pendingWriteups" :key="writeup.id" class="bg-gray-800 p-6 rounded-lg">
        <div class="flex justify-between items-start mb-4">
          <div>
            <h2 class="text-xl font-bold">Challenge: <span class="text-indigo-400">{{ writeup.challenge.name }}</span></h2>
            <p class="text-sm text-gray-400">Submitted by: {{ writeup.user.username }} on {{ new Date(writeup.created_at).toLocaleString() }}</p>
          </div>
          <div class="flex space-x-2">
            <button @click="handleModerate(writeup.id, 'approved')" class="px-3 py-1 bg-green-600 hover:bg-green-700 rounded-md text-sm font-semibold">Approve</button>
            <button @click="handleModerate(writeup.id, 'rejected')" class="px-3 py-1 bg-red-600 hover:bg-red-700 rounded-md text-sm font-semibold">Reject</button>
          </div>
        </div>
        <div class="bg-gray-900 p-4 rounded-md">
          <p class="text-gray-300 whitespace-pre-wrap">{{ writeup.content }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useAdminWriteupsStore } from '../../stores/admin/writeups';
import { storeToRefs } from 'pinia';

const store = useAdminWriteupsStore();
const { writeups } = storeToRefs(store);
const loading = ref(true);

const pendingWriteups = computed(() => writeups.value.filter(w => w.status === 'pending'));

onMounted(async () => {
  try {
    await store.fetchWriteups();
  } catch (error) {
    alert("Failed to load write-ups.");
  } finally {
    loading.value = false;
  }
});

const handleModerate = async (writeupId, status) => {
  let points = 0;
  if (status === 'approved') {
    const pointsStr = prompt("Enter bonus points to award for this write-up:", "10");
    if (pointsStr === null) return; // User cancelled
    points = parseInt(pointsStr, 10);
    if (isNaN(points)) {
      alert("Invalid number for points.");
      return;
    }
  }
  
  try {
    await store.moderateWriteup({ writeupId, status, points });
  } catch (error) {
    alert(error.detail || `Failed to ${status} write-up.`);
  }
};
</script>
