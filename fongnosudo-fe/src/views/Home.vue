<template>
  <div class="container">
    <section class="section-block animate-fade-in-up">
      <h2 class="section-title">Bài viết mới nhất</h2>
      <!-- <div class="posts-grid">
        <router-link v-for="post in featuredPosts" :key="post.id" :to="`/blog/${post.slug}`" class="post-card-link">
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
      </div> -->

      <div class="posts-grid">
        <router-link v-for="post in latestPosts" :key="post.id" :to="`/blog/${post.slug}`" class="post-card-link">
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
    </section>
    <section class="section-block mt-4 animate-fade-in-up" style="animation-delay: 0.3s;">
      <h2 class="section-title">Nổi bật</h2>
      <!-- <div class="featured-list">
        <div v-for="post in featuredPosts" :key="post.id" class="featured-item">
          <span class="featured-date">{{ formatDate(post.created_at) }}</span>
          <div class="featured-details">
            <h3 class="featured-title">{{ post.title }}</h3>
            <p class="featured-description">{{ getExcerpt(post.content) }}</p>
            <router-link to="/blog/sample-slug" class="read-more">Xem thêm →</router-link>
          </div>
        </div> -->
      <div class="posts-grid">
        <router-link v-for="post in featuredPosts" :key="post.id" :to="`/blog/${post.slug}`" class="post-card-link">
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
    </section>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import api from '@/api'; // Đảm bảo import api instance của bạn

export default {
  name: 'HomeView',
  setup() {
    const latestPosts = ref([]);
    const featuredPosts = ref([]);


    const fetchLatestPosts = async () => {
      try {
        const response = await api.get('/posts?is_latest=true&limit=2');
        latestPosts.value = response.data;
        console.log("Latest Posts:", response.data);
      } catch (error) {
        console.error('Failed to fetch latest posts:', error);
        latestPosts.value = []; // Đảm bảo array rỗng khi có lỗi
      }
    };

    // Hàm để fetch các bài viết nổi bật
    const fetchFeaturedPosts = async () => {
      try {
        // Gọi API với tham số 'is_featured=true'
        // API backend của bạn phải được cấu hình để lọc các bài viết có is_featured=true
        const response = await api.get('/posts', {
          params: {
            is_featured: 'true',
            limit: 2 // Lấy 2 bài nổi bật (số lượng này tùy bạn)
          }
        });
        featuredPosts.value = response.data;
        console.log("Featured Posts:", response.data);
      } catch (error) {
        console.error('Failed to fetch featured posts:', error);
        featuredPosts.value = []; // Đảm bảo array rỗng khi có lỗi
      }
    };

    // Hàm định dạng ngày
    const formatDate = (dateString) => {
      if (!dateString) return '';
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(dateString).toLocaleDateString('vi-VN', options);
    };

    // Hàm tạo tóm tắt từ nội dung
    const getExcerpt = (content, maxLength = 150) => {
      if (!content) return '';
      // Loại bỏ các tag HTML khỏi nội dung (quan trọng nếu bạn dùng Quill hoặc Milkdown)
      const strippedContent = content.replace(/(<([^>]+)>)/gi, '');
      if (strippedContent.length <= maxLength) {
        return strippedContent;
      }
      return strippedContent.substring(0, maxLength) + '...';
    };

    onMounted(() => {
      fetchLatestPosts();
      fetchFeaturedPosts();
    });

    return {
      latestPosts,
      featuredPosts,
      formatDate,
      getExcerpt,
    };
  }
}
</script>

<style scoped>
.section-block {
  margin-bottom: 2.5rem;
}

.section-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--background-color-dark);
  /* Dùng màu đậm để nổi bật */
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid var(--primary-color);
  /* Đường gạch dưới theo màu chủ đạo */
  display: inline-block;
  /* Để border-bottom chỉ rộng bằng text */
}

/* Featured List Styles */
.featured-list {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.featured-item {
  display: flex;
  gap: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px dashed var(--border-color);
  /* Gạch ngang mảnh */
}

.featured-item:last-child {
  border-bottom: none;
  /* Không có gạch ngang cho item cuối cùng */
}

.featured-date {
  font-size: 0.9rem;
  color: #888;
  flex-shrink: 0;
  /* Ngăn không cho ngày bị co lại */
  width: 120px;
  /* Cố định chiều rộng cho ngày */
}

.featured-details {
  flex-grow: 1;
}

.featured-title {
  font-size: 1.35rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: var(--background-color-dark);
}

.featured-description {
  font-size: 1rem;
  color: #555;
  margin-bottom: 0.75rem;
}

.read-more {
  font-weight: 500;
  color: var(--accent-color);
  text-decoration: none;
}

.read-more:hover {
  text-decoration: underline;
}

/* Responsive adjustments for featured list */
@media (max-width: 768px) {
  .featured-item {
    flex-direction: column;
    gap: 0.5rem;
  }

  .featured-date {
    width: auto;
    /* Cho phép ngày co dãn tự động */
  }
}

.card-description {
  display: -webkit-box;
  /* Giới hạn 2 dòng */
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.4;
  max-height: 2.8em;
  /* 2 dòng × line-height */
  margin: 0.5rem 0;
  color: #666;
  font-size: 0.9rem;
}

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
  margin-bottom: 4rem;
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