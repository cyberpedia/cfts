<template>
  <div>
    <h1 class="text-4xl font-bold mb-6">Edit User</h1>
    <div v-if="loading" class="text-center">Loading user data...</div>
    <div v-else-if="!user" class="text-center text-red-400">User not found.</div>
    <form v-else @submit.prevent="handleUpdate" class="max-w-2xl p-6 bg-gray-800 rounded-lg space-y-6">
      <div>
        <label class="block text-sm font-medium text-gray-300">Username</label>
        <input type="text" :value="user.username" disabled class="w-full px-3 py-2 mt-1 text-gray-400 bg-gray-700 border border-gray-600 rounded-md cursor-not-allowed"/>
      </div>
      <div>
        <label for="score" class="block text-sm font-medium text-gray-300">Score</label>
        <input v-model.number="form.score" type="number" id="score" class="w-full px-3 py-2 mt-1 text-white bg-gray-700 border border-gray-600 rounded-md"/>
      </div>
      <div>
        <label for="team_id" class="block text-sm font-medium text-gray-300">Team ID (Optional)</label>
        <input v-model.number="form.team_id" type="number" id="team_id" placeholder="Enter Team ID or leave blank" class="w-full px-3 py-2 mt-1 text-white bg-gray-700 border border-gray-600 rounded-md"/>
      </div>
      <div class="flex items-center space-x-4">
        <div class="flex items-center">
          <input v-model="form.is_active" type="checkbox" id="is_active" class="h-4 w-4 text-indigo-600 bg-gray-700 border-gray-600 rounded"/>
          <label for="is_active" class="ml-2 block text-sm text-gray-300">Is Active</label>
        </div>
        <div class="flex items-center">
          <input v-model="form.is_staff" type="checkbox" id="is_staff" class="h-4 w-4 text-indigo-600 bg-gray-700 border-gray-600 rounded"/>
          <label for="is_staff" class="ml-2 block text-sm text-gray-300">Is Staff (Admin)</label>
        </div>
      </div>
      <div v-if="statusMessage" :class="isError ? 'text-red-400' : 'text-green-400'" class="text-sm">
        {{ statusMessage }}
      </div>
      <div class="flex justify-end space-x-4">
        <router-link :to="{ name: 'admin-users' }" class="px-4 py-2 bg-gray-600 hover:bg-gray-500 rounded-md">Cancel</router-link>
        <button type="submit" class="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 rounded-md">Save Changes</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue';
import { useAdminUsersStore } from '../../stores/admin/users';
import { storeToRefs } from 'pinia';
import { useRouter } from 'vue-router';

const props = defineProps({ id: { type: String, required: true } });
const store = useAdminUsersStore();
const router = useRouter();
const { currentUser: user } = storeToRefs(store);

const loading = ref(true);
const statusMessage = ref('');
const isError = ref(false);

const form = reactive({
  score: 0,
  is_staff: false,
  is_active: false,
  team_id: null,
});

// Sync form with fetched user data
watch(user, (newUser) => {
  if (newUser) {
    form.score = newUser.score;
    form.is_staff = newUser.is_staff;
    form.is_active = newUser.is_active;
    form.team_id = newUser.team_id;
  }
});

onMounted(async () => {
  try {
    await store.fetchUser(props.id);
  } catch (error) {
    console.error('Failed to fetch user for editing.', error);
  } finally {
    loading.value = false;
  }
});

const handleUpdate = async () => {
  statusMessage.value = '';
  isError.value = false;
  try {
    const dataToUpdate = { ...form };
    // API might not accept an empty string for a nullable integer
    if (dataToUpdate.team_id === '') {
        dataToUpdate.team_id = null;
    }
    await store.updateUser({ userId: parseInt(props.id), data: dataToUpdate });
    statusMessage.value = 'User updated successfully!';
    setTimeout(() => router.push({ name: 'admin-users' }), 1500);
  } catch (error) {
    isError.value = true;
    statusMessage.value = error.detail || 'Failed to update user.';
  }
};
</script>
