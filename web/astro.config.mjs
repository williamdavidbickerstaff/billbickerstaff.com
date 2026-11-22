// @ts-check
import { defineConfig, fontProviders } from "astro/config";

import sanity from "@sanity/astro";

import react from "@astrojs/react";

// https://astro.build/config
export default defineConfig({
  build: { format: "file" },
  integrations: [
    sanity({
      projectId: "fqy1er6l",
      dataset: "production",
      apiVersion: "2026-11-01",
      useCdn: false,
      studioBasePath: "/studio",
    }),
    react(),
  ],
  fonts: [
    {
      provider: fontProviders.local(),
      name: "Beowolf",
      cssVariable: "--font-beowolf",
      options: {
        variants: [
          {
            src: ["./src/assets/fonts/BeowolfOT-R24.woff2"],
            weight: "normal",
            style: "normal",
          },
        ],
      },
    },
  ],
});
