<template>
  <v-navigation-drawer v-model="Sidebar.State" permanent>
    <v-list>
      <v-list-item prepend-icon="mdi-home" title="Home" value="home" to="/" />
      <v-list-item prepend-icon="mdi-account" title="Profile" value="profile" to="/profile" />
      <v-list-item prepend-icon="mdi-cog" title="Settings" value="settings" to="/settings" />
    </v-list>
    <template v-slot:append>
      <div class="pa-2">
        <v-btn block color="primary" @click="logout"> Logout </v-btn>
      </div>
    </template>
  </v-navigation-drawer>
</template>

<script setup lang="ts">
import * as Store from '@/lib/stores';
const Sidebar = Store.useSidebar();

const logout = () => {
  console.log('Logout clicked');
};
</script>
