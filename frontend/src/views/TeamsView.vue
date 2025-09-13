<template>
  <div class="p-8 text-white">
    <h1 class="text-4xl font-bold mb-8">Teams</h1>

    <!-- View when team functionality is disabled -->
    <div v-if="!settingsStore.settings?.allow_teams" class="text-center text-gray-400 bg-gray-800 p-8 rounded-lg">
      <p>Team functionality is currently disabled by the administrators.</p>
    </div>

    <!-- Main view when enabled -->
    <div v-else>
      <!-- View for users already on a team -->
      <div v-if="authStore.user?.team_id">
        <div v-if="loadingTeam" class="text-center">Loading your team...</div>
        <div v-else-if="teamsStore.currentTeamDetails" class="bg-gray-800 p-6 rounded-lg">
          <h2 class="text-3xl font-bold mb-4">{{ teamsStore.currentTeamDetails.name }}</h2>
          <h3 class="text-xl font-semibold mb-3 text-gray-300">Members</h3>
          <ul class="list-disc list-inside mb-6">
            <li v-for="member in teamsStore.currentTeamDetails.members" :key="member.id">
              {{ member.username }} - {{ member.score }} points
            </li>
          </ul>
          <button @click="handleLeaveTeam" class="bg-red-600 hover:bg-red-700 text-white font-semibold py-2 px-4 rounded-md">
            Leave Team
          </button>
        </div>
      </div>

      <!-- View for users not on a team -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <!-- Create Team -->
        <div class="bg-gray-800 p-6 rounded-lg">
          <h2 class="text-2xl font-semibold mb-4">Create a New Team</h2>
          <form @submit.prevent="handleCreateTeam" class="space-y-4">
            <div>
              <label for="teamName" class="block text-sm font-medium text-gray-300">Team Name</label>
              <input v-model="newTeamName" type="text" id="teamName" required class="w-full px-3 py-2 mt-1 text-white bg-gray-700 border border-gray-600 rounded-md">
            </div>
            <p v-if="formError" class="text-sm text-red-400">{{ formError }}</p>
            <button type="submit" class="w-full py-2 font-semibold text-white bg-indigo-600 rounded-md hover:bg-indigo-700">
              Create Team
            </button>
          </form>
        </div>

        <!-- Join Team -->
        <div class="bg-gray-800 p-6 rounded-lg">
          <h2 class="text-2xl font-semibold mb-4">Join an Existing Team</h2>
          <div v-if="loadingTeams" class="text-center">Loading teams...</div>
          <ul v-else class="space-y-3 max-h-96 overflow-y-auto">
            <li v-for="team in teamsStore.teams" :key="team.id" class="flex justify-between items-center bg-gray-700 p-3 rounded-md">
              <span>{{ team.name }}</span>
              <button @click="handleJoinTeam(team.id)" class="bg-green-600 hover:bg-green-700 text-white font-semibold py-1 px-3 rounded-md text-sm">
                Join
              </button>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useTeamsStore } from '../stores/teams';
import { useSettingsStore } from '../stores/settings';

const authStore = useAuthStore();
const teamsStore = useTeamsStore();
const settingsStore = useSettingsStore();

const loadingTeam = ref(false);
const loadingTeams = ref(false);
const newTeamName = ref('');
const formError = ref('');

const fetchUserTeamDetails = async (teamId) => {
  if (teamId) {
    loadingTeam.value = true;
    try {
      await teamsStore.fetchTeamDetails(teamId);
    } catch (error) {
      console.error("Could not fetch user's team details", error);
    } finally {
      loadingTeam.value = false;
    }
  }
};

onMounted(async () => {
  if (settingsStore.settings?.allow_teams) {
    if (authStore.user?.team_id) {
      fetchUserTeamDetails(authStore.user.team_id);
    } else {
      loadingTeams.value = true;
      try {
        await teamsStore.fetchTeams();
      } catch (error) {
        console.error("Could not fetch teams list", error);
      } finally {
        loadingTeams.value = false;
      }
    }
  }
});

watch(() => authStore.user?.team_id, (newTeamId, oldTeamId) => {
  if (newTeamId) {
    fetchUserTeamDetails(newTeamId);
  } else if (oldTeamId && !newTeamId) {
    teamsStore.fetchTeams(); // User left a team, refresh list
  }
});

const handleCreateTeam = async () => {
  formError.value = '';
  if (!newTeamName.value.trim()) {
    formError.value = 'Team name cannot be empty.';
    return;
  }
  try {
    await teamsStore.createTeam(newTeamName.value);
    newTeamName.value = ''; // Clear form on success
  } catch (error) {
    formError.value = error.detail || 'Failed to create team.';
  }
};

const handleJoinTeam = async (teamId) => {
  try {
    await teamsStore.joinTeam(teamId);
  } catch (error) {
    alert(error.detail || 'Could not join team.');
  }
};

const handleLeaveTeam = async () => {
  if (confirm('Are you sure you want to leave your team?')) {
    try {
      await teamsStore.leaveTeam();
    } catch (error) {
      alert(error.detail || 'Could not leave team.');
    }
  }
};
</script>
