import { defineStore } from 'pinia';
import { ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import apiClient from '../services/api';
import { useSolvesStore } from './solves';

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter();
  
  const user = ref(JSON.parse(localStorage.getItem('user')));
  const accessToken = ref(localStorage.getItem('accessToken'));

  watch(accessToken, (token) => {
    if (token) localStorage.setItem('accessToken', token);
    else localStorage.removeItem('accessToken');
  });

  watch(user, (newUser) => {
    if (newUser) localStorage.setItem('user', JSON.stringify(newUser));
    else localStorage.removeItem('user');
  });

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
    const solvesStore = useSolvesStore();
    try {
      const response = await apiClient.get('/users/me');
      user.value = response.data;
      solvesStore.populateUserSolves(response.data.solves || []);
    } catch (error) {
      console.error('Failed to fetch user:', error);
      await logout();
      throw error;
    }
  }

  async function refreshUserProfile() {
    if (!accessToken.value) return;
    const solvesStore = useSolvesStore();
    try {
        const response = await apiClient.get('/users/me');
        user.value = response.data;
        solvesStore.populateUserSolves(response.data.solves || []);
    } catch (error) {
        console.error("Could not refresh user profile.", error);
        if (error.response?.status === 401) {
            await logout();
        }
    }
  }
  
  async function handleSocialLogin(token) {
    accessToken.value = token;
    await fetchUser();
  }

  async function logout() {
    user.value = null;
    accessToken.value = null;
    // Also clear solves on logout
    const solvesStore = useSolvesStore();
    solvesStore.clearSolves();
    
    if (router) {
      router.push({ name: 'login' });
    }
  }
  
  return { user, accessToken, register, login, logout, fetchUser, refreshUserProfile, handleSocialLogin };
});
