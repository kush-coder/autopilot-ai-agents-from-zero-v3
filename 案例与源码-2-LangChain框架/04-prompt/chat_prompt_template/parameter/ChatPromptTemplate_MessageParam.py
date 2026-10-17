"""
【案例】用「Message 模板类」定义 ChatPromptTemplate 的消息

对应教程章节：第 13 章 - 提示词与消息模板 → 7、对话提示词模板（ChatPromptTemplate）

知识点速览：
- `SystemMessagePromptTemplate`、`HumanMessagePromptTemplate` 用于定义可填充变量的消息模板。
- `SystemMessage`、`HumanMessage` 是已经生成的固定消息，内容不会再次进行占位符替换。
- 简单场景可使用元组；希望显式表达消息类型时，可以使用 Message 模板类。
"""

from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

# 用 Message 模板类定义系统消息和用户消息，其中的占位符会在格式化时被替换
chat_prompt = ChatPromptTemplate(
    [
        SystemMessagePromptTemplate.from_template("你是AI助手，你的名字叫{name}。"),
        HumanMessagePromptTemplate.from_template("请问：{question}"),
    ]
)

# 传入占位符变量，得到消息列表
message = chat_prompt.format_messages(name="亮仔", question="什么是LangChain")
print(message)

"""
【输出示例】
[SystemMessage(content='你是AI助手，你的名字叫亮仔。', additional_kwargs={}, response_metadata={}), HumanMessage(content='请问：什么是LangChain', additional_kwargs={}, response_metadata={})]
"""
