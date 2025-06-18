<template>
  <div class="container post-detail-page">
    <h1 class="post-title">{{ post.title }}</h1>
    <div class="post-meta">
      <span>Ngày đăng: {{ new Date(post.created_at).toLocaleDateString() }}</span>
      <span>Tác giả: {{ post.author ? post.author.username : 'Unknown' }}</span>
    </div>
    <img v-if="post.image_url" :src="post.image_url" :alt="post.title" class="post-image">
    <div class="post-content" v-html="post.content" ref="postContentRef"></div>
  </div>
</template>

<script>
import { ref, onMounted, nextTick } from 'vue';
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
    const postContentRef = ref(null);

    const handleCodeBlocks = () => {
      if (!postContentRef.value) {
        // console.log("postContentRef is null, cannot process code blocks yet."); // Debugging
        return;
      }

      const codeBlocks = postContentRef.value.querySelectorAll('pre.ql-syntax');
      const MAX_LINES = 7; // Giới hạn số dòng hiển thị ban đầu

      codeBlocks.forEach(block => {
        // Đảm bảo không xử lý block đã được thêm nút rồi để tránh trùng lặp
        if (block.querySelector('.code-header')) {
          return;
        }

        const lines = block.textContent.split('\n').filter(line => line.trim() !== '');

        const header = document.createElement('div');
        header.className = 'code-header';

        const copyButton = document.createElement('button');
        copyButton.className = 'copy-button';
        copyButton.textContent = 'Copy';
        copyButton.onclick = () => {
          // Tạo một bản sao của block để xử lý
          const blockClone = block.cloneNode(true);

          // Xóa tất cả các nút (copy, toggle) khỏi bản sao
          const buttons = blockClone.querySelectorAll('.code-header, .copy-button, .toggle-button');
          buttons.forEach(btn => btn.remove());

          // Lấy text thuần túy từ bản sao đã xóa nút
          const codeText = blockClone.textContent || blockClone.innerText;

          navigator.clipboard.writeText(codeText)
            .then(() => {
              copyButton.textContent = 'Copied!';
              setTimeout(() => { copyButton.textContent = 'Copy'; }, 1500);
            })
            .catch(err => {
              console.error('Could not copy text: ', err);
              copyButton.textContent = 'Failed!';
            });
        };
        header.appendChild(copyButton);

        if (lines.length > MAX_LINES) {
          const toggleButton = document.createElement('button');
          toggleButton.className = 'toggle-button';
          toggleButton.textContent = 'Xem thêm';

          block.classList.add('collapsed');

          toggleButton.onclick = () => {
            if (block.classList.contains('collapsed')) {
              block.classList.remove('collapsed');
              block.classList.add('expanded');
              toggleButton.textContent = 'Thu gọn';
            } else {
              block.classList.remove('expanded');
              block.classList.add('collapsed');
              toggleButton.textContent = 'Xem thêm';
            }
          };
          header.appendChild(toggleButton);
        }
        block.prepend(header);
      });
    };

    const fetchPost = async () => {
      try {
        const slug = route.params.slug;
        const response = await api.get(`/posts/${slug}`);
        post.value = response.data;

        await nextTick();
        handleCodeBlocks();
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
      error,
      postContentRef
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
  margin-bottom: 2rem;
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
  margin-bottom: 3rem;
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

/* Các styles chung cho trang của bạn (đã có) */
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
  margin-bottom: 2rem;
  display: block;
  margin-left: auto;
  margin-right: auto;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.post-content {
  font-size: 1.1rem;
  line-height: 1.8;
  color: var(--text-color-dark);
  margin-bottom: 3rem;
}

/* =================================================
   QUAN TRỌNG: Styles cho nội dung được render bởi Quill (v-html)
   Sử dụng :deep() để style các phần tử con trong shadow DOM
   =================================================
*/

.post-content :deep(p) {
  margin-bottom: 1em;
}

.post-content :deep(h1),
.post-content :deep(h2),
.post-content :deep(h3),
.post-content :deep(h4) {
  color: var(--background-color-dark);
  margin-top: 1.5em;
  margin-bottom: 0.75em;
  font-weight: 600;
}

.post-content :deep(h1) {
  font-size: 2.5em;
}

.post-content :deep(h2) {
  font-size: 2em;
}

.post-content :deep(h3) {
  font-size: 1.75em;
}

.post-content :deep(h4) {
  font-size: 1.5em;
}

.post-content :deep(ul),
.post-content :deep(ol) {
  margin-bottom: 1em;
  padding-left: 1.5em;
}

.post-content :deep(li) {
  margin-bottom: 0.5em;
}

.post-content :deep(a) {
  color: var(--accent-color);
  text-decoration: underline;
}

.post-content :deep(a:hover) {
  text-decoration: none;
}

.post-content :deep(strong) {
  font-weight: 700;
}

.post-content :deep(em) {
  font-style: italic;
}

/* ================================================= */
/* STYLES CHO CODE BLOCK (PRE.QL-SYNTAX) VÀ CÁC NÚT */
/* ================================================= */

.post-content :deep(pre.ql-syntax) {
  /* QUAN TRỌNG: đảm bảo selector này đúng */
  position: relative;
  /* Rất quan trọng để các nút absolute hoạt động đúng */
  max-height: 200px;
  /* Giới hạn chiều cao mặc định */
  overflow: hidden;
  /* Ẩn nội dung vượt quá max-height */
  margin: 1.5em 0;
  /* Điều chỉnh margin cho phù hợp */
  border: 1px solid #ddd;
  border-left: 3px solid var(--accent-color);
  background-color: #f6f8fa;
  padding: 1em 0.5em;
  /* Padding bên trong, chừa chỗ cho nút */
  line-height: 1.5;
  font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace;
  font-size: 0.9em;
  color: #333;
  border-radius: 5px;
  /* Bo góc */
  box-sizing: border-box;
  /* Đảm bảo padding không làm tăng kích thước tổng */
}

/* Hiệu ứng mờ dần ở cuối khi collapsed */
.post-content :deep(pre.ql-syntax.collapsed::after) {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 50px;
  /* Chiều cao của hiệu ứng mờ */
  background: linear-gradient(to top, rgba(255, 255, 255, 1) 0%, rgba(255, 255, 255, 0) 100%);
  pointer-events: none;
  /* Đảm bảo không chặn click vào nút xem thêm */
  z-index: 5;
  /* Đảm bảo hiệu ứng mờ nằm dưới các nút */
}

/* Header chứa các nút Copy và Xem thêm */
.post-content :deep(.code-header) {
  position: absolute;
  /* Quan trọng: đặt header này theo pre.ql-syntax */
  top: 10px;
  /* Điều chỉnh vị trí từ trên xuống */
  right: 10px;
  /* Điều chỉnh vị trí từ phải sang */
  display: flex;
  gap: 8px;
  /* Khoảng cách giữa các nút */
  z-index: 10;
  /* Đảm bảo nút nằm trên nội dung code và hiệu ứng mờ */
}

.post-content :deep(.copy-button),
.post-content :deep(.toggle-button) {
  background-color: rgba(247, 130, 194, 0.6);
  color: var(--accent-dark);
  border: none;
  border-radius: 4px;
  /* Bo góc nút */
  padding: 6px 12px;
  /* Kích thước nút */
  font-size: 0.85em;
  cursor: pointer;
  opacity: 0.8;
  transition: opacity 0.2s ease, background-color 0.2s ease;
  font-weight: 500;
}

.post-content :deep(.copy-button:hover),
.post-content :deep(.toggle-button:hover) {
  opacity: 1;
  background-color: rgba(0, 0, 0, 0.8);
  color: var(--primary-color);
}

.post-content :deep(pre.ql-syntax.expanded) {
  max-height: none;
  overflow: visible;
}

.post-content :deep(pre.ql-syntax.expanded::after) {
  content: none;
}

.post-content :deep(img) {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 1em auto;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.post-content :deep(blockquote) {
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

.post-content :deep(h1),
.post-content :deep(h2),
.post-content :deep(h3),
.post-content :deep(h4) {
  color: var(--background-color-dark);
  margin-top: 0;
  /* Thay đổi từ 1.5em thành 0 */
  margin-bottom: 0;
  /* Thay đổi từ 0.75em thành 0 */
  font-weight: 600;
}
</style>