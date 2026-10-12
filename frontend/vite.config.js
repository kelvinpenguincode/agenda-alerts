import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// In development, any request starting with /api is forwarded to the
// FastAPI server, so the frontend never has to hardcode a backend URL.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/api": "http://localhost:8000",
    },
  },
});
