<template>
  <div class="container auth-form-container">
    <h1 class="form-title">Đăng nhập Admin</h1>
    <form @submit.prevent="login" class="auth-form">
      <div class="form-group">
        <label for="username">Tên đăng nhập:</label>
        <input type="text" id="username" v-model="username" required>
      </div>
      <div class="form-group">
        <label for="password">Mật khẩu:</label>
        <input type="password" id="password" v-model="password" required>
      </div>
      <button type="submit" class="submit-button">Đăng nhập</button>
      <p v-if="error" class="error-message">{{ error }}</p>
    </form>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/api'; // Import api instance

export default {
  name: 'AdminLoginPage',
  setup() {
    const username = ref('');
    const password = ref('');
    const error = ref('');
    const router = useRouter();

    const login = async () => {
      error.value = ''; // Clear previous errors
      try {
        const response = await api.post('/auth/login', {
          username: username.value,
          password: password.value
        });
        const token = response.data.access_token;
        localStorage.setItem('access_token', token); // Lưu token vào Local Storage
        console.log('Login successful, token:', token);
        router.push('/admin/dashboard'); // Điều hướng đến trang quản lý admin
      } catch (err) {
        console.error('Login failed:', err.response ? err.response.data : err.message);
        error.value = err.response && err.response.data && err.response.data.msg ? err.response.data.msg : 'Đăng nhập thất bại. Vui lòng thử lại.';
      }
    };

    return {
      username,
      password,
      error,
      login
    };
  }
}
</script>

<style scoped>
.auth-form-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 150px);
}

.form-title {
  font-size: 2rem;
  color: var(--background-color-dark);
  margin-bottom: 2rem;
}

.auth-form {
  background-color: var(--card-background);
  padding: 2.5rem;
  border-radius: 8px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--text-color-dark);
}

.submit-button {
  width: 100%;
  padding: 0.85rem;
  font-size: 1.1rem;
  background-color: var(--primary-color);
  color: var(--background-color-dark);
}

.submit-button:hover {
  background-color: var(--accent-hover);
  color: var(--primary-color);
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.error-message {
  color: #e74c3c;
  margin-top: 1rem;
  text-align: center;
  font-size: 0.9rem;
}
</style>