import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
  ],
  server: {
    // This allows the dev server to be accessible from the Docker container
    host: '0.0.0.0',
    port: 5173,
    // Proxy API requests to the backend during development
    proxy: {
      '/api': {
        target: 'http://backend:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
       '/ws': {
        target: 'ws://backend:8000',
        ws: true,
      },
    },
  },
})
