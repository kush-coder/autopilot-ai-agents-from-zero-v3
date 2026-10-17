/**
 * Commitlint 配置：规范 commit message
 * 使用 Conventional Commits：type(scope): subject
 * 示例：docs(README): 优化教程目录
 */
module.exports = {
  extends: ["@commitlint/config-conventional"],
  rules: {
    // type 枚举：常用类型
    "type-enum": [
      2,
      "always",
      [
        "feat", // 新功能
        "fix", // 修复 bug
        "docs", // 文档
        "style", // 格式（不影响代码）
        "refactor", // 重构
        "perf", // 性能
        "test", // 测试
        "chore", // 构建/工具
      ],
    ],
    // subject 不能为空
    "subject-empty": [2, "never"],
    // type 不能为空
    "type-empty": [2, "never"],
    // subject 以 . 结尾时警告
    "subject-full-stop": [2, "never", "."],
    // header 最大长度
    "header-max-length": [2, "always", 100],
  },
};
