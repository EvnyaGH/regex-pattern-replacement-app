import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [viteClientPathCompatibility(), react()],
  resolve: {
    preserveSymlinks: true,
  },
  server: {
    port: 5173,
    strictPort: false,
  },
});

function viteClientPathCompatibility() {
  const virtualModuleId = "virtual:rrapp-vite-client-env";
  const resolvedVirtualModuleId = `\0${virtualModuleId}`;

  return {
    name: "rrapp-vite-client-path-compatibility",
    enforce: "pre",
    resolveId(source) {
      return source === virtualModuleId ? resolvedVirtualModuleId : null;
    },
    load(id) {
      return id === resolvedVirtualModuleId ? "export {};" : null;
    },
    transform(code, id) {
      const normalizedId = id.replaceAll("\\", "/");
      if (!normalizedId.endsWith("/vite/dist/client/client.mjs")) {
        return null;
      }
      return code.replace('import "@vite/env";', `import "${virtualModuleId}";`);
    },
  };
}
