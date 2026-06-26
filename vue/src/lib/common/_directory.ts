import Home from '@/views/HomePage.vue';
import NotFound from '@/views/NotFound.vue';

import { WEB_TITLE } from './_const';

export const routesDirectory = [
  {
    path: '/',
    name: 'home',
    component: Home,
    meta: {
      title: `Dashboard - ${WEB_TITLE}`,
      auth: true,
    },
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: NotFound,
    meta: {
      title: `Not Found - ${WEB_TITLE}`,
      auth: true,
    },
  },
];
