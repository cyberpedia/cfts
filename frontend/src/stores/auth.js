import { defineStore } from 'pinia';
import { ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import apiClient from '../services/api';

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter();
  
  // State
  const user = ref(JSON.parse(localStorage.getItem('user')));
  const accessToken = ref(localStorage.getItem('accessToken'));

  // Persist state to localStorage whenever it changes
  watch(accessToken, (newToken) => {
    if (newToken) {
      localStorage.setItem('accessToken', newToken);
    } else {
      localStorage.removeItem('accessToken');
    }
  });

  watch(user, (newUser) => {
    if (newUser) {
      localStorage.setItem('user', JSON.stringify(newUser));
    } else {
      localStorage.removeItem('user');
    }
  });

  // Actions
  async function register(userInfo) {
    try {
      const response = await apiClient.post('/users/', userInfo);
      // On success, you might want to automatically log them in or just redirect
      // For now, we'll redirect to login with a success message
      return response.data;
    } catch (error) {
      throw error.response.data;
    }
  }

  async function login(credentials) {
    // FastAPI's OAuth2PasswordRequestForm requires form data
    const formData = new FormData();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);

    try {
      const response = await apiClient.post('/token', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      accessToken.value = response.data.access_token;
      
      // After getting the token, fetch the user's profile
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
      // If fetching the user fails, the token might be invalid, so log out
      console.error('Failed to fetch user:', error);
      await logout();
      throw error;
    }
  }
  
  async function logout() {
    user.value = null;
    accessToken.value = null;
    if (router) {
      router.push({ name: 'login' });
    }
  }
  
  return { user, accessToken, register, login, logout, fetchUser };
});
