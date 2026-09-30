import { defineConfig } from 'vite';
import preact from '@preact/preset-vite';

export default defineConfig({
  plugins: [preact()],
  // relative asset URLs so the app works behind a reverse proxy sub-path (#16)
  base: './',
  server: { proxy: { '/api': 'http://localhost:5000', '/docs': 'http://localhost:5000', '/openapi.json': 'http://localhost:5000' } },
});
