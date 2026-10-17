const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");

const pluginPath = path.resolve(__dirname, "../lib/plugins/language-switch.js");
function plugin() {
  assert.ok(
    fs.existsSync(pluginPath),
    "website language switch is implemented",
  );
  return require(pluginPath);
}

const chapter = "1-1-大模型认知与工程概览.md";
const metadata = {
  "README.md": { language_code: "en" },
  [chapter]: { language_code: "en" },
};

test("both homepage URLs switch to the corresponding language homepage", () => {
  const { switchTarget } = plugin();
  assert.equal(switchTarget("/", "en", metadata), "#/translations/en/");
  assert.equal(
    switchTarget("/README.md", "en", metadata),
    "#/translations/en/",
  );
  assert.equal(switchTarget("/translations/en/", "zh", metadata), "#/");
  assert.equal(switchTarget("/translations/en/README", "zh", metadata), "#/");
});

test("switching a translated chapter preserves the page and handles encoded paths", () => {
  const { switchTarget } = plugin();
  const source = "/" + encodeURIComponent(chapter.replace(/\.md$/, ""));
  assert.equal(
    switchTarget(source + "?id=中文标题", "en", metadata),
    "#/translations/en/" + encodeURIComponent(chapter),
  );
  assert.equal(
    switchTarget(
      "/translations/en/" + encodeURIComponent(chapter),
      "zh",
      metadata,
    ),
    "#/" + encodeURIComponent(chapter),
  );
});

test("an untranslated page stays in Chinese instead of navigating to a missing file", () => {
  const { switchTarget } = plugin();
  assert.equal(switchTarget("/1-2-提示词工程基础", "en", metadata), null);
  assert.equal(switchTarget("/1-2-提示词工程基础", "en", {}), null);
  assert.equal(
    switchTarget("/1-2-提示词工程基础", "zh", metadata),
    "#/" + encodeURIComponent("1-2-提示词工程基础.md"),
  );
});

test("nested source paths and special characters remain valid routes", () => {
  const { switchTarget } = plugin();
  const name = "案例/Coze&Dify 入门.md";
  const manifest = { [name]: { language_code: "en" } };
  assert.equal(
    switchTarget("/" + name, "en", manifest),
    "#/translations/en/" + name.split("/").map(encodeURIComponent).join("/"),
  );
  assert.equal(
    switchTarget("/" + name, "en", { [name]: { language_code: "fr" } }),
    null,
  );
});

test("English HTML images resolve from the document directory on GitHub Pages", () => {
  const { resolveImageSource } = plugin();
  assert.equal(
    resolveImageSource(
      "../../images/banner-v8.png",
      "/translations/en/",
      "/ai-agents-from-zero/",
      "https://didilili.github.io/ai-agents-from-zero/#/translations/en/",
    ),
    "https://didilili.github.io/ai-agents-from-zero/images/banner-v8.png",
  );
  assert.equal(
    resolveImageSource(
      "../../images/31/31-7-3-1.jpg",
      "/translations/en/31-LLaMA-Factory环境搭建与微调实战",
      "/ai-agents-from-zero/",
      "https://didilili.github.io/ai-agents-from-zero/",
    ),
    "https://didilili.github.io/ai-agents-from-zero/images/31/31-7-3-1.jpg",
  );
});

test("nested English HTML images retain encoded names, queries and fragments", () => {
  const { resolveImageSource } = plugin();
  assert.equal(
    resolveImageSource(
      "../../../images/示例 图.png?version=2#preview",
      "/translations/en/案例/README.md",
      undefined,
      "http://localhost:3000/#/translations/en/案例/",
    ),
    "http://localhost:3000/images/%E7%A4%BA%E4%BE%8B%20%E5%9B%BE.png?version=2#preview",
  );
  assert.equal(
    resolveImageSource(
      "../../images/banner-v8.png",
      "/translations/en/README.md",
      undefined,
      "http://localhost:3000/index.html#/translations/en/",
    ),
    "http://localhost:3000/images/banner-v8.png",
  );
});

test("Chinese, absolute, external and already compiled image URLs are preserved", () => {
  const { resolveImageSource } = plugin();
  const page = "https://didilili.github.io/ai-agents-from-zero/";
  assert.equal(
    resolveImageSource(
      "./images/banner-v8.png",
      "/",
      "/ai-agents-from-zero/",
      page,
    ),
    "./images/banner-v8.png",
  );
  for (const src of [
    "",
    "/ai-agents-from-zero/images/banner-v8.png",
    "https://example.org/image.png",
    "//example.org/image.png",
    "data:image/png;base64,example",
    "blob:https://example.org/id",
    "#diagram",
  ]) {
    assert.equal(
      resolveImageSource(
        src,
        "/translations/en/",
        "/ai-agents-from-zero/",
        page,
      ),
      src,
    );
  }
});

test("expired ByteDance image previews have a clear notice in both languages", () => {
  const { expiredImageNotice } = plugin();
  const src =
    "https://p9-official-plugin-sign.byteimg.com/example.png?x-expires=100&x-signature=example";
  assert.match(expiredImageNotice(src, "zh", 101000), /临时链接已过期/);
  assert.match(
    expiredImageNotice(src, "en", 101000),
    /temporary link has expired/,
  );
  assert.equal(expiredImageNotice(src, "en", 99000), null);
  assert.equal(
    expiredImageNotice(
      "https://example.org/image.png?x-expires=100",
      "en",
      101000,
    ),
    null,
  );
  assert.equal(
    expiredImageNotice(
      "https://p9-official-plugin-sign.byteimg.com/image.png",
      "en",
      101000,
    ),
    null,
  );
  assert.equal(
    expiredImageNotice(
      "https://p9-official-plugin-sign.byteimg.com/image.png?x-expires=invalid",
      "en",
      101000,
    ),
    null,
  );
});
