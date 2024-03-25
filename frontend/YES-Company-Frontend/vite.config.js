import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  //change port for production
  preview: {
    port: 3001,
    // host: "https://yes-company-frontend-react.onrender.com",
    // https: true,
  },
  // for dev
  server: {
    port: 3000,
  },
  define: {
    "process.env": { PORT: 3000 },
  },
});
