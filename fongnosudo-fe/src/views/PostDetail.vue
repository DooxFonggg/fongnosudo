<template>
  <div class="container post-detail-page">
    <h1 class="post-title">{{ post.title }}</h1>
    <div class="post-meta">
      <span>Ngày đăng: {{ new Date(post.created_at).toLocaleDateString() }}</span>
      <span>Tác giả: {{ post.author ? post.author.username : 'Unknown' }}</span>
    </div>
    <img v-if="post.image_url" :src="post.image_url" :alt="post.title" class="post-image">
    <div class="post-content" v-html="post.content"></div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import api from '@/api';

export default {
  name: 'PostDetailPage',
  setup() {
    const route = useRoute();
    const post = ref({
      title: 'Đang tải bài viết...',
      content: '<p>Vui lòng đợi...</p>',
      image_url: '',
      created_at: new Date(),
      author: { username: 'Loading...' }
    });
    const error = ref(null);

    const fetchPost = async () => {
      try {
        const slug = route.params.slug;
        const response = await api.get(`/posts/${slug}`);
        post.value = response.data;
      } catch (err) {
        console.error('Failed to fetch post:', err);
        error.value = 'Không tìm thấy bài viết hoặc có lỗi xảy ra.';
        post.value.title = 'Bài viết không tồn tại';
        post.value.content = '<p>Xin lỗi, bài viết bạn tìm kiếm không có sẵn hoặc đã bị xóa.</p>';
        post.value.image_url = '';
      }
    };

    onMounted(fetchPost);

    return {
      post,
      error
    };
  }
}
</script>

<style scoped>
.post-detail-page {
  padding: 2rem 1rem;
}

.post-title {
  font-size: 3rem;
  font-weight: 700;
  color: var(--background-color-dark);
  margin-bottom: 1rem;
  text-align: center;
}

.post-meta {
  text-align: center;
  font-size: 0.9rem;
  color: #777;
  margin-bottom: 1.5rem;
}

.post-meta span:not(:last-child)::after {
  content: " • ";
}

.post-image {
  max-width: 75%;
  height: auto;
  border-radius: 8px;
  /* margin-bottom: 2rem; */
  display: block;
  /* To center */
  margin-left: auto;
  margin-right: auto;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.post-content {
  font-size: 1.1rem;
  line-height: 1.8;
  color: var(--text-color-dark);
  /* margin-bottom: 3rem; */
}


/* Styles for content rendered from Quill (basic rich text) */
.post-content>>>p {
  margin-bottom: 1em;
}

.post-content>>>h1,
.post-content>>>h2,
.post-content>>>h3,
.post-content>>>h4 {
  color: var(--background-color-dark);
  margin-top: 1.5em;
  margin-bottom: 0.75em;
  font-weight: 600;
}

.post-content>>>h1 {
  font-size: 2.5em;
}

.post-content>>>h2 {
  font-size: 2em;
}

.post-content>>>h3 {
  font-size: 1.75em;
}

.post-content>>>h4 {
  font-size: 1.5em;
}

.post-content>>>ul,
.post-content>>>ol {
  margin-bottom: 1em;
  padding-left: 1.5em;
}

.post-content>>>li {
  margin-bottom: 0.5em;
}

.post-content>>>a {
  color: var(--accent-color);
  text-decoration: underline;
}

.post-content>>>a:hover {
  text-decoration: none;
}

.post-content>>>strong {
  font-weight: 700;
}

.post-content>>>em {
  font-style: italic;
}

.post-content>>>pre {
  /* For code blocks */
  background-color: #f4f4f4;
  border: 1px solid #ddd;
  border-left: 3px solid var(--accent-color);
  padding: 1em;
  overflow-x: auto;
  margin-bottom: 1em;
  border-radius: 5px;
}

.post-content>>>img {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 1em auto;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.post-content>>>blockquote {
  border-left: 4px solid var(--primary-color);
  padding-left: 1em;
  margin: 1em 0;
  color: #666;
  font-style: italic;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .post-title {
    font-size: 2rem;
  }

  .post-content {
    font-size: 1rem;
  }
}
</style>