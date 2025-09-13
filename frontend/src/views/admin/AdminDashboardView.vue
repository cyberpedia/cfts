<template>
  <div>
    <h1 class="text-4xl font-bold mb-6">Admin Dashboard</h1>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <!-- Total Users -->
      <div class="bg-gray-800 p-6 rounded-lg shadow-lg">
        <h2 class="text-lg font-semibold text-gray-400">Total Users</h2>
        <p class="text-4xl font-bold mt-2">{{ stats.totalUsers }}</p>
      </div>
      <!-- Total Challenges -->
      <div class="bg-gray-800 p-6 rounded-lg shadow-lg">
        <h2 class="text-lg font-semibold text-gray-400">Total Challenges</h2>
        <p class="text-4xl font-bold mt-2">{{ stats.totalChallenges }}</p>
      </div>
      <!-- Total Solves -->
      <div class="bg-gray-800 p-6 rounded-lg shadow-lg">
        <h2 class="text-lg font-semibold text-gray-400">Total Solves</h2>
        <p class="text-4xl font-bold mt-2">{{ stats.totalSolves }}</p>
      </div>
       <!-- Pending Writeups -->
       <div class="bg-gray-800 p-6 rounded-lg shadow-lg">
        <h2 class="text-lg font-semibold text-gray-400">Pending Writeups</h2>
        <p class="text-4xl font-bold mt-2">{{ stats.pendingWriteups }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, onMounted } from 'vue';
import { useAdminUsersStore } from '../../stores/admin/users';
import { useAdminChallengesStore } from '../../stores/admin/challenges';
import { useAdminWriteupsStore } from '../../stores/admin/writeups';

const usersStore = useAdminUsersStore();
const challengesStore = useAdminChallengesStore();
const writeupsStore = useAdminWriteupsStore();

const stats = reactive({
  totalUsers: 0,
  totalChallenges: 0,
  totalSolves: 0,
  pendingWriteups: 0,
});

onMounted(async () => {
    try {
        await Promise.all([
            usersStore.fetchUsers(),
            challengesStore.fetchChallenges(),
            writeupsStore.fetchWriteups(),
        ]);
        stats.totalUsers = usersStore.users.length;
        stats.totalChallenges = challengesStore.challenges.length;
        // This is an approximation. A real API would provide this aggregate.
        stats.totalSolves = challengesStore.challenges.reduce((acc, chal) => acc + (chal.solves?.length || 0), 0);
        stats.pendingWriteups = writeupsStore.writeups.filter(w => w.status === 'pending').length;
    } catch (error) {
        console.error("Failed to load dashboard stats", error);
    }
});
</script>
