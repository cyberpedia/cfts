import { defineStore } from 'pinia';
import { ref } from 'vue';
import apiClient from '../services/api';
import { useAuthStore } from './auth';

export const useTeamsStore = defineStore('teams', () => {
  // State
  const teams = ref([]);
  const currentTeamDetails = ref(null);

  // Actions
  async function fetchTeams() {
    try {
      const response = await apiClient.get('/teams/');
      teams.value = response.data;
    } catch (error) {
      console.error('Failed to fetch teams:', error);
      throw error;
    }
  }
  
  async function fetchTeamDetails(teamId) {
    try {
      const response = await apiClient.get(`/teams/${teamId}`);
      currentTeamDetails.value = response.data;
    } catch (error) {
      console.error('Failed to fetch team details:', error);
      throw error;
    }
  }

  async function createTeam(teamName) {
    const authStore = useAuthStore();
    try {
      await apiClient.post('/teams/', { name: teamName });
      await authStore.fetchUser(); // Refresh user data to get new team_id
    } catch (error) {
      console.error('Failed to create team:', error);
      throw error.response.data;
    }
  }

  async function joinTeam(teamId) {
    const authStore = useAuthStore();
    try {
      await apiClient.post(`/teams/${teamId}/join`);
      await authStore.fetchUser(); // Refresh user data
    } catch (error) {
      console.error('Failed to join team:', error);
      throw error.response.data;
    }
  }

  async function leaveTeam() {
    const authStore = useAuthStore();
    try {
      await apiClient.post('/teams/leave');
      currentTeamDetails.value = null; // Clear details view
      await authStore.fetchUser(); // Refresh user data
    } catch (error) {
      console.error('Failed to leave team:', error);
      throw error.response.data;
    }
  }

  return { teams, currentTeamDetails, fetchTeams, fetchTeamDetails, createTeam, joinTeam, leaveTeam };
});
