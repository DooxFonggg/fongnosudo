import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api', 
  headers: {
    'Content-Type': 'application/json',
  },
});

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('access_token') || null);
  const user = ref(JSON.parse(localStorage.getItem('user_data')) || null);

  const isAuthenticated = computed(() => !!token.value);

  async function login(credentials) {
    try {
      const response = await api.post('/admin/login', credentials);
      token.value = response.data.access_token;
      
      localStorage.setItem('access_token', response.data.access_token);
      
      return true;
    } catch (error) {
      console.error('Login failed:', error.response?.data || error.message);
      this.logout();
      throw error;
    }
  }

  function logout() {
    token.value = null;
    user.value = null;
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_data');
  }

  return {
    token,
    user,
    isAuthenticated,
    login,
    logout
  };
});