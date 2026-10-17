const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");

const root = path.resolve(__dirname, "..");
const pluginPath = path.join(root, "lib/plugins/giscus.js");
const syncScriptPath = path.join(root, "scripts/sync-giscus-discussions.cjs");

assert.ok(fs.existsSync(pluginPath), "the local giscus plugin should exist");

const { resolveDiscussion } = require(pluginPath);

assert.deepEqual(
  resolveDiscussion(
    "AI 智能体实战速成指南：从零到企业级落地 | ai-agents-from-zero",
    "title",
  ),
  { mapping: "number", term: "5" },
);

assert.deepEqual(resolveDiscussion("第 1-1 章 大模型认知与工程概览", "title"), {
  mapping: "number",
  term: "32",
});

assert.deepEqual(
  resolveDiscussion("第 1-3 章 RAG、微调、续训与智能体选型", "title"),
  { mapping: "number", term: "141" },
);

assert.deepEqual(
  resolveDiscussion(
    "Chapter 20 MCP Model Context Protocol",
    "title",
    "#/translations/en/20-MCP%E6%A8%A1%E5%9E%8B%E4%B8%8A%E4%B8%8B%E6%96%87%E5%8D%8F%E8%AE%AE.md",
  ),
  { mapping: "number", term: "136" },
);

assert.deepEqual(
  resolveDiscussion(
    "Chapter 1-1 LLM Understanding and Engineering Overview",
    "title",
    "#/translations/en/1-1-%E5%A4%A7%E6%A8%A1%E5%9E%8B%E8%AE%A4%E7%9F%A5%E4%B8%8E%E5%B7%A5%E7%A8%8B%E6%A6%82%E8%A7%88",
  ),
  { mapping: "number", term: "32" },
);

assert.deepEqual(
  resolveDiscussion("English home", "title", "#/translations/en/"),
  { mapping: "number", term: "5" },
);

assert.deepEqual(resolveDiscussion("尚未建立讨论的新页面", "title"), {
  mapping: "title",
});

let syncModule = {};
if (fs.existsSync(syncScriptPath)) {
  syncModule = require(syncScriptPath);
}

assert.equal(
  typeof syncModule.selectDiscussionNumbers,
  "function",
  "the sync script should expose its selection logic",
);

const selection = syncModule.selectDiscussionNumbers([
  {
    number: 50,
    title: "重复页面",
    createdAt: "2026-06-14T04:57:53Z",
    comments: { totalCount: 0 },
  },
  {
    number: 141,
    title: "重复页面",
    createdAt: "2026-10-13T09:57:34Z",
    comments: { totalCount: 1 },
  },
  {
    number: 7,
    title: "唯一页面",
    createdAt: "2026-03-18T06:05:11Z",
    comments: { totalCount: 0 },
  },
]);

assert.deepEqual(selection.discussionNumbers, {
  唯一页面: 7,
  重复页面: 141,
});
assert.deepEqual(selection.duplicates, [
  { title: "重复页面", selected: 141, skipped: [50] },
]);

assert.equal(
  typeof syncModule.buildDiscussionRoutes,
  "function",
  "the sync script should build shared routes for translated pages",
);

assert.deepEqual(
  syncModule.buildDiscussionRoutes(
    "- [第 20 章 MCP 模型上下文协议](20-MCP模型上下文协议.md)",
    "- [Chapter 20 MCP Model Context Protocol](/translations/en/20-MCP%E6%A8%A1%E5%9E%8B%E4%B8%8A%E4%B8%8B%E6%96%87%E5%8D%8F%E8%AE%AE.md)",
    { "第 20 章 MCP 模型上下文协议": 136 },
  ),
  { "20-MCP模型上下文协议.md": 136 },
);

const sourceWithGeneratedMap = [
  "before",
  "  // giscus-discussions:start",
  "  var discussionNumbers = {};",
  "  // giscus-discussions:end",
  "after",
].join("\n");

assert.equal(
  syncModule.replaceDiscussionNumbers(sourceWithGeneratedMap, {
    "页面 A": 5,
  }),
  [
    "before",
    "  // giscus-discussions:start",
    '  var discussionNumbers = {\n    "页面 A": 5\n  };',
    "  // giscus-discussions:end",
    "after",
  ].join("\n"),
);

console.log("giscus plugin tests passed");
