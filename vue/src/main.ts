import 'vuetify/styles';
import '@mdi/font/css/materialdesignicons.css';
import '@/assets/vuetify.scss';
import '@/assets/style.css';

import * as plugins from './lib/plugins';

import App from './App.vue';

import { createApp } from 'vue';

const app = createApp(App);

app.config.errorHandler = (err) => {
  console.log(err);
};

app.use(plugins.pinia);
app.use(plugins.router);
app.use(plugins.vuetify);

app.mount('#app');
