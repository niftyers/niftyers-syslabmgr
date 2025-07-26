<template>
  <v-app class="layout">
    <AppSidebar />
    <AppHeader />
    <v-main class="main">
      <v-container fluid>
        <slot name="content">
          <router-view :key="$route.fullPath" />
        </slot>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import AppHeader from './AppHeader.vue';
import AppSidebar from './AppSidebar.vue';
</script>
