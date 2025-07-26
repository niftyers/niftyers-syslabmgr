import { nextTick } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';

import { routesDirectory, WEB_TITLE } from '../common';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routesDirectory,
});

router.afterEach((to) => {
  const title = (to.meta.title as string) ?? WEB_TITLE;
  nextTick(() => {
    document.title = title;
  });
});

export { router };
