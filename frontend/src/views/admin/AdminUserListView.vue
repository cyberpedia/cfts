<template>
  <div>
    <h1 class="text-4xl font-bold mb-6">User Management</h1>
    <div v-if="loading" class="text-center">Loading users...</div>
    <div v-else class="bg-gray-800 rounded-lg shadow-lg overflow-hidden">
      <table class="min-w-full">
        <thead class="bg-gray-700">
          <tr>
            <th class="py-3 px-6 text-left">ID</th>
            <th class="py-3 px-6 text-left">Username</th>
            <th class="py-3 px-6 text-left">Email</th>
            <th class="py-3 px-6 text-center">Score</th>
            <th class="py-3 px-6 text-center">Active</th>
            <th class="py-3 px-6 text-center">Admin</th>
            <th class="py-3 px-6 text-right">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-700">
          <tr v-for="user in users" :key="user.id" class="hover:bg-gray-700/50">
            <td class="py-4 px-6">{{ user.id }}</td>
            <td class="py-4 px-6 font-medium">{{ user.username }}</td>
            <td class="py-4 px-6">{{ user.email }}</td>
            <td class="py-4 px-6 text-center">{{ user.score }}</td>
            <td class="py-4 px-6 text-center">
              <span :class="user.is_active ? 'text-green-400' : 'text-red-400'">
                {{ user.is_active ? 'Yes' : 'No' }}
              </span>
            </td>
            <td class="py-4 px-6 text-center">
              <span :class="user.is_staff ? 'text-green-400' : 'text-gray-400'">
                {{ user.is_staff ? 'Yes' : 'No' }}
              </span>
            </td>
            <td class="py-4 px-6 text-right space-x-2">
              <router-link :to="{ name: 'admin-user-edit', params: { id: user.id } }" class="text-sm bg-blue-600 hover:bg-blue-700 px-3 py-1 rounded-md">
                Edit
              </router-link>
              <button @click="handleDelete(user.id)" class="text-sm bg-red-600 hover:bg-red-700 px-3 py-1 rounded-md">
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
import { useAdminUsersStore } from '../../stores/admin/users';
import { storeToRefs } from 'pinia';

const store = useAdminUsersStore();
const { users } = storeToRefs(store);
const loading = ref(true);

onMounted(async () => {
  try {
    await store.fetchUsers();
  } catch (error) {
    console.error("Could not fetch user list.", error);
    alert("Failed to load users.");
  } finally {
    loading.value = false;
  }
});

const handleDelete = async (userId) => {
  if (confirm(`Are you sure you want to delete user ${userId}? This action cannot be undone.`)) {
    try {
      await store.deleteUser(userId);
    } catch (error) {
      alert(error.detail || 'Failed to delete user.');
    }
  }
};
</script>
