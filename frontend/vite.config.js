import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/axl': {
        target: 'http://localhost:9092',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/axl/, '')
      }
    }
  }
})
