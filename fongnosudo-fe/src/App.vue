<script setup>
import { RouterView } from 'vue-router'
import MainHeader from './components/Header.vue' // Import Header
import Dooxfonggg from './components/Fooder.vue'; // Import component footer
</script>

<template>
  <div id="app">
    <MainHeader />
    <main>
      <router-view v-slot="{ Component, route }">
        <transition name="page-fade" mode="out-in">
          <component :is="Component" :key="route.path" />
        </transition>
      </router-view>
      <!-- <router-view /> -->
    </main>
    <Dooxfonggg />
  </div>
</template>

<style scoped>
main {
  padding-top: 1rem;
  min-height: calc(100vh - 80px);

}

body {
  margin: 0;
  font-family: 'Inter', sans-serif;
  background-color: #f0f2f5;
  color: #333;
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.page-fade-enter-active,
.page-fade-leave-active {
  transition: all 0.3s ease;
}

.page-fade-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.page-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>