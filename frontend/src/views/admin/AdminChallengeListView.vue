<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-4xl font-bold">Challenge Management</h1>
      <router-link :to="{ name: 'admin-challenge-new' }" class="px-4 py-2 bg-green-600 hover:bg-green-700 rounded-md font-semibold">
        Create New Challenge
      </router-link>
    </div>
    <div v-if="loading" class="text-center">Loading challenges...</div>
    <div v-else class="bg-gray-800 rounded-lg shadow-lg overflow-hidden">
      <table class="min-w-full">
        <thead class="bg-gray-700">
          <tr>
            <th class="py-3 px-6 text-left">ID</th>
            <th class="py-3 px-6 text-left">Name</th>
            <th class="py-3 px-6 text-center">Points</th>
            <th class="py-3 px-6 text-center">Visible</th>
            <th class="py-3 px-6 text-right">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-700">
          <tr v-for="challenge in challenges" :key="challenge.id" class="hover:bg-gray-700/50">
            <td class="py-4 px-6">{{ challenge.id }}</td>
            <td class="py-4 px-6 font-medium">{{ challenge.name }}</td>
            <td class="py-4 px-6 text-center">{{ challenge.points }}</td>
            <td class="py-4 px-6 text-center">
              <span :class="challenge.is_visible ? 'text-green-400' : 'text-gray-500'">
                {{ challenge.is_visible ? 'Yes' : 'No' }}
              </span>
            </td>
            <td class="py-4 px-6 text-right space-x-2">
              <router-link :to="{ name: 'admin-challenge-edit', params: { id: challenge.id } }" class="text-sm bg-blue-600 hover:bg-blue-700 px-3 py-1 rounded-md">
                Edit
              </router-link>
              <button @click="handleDelete(challenge.id)" class="text-sm bg-red-600 hover:bg-red-700 px-3 py-1 rounded-md">
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useAdminChallengesStore } from '../../stores/admin/challenges';
import { storeToRefs } from 'pinia';

const store = useAdminChallengesStore();
const { challenges } = storeToRefs(store);
const loading = ref(true);

onMounted(async () => {
  try {
    await store.fetchChallenges();
  } catch (error) {
    console.error("Could not fetch challenge list.", error);
    alert("Failed to load challenges.");
  } finally {
    loading.value = false;
  }
});

const handleDelete = async (challengeId) => {
  if (confirm(`Are you sure you want to delete challenge ${challengeId}? This action cannot be undone.`)) {
    try {
      await store.deleteChallenge(challengeId);
    } catch (error) {
      alert(error.detail || 'Failed to delete challenge.');
    }
  }
};
</script>```
