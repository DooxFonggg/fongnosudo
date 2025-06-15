<template>
  <div class="container about-page">
    <h3 class="page-title">Giới thiệu về tôi</h3>
    <div class="about-content">
      <img src="../assets/logo-fongnosudo-2.png" alt="Your Photo" class="profile-photo">
      <p>Chào bạn, tôi là Phong, hiện đang làm DevOps tại FPT Education. Blog này là nơi tôi chia sẻ kiến thức và kinh
        nghiệm về DevOps.</p>
      <p>Với niềm đam mê công nghệ và mong muốn đóng góp cho cộng đồng, tôi hy vọng những bài viết tại đây sẽ mang lại
        giá trị cho bạn. Hãy cùng nhau khám phá thế giới DevOps!</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AboutPage'
}
</script>

<style scoped>
.about-page {
  padding: 2rem 1rem;
  text-align: center;
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

.about-content {
  max-width: 800px;
  margin: 0 auto;
  background-color: var(--card-background);
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px -1px var(--box-shadow-light);
}

.profile-photo {
  width: 250px;
  height: 250px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 1.5rem;
  border: 3px solid var(--primary-color);
}

.about-content p {
  font-size: 1.1rem;
  line-height: 1.8;
  margin-bottom: 1rem;
  color: var(--text-color-dark);
}
</style>