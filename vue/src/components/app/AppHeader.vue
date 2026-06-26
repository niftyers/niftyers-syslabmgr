<template>
  <v-app-bar
    color="primary"
    density="compact"
    app:permanent="false"
    class="transition-all duration-300"
  >
    <template v-slot:prepend>
      <v-app-bar-nav-icon @click="Sidebar.Save(!Sidebar.State)"></v-app-bar-nav-icon>
    </template>
    <v-app-bar-title>AD Manager</v-app-bar-title>
    <v-spacer></v-spacer>
    <v-btn icon>
      <v-icon>mdi-bell</v-icon>
    </v-btn>
    <v-btn icon>
      <v-icon>mdi-account</v-icon>
    </v-btn>
  </v-app-bar>
</template>

<script setup lang="ts">
import * as Store from '@/lib/stores';
const Sidebar = Store.useSidebar();
</script>
