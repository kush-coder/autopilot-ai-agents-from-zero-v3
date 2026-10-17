"""
【案例】从 YAML 文件加载提示词模板

对应教程章节：第 13 章 - 提示词与消息模板 → 8、从文件加载提示词（JSON / YAML）

知识点速览：
- YAML 版本与 JSON 版本的使用方式完全一致，差别主要在于文件格式是否更适合人读和写注释。
- 本案例的 `prompt.yaml` 同样描述的是一个文本模板，因此加载后的使用方式仍然是 `.format(...)`。
- 通过 `Path(__file__)` 从脚本所在目录定位 `prompt.yaml`，不依赖运行命令时的工作目录。
"""

import warnings
from pathlib import Path

warnings.filterwarnings(
    "ignore", message="Core Pydantic V1 functionality isn't compatible with Python 3.14"
)

# 从 YAML 加载提示词模板，API 与 load_prompt("prompt.json") 一致
from langchain_core.prompts import load_prompt

prompt_path = Path(__file__).resolve().with_name("prompt.yaml")
template = load_prompt(prompt_path, encoding="utf-8")
print(template.format(name="年轻人", what="滑稽"))
#

"""
【输出示例】
请年轻人讲一个滑稽的故事
"""
