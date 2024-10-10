import { defineConfig } from "vite";

export default defineConfig({
  css: {
    preprocessorOptions: {
      scss: {
        javascriptEnabled: true,
        additionalData: '@import "./src/styles/index.scss";',
      },
    },
  },
});