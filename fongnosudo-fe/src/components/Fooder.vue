<template>
  <footer class="blog-footer">
    <div class="social-icons">
      <a href="#" target="_blank" rel="noopener noreferrer"><i class="fas fa-envelope"></i></a>
      <a href="#" target="_blank" rel="noopener noreferrer"><i class="fab fa-github"></i></a>
      <a href="#" target="_blank" rel="noopener noreferrer"><i class="fab fa-facebook-f"></i></a>
      <!-- <a href="#" target="_blank" rel="noopener noreferrer"><i class="fab fa-youtube"></i></a> -->
      <a href="#" target="_blank" rel="noopener noreferrer"><i class="fab fa-linkedin-in"></i></a>
      <!-- <a href="#" target="_blank" rel="noopener noreferrer"><i class="fab fa-x-twitter"></i></a>
      <a href="#" target="_blank" rel="noopener noreferrer"><i class="fab fa-instagram"></i></a>
      <a href="#" target="_blank" rel="noopener noreferrer" class="custom-icon">A</a> -->
    </div>
    <div class="copyright-info">
      <span>Dooxfonggg</span> •
      <span>© 2025</span> •
      <span>Trang cá nhân của Dooxfonggg</span>
    </div>
    <div class="personal-name">
      <span>Dooxfonggg</span>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'Dooxfonggg' // Tên component đã được đổi thành Dooxfonggg
};
</script>

<style scoped>
.blog-footer {
  background-color: var(--background-color-dark);
  /* Nền tối như trong ảnh bạn cung cấp*/
  color: var(--text-color-light);
  /* Màu chữ sáng */
  padding: 5px 0;
  text-align: center;
}

.social-icons {
  margin-top: 5px;
}

.social-icons a {
  color: var(--text-color-light);
  /* Màu icon sáng */
  font-size: 1.5rem;
  margin: 0 10px;
  text-decoration: none;
  opacity: 0.8;
  transition: opacity 0.3s ease;
}

.social-icons a:hover {
  opacity: 1;
  transform: translateY(-2px);
  /* Hiệu ứng nhấc nhẹ khi di chuột */
}

.copyright-info {
  font-size: 0.8rem;
}

.copyright-info span {
  margin: 0 5px;
}

.personal-name {
  font-size: 0.9rem;
  margin-top: 5px;
}

.custom-icon {
  /* Style cho icon 'A' tùy chỉnh nếu nó không phải là Font Awesome */
  font-family: sans-serif;
  /* Hoặc font chữ cụ thể khác */
  font-weight: bold;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .social-icons a {
    font-size: 1.3rem;
    margin: 0 8px;
  }

  /* .blog-footer {
    padding: 15px 0;
  } */
  .copyright-info,
  .personal-name {
    font-size: 0.75rem;
  }
}

@media (max-width: 480px) {
  .social-icons a {
    font-size: 1.2rem;
    margin: 0 6px;
  }

  /* .blog-footer {
    padding: 10px 0;
  } */

  .copyright-info,
  .personal-name {
    font-size: 0.7rem;
  }
}
</style>