<template>
  <div>
    <h1 class="text-4xl font-bold mb-6">Platform Settings</h1>
    <div v-if="loading" class="text-center">Loading settings...</div>
    <form v-else-if="form" @submit.prevent="handleSave" class="max-w-3xl p-6 bg-gray-800 rounded-lg space-y-6">
      <!-- UI & Event -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label for="event_title" class="form-label">Event Title</label>
          <input v-model="form.event_title" type="text" id="event_title" class="form-input"/>
        </div>
        <div>
          <label for="ui_theme" class="form-label">UI Theme</label>
          <select v-model="form.ui_theme" id="ui_theme" class="form-input">
            <option>dark</option>
            <option>light</option>
          </select>
        </div>
        <div>
          <label for="event_start_time" class="form-label">Event Start Time</label>
          <input v-model="form.event_start_time" type="datetime-local" id="event_start_time" class="form-input"/>
        </div>
        <div>
          <label for="event_end_time" class="form-label">Event End Time</label>
          <input v-model="form.event_end_time" type="datetime-local" id="event_end_time" class="form-input"/>
        </div>
      </div>
      
      <!-- Toggles -->
      <fieldset class="border-t border-gray-700 pt-4">
        <legend class="text-lg font-semibold mb-2">Feature Toggles</legend>
        <div class="flex items-center space-x-6">
          <div class="flex items-center">
            <input v-model="form.allow_registrations" type="checkbox" id="allow_registrations" class="form-checkbox"/>
            <label for="allow_registrations" class="ml-2">Allow Registrations</label>
          </div>
          <div class="flex items-center">
            <input v-model="form.allow_teams" type="checkbox" id="allow_teams" class="form-checkbox"/>
            <label for="allow_teams" class="ml-2">Allow Teams</label>
          </div>
        </div>
      </fieldset>
      
      <!-- Scoring -->
       <fieldset class="border-t border-gray-700 pt-4">
        <legend class="text-lg font-semibold mb-2">Scoring</legend>
        <div>
          <label for="scoring_mode" class="form-label">Scoring Mode</label>
          <select v-model="form.scoring_mode" id="scoring_mode" class="form-input">
            <option value="static">Static</option>
            <option value="dynamic">Dynamic</option>
          </select>
        </div>
      </fieldset>
      
      <div v-if="statusMessage" :class="isError ? 'text-red-400' : 'text-green-400'" class="text-sm">
        {{ statusMessage }}
      </div>
      <div class="flex justify-end">
        <button type="submit" class="px-6 py-2 bg-indigo-600 hover:bg-indigo-700 rounded-md font-semibold">Save Settings</button>
      </div>
    </form>
  </div>
</template>

<style scoped>
.form-label { @apply block text-sm font-medium text-gray-300; }
.form-input { @apply w-full px-3 py-2 mt-1 text-white bg-gray-700 border border-gray-600 rounded-md; }
.form-checkbox { @apply h-4 w-4 text-indigo-600 bg-gray-700 border-gray-600 rounded; }
</style>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue';
import { useAdminSettingsStore } from '../../stores/admin/settings';

const store = useAdminSettingsStore();
const loading = ref(true);
const statusMessage = ref('');
const isError = ref(false);

const form = reactive({
  event_title: '', ui_theme: 'dark', event_start_time: '', event_end_time: '',
  allow_registrations: true, allow_teams: true, scoring_mode: 'static'
});

// Helper to format ISO strings to what datetime-local input expects
const toLocalISOString = (isoString) => {
  if (!isoString) return '';
  const date = new Date(isoString);
  // Adjust for timezone offset
  const tzoffset = date.getTimezoneOffset() * 60000;
  const localISOTime = (new Date(date.getTime() - tzoffset)).toISOString().slice(0, 16);
  return localISOTime;
};

watch(() => store.settings, (newSettings) => {
  if (newSettings) {
    form.event_title = newSettings.event_title;
    form.ui_theme = newSettings.ui_theme;
    form.event_start_time = toLocalISOString(newSettings.event_start_time);
    form.event_end_time = toLocalISOString(newSettings.event_end_time);
    form.allow_registrations = newSettings.allow_registrations;
    form.allow_teams = newSettings.allow_teams;
    form.scoring_mode = newSettings.scoring_mode;
  }
});

onMounted(async () => {
  try {
    await store.fetchSettings();
  } catch (error) {
    statusMessage.value = 'Failed to load settings.';
    isError.value = true;
  } finally {
    loading.value = false;
  }
});

const handleSave = async () => {
  statusMessage.value = 'Saving...';
  isError.value = false;
  try {
    const payload = { ...form };
    // Convert local time back to ISO UTC string if not empty
    payload.event_start_time = payload.event_start_time ? new Date(payload.event_start_time).toISOString() : null;
    payload.event_end_time = payload.event_end_time ? new Date(payload.event_end_time).toISOString() : null;
    await store.updateSettings(payload);
    statusMessage.value = 'Settings saved successfully!';
  } catch (error) {
    statusMessage.value = error.detail || 'Failed to save settings.';
    isError.value = true;
  }
};
</script>
