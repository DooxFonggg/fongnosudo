// frontend/src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/Home.vue';
import BlogView from '../views/Blog.vue';
import PostDetailView from '../views/PostDetail.vue';
import AboutView from '../views/About.vue';
import AdminLoginView from '../views/AdminLogin.vue';
import AdminDashboardView from '../views/AdminDashboard.vue';
import AdminEditPostView from '../views/AdminEditPost.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/blog',
      name: 'blog',
      component: BlogView
    },
    {
      path: '/blog/:slug', // Dynamic segment for post slug
      name: 'post-detail',
      component: PostDetailView
    },
    {
      path: '/about',
      name: 'about',
      component: AboutView
    },
    {
      path: '/admin/login',
      name: 'admin-login',
      component: AdminLoginView
    },
    {
      path: '/admin/dashboard',
      name: 'admin-dashboard',
      component: AdminDashboardView,
      meta: { requiresAuth: true } 
    },
    {
      path: '/admin/posts/new',
      name: 'admin-new-post',
      component: AdminEditPostView,
      meta: { requiresAuth: true }
    },
    {
      path: '/admin/posts/edit/:slug', 
      name: 'admin-edit-post',
      component: AdminEditPostView,
      meta: { requiresAuth: true }
    }
  ]
});

// Navigation Guard để bảo vệ các route cần xác thực
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth) {
    const token = localStorage.getItem('access_token');
    if (token) {
      next(); 
    } else {
      next('/admin/login'); 
    }
  } else {
    next(); 
  }
});

export default router;