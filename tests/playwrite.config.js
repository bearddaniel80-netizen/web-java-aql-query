import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: ".",

  use: {
    baseURL: "http://node",
  },

  webServer: {
    command: "npm run start",
    url: "http://node",
    reuseExistingServer: !process.env.CI,
    timeout: 30_000,
  },
});