<template>
  <div class="container edit-post-page">
    <h1 class="page-title">{{ isEditing ? 'Chỉnh sửa bài viết' : 'Viết bài mới' }}</h1>

    <form @submit.prevent="savePost" class="post-form">
      <div class="form-group">
        <label for="title">Tiêu đề bài viết:</label>
        <input type="text" id="title" v-model="post.title" required>
      </div>

      <div class="form-group">
        <label for="image_url">URL ảnh đại diện:</label>
        <input type="text" id="image_url" v-model="post.image_url">
      </div>

      <!-- <div class="form-group">
        <label for="image_url">Chọn tin cho home:</label>
        <div class="checkbox">
          <input type="checkbox" id="is_featured" v-model="post.is_featured" />
          <label for="is_featured">Nổi bật</label>
        </div>
        <div class="checkbox">
          <input type="checkbox" id="is_latest" v-model="post.is_latest" />
          <label for="is_latest">Mới nhất</label>
        </div>
      </div> -->
      <div class="checkbox-row">
        <label for="image_url">Chọn tin cho home:</label>
        <div class="checkbox">
          <input type="checkbox" id="is_featured" v-model="post.is_featured" />
          <label for="is_featured">Nổi bật</label>
        </div>
        <div class="checkbox">
          <input type="checkbox" id="is_latest" v-model="post.is_latest" />
          <label for="is_latest">Mới nhất</label>
        </div>
      </div>
      <div class="form-group editor-container">
        <label>Nội dung bài viết:</label>
        <QuillEditor theme="snow" toolbar="full" v-model:content="post.content" contentType="html" />
      </div>

      <button type="submit" class="submit-button">{{ isEditing ? 'Cập nhật bài viết' : 'Đăng bài' }}</button>
      <p v-if="message" :class="messageType">{{ message }}</p>
    </form>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { QuillEditor } from '@vueup/vue-quill';
import '@vueup/vue-quill/dist/vue-quill.snow.css'; // Import Quill's snow theme CSS
import api from '@/api'; // Import api instance

export default {
  name: 'AdminEditPost',
  components: {
    QuillEditor,
  },
  setup() {
    const router = useRouter();
    const route = useRoute();
    const postSlug = route.params.slug; // Get post slug from route params
    const isEditing = computed(() => !!postSlug);

    const post = ref({
      title: '',
      content: '',
      image_url: '',
      is_featured: false,
      is_latest: false
    });

    const message = ref('');
    const messageType = ref(''); // 'success' or 'error'

    const fetchPost = async () => {
      if (isEditing.value) {
        try {
          const token = localStorage.getItem('access_token');
          if (!token) {
            router.push('/admin/login');
            return;
          }
          api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
          const response = await api.get(`/posts/${postSlug}`);
          console.log('Fetched post data:', response.data);
          post.value = response.data;
        } catch (error) {
          console.error('Failed to fetch post:', error);
          message.value = 'Không thể tải bài viết.';
          messageType.value = 'error';
          if (error.response && (error.response.status === 401 || error.response.status === 403)) {
            localStorage.removeItem('access_token');
            router.push('/admin/login');
          }
        }
      }
    };

    const savePost = async () => {
      message.value = '';
      messageType.value = '';
      try {
        const token = localStorage.getItem('access_token');
        if (!token) {
          router.push('/admin/login');
          return;
        }
        api.defaults.headers.common['Authorization'] = `Bearer ${token}`;

        let response;
        if (isEditing.value) {
          response = await api.put(`/posts/${postSlug}`, {
            title: post.value.title,
            content: post.value.content,
            image_url: post.value.image_url,
            is_featured: post.value.is_featured, // Sửa ở đây
            is_latest: post.value.is_latest // Sửa ở đây
          });
          message.value = 'Bài viết đã được cập nhật thành công!';
          messageType.value = 'success';
        } else {
          response = await api.post('/posts', {
            title: post.value.title,
            content: post.value.content,
            image_url: post.value.image_url,
            is_featured: post.value.is_featured,
            is_latest: post.value.is_latest
          });
          message.value = 'Bài viết đã được đăng thành công!';
          messageType.value = 'success';
          // Clear form after successful creation
          post.value = { title: '', content: '', image_url: '', is_featured: false, is_latest: false }; // Đảm bảo reset cả hai trường này
        }
        console.log('Post saved:', response.data);
        // Optionally redirect after a short delay
        setTimeout(() => {
          router.push('/admin/dashboard');
        }, 2000);
      } catch (error) {
        console.error('Failed to save post:', error.response ? error.response.data : error.message);
        message.value = error.response && error.response.data && error.response.data.msg ? error.response.data.msg : 'Lỗi khi lưu bài viết. Vui lòng thử lại.';
        messageType.value = 'error';
        if (error.response && (error.response.status === 401 || error.response.status === 403)) {
          localStorage.removeItem('access_token');
          router.push('/admin/login');
        }
      }
    };
    onMounted(fetchPost);

    // const updatePostStatus = async (post, field) => {
    //   try {
    //     const updateData = {
    //       title: post.title,
    //       content: post.content,
    //       image_url: post.image_url,
    //       is_featured: post.is_featured,
    //       is_latest: post.is_latest,
    //     };

    //     // await api.put(`/posts/${post.slug}`, updateData);
    //     console.log(`${field} status updated for post: ${post.title}`);
    //   } catch (error) {
    //     console.error(`Failed to update ${field} status for post:`, post.title, error);
    //     post[field] = !post[field];

    //   }
    // };

    return {
      post,
      isEditing,
      savePost,
      message,
      messageType,
    };
  }
}
</script>

<style scoped>
.edit-post-page {
  padding: 2rem 1rem;
}

.page-title {
  font-size: 2.5rem;
  color: var(--background-color-dark);
  margin-bottom: 2rem;
  text-align: center;
}

.post-form {
  background-color: var(--card-background);
  padding: 2.5rem;
  border-radius: 8px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 900px;
  /* Make form wider for editor */
  margin: 0 auto;
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

.editor-container {
  /* Quill editor needs height */
  margin-bottom: 2rem;
}

.editor-container .ql-container {
  min-height: 400px;
  /* Minimum height for the editor area */
  border-bottom-left-radius: 5px;
  border-bottom-right-radius: 5px;
}

.editor-container .ql-toolbar {
  border-top-left-radius: 5px;
  border-top-right-radius: 5px;
}

.submit-button {
  width: auto;
  /* Auto width */
  padding: 0.85rem 2rem;
  font-size: 1.1rem;
  display: block;
  /* Center button */
  margin: 0 auto 1rem auto;
  background-color: var(--primary-color);
  color: var(--background-color-dark);
}

.submit-button:hover {
  background-color: var(--accent-hover);
  color: var(--primary-color);
}

.message {
  text-align: center;
  margin-top: 1rem;
  padding: 0.75rem;
  border-radius: 5px;
  font-weight: 500;
}

.message.success {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.message.error {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.checkbox {
  padding-right: 20px;
}

.checkbox-row {
  display: flex;
  gap: 2rem;
  align-items: center;
  flex-wrap: wrap;
  margin-bottom: 1.5rem;
  /* Cho phép xuống hàng trên mobile */
}

.checkbox {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background-color: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 6px;
  transition: all 0.3s ease;
  min-width: 120px;
  /* Đảm bảo width tối thiểu */
}

.checkbox:hover {
  background-color: #e9ecef;
}

.checkbox input[type="checkbox"] {
  width: 16px;
  height: 16px;
  margin: 0;
  cursor: pointer;
}

.checkbox label {
  margin: 0;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  color: #495057;
  white-space: nowrap;
  /* Không cho text xuống hàng */
}

.checkbox input[type="checkbox"]:checked+label {
  color: #007bff;
  font-weight: 600;
}

/* Responsive - mobile xuống 2 hàng */
@media (max-width: 768px) {
  .checkbox-row {
    gap: 1rem;
  }

  .checkbox {
    flex: 1 1 calc(50% - 0.5rem);
    /* 2 checkbox mỗi hàng trên mobile */
    min-width: 0;
    justify-content: center;
  }
}

/* Responsive - mobile nhỏ xuống 1 cột */
@media (max-width: 480px) {
  .checkbox {
    flex: 1 1 100%;
    /* 1 checkbox mỗi hàng */
  }
}
</style>