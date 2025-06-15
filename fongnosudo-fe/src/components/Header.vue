<template>
  <header class="main-header">
    <div class="container header-content">
      <router-link to="/" class="logo">
        <img class="logo-icon" src="../assets/logo-fongnosudo-2.png" alt="">
        <span class="logo-text">fongnosudo</span>
      </router-link>

      <nav class="main-nav">
        <ul>
          <li><router-link to="/blog" active-class="active-link">Bài viết</router-link></li>
          <li><router-link to="/about" active-class="active-link">Giới thiệu</router-link></li>
        </ul>
      </nav>

      <div class="header-right">
        <div class="search-box">
          <input class="search-input" type="text" placeholder="Tìm kiếm bài viết..." v-model="searchQuery"
            @keyup.enter="performSearch" />
          <button @click="performSearch" class="search-button">
            <svg class="search-icon" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
              <path fill-rule="evenodd"
                d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z"
                clip-rule="evenodd"></path>
            </svg>
          </button>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';


export default {
  name: 'MainHeader',
  setup() {
    const searchQuery = ref('');
    const router = useRouter();

    const performSearch = () => {
      if (searchQuery.value.trim()) {
        router.push({
          path: '/blog',
          query: { search: searchQuery.value.trim() } // Đổi từ 'q' thành 'search'
        });
        searchQuery.value = ''; // Clear search after redirect
      }
    };

    return {
      searchQuery,
      performSearch,
    };
  }
};
</script>

<style scoped>
.main-header {
  background-color: var(--background-color-dark);
  color: var(--text-color-light);
  /* padding: 0.1rem 0; */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-color-light);
  text-decoration: none;
}

.logo-icon {
  /* Placeholder for an actual logo image or SVG */
  width: 80px;
  /* Example size */
  height: 60px;
  /* Example size */
  background-color: var(--primary-color);
  /* Just for visualization */
  border-radius: 4px;
  margin-right: 8px;
}

.main-nav ul {
  list-style: none;
  display: flex;
  gap: 1.5rem;
}

.main-nav a {
  color: var(--text-color-light);
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.main-nav a:hover,
.main-nav a.active-link {
  background-color: rgba(255, 255, 255, 0.1);
  text-decoration: none;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.search-box {
  display: flex;
  align-items: center;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 5px;
  padding: 0.25rem 0.5rem;
}

.search-box .search-input {
  color: var(--primary-color);
}

.search-box input {
  background: transparent;
  border: none;
  color: var(--text-color-light);
  padding: 0.5rem;
  margin-bottom: 0;
  /* Override main.css margin */
  width: 180px;
  /* Adjust as needed */
}

.search-box input::placeholder {
  color: var(--primary-color);
  opacity: 0.7;
  font-style: italic;
}

.search-box input:focus {
  outline: none;
  box-shadow: none;
}

.search-button {
  background: none;
  border: none;
  padding: 0.5rem;
  cursor: pointer;
  color: var(--text-color-light);
  display: flex;
  /* To center SVG */
  align-items: center;
  justify-content: center;
}

.search-button:hover {
  color: var(--primary-color);
  background: none;
  /* No background change on hover for button */
}

.search-icon {
  width: 1.25rem;
  height: 1.25rem;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .header-content {
    flex-wrap: wrap;
    justify-content: center;
    gap: 1rem;
  }

  .main-nav ul {
    width: 100%;
    justify-content: center;
    gap: 1rem;
  }

  .header-right {
    width: 100%;
    justify-content: center;
  }

  .search-box {
    width: 100%;
    max-width: 300px;
    /* Limit search box width on small screens */
  }
}


.logo-text {
  font-size: 1.8rem;
}
</style>