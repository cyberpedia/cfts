<template>
  <div class="p-8 max-w-4xl mx-auto text-white">
    <div v-if="user" class="space-y-8">
      <!-- User Info Header -->
      <div class="bg-gray-800 p-6 rounded-lg shadow-lg text-center">
        <h1 class="text-4xl font-bold">{{ user.username }}</h1>
        <p class="text-xl text-indigo-400 mt-2">{{ user.score }} Points</p>
        <p v-if="teamName" class="text-lg text-gray-400 mt-1">Team: {{ teamName }}</p>
      </div>

      <!-- Badges Section -->
      <div>
        <h2 class="text-3xl font-bold mb-4">Badges Earned</h2>
        <div v-if="!user.badges || !user.badges.length" class="bg-gray-800 p-6 rounded-lg text-gray-400">
          No badges earned yet. Keep solving challenges!
        </div>
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div v-for="userBadge in user.badges" :key="userBadge.badge.id" class="bg-gray-800 p-4 rounded-lg flex items-center space-x-4">
            <img v-if="userBadge.badge.icon_url" :src="userBadge.badge.icon_url" alt="Badge icon" class="w-16 h-16">
            <div v-else class="w-16 h-16 bg-gray-700 rounded-full flex items-center justify-center text-2xl">🏆</div>
            <div>
              <h3 class="font-bold text-lg">{{ userBadge.badge.name }}</h3>
              <p class="text-sm text-gray-400">{{ userBadge.badge.description }}</p>
              <p class="text-xs text-gray-500 mt-1">Awarded: {{ new Date(userBadge.awarded_at).toLocaleDateString() }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="text-center">
      Loading profile...
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, watch } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useTeamsStore } from '../stores/teams';
import { storeToRefs } from 'pinia';

const authStore = useAuthStore();
const teamsStore = useTeamsStore();
const { user } = storeToRefs(authStore);
const { currentTeamDetails } = storeToRefs(teamsStore);

const teamName = ref('');

const fetchTeamName = async (teamId) => {
    if (!teamId) {
        teamName.value = '';
        return;
    }
    // Simple optimization: check if we already have the details
    if (currentTeamDetails.value && currentTeamDetails.value.id === teamId) {
        teamName.value = currentTeamDetails.value.name;
    } else {
        try {
            // Fetch team details to get the name
            await teamsStore.fetchTeamDetails(teamId);
            teamName.value = teamsStore.currentTeamDetails?.name || '';
        } catch (e) {
            console.error("Couldn't fetch team name for profile");
            teamName.value = 'Unknown';
        }
    }
};

onMounted(() => {
    fetchTeamName(user.value?.team_id);
});

// Watch for changes in the user's team ID (e.g., after joining/leaving a team)
watch(() => user.value?.team_id, (newTeamId) => {
    fetchTeamName(newTeamId);
});

</script>
