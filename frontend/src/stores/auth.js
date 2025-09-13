import { defineStore } from 'pinia';
import { ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import apiClient from '../services/api';

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter();
  
  // State
  const user = ref(JSON.parse(localStorage.getItem('user')));
  const accessToken = ref(localStorage.getItem('accessToken'));

  // Persist state
  watch(accessToken, (token) => {
    if (token) localStorage.setItem('accessToken', token);
    else localStorage.removeItem('accessToken');
  });

  watch(user, (newUser) => {
    if (newUser) localStorage.setItem('user', JSON.stringify(newUser));
    else localStorage.removeItem('user');
  });

  // Actions
  async function register(userInfo) {
    try {
      return await apiClient.post('/users/', userInfo);
    } catch (error) {
      throw error.response.data;
    }
  }

  async function login(credentials) {
    const formData = new FormData();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);

    try {
      const response = await apiClient.post('/token', formData, { headers: { 'Content-Type': 'multipart/form-data' } });
      accessToken.value = response.data.access_token;
      await fetchUser();
    } catch (error) {
      throw error.response.data;
    }
  }

  async function fetchUser() {
    try {
      const response = await apiClient.get('/users/me');
      user.value = response.data;
    } catch (error) {
      console.error('Failed to fetch user:', error);
      await logout();
      throw error;
    }
  }

  async function refreshUserProfile() {
    // Re-fetches user data without a full login cycle
    if (!accessToken.value) return;
    try {
        const response = await apiClient.get('/users/me');
        user.value = response.data;
    } catch (error) {
        console.error("Could not refresh user profile, token might be expired.", error);
        // If the token is invalid, this will fail. Consider logging out.
        if (error.response?.status === 401) {
            await logout();
        }
    }
  }
  
  async function logout() {
    user.value = null;
    accessToken.value = null;
    if (router) {
      router.push({ name: 'login' });
    }
  }
  
  return { user, accessToken, register, login, logout, fetchUser, refreshUserProfile };
});
