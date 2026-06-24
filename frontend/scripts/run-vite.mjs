import { existsSync } from "node:fs";
import { join } from "node:path";
import { spawnSync } from "node:child_process";
import { pathToFileURL } from "node:url";

const projectRoot = process.cwd();
const { viteRoot, cleanup } = resolveViteRoot(projectRoot);
const viteEntry = join(viteRoot, "node_modules", "vite", "bin", "vite.js");

if (cleanup) {
  let cleanedUp = false;
  const runCleanup = () => {
    if (!cleanedUp) {
      cleanedUp = true;
      cleanup();
    }
  };

  process.once("exit", runCleanup);
  process.once("SIGINT", () => {
    runCleanup();
    process.exit(130);
  });
  process.once("SIGTERM", () => {
    runCleanup();
    process.exit(143);
  });
}

process.chdir(viteRoot);
process.argv = [process.execPath, viteEntry, ...process.argv.slice(2)];
await import(pathToFileURL(viteEntry).href);

function resolveViteRoot(root) {
  if (process.platform !== "win32" || !root.includes("%")) {
    return { viteRoot: root, cleanup: null };
  }

  const substExecutable = join(process.env.SystemRoot ?? "C:\\Windows", "System32", "subst.exe");
  const drive = findAvailableDrive();
  const result = spawnSync(substExecutable, [drive, root], {
    encoding: "utf8",
    windowsHide: true,
  });

  if (result.status !== 0) {
    throw new Error(`Could not create temporary drive ${drive}: ${result.stderr || result.stdout}`);
  }

  return {
    viteRoot: `${drive}\\`,
    cleanup: () => {
      spawnSync(substExecutable, [drive, "/D"], {
        encoding: "utf8",
        windowsHide: true,
      });
    },
  };
}

function findAvailableDrive() {
  for (let code = "Z".charCodeAt(0); code >= "P".charCodeAt(0); code -= 1) {
    const drive = `${String.fromCharCode(code)}:`;
    if (!existsSync(`${drive}\\`)) {
      return drive;
    }
  }
  throw new Error("No free drive letter is available for the Vite development server.");
}
