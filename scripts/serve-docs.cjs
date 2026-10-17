"use strict";

const fs = require("node:fs");
const path = require("node:path");
const { createRequire } = require("node:module");

const rootDir = path.resolve(__dirname, "..");
const requireFromDocsify = createRequire(
  require.resolve("docsify-cli/package.json"),
);
const livereload = requireFromDocsify("livereload");
const requireFromLivereload = createRequire(
  requireFromDocsify.resolve("livereload/package.json"),
);
const chokidar = requireFromLivereload("chokidar");
const serve = requireFromDocsify("./lib/commands/serve.js");

const ignoredDirectoryNames = new Set([
  ".git",
  ".venv",
  "env",
  "node_modules",
  "venv",
]);

const ignoredRootSymlinkDirectories = new Set(
  fs
    .readdirSync(rootDir, { withFileTypes: true })
    .filter((entry) => entry.isSymbolicLink())
    .filter((entry) => {
      try {
        return fs.statSync(path.join(rootDir, entry.name)).isDirectory();
      } catch {
        return true;
      }
    })
    .map((entry) => entry.name),
);

function shouldIgnore(filePath) {
  const relativePath = path.relative(rootDir, path.resolve(filePath));

  if (!relativePath) {
    return false;
  }

  if (relativePath === ".." || relativePath.startsWith(`..${path.sep}`)) {
    return true;
  }

  const pathSegments = relativePath.split(path.sep);

  return (
    ignoredRootSymlinkDirectories.has(pathSegments[0]) ||
    pathSegments.some((segment) => ignoredDirectoryNames.has(segment))
  );
}

const createLiveReloadServer = livereload.createServer;
const watch = chokidar.watch;

chokidar.watch = (paths, options = {}) =>
  watch(paths, { ...options, followSymlinks: false });

livereload.createServer = (config) =>
  createLiveReloadServer({
    ...config,
    exclusions: [...(config.exclusions || []), shouldIgnore],
  });

serve(rootDir, !process.argv.includes("--no-open"), 3000, 35729);
