<template>
  <div class="container admin-dashboard">
    <h1 class="page-title">Chào mừng, Admin!</h1>
    <div class="dashboard-actions">
      <router-link to="/admin/posts/new" class="button-link">Viết bài mới</router-link>
      <button @click="logout" class="button-link logout-button">Đăng xuất</button>
    </div>

    <h2 class="section-title mt-4">Bài viết của bạn</h2>
    <div class="posts-list">
      <div v-for="post in adminPosts" :key="post.id" class="post-item">
        <div class="post-info">
          <h3>{{ post.title }}</h3>
          <p class="post-date">Ngày đăng: {{ new Date(post.created_at).toLocaleDateString() }}</p>
        </div>
        <div class="post-actions">
          <router-link :to="`/admin/posts/edit/${post.slug}`" class="action-button edit-button">Sửa</router-link>
          <button @click="confirmDelete(post.id)" class="action-button delete-button">Xóa</button>
        </div>
      </div>
      <p v-if="adminPosts.length === 0">Bạn chưa có bài viết nào.</p>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/api'; // Import api instance

export default {
  name: 'AdminDashboard',
  setup() {
    const router = useRouter();
    const adminPosts = ref([]);

    const fetchAdminPosts = async () => {
      try {
        const token = localStorage.getItem('access_token');
        if (!token) {
          router.push('/admin/login'); // Redirect if no token
          return;
        }
        api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        const response = await api.get('/posts'); // Assuming this API lists all posts
        // Filter by current admin's ID if needed, or assume backend filters
        adminPosts.value = response.data;
      } catch (error) {
        console.error('Failed to fetch admin posts:', error);
        if (error.response && (error.response.status === 401 || error.response.status === 403)) {
          alert('Phiên làm việc hết hạn hoặc không có quyền. Vui lòng đăng nhập lại.');
          localStorage.removeItem('access_token');
          router.push('/admin/login');
        } else {
          adminPosts.value = [];
        }
      }
    };

    const confirmDelete = async (postId) => {
      if (confirm('Bạn có chắc chắn muốn xóa bài viết này không?')) {
        try {
          const token = localStorage.getItem('access_token');
          api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
          await api.delete(`/posts/${postId}`);
          alert('Bài viết đã được xóa thành công!');
          fetchAdminPosts(); // Refresh list
        } catch (error) {
          console.error('Failed to delete post:', error);

          // Alert ra status code nếu có response
          if (error.response) {
            alert(`Failed to delete post. Status: ${error.response.status}`);
          } else if (error.request) {
            alert('Failed to delete post: No response from server');
          } else {
            alert(`Failed to delete post: ${error.message}`);
          }

          if (error.response && (error.response.status === 401 || error.response.status === 403)) {
            localStorage.removeItem('access_token');
            router.push('/admin/login');
          }
        }
      }
    };

    const logout = () => {
      localStorage.removeItem('access_token');
      router.push('/admin/login');
    };

    const updatePostStatus = async (post, field) => {
      try {
        // Tạo một object chỉ chứa các trường cần cập nhật
        const updateData = {
          title: post.title, // Cần gửi đủ các trường bắt buộc của post
          content: post.content,
          image_url: post.image_url,
          is_featured: post.is_featured,
          is_latest: post.is_latest,
        };

        await api.put(`/posts/${post.slug}`, updateData);
        console.log(`${field} status updated for post: ${post.title}`);
      } catch (error) {
        console.error(`Failed to update ${field} status for post:`, post.title, error);
        // Revert checkbox state on error if needed
        post[field] = !post[field];

      }
    };

    onMounted(fetchAdminPosts); // Fetch posts when component is mounted

    return {
      adminPosts,
      confirmDelete,
      logout,
    };
  }
}
</script>

<style scoped>
.admin-dashboard {
  padding: 2rem 1rem;
}

.dashboard-actions {
  display: flex;
  gap: 1rem;
  margin-bottom: 2.5rem;
  justify-content: flex-end;
  /* Align buttons to the right */
}

.button-link {
  display: inline-block;
  padding: 0.75rem 1.25rem;
  border-radius: 5px;
  background-color: var(--primary-color);
  color: var(--background-color-dark);
  font-weight: 600;
  text-decoration: none;
  transition: background-color 0.3s ease;
  cursor: pointer;
  border: none;
  /* Make it look like a button */
}

.button-link:hover {
  background-color: var(--accent-hover);
  color: var(--primary-color);
  text-decoration: none;
}

.logout-button {
  background-color: var(--black-primary);
  /* Red color for logout */
  color: var(--text-color-light);
  font-weight: 600;
}

.logout-button:hover {
  background-color: var(--primary-color);
  color: var(--accent-hover);
}

.posts-list {
  background-color: var(--card-background);
  border-radius: 8px;
  box-shadow: 0 4px 6px -1px var(--box-shadow-light);
  padding: 1.5rem;
}

.post-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 0;
  border-bottom: 1px solid var(--border-color);
}

.post-item:last-child {
  border-bottom: none;
}

.post-info h3 {
  font-size: 1.25rem;
  color: var(--background-color-dark);
  margin-bottom: 0.25rem;
}

.post-info .post-date {
  font-size: 0.85rem;
  color: #777;
}

.post-actions {
  display: flex;
  gap: 0.75rem;
}

.action-button {
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
  border-radius: 5px;
  text-decoration: none;
  font-weight: 500;
  cursor: pointer;
  border: none;
  transition: background-color 0.3s ease;
}

.edit-button {
  background-color: var(--primary-color);
  color: var(--background-color-dark);
  font-weight: 600;
}

.edit-button:hover {
  background-color: var(--accent-hover);
  color: var(--primary-color);
}

.delete-button {
  background-color: var(--background-color-dark);
  color: var(--primary-color);
  font-weight: 600;
}

.delete-button:hover {
  background-color: var(--primary-color);
  color: var(--accent-hover);

}

/* Responsive adjustments */
@media (max-width: 768px) {
  .post-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .post-actions {
    width: 100%;
    justify-content: flex-end;
  }

  .dashboard-actions {
    justify-content: center;
  }
}
</style>