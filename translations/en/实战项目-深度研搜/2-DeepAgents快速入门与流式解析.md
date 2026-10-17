# 2 - Deep Research: Quick Start with DeepAgents and Streaming Parsing

---

**Chapter objectives:**

- Get your first DeepAgent running: configure an internet search tool for the agent, and use `invoke()` to obtain the final result.
- Understand the result structure of `result["messages"]`, and know what the model and tools each do during a single agent execution.
- Master the basic usage of `stream()`, and be able to parse DeepAgents streaming output.
- Distinguish key event types such as "model decision," "tool execution," and "final response," and understand that sub-agent orchestration can also be identified as events in later extensions.
- Prepare for the next chapter, which covers `subagents` configuration and main agent orchestration.

**Study suggestion:** In this chapter, run first, then dissect. First get the minimal example working and confirm that both the regular return and `stream()` produce visible results; then look back at where fields such as `messages`, `chunk`, `tool_calls`, and `content` come from. There is no need to trace every internal DeepAgents node on the first pass; just be able to understand what each segment of the streaming output represents.

**Corresponding code branch:** `02-quickstart-streaming`

---

In the previous chapter, we already understood DeepAgents' positioning: it is suited for long-chain, complex, multi-step agent tasks that require autonomous planning and division of labor.

Starting with this chapter, we move into the code. Before rushing into the complete "Deep Research" project, we will first use a minimal example to understand the creation, execution, and streaming output of a DeepAgent.

The example to complete in this chapter is very simple:

```text
用户提问：请查询人工智能和机器人领域的热门新闻信息，并整理为一份简要报告。
智能体动作：判断需要搜索 -> 调用 internet_search -> 整理搜索结果 -> 返回报告
```

Through this example, you will see that a single agent execution is not simply "the model directly returns an answer," but rather the following chain:

```text
用户问题
  -> 模型判断是否需要工具
  -> Agent 执行搜索工具
  -> 工具返回搜索结果
  -> 模型整理搜索结果
  -> 返回最终报告
```

This flow diagram can be read in terms of "who is doing the work": the user only raises the question, the model determines the next step, the tool retrieves external material, and finally the model organizes the tool results into a human-readable report. Once this chain is clearly understood, adding sub-agents, knowledge bases, databases, file generation, and WebSocket real-time push later is essentially just extending it.

---

## 1. Quick Start: Create Your First DeepAgent

### 1.1 Install Dependencies

Before running the code, prepare the Python environment and dependencies. The current teaching code repository `deepsearch-agents` already uses `uv` to manage the Python environment and dependencies.

If you are not yet familiar with `uv`, you can first refer to the introduction to `uv` in "[3 - Shopkeeper Data Q&A: Development Environment and Basic Service Preparation](../%E5%AE%9E%E6%88%98%E9%A1%B9%E7%9B%AE-%E7%94%B5%E5%95%86%E9%97%AE%E6%95%B0/3-%E5%BC%80%E5%8F%91%E7%8E%AF%E5%A2%83%E4%B8%8E%E5%9F%BA%E7%A1%80%E6%9C%8D%E5%8A%A1%E5%87%86%E5%A4%87.md)". This chapter will not expand on the basic concepts of `uv`. You only need to know that in this project, dependencies are already listed in `pyproject.toml`, and you can simply sync them on first run.

The Python version specified in the current `deepsearch-agents/pyproject.toml` is:

```toml
requires-python = ">=3.12,<3.13"
```

That is, this project recommends using `Python 3.12`. If you already have `uv` installed, enter the `deepsearch-agents` project root directory and run:

```bash
uv sync
```

`uv sync` will automatically create `.venv` based on the project's `pyproject.toml` and `uv.lock`, and install the locked dependency versions. The core dependencies of the current project are as follows:

| Dependency               | Current Version | Purpose                                   |
| ------------------ | -------- | -------------------------------------- |
| `deepagents`       | `0.5.7`  | Core framework for creating DeepAgents              |
| `langchain`        | `1.2.17` | Provides tool wrappers, message structures, and model initialization entry points |
| `langchain-openai` | `1.2.1`  | Connects to model services via the OpenAI-compatible protocol       |
| `langgraph`        | `1.1.10` | Underlying graph execution and state flow capabilities for DeepAgents    |
| `python-dotenv`    | `1.2.2`  | Reads environment variables from the `.env` file             |
| `tavily-python`    | `0.7.24` | Calls Tavily internet search                   |

If you need to add new dependencies later, use `uv add 包名`; if you are only running the teaching examples in the current repository, executing `uv sync` is usually sufficient.

### 1.2 Code Location and Execution Steps

Corresponding project file paths: `deepsearch-agents/examples/1-deep-agent-quickstart-search.py`, `deepsearch-agents/examples/2-deep-agent-streaming-chunks.py`

Among them, `1-deep-agent-quickstart-search.py` is used to demonstrate non-streaming invocation, and `2-deep-agent-streaming-chunks.py` is used to demonstrate streaming parsing.

The code execution order is as follows:

1. Install the dependencies for this chapter.
2. Configure `.env`.
3. Create the Tavily search client.
4. Use `@tool` to wrap an ordinary Python function into an agent-callable tool.
5. Initialize the LLM.
6. Use `create_deep_agent()` to create the DeepAgent.
7. Use `invoke()` for non-streaming execution.
8. Retrieve the final result from `result["messages"][-1].content`.

Run the non-streaming example:

```bash
uv run examples/1-deep-agent-quickstart-search.py
```

Run the streaming parsing example:

```bash
uv run examples/2-deep-agent-streaming-chunks.py
```

### 1.3 Configure Environment Variables

The code reads the model and Tavily search configuration from `.env`. In actual development, do not write real keys into documentation or commit them to the repository. It is recommended to use the following placeholder approach:

```bash
OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
OPENAI_API_KEY=你的大模型_API_KEY
LLM_QWEN_MAX=qwen-max

# 在 https://app.tavily.com/ 注册账号，然后创建API KEY
TAVILY_API_KEY=你的_TAVILY_API_KEY
```

### 1.4 Wrap the Internet Search Tool

DeepAgents need tools to interact with the outside world. This chapter uses `TavilyClient` to wrap a simple internet search tool.

```python
import os
from typing import Literal

from dotenv import load_dotenv, find_dotenv
from langchain.tools import tool
from tavily import TavilyClient

load_dotenv(find_dotenv())

tavily_key = os.getenv("TAVILY_API_KEY")

# Tavily 客户端负责真正的联网搜索，工具函数中会复用这个客户端
tavily_client = TavilyClient(api_key=tavily_key)


@tool
def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["news", "finance", "general"] = "general",
    include_raw_content: bool = False,
):
    """
    互联网搜索工具

    DeepAgent 会根据工具描述和参数签名，自动决定是否调用该工具
    :param query: 搜索关键词
    :param max_results: 返回结果数量
    :param topic: 查询主题，可选 news、finance、general
    :param include_raw_content: 是否返回更详细的原文内容，include_raw_content=False 时返回摘要内容；True 时会尝试返回更完整的网页原文
    :return: Tavily 搜索结果
    """
    print(
        f"开始调用网络搜索工具，核心参数为：{query},{max_results},{topic},{include_raw_content}"
    )
    return tavily_client.search(
        query=query,
        max_results=max_results,
        topic=topic,
        include_raw_content=include_raw_content,
    )
```

The most critical part here is the `@tool` decorator. It wraps an ordinary Python function into a LangChain tool, allowing the agent to call it during reasoning.

The tool's function signature and docstring are also important. The model determines when to call this tool and what parameters to pass based on the tool name, parameter types, and description. If the tool description is too vague, the model is more likely to misuse it.

### 1.5 Initialize the Model

Next, initialize the LLM object:

```python
from langchain.chat_models import init_chat_model

llm_name = os.getenv("LLM_QWEN_MAX")

llm = init_chat_model(
    model=llm_name,
    model_provider="openai",
)
```

Here, `llm` is the model object used by the DeepAgent for decision-making and response generation. Whether it is an ordinary agent or a DeepAgent, a model must be involved in decision-making.

### 1.6 Create the DeepAgent

The core function for creating a DeepAgent is `create_deep_agent()`.

```python
from deepagents import create_deep_agent

# 当前示例不配置子智能体，重点观察“主智能体 + 搜索工具”的基本流程
deep_agent = create_deep_agent(
    model=llm,
    tools=[internet_search],
    subagents=[],
    system_prompt="""
    你是一名严谨的研究员，可以使用 internet_search 工具检索网络信息。
    请根据检索结果进行归纳、分析和交叉验证，生成一份结构清晰、信息可靠的中文报告。
    """,
)
```

Let's look at the four core parameters first:

| Parameter            | Meaning                                                   |
| --------------- | ------------------------------------------------------ |
| `model`         | The LLM used by the agent                                     |
| `tools`         | List of tools that the main agent can directly call                         |
| `subagents`     | List of sub-agents; left empty for now in this section                               |
| `system_prompt` | System prompt for the main agent, used to define its role, goals, and tool usage boundaries |

Although `subagents=[]` in this version of the code, it is still a DeepAgent. The current example simply uses one search tool to help us understand the agent's execution process; sub-agents will be covered separately later.

### 1.7 First Run with invoke

The minimal example first uses `invoke()` for execution:

```python
# 非流式执行，invoke 会等整条 agent 链路完成后，一次性返回最终状态
result = deep_agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "请查询人工智能和机器人领域的热门新闻信息，并整理为一份简要报告。",
            }
        ]
    }
)

# result 中会保留完整消息轨迹，便于观察模型决策、工具返回和最终回答
print(result)

# messages 的最后一条通常就是 DeepAgent 整理后的最终回答
print(result["messages"][-1].content)
```

Note that the input is not a simple string, but a dictionary containing `messages`:

```python
{
    "messages": [
        {"role": "user", "content": "用户问题"}
    ]
}
```

This is because DeepAgents inherits the message model of LangGraph / LangChain under the hood, and the entire execution process revolves around passing state through `messages`.

Running the file to verify, success:

```text
uv run examples/1-deep-agent-quickstart-search.py

LangChainPendingDeprecationWarning: The default value of `allowed_objects` will change in a future version.
开始调用网络搜索工具，核心参数为：人工智能 机器人 热门新闻,5,news,False

{
  "messages": [
    HumanMessage(
      content="请查询人工智能和机器人领域的热门新闻信息，并整理为一份简要报告。"
    ),
    AIMessage(
      content="",
      tool_calls=[
        {
          "name": "internet_search",
          "args": {
            "query": "人工智能 机器人 热门新闻",
            "topic": "news",
            "max_results": 5,
            "include_raw_content": False
          }
        }
      ]
    ),
    ToolMessage(
      name="internet_search",
      content="Tavily 返回了 5 条新闻结果，包含 url、title、score、published_date、content 等字段"
    ),
    AIMessage(
      content="## 人工智能与机器人领域热门新闻简报\n\n1. Genesis AI 推出新型机器人大脑...\n2. Meta 收购 ARI...\n3. 无人驾驶出租车将重塑出行市场..."
    )
  ]
}

## 人工智能与机器人领域热门新闻简报

1. Genesis AI 推出新型机器人“大脑”
2. Meta 收购 Assured Robot Intelligence（ARI）
3. 无人驾驶出租车将重塑出行市场
4. 四月机器人行业十大新闻回顾
5. 值得关注的欧洲初创企业
```

Among the output, `LangChainPendingDeprecationWarning` is a version notice from inside the LangGraph / LangChain dependencies and does not affect this chapter's example. What really needs attention is the subsequent tool invocation logs, the `messages` trajectory, and the final report.

This output can be viewed at three layers:

| Output Location                  | Description                                                         |
| ------------------------- | ------------------------------------------------------------ |
| `开始调用网络搜索工具...` | The `print()` inside the tool function, indicating that `internet_search` was actually executed  |
| `result["messages"]`      | Complete execution trajectory, including user message, model tool call, tool return, and final answer |
| Final Markdown report      | `result["messages"][-1].content`, which is the final content presented to the user |

Establish an intuition here: although `invoke()` ultimately returns a report, internally it is not "a single model response," but rather a complete chain of "model decides to call tool -> tool returns result -> model organizes answer."

---

## 2. Non-Streaming Invocation: invoke and messages

### 2.1 Actual Invocation Analysis

What `invoke()` returns is not a piece of plain text, but a dictionary containing the complete message process. Simplified, it can be understood as follows:

```text
result = {
    "messages": [
        # 用户问题
        HumanMessage(
            content="请查询人工智能和机器人领域的热门新闻信息，并整理为一份简要报告。"
        ),
        # 模型决定调用 internet_search 工具
        AIMessage(
            content="",
            tool_calls=[
                {
                    "name": "internet_search",
                    "args": {
                        "query": "人工智能 机器人 热门新闻",
                        "topic": "news",
                        "max_results": 5,
                        "include_raw_content": False
                    }
                }
            ]
        ),
        # internet_search 工具返回搜索结果
        ToolMessage(
            name="internet_search",
            content='{"query": "人工智能 机器人 热门新闻", "results": [...]}'
        ),
        # 模型基于工具结果生成最终回答
        AIMessage(
            content="## 人工智能与机器人领域热门新闻简报..."
        ),
    ]
}
```

That is, a single agent execution roughly goes through the following steps:

1. The user sends the question to the agent.
2. The agent passes the user question, system prompt, and tool descriptions to the model.
3. The model determines that it needs to call `internet_search`.
4. The agent actually executes the search tool.
5. The tool returns the search results.
6. The agent passes the tool results back to the model.
7. The model organizes the search results and generates the final report.

Behind these 7 steps, four roles are actually cooperating:

```text
用户 -> Agent -> 大模型 -> 工具 -> Agent -> 大模型 -> 用户
```

In the first step, the user does not directly call the LLM, but instead passes the question to `deep_agent`:

```python
result = deep_agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "请查询人工智能和机器人领域的热门新闻信息，并整理为一份简要报告。",
            }
        ]
    }
)
```

What is passed in at this step is `messages`. DeepAgents will first wrap this user message into `HumanMessage` and place it into the current execution state.

In the second step, the agent passes the following types of information to the LLM together:

- User question: `请查询人工智能和机器人领域的热门新闻信息，并整理为一份简要报告。`
- System prompt: You are a rigorous researcher and can use search tools to generate well-structured, reliable Chinese reports
- Tool description: The currently available tool is `internet_search`
- Tool parameter structure: `query`, `max_results`, `topic`, `include_raw_content`

That is, the LLM does not "naturally know" what tools the agent has. Instead, when the agent calls the model, it places the tool names, parameters, and descriptions into the context. Only after the model reads this information does it determine that this question requires internet search, and then generates a tool call.

This step corresponds to the second message in `result["messages"]`:

```text
AIMessage(
    content="",
    tool_calls=[
        {
            "name": "internet_search",
            "args": {
                "query": "人工智能 机器人 热门新闻",
                "topic": "news",
                "max_results": 5,
                "include_raw_content": False
            }
        }
    ]
)
```

Note here: this `AIMessage` is not yet the final answer. Its `content` is empty, but `tool_calls` has a value, meaning the model is telling the agent: "Next, please call the `internet_search` tool and pass these parameters."

In the third step, the agent actually executes the tool according to `tool_calls`, that is, it calls the Python function we defined earlier:

```python
@tool
def internet_search(query: str, max_results: int = 5, ...):
    return tavily_client.search(...)
```

After the tool execution completes, a `ToolMessage` is generated. This message stores the raw search results returned by Tavily, usually structured data that may include titles, links, summaries, publication times, and other information.

Based on the actual output, the JSON in `ToolMessage(content=...)` mainly contains these fields:

| Field             | Meaning                         |
| ---------------- | ---------------------------- |
| `query`          | The search keyword passed to Tavily this time |
| `results`        | List of search results                 |
| `url`            | Webpage link of a single search result       |
| `title`          | Title of a single search result           |
| `content`        | Summary content of a single search result       |
| `published_date` | News publication time                 |
| `response_time`  | Time consumed by this Tavily request          |
| `request_id`     | Tavily request ID for this request           |

Step 4: The tool result is not directly returned to the user. The Agent will pass `ToolMessage` back to the large language model, letting the model organize, translate, filter, and polish based on the search results. For example, the results returned by Tavily may contain English webpage summaries, but the user's question is in Chinese, so the final result is usually organized into a Chinese report by the model.

This step corresponds to the last `AIMessage`:

```text
AIMessage(
    content="## 人工智能与机器人领域热门新闻简报..."
)
```

At this point, `tool_calls` no longer has a value, and `content` has complete content, indicating that the model is no longer calling tools and has already generated the final reply.

Therefore, when we retrieve the final reply, we usually directly take the last message:

```python
final_answer = result["messages"][-1].content
```

If you only care about the final report, just read the last message; if you need to debug the Agent's execution chain, then inspect the complete `result`.

### 2.2 Why does the model know which tool to call

It is the core of the Agent's tool calling.

The model itself does not actively scan your Python code, nor does it know on its own which functions exist in the project. What actually happens is: when we create the agent through `create_deep_agent()`, we have already passed the tool list to the Agent.

```python
deep_agent = create_deep_agent(
    model=llm,
    tools=[internet_search],
    subagents=[],
    system_prompt="..."
)
```

When executing `invoke()`, the Agent will organize the names, descriptions, and parameter structures of `internet_search` and pass them to the model. Only after the model reads them will it decide whether to generate `tool_calls`.

Therefore, the judgment chain for tool calling can be remembered like this:

```text
工具注册到 Agent
  -> Agent 把工具描述交给模型
  -> 模型判断是否需要调用工具
  -> 模型生成 tool_calls
  -> Agent 根据 tool_calls 执行真实工具
```

This also explains why we have emphasized earlier that the names, parameter types, and comments of tool functions should be written clearly. They are not only for developers to read; they also affect whether the model can correctly call the tool.

### 2.3 Understanding the four types of messages

To understand `result["messages"]`, you can first remember the following table:

| Message type       | Role in the execution chain                           | Common characteristics                         |
| -------------- | -------------------------------------------- | -------------------------------- |
| `HumanMessage` | The question input by the user                               | `content` is the user's original question         |
| `AIMessage`    | The model's thinking result, which may be a tool call or a reply | When there is `tool_calls`, it means it is preparing to call a tool |
| `ToolMessage`  | The return result after the tool actually executes                     | `name` is usually the tool name              |
| `AIMessage`    | The final answer organized by the model based on the tool result             | `content` has the final natural language result     |

The most confusing one is `AIMessage`. It has two situations:

- `AIMessage(content="", tool_calls=[...])`: The model has not answered yet; it is only deciding which tool to call next.
- `AIMessage(content="...")`: The model has already generated the final answer.

Therefore, to judge what the Agent is actually doing, you cannot only look at the message type; you also need to continue examining `tool_calls` and `content`.

---

## 3. Streaming invocation: stream and chunk

### 3.1 Why switch to stream

`invoke()` is a non-streaming execution. Its characteristic is that it keeps waiting after being called until the entire agent task is completed, and then returns the complete result all at once.

```text
用户点击发送 -> 后端执行 5 秒或 10 秒 -> 一次性返回最终结果
```

This approach is simple to write, but the user experience is not good enough. Especially for long-chain tasks like DeepAgents, the agent may search, read, call multiple tools, and dispatch subtasks. If the frontend receives no feedback, it is difficult for users to judge whether the system is processing or has become stuck.

The goal of streaming execution is to let users see the process:

```text
开始处理
模型决定调用搜索工具
搜索工具返回结果
模型整理搜索结果
最终回复
```

Later, when building Web projects, these processes will usually be pushed to the frontend through `SSE` or `WebSocket`. The complete version of this project uses WebSocket, because it is more suitable for continuously pushing the Agent's execution status and tool logs.

### 3.2 Using stream to obtain the execution process

Corresponding file path in the project: `deepsearch-agents/examples/2-deep-agent-streaming-chunks.py`

After replacing `invoke()` with `stream()`, the return value is no longer the complete result, but a stream that can be iterated continuously:

```python
# 流式执行，stream 会在每个图节点完成后产出一个 chunk
# 常见节点包括 model（模型决策或最终回答）和 tools（工具执行结果）
stream = deep_agent.stream(
    {
        "messages": [
            {
                "role": "user",
                "content": "请查询人工智能和机器人领域的热门新闻信息，并整理为一份简要报告。",
            }
        ]
    }
)

# 每个 chunk 是一个按节点名组织的字典
for chunk in stream:
    print(chunk)
```

Each `chunk` indicates that a certain node has just produced a state update. Because DeepAgents is built on LangGraph underneath, the streaming output carries node information.

In simplified terms, common `chunk` may look like this:

```python
{
    "model": {
        "messages": [AIMessage(content="", tool_calls=[...])]
    }
}
```

Or:

```python
{
    "tools": {
        "messages": [ToolMessage(content="工具返回结果...")]
    }
}
```

When parsing streaming output, focus on two layers of information:

1. Outer node name: whether it is currently the `model` node or the `tools` node.
2. The last message in the inner layer: whether the model has decided to call a tool, or has already provided the final answer.

### 3.3 Four key states of chunk

| State                 | How to identify                                                                 | Meaning                                     |
| -------------------- | ------------------------------------------------------------------------ | ---------------------------------------- |
| Model decides to call a tool     | `node_name == "model"` and the tool name in `last_msg.tool_calls` is not `task`      | The model determines that the next step is to call an ordinary tool         |
| Model decides to call a sub-agent | `node_name == "model"` and `tool_call["name"] == "task"`                  | The model determines that the next step is to dispatch the task to a sub-agent |
| Tool execution completed         | `node_name == "tools"`                                                   | The Agent actually calls the tool and obtains the tool return result |
| Model returns the final result     | `node_name == "model"` and no `tool_calls`, but `last_msg.content` has content | The model generates the final reply based on the previous results             |

The examples in this chapter only configure `internet_search`, so during runtime you will mainly see "ordinary tool calls." The sub-agent state in the table is an entry point reserved for later: after Chapter 3 actually configures `subagents`, such scheduling events may appear in the streaming output.

### 3.4 Object view examples of the four chunk states

Just looking at the table above is still somewhat abstract. Below, referring to the writing in the project documentation, the several types of `chunk` that may appear during the iteration of `stream()` are expanded into Python object views.

Note that this does not require you to write these objects by hand; it is to help you quickly identify which step the Agent is currently at when `print(chunk)`.

**Scenario A: The model decides to call an ordinary tool.**

This is the most common type in the code of this chapter. After the model reads the user's question, it finds that web search is needed, so it generates a `tool_calls` with the tool name `internet_search`.

```python
{
    "model": {
        "messages": [
            AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "internet_search",
                        "args": {
                            "query": "人工智能和机器人 热门新闻",
                            "topic": "news",
                            "max_results": 5,
                        },
                        "id": "call_xxx",
                    }
                ],
            )
        ]
    }
}
```

The key point of this state is: `content` is empty, and `tool_calls` has a value. This indicates that the model has not yet answered the user, but is telling the Agent: "Next, please call this tool."

**Scenario B: Tool execution is completed and a result is returned.**

After the Agent actually finishes executing `internet_search`, it will produce `ToolMessage` from the `tools` node:

```python
{
    "tools": {
        "messages": [
            ToolMessage(
                content='{"query": "人工智能和机器人 热门新闻", "results": [...]}',
                name="internet_search",
                tool_call_id="call_xxx",
            )
        ]
    }
}
```

The key point of this state is: the outer node name becomes `tools`. At this moment, it is not the model thinking, but the tool has finished executing and handed the original result back to the Agent.

**Scenario C: The model decides to call a sub-agent.**

This chapter has not actually configured a sub-agent yet, so this type of state usually does not appear in the current examples. But later in Chapter 3, after adding `subagents`, if the model decides to delegate the task to a sub-agent, you will see the special tool `task`:

```python
{
    "model": {
        "messages": [
            AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "task",
                        "args": {
                            "subagent_type": "network_search_agent",
                            "description": "查询人工智能和机器人领域的热门新闻，并返回来源、摘要和关键信息。",
                        },
                        "id": "call_yyy",
                    }
                ],
            )
        ]
    }
}
```

`task` is essentially also a tool call, except that it calls not an ordinary Python tool, but the sub-agent dispatch entry of DeepAgents. During parsing, as long as you see `tool_call["name"] == "task"`, you can identify it as "dispatching to a sub-agent."

**Scenario D: The model generates the final reply.**

After the tool result has been returned and the model has finished organizing it, it will once again produce a message from the `model` node. This time there is no `tool_calls`, but there is a real `content`:

```python
{
    "model": {
        "messages": [
            AIMessage(
                content="以下是关于人工智能和机器人领域的热门新闻概要：...",
                tool_calls=[],
            )
        ]
    }
}
```

This state indicates that the Agent chain has converged, and the model is no longer calling tools or sub-agents, but instead returning the final result to the user.

In addition to the four types of business events above, the actual output may also contain some middleware nodes, such as `PatchToolCallsMiddleware.before_agent` and `TodoListMiddleware.after_model`. These nodes may not contain `messages`, or they may not be business progress that we want to show to users, so the parsing code later will use the following line to filter them out:

```python
if not state or "messages" not in state:
    continue
```

### 3.5 Complete code for parsing chunks

Corresponding file path in the project: `deepsearch-agents/examples/2-deep-agent-streaming-chunks.py`

```python
# 流式执行，stream 会在每个图节点完成后产出一个 chunk
stream = deep_agent.stream(
    {
        "messages": [
            {
                "role": "user",
                "content": "请查询人工智能和机器人领域的热门新闻信息，并整理为一份简要报告。",
            }
        ]
    }
)

for chunk in stream:
    # chunk 是一个按节点名组织的字典，例如
    # {"model": {"messages": [...]}} 或 {"tools": {"messages": [...]}}
    for node_name, state in chunk.items():
        # DeepAgents 内部中间件也可能产出空状态或非消息状态，这里只解析消息类状态
        if not state or "messages" not in state:
            continue

        messages = state["messages"]

        if not messages or not isinstance(messages, list):
            continue

        # 每个 chunk 的最后一条消息，通常就是这个节点本次产出的核心信息
        last_msg = messages[-1]

        if node_name == "model":
            # model 节点有两类重点事件：
            # 1. tool_calls 非空，模型决定下一步调用工具或子智能体
            # 2. content 非空，模型已经生成最终回答
            if last_msg.tool_calls:
                for tool_call in last_msg.tool_calls:
                    if tool_call["name"] == "task":
                        print(
                            f"【大模型】决定调用子智能体：{tool_call['args']['subagent_type']}"
                        )
                    else:
                        print(
                            f"【大模型】决定调用工具：{tool_call['name']} 传入的参数：{tool_call['args']}"
                        )

            elif last_msg.content:
                print(f"【大模型】最终执行的结果：{last_msg.content}")

        elif node_name == "tools":
            # tools 节点返回的是具体工具的执行结果，通常可以推送给前端展示执行进度
            tool_return_result = last_msg.content[:100] + "..."
            tool_name = last_msg.name
            print(f"【agent】调用了{tool_name}工具，返回的结果为：{tool_return_result}")
```

There are several details in this code that require special attention.

**First,** the outer loop takes `node_name` and `state`:

```python
for node_name, state in chunk.items():
```

`node_name` is used to determine which type of node produced the output, such as `model` or `tools`. `state` contains the actual state data.

**Second,** some middleware nodes do not contain `messages` and should be skipped first:

```python
if not state or "messages" not in state:
    continue
```

Some middleware nodes may appear inside DeepAgents, such as `TodoListMiddleware.after_model`. They are meaningful for framework execution, but they are not necessarily business events that we want to show to users.

**Third,** only take `messages[-1]`:

```python
last_msg = messages[-1]
```

Because each state update may contain multiple messages, but the most critical one for the current update is usually the last one.

**Fourth,** the `model` node should further distinguish between two situations:

- `last_msg.tool_calls` has a value: the model is not giving the final answer, but deciding what to call next.
- `last_msg.content` has a value: the model has already generated the final reply.

**Fifth,** the `tools` node represents that the tool has actually finished executing. Here you can truncate the tool name and return result before pushing them to the frontend, to avoid flooding the interface with a large block of search results.

Execute the file for verification, and it succeeds:

```text
uv run examples/2-deep-agent-streaming-chunks.py

LangChainPendingDeprecationWarning: The default value of `allowed_objects` will change in a future version.
【大模型】决定调用工具：internet_search 传入的参数：{'query': '人工智能和机器人 热门新闻', 'topic': 'news', 'max_results': 5}
开始调用网络搜索工具，核心参数为：人工智能和机器人 热门新闻,5,news,False
【agent】调用了internet_search工具，返回的结果为：{"query": "人工智能和机器人 热门新闻", "follow_up_questions": null, "answer": null, "images": [], "results": [{"....
【大模型】最终执行的结果：以下是关于人工智能和机器人的几条热门新闻概要：

1. **新AI大脑让机器人像人类一样移动 - Fox News**
   - Genesis AI推出了一款名为GENE-26.5的机器人“大脑”，它能够帮助通用型机器人执行复杂的物理任务，就像人类一样操作。该系统通过大量数据训练，可以让机器人手部模仿人类手部的动作，完成诸如制作煎蛋等多步骤过程的任务。

2. **如何重塑乘车市场 - Financial Times 视频报道**
   - 本视频探讨了人工智能如何推动下一代自动驾驶出租车的发展，并分析了这一技术对当前乘车市场的潜在影响。

3. **为什么实体AI才是真正的制造业革命 - The Robot Report**
   - 文章讨论了实体AI在制造业中的应用以及其对于硬件创新的重要性。指出实体AI正在使机器人学习与适应环境的能力变得更快更强，并且强调了区分人形机器人炒作与实际硬件扩展之间的差异。

4. **不仅仅是汽车：关注2026年中国汽车展上的机器人转变 - CleanTechnica**
   - 在北京国际汽车展览会上，中国汽车产业开始从电动汽车和软件定义车辆转向所谓的“实体AI”——即超越车辆本身、进入现实世界的机器智能。多家参展商展示了基于共享智能平台的各种机器人和服务机器人。

如果您需要更多详细信息或想深入了解某个特定主题，请告诉我！
```

This output is more suitable for observing the execution process than `invoke()`, and it can be read in order:

| Output fragment                                | Corresponding execution stage                                         |
| --------------------------------------- | ------------------------------------------------------ |
| `【大模型】决定调用工具...`             | `model` node output, the model decides to call `internet_search` next |
| `开始调用网络搜索工具...`               | The Python tool function actually starts executing                            |
| `【agent】调用了internet_search工具...` | `tools` node output, the tool result has been returned                     |
| `【大模型】最终执行的结果...`           | `model` node outputs again, the model generates the final answer based on the tool result     |

This is the core value of streaming parsing: without waiting for the final report to be generated, both developers and the frontend can see which step the Agent is currently at.

### 3.6 How to display when integrating with the frontend

Although this chapter has not yet written a FastAPI interface, you can establish the correspondence between backend events and frontend display in advance.

| Event parsed by the backend                   | What the frontend can display as       |
| ---------------------------------- | ------------------------ |
| Model decides to call tool `internet_search` | Searching web resources         |
| Tool returns search results                   | Search results obtained, organizing |
| Model decides to call sub-agent               | Dispatching to a specialized assistant   |
| Model returns final result                   | Display the final answer or report       |

This is also why streaming parsing is important. Enterprise-level agent projects do not only look at the final answer, but also need to let users perceive the execution process, and allow developers to locate what each step does.

**One-sentence summary:** `invoke()` shows the final result, `stream()` shows the execution process; when building real products, streaming processing is almost a mandatory skill to master.

---

**Chapter summary:**

In this chapter, we completed the quick start of DeepAgents. We first defined the `internet_search` search tool, then initialized the model, and finally assembled the main agent through `create_deep_agent()`, and used `invoke()` to obtain the final result.

Next, we focused on learning the streaming parsing approach of `stream()`. As long as you grasp the two node types `model` and `tools`, and combine them with `tool_calls` and `content`, you can determine whether the model is currently making a decision, a tool is executing, or the model has already produced the final result. Later, when sub-agents are introduced, they will also build on this parsing logic.

The complete sub-agent configuration, dispatch signals, and asynchronous execution will be covered in the next chapter. For now, you only need to grasp this layer: `invoke()` is suitable for viewing the final result, while `stream()` is suitable for clearly seeing what the Agent is doing at each step.
