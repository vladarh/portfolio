import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import vue from '@astrojs/vue';

export default defineConfig({
  site: 'https://example.com',
  integrations: [
    tailwind({ applyBaseStyles: true }),
    vue()
  ],
  prefetch: true,
  output: 'static',
  trailingSlash: 'never'
});
