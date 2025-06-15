<template>
  <div class="container">
    <h3 class="page-title animate-fade-in-up">Tất cả bài viết</h3>

    <!-- Search & Filter Section -->
    <div class="filter-search-area animate-fade-in-up" style="animation-delay: 0.2s;">
      <div class="search-container">
        <!-- <input 
          type="text" 
          placeholder="Tìm kiếm bài viết..." 
          v-model="searchQuery" 
          @keyup.enter="performSearch"
          @input="debounceSearch"
          class="search-input"
        > -->
        <!-- <button @click="performSearch" class="search-button-page">
          <i class="fas fa-search"></i>
        </button> -->
      </div>

      <div class="category-filter">
        <select v-model="selectedCategory" @change="applyFilters" class="category-select">
          <option value="">Tất cả chủ đề</option>
          <option value="Kubernetes">Kubernetes</option>
          <option value="docker">Docker</option>
          <option value="monitoring">Monitoring</option>
          <option value="CI/CD">CI/CD</option>
          <option value="devops">DevOps</option>
          <option value="automation">Automation</option>
        </select>
      </div>

      <!-- Active Filters Display -->
      <div v-if="hasActiveFilters" class="active-filters">
        <!-- <span class="filter-label">Bộ lọc:</span> -->
        <span v-if="searchQuery" class="filter-tag">
          Tìm kiếm: "{{ searchQuery }}"
          <button @click="clearSearch" class="clear-filter">×</button>
        </span>
        <span v-if="selectedCategory" class="filter-tag">
          Chủ đề: {{ getCategoryLabel(selectedCategory) }}
          <button @click="clearCategory" class="clear-filter">×</button>
        </span>
        <button @click="clearAllFilters" class="clear-all-filters">Xóa tất cả</button>
      </div>
    </div>

    <!-- Loading/Error/Content -->
    <div v-if="loading" class="loading-message animate-fade-in-up">
      <p><i class="fas fa-spinner animate-spin"></i> Đang tải bài viết...</p>
    </div>

    <div v-else-if="error" class="error-message animate-fade-in-up">
      <p style="color: red;"><i class="fas fa-exclamation-triangle"></i> {{ error }}</p>
    </div>

    <div v-else-if="posts.length > 0" class="posts-grid">
      <router-link v-for="post in posts" :key="post.id" :to="`/blog/${post.slug}`" class="post-card-link">
        <div class="post-card">
          <div class="post-image-wrapper">
            <img v-if="post.image_url" :src="post.image_url" :alt="post.title" @error="handleImageError" />
            <div v-else class="placeholder-image">
              <i class="fas fa-image"></i>
            </div>
            <div class="image-overlay"></div>
          </div>

          <div class="post-content">
            <p class="post-title">{{ post.title }}</p>

            <div class="post-meta">
              <span class="post-author">
                <i class="fas fa-user"></i>
                {{ post.author }}
              </span>
              <span class="post-date">
                <i class="fas fa-clock"></i>
                {{ formatDate(post.created_at) }}
              </span>
            </div>
          </div>
        </div>
      </router-link>
    </div>

    <div v-else class="no-posts-message">
      <p><i class="fas fa-search"></i> Không có bài viết nào được tìm thấy.</p>
      <p v-if="hasActiveFilters" class="suggestion">
        Thử <button @click="clearAllFilters" class="link-button">xóa bộ lọc</button> để xem tất cả bài viết.
      </p>
    </div>

    <!-- New Pagination Component -->
    <div v-if="pagination.total_pages > 1" class="pagination">
      <!-- Previous button -->
      <button @click="changePage(pagination.current_page - 1)" :disabled="!pagination.has_prev"
        class="pagination-btn pagination-nav" title="Trang trước">
        <i class="fas fa-chevron-left"></i>
      </button>

      <!-- Page numbers -->
      <template v-for="page in pageNumbers" :key="page">
        <button v-if="page !== '...'" @click="changePage(page)"
          :class="['pagination-btn', 'pagination-number', { 'active': page === pagination.current_page }]">
          {{ page }}
        </button>
        <span v-else class="pagination-ellipsis">...</span>
      </template>

      <!-- Next button -->
      <button @click="changePage(pagination.current_page + 1)" :disabled="!pagination.has_next"
        class="pagination-btn pagination-nav" title="Trang sau">
        <i class="fas fa-chevron-right"></i>
      </button>
    </div>

    <!-- Test lọc -->
    <!-- <div v-if="pagination.total_posts > 0" class="pagination-info">
      Hiển thị {{ ((pagination.current_page - 1) * pagination.per_page) + 1 }} -
      {{ Math.min(pagination.current_page * pagination.per_page, pagination.total_posts) }}
      của {{ pagination.total_posts }} bài viết
      <span v-if="hasActiveFilters"> (đã lọc)</span>
    </div> -->
  </div>
</template>

<script>
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '@/api/index.js';

export default {
  name: 'Blog',
  setup() {
    const route = useRoute();
    const router = useRouter();

    const posts = ref([]);
    const loading = ref(true);
    const error = ref(null);
    const searchQuery = ref(route.query.search || '');
    const selectedCategory = ref(route.query.category || '');
    const searchTimeout = ref(null);

    const pagination = ref({
      current_page: 1,
      total_pages: 1,
      total_posts: 0,
      per_page: 6,
      has_next: false,
      has_prev: false
    });

    const categoryLabels = {
      'k8s': 'Kubernetes',
      'docker': 'Docker',
      'monitoring': 'Monitoring',
      'ci-cd': 'CI/CD',
      'devops': 'DevOps',
      'automation': 'Automation'
    };

    const hasActiveFilters = computed(() => {
      return searchQuery.value.trim() !== '' || selectedCategory.value !== '';
    });

    const fetchPosts = async (page = 1, resetPage = false) => {
      loading.value = true;
      error.value = null;

      try {
        const params = {
          page: resetPage ? 1 : page,
          per_page: 6
        };

        if (searchQuery.value.trim()) {
          params.search = searchQuery.value.trim();
        }

        if (selectedCategory.value) {
          params.category = selectedCategory.value;
        }

        const response = await api.get('/posts', { params });

        if (response.data && response.data.posts) {
          posts.value = response.data.posts;
          pagination.value = response.data.pagination;

          // Update URL without page reload
          updateURL();
        } else {
          // Fallback for current API structure (array directly)
          if (Array.isArray(response.data)) {
            const allPosts = response.data;

            // Client-side filtering if backend doesn't support it yet
            let filteredPosts = allPosts;

            if (searchQuery.value.trim()) {
              const searchTerm = searchQuery.value.toLowerCase();
              filteredPosts = filteredPosts.filter(post =>
                post.title.toLowerCase().includes(searchTerm)
              );
            }

            if (selectedCategory.value) {
              const categoryTerm = selectedCategory.value.toLowerCase();
              filteredPosts = filteredPosts.filter(post =>
                post.title.toLowerCase().includes(categoryTerm) ||
                (post.content && post.content.toLowerCase().includes(categoryTerm))
              );
            }

            // Client-side pagination
            const startIndex = (page - 1) * 6;
            const endIndex = startIndex + 6;
            const paginatedPosts = filteredPosts.slice(startIndex, endIndex);

            posts.value = paginatedPosts;
            pagination.value = {
              current_page: page,
              total_pages: Math.ceil(filteredPosts.length / 6),
              total_posts: filteredPosts.length,
              per_page: 6,
              has_next: page < Math.ceil(filteredPosts.length / 6),
              has_prev: page > 1
            };

            updateURL();
          } else {
            posts.value = [];
            pagination.value = {
              current_page: 1,
              total_pages: 1,
              total_posts: 0,
              per_page: 6,
              has_next: false,
              has_prev: false
            };
          }
        }

      } catch (err) {
        console.error('Error fetching posts:', err);
        posts.value = [];
        if (err.response) {
          error.value = `Server Error: ${err.response.status} - ${err.response.data.message || err.message}`;
        } else if (err.request) {
          error.value = `Network Error: Không thể kết nối đến server.`;
        } else {
          error.value = `System Error: ${err.message}`;
        }
      } finally {
        loading.value = false;
      }
    };

    const updateURL = () => {
      const query = {};

      if (searchQuery.value.trim()) {
        query.search = searchQuery.value.trim();
      }

      if (selectedCategory.value) {
        query.category = selectedCategory.value;
      }

      if (pagination.value.current_page > 1) {
        query.page = pagination.value.current_page;
      }

      router.replace({ query });
    };

    const changePage = (page) => {
      if (page >= 1 && page <= pagination.value.total_pages && page !== pagination.value.current_page) {
        fetchPosts(page);
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    };

    const performSearch = () => {
      fetchPosts(1, true);
    };

    const debounceSearch = () => {
      clearTimeout(searchTimeout.value);
      searchTimeout.value = setTimeout(() => {
        performSearch();
      }, 500);
    };

    const applyFilters = () => {
      fetchPosts(1, true);
    };

    const clearSearch = () => {
      searchQuery.value = '';
      performSearch();
    };

    const clearCategory = () => {
      selectedCategory.value = '';
      applyFilters();
    };

    const clearAllFilters = () => {
      searchQuery.value = '';
      selectedCategory.value = '';
      fetchPosts(1, true);
    };

    const getCategoryLabel = (category) => {
      return categoryLabels[category] || category;
    };

    // Generate page numbers for pagination UI
    const pageNumbers = computed(() => {
      const pages = [];
      const maxVisiblePages = 5;
      const current = pagination.value.current_page;
      const total = pagination.value.total_pages;

      if (total <= maxVisiblePages) {
        for (let i = 1; i <= total; i++) {
          pages.push(i);
        }
      } else {
        // Always show first page
        pages.push(1);

        if (current > 3) {
          pages.push('...');
        }

        // Show pages around current
        const start = Math.max(2, current - 1);
        const end = Math.min(total - 1, current + 1);

        for (let i = start; i <= end; i++) {
          if (i !== 1 && i !== total) {
            pages.push(i);
          }
        }

        if (current < total - 2) {
          pages.push('...');
        }

        // Always show last page if more than 1 page
        if (total > 1) {
          pages.push(total);
        }
      }

      return [...new Set(pages)]; // Remove duplicates
    });

    const formatDate = (dateString) => {
      if (!dateString) return 'N/A';
      try {
        const date = new Date(dateString);
        if (isNaN(date.getTime())) return dateString;
        return date.toLocaleDateString('vi-VN', {
          year: 'numeric',
          month: 'long',
          day: 'numeric'
        });
      } catch (e) {
        return dateString;
      }
    };

    const handleImageError = (event) => {
      event.target.src = '/placeholder-image.png';
      event.target.alt = 'Placeholder Image';
    };

    // Watch route changes
    watch(() => route.query, (newQuery) => {
      searchQuery.value = newQuery.search || '';
      selectedCategory.value = newQuery.category || '';
      const page = parseInt(newQuery.page) || 1;
      fetchPosts(page);
    }, { immediate: false });

    onMounted(() => {
      const page = parseInt(route.query.page) || 1;
      fetchPosts(page);
    });

    return {
      posts,
      loading,
      error,
      searchQuery,
      selectedCategory,
      pagination,
      pageNumbers,
      hasActiveFilters,
      performSearch,
      debounceSearch,
      applyFilters,
      changePage,
      clearSearch,
      clearCategory,
      clearAllFilters,
      getCategoryLabel,
      formatDate,
      handleImageError,
    };
  }
};
</script>
<style scoped>
/* Define some CSS variables for consistency */
:root {
  --primary-color: #007bff;
  --primary-dark: #0056b3;
  --accent-color: #28a745;
  --accent-dark: #218838;
  --text-dark: #212529;
  --text-medium: #555;
  --text-light: #777;
  --bg-light: #f8f9fa;
  --bg-white: #ffffff;
  --border-color: #e0e0e0;
  --shadow-light: rgba(0, 0, 0, 0.08);
  --shadow-medium: rgba(0, 0, 0, 0.15);
  --shadow-strong: rgba(0, 0, 0, 0.2);
}

/* General Container and Title */
.container {
  max-width: 1200px;
  padding: 20px;
  font-family: 'Inter', sans-serif;
  /* A modern, clean font */
  color: var(--text-medium);
  background-color: var(--bg-light);
  /* Light background for the page */
  border-radius: 12px;
}

.page-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--text-dark);
  margin-bottom: 3rem;
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  position: relative;
}

.page-title::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 50%;
  transform: translateX(-50%);
  width: 80px;
  height: 4px;
  background-color: var(--primary-color);
  border-radius: 2px;
}

/* Filter and Search Area */
.filter-search-area {
  display: flex;
  gap: 1.2rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
}

.search-input {
  padding: 0.9rem 1.2rem;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background-color: var(--bg-white);
  color: var(--text-dark);
  font-size: 1rem;
  flex-grow: 1;
  max-width: 450px;
  box-shadow: inset 0 1px 4px rgba(0, 0, 0, 0.06);
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.2);
}

.search-input::placeholder {
  color: #a0a0a0;
}

.search-button-page {
  padding: 0.9rem 2rem;
  border: none;
  border-radius: 8px;
  background-color: var(--primary-color);
  color: white;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: background-color 0.3s ease, transform 0.2s ease, box-shadow 0.3s ease;
  box-shadow: 0 5px 15px var(--shadow-light);
}

.search-button-page:hover {
  background-color: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px var(--shadow-medium);
}

.category-select {
  padding: 0.9rem 1.2rem;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background-color: var(--bg-white);
  color: var(--text-dark);
  font-size: 1rem;
  cursor: pointer;
  box-shadow: inset 0 1px 4px rgba(0, 0, 0, 0.06);
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  background-image: url('data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%23333%22%20d%3D%22M287%2C116.7l-12.7%2C12.7L146.2%2C268.4L18.7%2C130.4L6%2C117.7l140.2%2C140.2L287%2C116.7z%22%2F%3E%3C%2Fsvg%3E');
  background-repeat: no-repeat;
  background-position: right 0.8em center;
  background-size: 0.65em auto;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.category-select:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.2);
}

/* Posts Grid */
.posts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  /* Min card width 320px */
  gap: 3rem;
  /* Increased gap for more breathing room */
  padding: 0 0 3rem 0;
}

.post-card-link {
  text-decoration: none;
  /* Remove underline from router-link */
  color: inherit;
  /* Inherit text color */
  display: block;
  /* Make the whole link block clickable */
}

.post-card {
  background: var(--bg-white);
  border-radius: 15px;
  /* More rounded corners */
  box-shadow: 0 10px 30px var(--shadow-light);
  /* Softer, larger initial shadow */
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  /* Smooth transition */
  overflow: hidden;
  border: 1px solid #f5f5f5;
  /* Very subtle border */
  display: flex;
  flex-direction: column;
  height: 100%;
  /* Ensure cards in a row have equal height */
}

.post-card:hover {
  transform: translateY(-10px);
  /* Lift higher on hover */
  box-shadow: 0 20px 40px var(--shadow-medium);
  /* Stronger shadow on hover */
}

.post-image-wrapper {
  position: relative;
  width: 100%;
  height: 220px;
  /* Taller image area */
  overflow: hidden;
  background-color: #34495e;
  /* Darker background for images/placeholders */
  display: flex;
  align-items: center;
  justify-content: center;
}

.post-image-wrapper img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease-out;
  /* Slower, smoother zoom */
}

.post-card:hover .post-image-wrapper img {
  transform: scale(1.15);
  /* More zoom on hover */
}

.placeholder-image {
  color: #ecf0f1;
  /* Light grey for icon */
  font-size: 4rem;
  /* Even larger icon */
}

/* Optional: Gradient Overlay for images */
.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0) 50%, rgba(0, 0, 0, 0.2) 100%);
  opacity: 1;
  transition: opacity 0.3s ease;
}

.post-card:hover .image-overlay {
  opacity: 0;
  /* Make overlay disappear on hover if desired */
}


.post-content {
  padding: 0.8rem;
  /* More padding */
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  /* Pushes meta to bottom */
}

.post-title {
  font-size: 1rem;
  /* Larger, bolder title */
  font-weight: 800;
  color: var(--text-dark);
  margin-bottom: 0.8rem;
  line-height: 1.3;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 1.8em;
  /* Consistent height for 2 lines */
  transition: color 0.3s ease;
}

.post-card-link:hover .post-title {
  color: var(--primary-color);
  /* Highlight title on hover */
}

.post-description {
  font-size: 0.98rem;
  color: var(--text-medium);
  line-height: 1.7;
  margin-bottom: 1.5rem;
  flex-grow: 1;
  display: -webkit-box;
  /* -webkit-line-clamp: 3; */
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 4.8em;
  /* Consistent height for 3 lines */
}

.post-meta {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  /* Space out author and date */
  gap: 0.8rem;
  font-size: 0.88rem;
  color: var(--text-light);
  padding-top: 1rem;
  /* Add some padding above to visually separate */
  border-top: 1px solid var(--primary-dark);
  /* Subtle top border for meta */
}

.post-meta span {
  display: flex;
  align-items: center;
}

.post-meta i {
  margin-right: 0.6rem;
  color: var(--primary-color);
  /* Primary color for meta icons */
  font-size: 1rem;
}

/* Pagination Styles */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1.5rem;
  /* margin-top: 5rem;
  margin-bottom: 3rem; */
}

.pagination button {
  padding: 0.8rem 1.6rem;
  font-size: 1.05rem;
  border: 1px solid var(--primary-color);
  border-radius: 8px;
  background-color: var(--bg-white);
  color: var(--primary-color);
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
}

.pagination button:hover:not(:disabled) {
  background-color: var(--primary-color);
  color: white;
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.2);
}

.pagination button:disabled {
  background-color: #e9ecef;
  cursor: not-allowed;
  color: #a0a0a0;
  border-color: #dee2e6;
  box-shadow: none;
}

.pagination span {
  font-size: 1.2rem;
  color: var(--text-dark);
  font-weight: 500;
}

/* Message Styles */
.loading-message,
.no-posts-message,
.error-message {
  text-align: center;
  font-size: 1.3rem;
  padding: 50px 20px;
  margin-top: 3rem;
  border-radius: 12px;
  background-color: var(--bg-white);
  box-shadow: 0 5px 15px var(--shadow-light);
}

.error-message {
  color: #dc3545;
  border: 1px solid #dc3545;
  background-color: #fff0f0;
}

.no-posts-message {
  color: #6c757d;
  border: 1px solid #dee2e6;
}

/* Responsive Adjustments */
@media (max-width: 992px) {
  .posts-grid {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 2rem;
  }
}

@media (max-width: 768px) {
  .page-title {
    font-size: 2.2rem;
    margin-bottom: 2rem;
  }

  .filter-search-area {
    flex-direction: column;
    align-items: stretch;
    gap: 0.8rem;
    margin-bottom: 2.5rem;
  }

  .search-input,
  .search-button-page,
  .category-select {
    width: 100%;
    max-width: none;
  }

  .posts-grid {
    grid-template-columns: 1fr;
    /* Single column on smaller screens */
    gap: 1.8rem;
  }

  .post-image-wrapper {
    height: 180px;
  }

  .post-title {
    font-size: 1.3rem;
    min-height: auto;

  }

  .post-description {
    font-size: 0.9rem;
    min-height: auto;
  }
}

@media (max-width: 480px) {
  .container {
    padding: 15px;
  }

  .page-title {
    font-size: 1.8rem;
    margin-bottom: 1.5rem;
  }

  .search-input,
  .search-button-page,
  .category-select,
  .pagination button {
    font-size: 0.9rem;
    padding: 0.7rem 1rem;
  }

  .pagination span {
    font-size: 1rem;
  }

  .post-content {
    padding: 1.2rem;
  }

  .post-title {
    font-size: 1.2rem;
  }

  .post-description {
    font-size: 0.85rem;
  }
}

button.clear-filter,
button.clear-all-filters {
  margin-left: 10px;
}

.category-filter {
  flex-grow: 1;
  align-items: flex-end;
}
</style>