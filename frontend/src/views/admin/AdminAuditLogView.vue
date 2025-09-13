<template>
  <div>
    <h1 class="text-4xl font-bold mb-6">Audit Log</h1>
    <div v-if="loading" class="text-center">Loading logs...</div>
    <div v-else class="bg-gray-800 rounded-lg shadow-lg overflow-x-auto">
      <table class="min-w-full">
        <thead class="bg-gray-700">
          <tr>
            <th class="py-3 px-6 text-left">Timestamp</th>
            <th class="py-3 px-6 text-left">User</th>
            <th class="py-3 px-6 text-left">Action</th>
            <th class="py-3 px-6 text-left">Details</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-700">
          <tr v-for="log in logs" :key="log.id" class="hover:bg-gray-700/50">
            <td class="py-4 px-6 whitespace-nowrap">{{ new Date(log.timestamp).toLocaleString() }}</td>
            <td class="py-4 px-6">{{ log.user ? `${log.user.username} (ID: ${log.user.id})` : 'System/Anonymous' }}</td>
            <td class="py-4 px-6 font-mono text-cyan-400">{{ log.action }}</td>
            <td class="py-4 px-6 text-sm text-gray-300">
              <pre class="bg-gray-900 p-2 rounded-md max-w-md overflow-x-auto"><code>{{ JSON.stringify(log.details, null, 2) }}</code></pre>
            </td>
          </tr>
        </tbody>
      </table>
      <!-- Simple pagination placeholder -->
      <div class="p-4 text-center text-gray-400">
        Pagination controls would go here.
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useAdminLogsStore } from '../../stores/admin/logs';
import { storeToRefs } from 'pinia';

const store = useAdminLogsStore();
const { logs } = storeToRefs(store);
const loading = ref(true);

onMounted(async () => {
  try {
    await store.fetchLogs();
  } catch (error) {
    alert("Failed to load audit logs.");
  } finally {
    loading.value = false;
  }
});
</script>
