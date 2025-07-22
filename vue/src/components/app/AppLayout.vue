<script setup lang="ts">
import { RouterView } from 'vue-router'

import AppHeader from './AppHeader.vue'
import AppSidebar from './AppSidebar.vue'
</script>

<template>
  <div class="app-layout">
    <AppHeader />
    <div class="layout-container">
      <AppSidebar />
      <main class="main-content">
        <RouterView />
      </main>
    </div>
  </div>
</template>
