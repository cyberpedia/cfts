<template>
  <div>
    <h1 class="text-4xl font-bold mb-6">{{ isEditMode ? 'Edit Challenge' : 'Create New Challenge' }}</h1>
    <div v-if="loading" class="text-center">Loading...</div>
    <form v-else @submit.prevent="handleSubmit" class="max-w-4xl p-6 bg-gray-800 rounded-lg space-y-6">
      <!-- Core Details -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label for="name" class="block text-sm font-medium text-gray-300">Name</label>
          <input v-model="form.name" type="text" id="name" required class="form-input" />
        </div>
        <div>
          <label for="points" class="block text-sm font-medium text-gray-300">Static Points</label>
          <input v-model.number="form.points" type="number" id="points" required class="form-input" />
        </div>
      </div>
      <div>
        <label for="description" class="block text-sm font-medium text-gray-300">Description</label>
        <textarea v-model="form.description" id="description" rows="4" required class="form-input"></textarea>
      </div>
      <div>
        <label for="flag" class="block text-sm font-medium text-gray-300">Flag</label>
        <input v-model="form.flag" type="text" id="flag" required class="form-input" />
      </div>
       <div class="flex items-center">
        <input v-model="form.is_visible" type="checkbox" id="is_visible" class="h-4 w-4 text-indigo-600 bg-gray-700 border-gray-600 rounded"/>
        <label for="is_visible" class="ml-2 block text-sm text-gray-300">Is Visible to Players</label>
      </div>

      <!-- Dynamic Scoring -->
      <fieldset class="border-t border-gray-700 pt-4">
        <legend class="text-lg font-semibold mb-2">Dynamic Scoring (Optional)</legend>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <label for="initial_points" class="block text-sm font-medium text-gray-300">Initial Points</label>
            <input v-model.number="form.initial_points" type="number" id="initial_points" class="form-input" />
          </div>
          <div>
            <label for="minimum_points" class="block text-sm font-medium text-gray-300">Minimum Points</label>
            <input v-model.number="form.minimum_points" type="number" id="minimum_points" class="form-input" />
          </div>
          <div>
            <label for="decay_factor" class="block text-sm font-medium text-gray-300">Decay Factor</label>
            <input v-model.number="form.decay_factor" type="number" id="decay_factor" class="form-input" />
          </div>
        </div>
      </fieldset>

      <!-- Tags & Dependencies -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 border-t border-gray-700 pt-4">
        <div>
          <label for="tags" class="block text-sm font-medium text-gray-300">Tags</label>
          <select v-model="form.tags" id="tags" multiple class="form-input h-48">
            <option v-for="tag in tagsStore.tags" :key="tag.id" :value="tag.id">{{ tag.name }}</option>
          </select>
        </div>
        <div>
          <label for="dependencies" class="block text-sm font-medium text-gray-300">Dependencies</label>
          <select v-model="form.dependencies" id="dependencies" multiple class="form-input h-48">
            <option v-for="challenge in availableDependencies" :key="challenge.id" :value="challenge.id">{{ challenge.name }}</option>
          </select>
        </div>
      </div>
      
      <div v-if="statusMessage" :class="isError ? 'text-red-400' : 'text-green-400'" class="text-sm">
        {{ statusMessage }}
      </div>
      <div class="flex justify-end space-x-4">
        <router-link :to="{ name: 'admin-challenges' }" class="px-4 py-2 bg-gray-600 hover:bg-gray-500 rounded-md">Cancel</router-link>
        <button type="submit" class="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 rounded-md">
          {{ isEditMode ? 'Save Changes' : 'Create Challenge' }}
        </button>
      </div>
    </form>
  </div>
</template>

<style scoped>
.form-input {
  @apply w-full px-3 py-2 mt-1 text-white bg-gray-700 border border-gray-600 rounded-md;
}
</style>

<script setup>
import { ref, reactive, onMounted, computed, watch } from 'vue';
import { useAdminChallengesStore } from '../../stores/admin/challenges';
import { useAdminTagsStore } from '../../stores/admin/tags';
import { useRouter } from 'vue-router';

const props = defineProps({ id: { type: String, required: false } });
const challengesStore = useAdminChallengesStore();
const tagsStore = useAdminTagsStore();
const router = useRouter();

const isEditMode = computed(() => !!props.id);
const loading = ref(true);
const statusMessage = ref('');
const isError = ref(false);

const form = reactive({
  name: '', description: '', flag: '', points: 100, is_visible: false,
  initial_points: null, minimum_points: null, decay_factor: null,
  tags: [], dependencies: [],
});

const availableDependencies = computed(() => {
  return challengesStore.challenges.filter(c => c.id !== parseInt(props.id));
});

watch(() => challengesStore.currentChallenge, (newChallenge) => {
  if (isEditMode.value && newChallenge) {
    form.name = newChallenge.name;
    form.description = newChallenge.description;
    form.flag = newChallenge.flag;
    form.points = newChallenge.points;
    form.is_visible = newChallenge.is_visible;
    form.initial_points = newChallenge.initial_points;
    form.minimum_points = newChallenge.minimum_points;
    form.decay_factor = newChallenge.decay_factor;
    form.tags = newChallenge.tags.map(t => t.id);
    form.dependencies = newChallenge.dependencies.map(d => d.id);
  }
});

onMounted(async () => {
  try {
    await Promise.all([
      tagsStore.fetchTags(),
      challengesStore.fetchChallenges(), // For dependencies list
      isEditMode.value ? challengesStore.fetchChallenge(props.id) : Promise.resolve(),
    ]);
  } catch (error) {
    console.error('Failed to load initial data for challenge form:', error);
    statusMessage.value = 'Failed to load necessary data.';
    isError.value = true;
  } finally {
    loading.value = false;
  }
});

const handleSubmit = async () => {
  statusMessage.value = '';
  isError.value = false;
  
  // Clean up nullable fields
  const payload = { ...form };
  if (payload.initial_points === '') payload.initial_points = null;
  if (payload.minimum_points === '') payload.minimum_points = null;
  if (payload.decay_factor === '') payload.decay_factor = null;

  try {
    if (isEditMode.value) {
      await challengesStore.updateChallenge({ challengeId: parseInt(props.id), data: payload });
      statusMessage.value = 'Challenge updated successfully!';
    } else {
      await challengesStore.createChallenge(payload);
      statusMessage.value = 'Challenge created successfully!';
    }
    setTimeout(() => router.push({ name: 'admin-challenges' }), 1500);
  } catch (error) {
    isError.value = true;
    statusMessage.value = error.detail || `Failed to ${isEditMode.value ? 'update' : 'create'} challenge.`;
  }
};
</script>
