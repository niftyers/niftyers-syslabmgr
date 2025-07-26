import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';

export const vuetify = createVuetify({
  ssr: true,
  components,
  directives,
  theme: {
    defaultTheme: 'niftyers',
    themes: {
      niftyers: {
        dark: false,
        colors: {
          primary: '#263238',
          secondary: '#78909C',
          error: '#C62828',
        },
      },
    },
  },
});
