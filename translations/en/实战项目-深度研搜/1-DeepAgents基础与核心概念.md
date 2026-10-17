# 1 - Deep Research: DeepAgents Fundamentals and Core Concepts

---

**Chapter learning objectives:**

- Understand why deep agent frameworks like DeepAgents are needed after regular LLM calls and tool-using agents.
- Master the positioning differences between `LangChain`, `LangGraph`, and `DeepAgents`.
- Understand the four core capabilities of DeepAgents: task planning, context management, sub-agents, and long-term memory.
- Understand why advanced prompting appears alongside DeepAgents and its role in complex tasks.
- Establish a sense of boundaries in multi-agent design: know when sub-agents are appropriate and when multi-agent approaches should not be overused.

**Study suggestions:** This chapter first establishes boundaries; don't rush into writing code. Focus on why regular agents struggle with long tasks, and where DeepAgents places capabilities like planning, files, sub-agents, and long-term context. After reading, you should be able to answer: which tasks are worth handing to DeepAgents, and which tasks can be handled by a regular agent or a simple chain. In the next chapter, we will dive into `create_deep_agent()`, `invoke()`, and `stream()`.

---

## 1. Project Introduction

### 1.1 Project Background

"Deep Research (DeepAgents Multi-Agent)" is an enterprise-level agent hands-on project for complex research tasks. Its ultimate goal is not simple Q&A, but enabling an agent to conduct information search, information organization, reflective supplementation, and report generation around an open-ended question.

To describe the project goal more specifically, it can be understood as a "Deep Research" system:

- The user poses a research question;
- The system automatically decomposes research directions;
- Different tools or sub-agents complete tasks such as searching, reading, analysis, and verification;
- The main agent aggregates intermediate results and generates a well-structured research report.

This type of task differs from ordinary chat Q&A. It usually has no fixed answer, and it is not always possible to hard-code the entire workflow in advance. The system needs to adjust subsequent actions based on intermediate results as it executes.

This is exactly where DeepAgents shines.

### 1.2 Why DeepAgents Is Needed

We have already learned many LLM application development approaches, such as:

- Directly calling LLM APIs and having the model return text;
- Using LangChain to wrap models, prompts, output parsers, and tools;
- Using LangGraph to break complex tasks into multiple fixed nodes;
- Using agents to let the model autonomously decide whether to call tools during execution.

These approaches are all important and can complete many tasks. However, as tasks become longer, more open-ended, and more complex, regular agents gradually encounter several problems:

- Context becomes increasingly cluttered, with tool results and historical messages easily crowding together;
- Task decomposition is unstable; the model may work on whatever comes to mind;
- Everything is placed on a single main agent, with unclear division of specialized work;
- Intermediate processes are hard to observe, making errors difficult to locate;
- When multiple rounds of search, reflection, and parallel exploration are involved, the execution chain can easily spiral out of control.

For example, suppose a user asks an agent to produce a "research report on hot news in the artificial intelligence and robotics industry." This task involves at least understanding the question, web searching, filtering materials, summarizing viewpoints, and organizing the report. If extended into deep search, it may also require supplementary searches, cross-validation, reflecting on missing information, and even having different sub-agents handle different directions.

DeepAgents is designed to solve exactly these more complex, longer-chain, and more autonomy-demanding agent tasks.

Simply put:

**DeepAgents is not just about having the model answer questions; it is about making the agent act like a task owner who can plan, divide work, use tools, and manage context.**

---

## 2. Agent Evolution: From LLM to DeepAgents

### 2.1 Three Stages of Development

Let's first build an overall impression with a diagram.

![Diagram of the capability evolution from LLM to AI Agent to Agentic AI](../../../%E5%AE%9E%E6%88%98%E9%A1%B9%E7%9B%AE-%E6%B7%B1%E5%BA%A6%E7%A0%94%E6%90%9C/images/1/1-2-1-1.png)

This diagram illustrates the progressive relationship of LLM application capabilities: early LLMs were mainly responsible for language generation; in the Agent stage, models began to call tools and perform actions; later, as they evolved into Agentic AI, systems gained stronger planning, collaboration, and long-term task execution capabilities.

If broken down into a learning path, it can be divided into three stages.

**Stage 1: Direct LLM Calls**

Early LLM applications were usually very simple: send a prompt to the model, and the model returns text.

```text
用户问题 -> Prompt -> LLM -> 文本结果
```

This approach is suitable for relatively simple tasks such as Q&A, summarization, rewriting, and classification. Its advantage is simplicity and directness, but the drawbacks are also obvious: the model can only answer based on existing context; it cannot proactively access external systems or truly perform actions.

For example, if you ask it "What AI news is there today?" and there is no web access tool, it can only answer based on training knowledge or context, without being able to obtain real-time information.

**Stage 2: Tool-Using Agents**

Later, we began equipping models with tools such as search tools, database tools, calculation tools, and file tools. The core change in agents is that the model no longer only answers questions; it can decide whether to call a tool based on the task.

```text
用户问题 -> Agent -> LLM 判断 -> 调用工具 -> 工具结果 -> LLM 总结 -> 最终结果
```

At this point, the agent has gained "action capability." It can first let the model decide what to do next, then call the corresponding tool, and finally organize the tool results into natural language.

However, a regular agent is usually still a single main agent handling everything. As tasks grow longer, all tool descriptions, historical messages, and tool results crowd into the same context window. The main agent has to plan, search, analyze, and write reports all at once, and the pressure keeps mounting.

**Stage 3: DeepAgents Multi-Agent**

DeepAgents builds on regular agents by further enhancing them: in addition to calling tools, it can also call sub-agents.

```text
用户任务
  -> 主智能体负责规划和调度
  -> 调用工具或分派给子智能体
  -> 子智能体独立完成局部任务
  -> 主智能体汇总并输出最终结果
```

The key change here is that the main agent no longer does everything itself, but acts more like a project leader. It can assign different tasks to different sub-agents, letting them complete specialized work in their own contexts, and then aggregate the results.

This is the meaning of "Deep" in DeepAgents: it is oriented toward deeper, longer-chain, and more complex agent execution processes.

### 2.2 Fixed Workflows vs. Autonomous Agents

Before understanding DeepAgents, it is also necessary to distinguish one concept: fixed workflows and autonomous agent decision-making are not the same thing.

In LangGraph projects, we often write a fixed graph. For example:

```text
START -> extract_keywords -> recall_info -> generate_sql -> validate_sql -> END
```

The characteristic of this kind of graph is that nodes and edges are mostly written by developers in advance. At runtime, there may be conditional branches, but the overall route is clear, controllable, and fixed.

An agent's execution approach is more flexible. It dynamically decides what to do next based on the user's question, system prompt, tool descriptions, and sub-agent descriptions. It may first call a search tool, or first write a to-do list, or assign the task to a sub-agent.

The following table provides a quick comparison:

| Form            | Who decides the workflow                     | Suitable scenarios                         |
| --------------- | ------------------------------------------ | -------------------------------- |
| Plain LLM call   | Developer writes the prompt in advance      | Simple Q&A, summarization, classification             |
| LangChain Agent | Model dynamically decides based on tool descriptions | Simple tool-calling tasks               |
| LangGraph       | Developer explicitly orchestrates nodes and edges | Tasks with clear workflows requiring strong control       |
| DeepAgents      | Main agent autonomously plans based on prompts, tools, and sub-agents | Long-chain, complex, multi-step, multi-role tasks |

The most easily confused pair in this table is LangGraph and DeepAgents.

If you already know exactly "what to do first, what to do second, and where to go after a failure," LangGraph is very suitable; if the task itself is relatively open-ended and the execution route needs the agent to plan and adjust on its own, DeepAgents is more suitable.

### 2.3 Deep Agents and Advanced Prompting

In the deep search project, besides Deep Agents, there is another concept you will encounter repeatedly: **advanced prompting**.

These two concepts are best understood together.

Deep Agents solve the problem of "how tasks are organized." When facing complex tasks, the agent no longer gives a one-shot answer, but needs the following capabilities:

- First break down complex tasks into executable sub-goals;
- Match tools or sub-agents to different sub-goals;
- Observe intermediate results during execution and fill gaps when discovered;
- Adjust the plan based on tool returns and subtask results;
- When deviations occur, use reflection and correction to keep the task converging toward the goal.

Advanced prompting solves the problem of "how the model should think."

Ordinary prompts usually tell the model "what to do," for example:

```text
请分析这条用户评论的情绪，并给出改进建议。
```

Advanced prompts further tell the model "what steps to think through," for example:

```text
请按以下流程分析：
1. 先提取评论中出现的具体问题；
2. 再判断情绪倾向，并给出理由；
3. 按影响程度对问题排序；
4. 每个问题给出可落地的改进建议；
5. 最后用一句话总结核心痛点。
```

The relationship between the two can be understood as:

- Deep Agents are the organizational architecture of the agent system, determining how tasks are planned, divided, executed, and fed back;
- Advanced prompting is the reasoning specification of the agent system, determining how the model analyzes problems, decomposes logic, and organizes output.

Therefore, when working on the deep search project later, we cannot only focus on "whether there are tools" and "whether there are sub-agents." What truly determines system stability is often whether these two things work well together: **use DeepAgents to organize the execution chain, and use advanced prompting to constrain the reasoning process.**

---

## 3. DeepAgents Framework Positioning

### 3.1 Relationship with LangChain and LangGraph

DeepAgents is an independent library in the LangChain ecosystem, built on top of the foundational capabilities of LangChain and LangGraph, used to build more complex autonomous multi-agent systems.

Its goal is not to replace LangChain or LangGraph, but to add higher-level agent capabilities on top of them:

- Built-in task planning capabilities;
- Built-in context management and file system capabilities;
- Support for sub-agent division of labor;
- Support for long-term memory;
- Support for continuous execution and streaming observation of complex tasks.

![Diagram of the capability stack relationship among DeepAgents, LangGraph, and LangChain](../../../%E5%AE%9E%E6%88%98%E9%A1%B9%E7%9B%AE-%E6%B7%B1%E5%BA%A6%E7%A0%94%E6%90%9C/images/1/1-3-1-1.png)

This diagram can be read from the inside out:

- The innermost layer is `LangChain`, responsible for basic interaction between LLMs and tools;
- The middle layer is `LangGraph`, responsible for organizing the execution process into a stateful, persistent, and streaming graph;
- The outermost layer is `DeepAgents`, which further provides planning tools, file system tools, sub-agents, and backend storage capabilities.

In other words, DeepAgents does not reinvent a model invocation framework; instead, it builds on existing model, tool, and graph execution capabilities to fill in the ability to "organize complex tasks over the long term."

### 3.2 Comparison of Usage Scenarios for the Three Frameworks

All three frameworks are part of the LangChain ecosystem, but their usage scenarios are not exactly the same.

| Framework         | Core positioning                                                     | When to use                                     |
| ------------ | ------------------------------------------------------------ | ------------------------------------------------------ |
| `LangChain`  | Foundational development framework, wrapping models, prompts, tools, agents, etc.           | Quickly building simple agents, or combining models and tools yourself             |
| `LangGraph`  | Graph execution framework, emphasizing state, nodes, edges, branching, persistence, and streaming output       | Complex workflows with clear processes requiring fine-grained control and stable orchestration     |
| `DeepAgents` | Deep agent framework, emphasizing autonomous planning, sub-agents, context management, and long-term memory | Long tasks, multi-step, multi-role, requiring the agent to plan and schedule on its own |

Here is another more engineering-oriented way to put it:

- If you just want the model to call a few tools, `LangChain Agent` is enough.
- If you already know exactly how each step of the business process should proceed and want strong control over each node, prefer `LangGraph`.
- If the task is highly open-ended, the steps are not fixed, and the agent needs to decompose tasks, call tools, and assign subtasks on its own, then `DeepAgents` is appropriate.

What this project ultimately aims to build is a "deep search" application: the user provides an open-ended question, and the system needs to search for materials, read information, reflect on gaps, continue supplementing, and finally generate a report. This type of task is very difficult to fully hard-code step by step in advance, making it an ideal hands-on project for DeepAgents.

![Comparison of LangChain, LangGraph, and Deep Agents capabilities across the Framework, Runtime, and Harness layers](../../../%E5%AE%9E%E6%88%98%E9%A1%B9%E7%9B%AE-%E6%B7%B1%E5%BA%A6%E7%A0%94%E6%90%9C/images/1/1-3-2-1.jpg)

These three layers can be understood from left to right:

- The `Framework` layer focuses more on foundational abstraction and integration, with an emphasis on helping developers connect to models, tools, and Agents faster;
- The `Runtime` layer focuses more on stable execution, with an emphasis on persistence, streaming output, human-computer interaction, and state management;
- The `Harness` layer focuses more on organizing complex tasks, with an emphasis on predefined tools, prompts, sub-agents, and stronger autonomy.

In the context of this project, it can be understood as follows:

- `LangChain` is more like a "foundational component library," providing basic capabilities such as models, tools, prompts, and Agents;
- `LangGraph` is more like a "process runtime," responsible for organizing multi-step tasks into stateful, recoverable, and stream-observable execution processes;
- `DeepAgents` is more like a "task organization suite," further providing planning, file system, sub-agent, and long-term memory capabilities on top of the previous two.

This is also why DeepAgents appears at a higher layer: what it addresses is not "how to call a model once," but "how to enable an agent system to continuously advance complex tasks." If LangChain helps us connect tools together, and LangGraph helps us manage processes, then DeepAgents focuses more on enabling agents to learn to "break down tasks, manage materials, dispatch sub-tasks, and aggregate results" on their own.

---

## 4. DeepAgents Core Capabilities

### 4.1 Task Planning and Task Decomposition

The most feared thing with complex tasks is jumping straight into execution.

For example, if a user asks: "Please help me research the recent development of the robotics industry and write a report," an ordinary model might immediately start writing content, but that content is likely just pieced together by intuition, without clear data sources, analytical structure, or supplementary mechanisms.

The approach DeepAgents recommends is: plan first, then execute.

Internally, it provides to-do list capabilities similar to `write_todos`, `read_todos`, and `update_todos`, allowing the agent to break down complex tasks into multiple steps. For example:

```text
1. 明确研究主题和范围
2. 搜索近期机器人产业新闻
3. 筛选高价值信息来源
4. 总结产业趋势
5. 补充典型企业和案例
6. 生成最终研究报告
```

The benefit of this approach is that the agent is no longer just "writing wherever its thoughts take it," but instead has a task plan that can be updated, tracked, and checked.

### 4.2 Context Management and File System

The context window of a large language model is limited. The more content tools return, and the longer the message history grows, the more easily the model gets distracted by irrelevant information.

DeepAgents has built-in file system capabilities, such as:

- `ls`: view the current files;
- `read_file`: read file contents;
- `write_file`: write files;
- `edit_file`: modify files.

This set of capabilities is not meant to let the agent arbitrarily manipulate local files, but to give the agent an external workspace. It can write long materials, staged notes, and intermediate reports to files, keeping only the most essential information needed at the moment in the main context.

It can be understood as follows: the model's context holds only what it is currently thinking about, while the file system is responsible for storing large amounts of intermediate material.

### 4.3 Sub-agents and Context Isolation

No matter how capable a single agent is, it is still constrained by context, tool permissions, and specialized prompts.

The core idea of multi-agent systems is "divide and conquer":

- The main agent is responsible for understanding user goals, breaking down tasks, scheduling resources, and aggregating results;
- Sub-agents are responsible for specific types of professional tasks, such as searching, database queries, code review, and report writing;
- Each sub-agent has its own system prompt, tool set, and execution context.

![Diagram showing how DeepAgents sub-agents achieve context isolation through the task tool](../../../%E5%AE%9E%E6%88%98%E9%A1%B9%E7%9B%AE-%E6%B7%B1%E5%BA%A6%E7%A0%94%E6%90%9C/images/1/1-4-3-1.png)

The most critical point in this diagram is that the main agent does not directly swallow all context, but instead delegates work through the `task` tool. Sub-agents complete the detailed work such as searching, coding, and general tasks in isolated contexts, and finally return only summarized results to the main agent.

This approach can significantly alleviate context bloat. Especially when tool outputs are very large, such as web search, file reading, or database queries, if everything is dumped into the main agent, it will quickly be overwhelmed by intermediate processes. The significance of the sub-agent mechanism is to let detailed work happen in local contexts, allowing the main agent to maintain a global perspective.

### 4.4 Long-term Memory

A common problem with ordinary agents is that once the current session ends, they no longer remember what they did before.

But many enterprise-level tasks are not one-off Q&A; they are continuously advancing. For example:

- Long-term follow-up on a specific customer requirement;
- Iterating on the same research report multiple times;
- Continuously maintaining a project document;
- Reusing previously accumulated experience across different sessions.

DeepAgents can leverage capabilities such as LangGraph's Store to save key memories to external storage, allowing the agent to read historical information across sessions.

In this chapter, it is enough to understand the value of long-term memory: **making the agent not just an assistant in the current session, but a task partner that can continuously accumulate context.**

Specific topics such as backend storage, file system backends, StoreBackend, and StateBackend will be covered in later advanced chapters.

### 4.5 Summary of the Four Core Capabilities

To consolidate the content above, DeepAgents' four most core categories of capabilities are:

| Core Capability           | What problem it solves                                       | How to understand it                             |
| ------------------ | -------------------------------------------------- | ---------------------------------------- |
| Intelligent planning and task decomposition | Complex tasks where it is unclear where to start or which steps count as complete       | Break down tasks first, then execute, then update progress             |
| Efficient context management     | Search results, file contents, and tool return values are too large and can easily overflow the context | Write large blocks of information to the file system and read them back when needed   |
| Sub-agent mechanism       | The main agent has to both plan and do the work, diluting both professionalism and context | The main agent handles scheduling, while sub-agents handle specialized sub-tasks |
| Long-term memory           | Memory loss between multi-turn sessions, making historical experience impossible to reuse             | Save key memories so that subsequent sessions can continue to read them   |

This chapter only establishes concepts. The next chapter will actually cover tool invocation, non-streaming execution, and streaming parsing, and will initially identify `task` sub-agent calls in streaming output. As for how sub-agents are configured, when to split them, and how to run them asynchronously and concurrently, that will be systematically covered in Chapter 3. File systems, long-term memory, backend storage, and other capabilities will be discussed in subsequent chapters.

---

## 5. Multi-Agent Design Boundaries

### 5.1 Sub-agent Definition

Many people first encountering "sub-agents" tend to think of them as simply "writing a few more role prompts." For example:

```text
你是搜索专家。
你是分析专家。
你是写作专家。
```

That is only a small part of the story. A true sub-agent is not just a role name, but a small assistant that can be invoked by the main agent.

Let us first understand this with an everyday example:

If you are renovating a house, you would not do the design, plumbing, electrical work, carpentry, and inspection all by yourself. A more reasonable approach is:

- You are responsible for determining the overall goal and budget;
- The designer is responsible for producing the design plan;
- The plumber and electrician are responsible for the plumbing and electrical lines;
- The carpenter is responsible for cabinets and ceilings;
- Finally, you integrate and inspect the results from each part.

In DeepAgents, the situation is similar:

- The **main agent** is responsible for understanding user goals, breaking down tasks, deciding who to hand them to, and finally integrating the results;
- The **sub-agent** is responsible for completing a specific type of more concrete task, such as searching, analysis, writing, or review.

Therefore, a sub-agent can be simply understood as: **a professional assistant hired by the main agent.**

Its execution chain looks roughly like this:

```text
用户目标
  -> 主智能体判断任务太复杂，需要分工
  -> 主智能体通过 task 工具把一部分任务交给子智能体
  -> 子智能体独立完成这部分任务
  -> 子智能体把结果返回给主智能体
  -> 主智能体整合所有结果，回复用户
```

The most important point here is not that "the number of Agents has increased," but that **the division of labor has become clearer.**

Without a clear division of labor, a multi-agent system can easily devolve into multiple models chatting with each other, with more calls but not necessarily better results.

### 5.2 The Relationship Between the Main Agent and Sub-agents

DeepAgents is better understood in terms of a "master-slave relationship":

```text
主智能体：项目负责人
  ├─ 搜索子智能体：负责查资料
  ├─ 分析子智能体：负责提炼观点
  ├─ 写作子智能体：负责组织报告
  └─ 审核子智能体：负责检查遗漏和错误
```

The main agent does not necessarily handle every detail personally; it is more like a project lead, focusing on:

1. Understanding the user's goal;
2. Determining which parts the task should be split into;
3. Deciding which parts to handle itself and which to delegate to sub-agents;
4. Receiving the results returned by sub-agents;
5. Organizing the results into a final answer.

Sub-agents, on the other hand, are more like people in specific roles, focusing only on their own piece of responsibility.

For example, in the "Deep Research" project, a user question might be: `请调研最近半年人形机器人行业的发展情况，并写一份带来源的分析报告。`

This task cannot be answered well in a single sentence. It may require:

- First checking news and policies;
- Then checking enterprise and product developments;
- Then organizing trends and risks;
- Finally writing a report.

In this case, it is appropriate to let the main agent coordinate, while different sub-agents handle the local tasks separately.

### 5.3 Core Value of Sub-agents

Sub-agents are not meant to make the system "look advanced"; they primarily solve three practical problems.

**First, context isolation: preventing the main agent from being overwhelmed by large amounts of intermediate information.**

In deep search tasks, what really takes up space is often not the final answer, but the intermediate process:

- The many webpage contents returned by search tools;
- Large amounts of material returned by file reading;
- Table results returned by database queries;
- Process records generated by multiple rounds of supplementary searches and repeated comparisons.

If all of this content is dumped into the main agent, the main agent can easily be led astray by the details and forget the original goal.

The benefit of sub-agents is that: **the detailed work is completed within the sub-agent, and the main agent only receives the consolidated conclusions.**

**Second, capability specialization: assigning different tasks to more suitable assistants.**

Different tasks require different capabilities. For example, the Deep Research project can divide work like this:

| Sub-agent | Responsibility                 | What it returns                 |
| -------- | ------------------------ | ------------------------ |
| Search assistant | Search webpages, news, reports, papers | Sources, summaries, key information     |
| Analysis assistant | Extract insights from materials         | Conclusions, evidence, risk points       |
| Writing assistant | Organize content into a report         | Well-structured, fluent body text |
| Review assistant | Check for omissions, conflicts, and uncertainties | Revision suggestions, risk alerts       |

This makes each assistant's tasks clearer, and prompts do not need to be written overly long and complex.

**Third, task parallelism: multiple directions can advance simultaneously.**

If a research task can be split into three directions such as "policy, market, and technology," and they are independent of each other, the main agent can assign them to three sub-agents separately.

This may reduce overall time. However, it is important to note that parallelism is not free. The more sub-agents there are, the more model calls, costs, and debugging difficulty increase.

### 5.4 Boundaries for Using Sub-agents

Multi-agent is not the default option. To decide whether to use it, first ask:

> Is this task really complex enough to require division of labor?

First look at the suitable use cases. Generally speaking, multi-agent is worth considering only when any of the following conditions are met:

| Criterion       | Description                                               | Example                                  |
| -------------- | -------------------------------------------------- | ------------------------------------- |
| Extremely open-ended problem   | The task has no fixed route and requires exploration, trial and error, and dynamic adjustment         | Industry research, strategic analysis, open-ended investigation        |
| Domain conflicts exist   | The task involves multiple specialized fields that can easily interfere with each other if placed in one context | Law + medicine, finance + engineering, code + product |
| Requires multi-directional parallelism | The task can naturally be split into multiple independent directions to advance in parallel               | Multi-source search, multi-scheme design, multi-file analysis      |

Conversely, if the task is very simple, there is no need for multi-agent.

For example:

- "What is the temperature in Beijing today?" Just calling the weather tool is enough;
- "Translate this sentence into English" can be done by a single ordinary Agent;
- "Summarize this short article" usually does not require splitting into multiple sub-agents.

But if the task is:

```text
从新闻、报告、论文、企业公告中调研某个行业，
并生成一份带引用来源、趋势判断和风险分析的深度报告。
```

This type of task is more suitable for multi-agent systems, because it requires multiple sources of information, multi-step processing, and final consolidation.

Now let's look at situations where multi-agent systems are not appropriate. More sub-agents are not always better; the following scenarios are actually not recommended for decomposition:

| Unsuitable scenario | Why it's unsuitable | Better approach |
| -------------------- | ------------------------------ | ------------------------ |
| Small tasks that can be completed in one step | Delegation itself also costs time and money | Answer directly or call a tool directly |
| Short tasks that require continuous reading | Decomposition tends to lose context | Let the same agent complete it in one pass |
| Sub-tasks are not clearly defined | The sub-agent doesn't know what to return | First clarify the task description and output format |
| Just to "look advanced" | Increases cost, logs, and failure points | First get it working with a single agent |
| Tool permissions are difficult to control | The sub-agent may call tools it shouldn't | Clarify the tool whitelist and approval rules |

A very practical rule of thumb is:

> First get the workflow running with a single agent, then observe where it repeatedly becomes longer, messier, or more specialized, and finally decompose that part into a sub-agent.

Don't design many sub-agents from the start. When you're a beginner, mastering the main path is more important than piling on complex architecture.

### 5.5 Delegation Mechanism in DeepAgents

In DeepAgents, when the main agent wants to call a sub-agent, it typically uses a special tool: `task`. You can think of `task` as the action of "assigning work."

For this chapter, you only need to understand: **When you see `task`, it usually means the main agent is delegating part of the task to a sub-agent.**

As for what the parameters of `task` look like, how to identify it in `stream()` output, and what the difference is between a regular tool call and a sub-agent call, these will be covered in Chapters 2 and 3 with code. The sub-agent's `name`, `description`, `system_prompt`, `tools` and other configuration fields will also be formally expanded in Chapter 3.

### 5.6 Drawbacks of Multi-Agent Systems

Multi-agent systems can solve complex problems, but they also come with costs.

**First, the number of calls and costs will increase.**

Each sub-agent may call the model independently. The more sub-agents there are, the more tokens and costs are typically consumed. So don't decompose everything just because "multi-agent sounds more advanced." Simple tasks are actually faster and cheaper if the main agent handles them directly.

**Second, troubleshooting becomes more difficult.**

When a single agent fails, you usually only need to look at one execution path.

When a multi-agent system fails, you need to trace:

- Why the main agent chose this sub-agent;
- What task the sub-agent received;
- Which tools the sub-agent called;
- What the sub-agent returned;
- How the main agent integrated these results.

Therefore, when writing code later, we will pay special attention to `stream()` output and logs. They are not decorative; they are important clues for troubleshooting.

### 5.7 Two Types of Multi-Agent Architectures

There are two common ways to organize multi-agent systems. This section is just for understanding; no need to memorize concepts.

**First: Hierarchical pattern, also known as the orchestrator pattern.**

The core logic of the hierarchical pattern (Orchestrator-Workers) is: **one main agent handles orchestration, and multiple sub-agents handle execution.**

You can think of it as a project lead working with multiple specialized assistants. The main agent first understands the user's goal, then decomposes the task, selects the appropriate sub-agents, collects the sub-agent results, and finally consolidates everything into the final output. Sub-agents don't need to worry about the overall goal; they just need to do their assigned local tasks well.

![Diagram of hierarchical workflow Orchestrator-Workers where the main orchestrator decomposes tasks and consolidates outputs](../../../%E5%AE%9E%E6%88%98%E9%A1%B9%E7%9B%AE-%E6%B7%B1%E5%BA%A6%E7%A0%94%E6%90%9C/images/1/1-5-7-1.png)

Its typical flow is:

1. The user inputs a complex task;
2. The main agent understands the goal and decomposes it into multiple sub-tasks;
3. The main agent assigns sub-tasks to different specialized sub-agents;
4. Sub-agents complete their local tasks within their own contexts;
5. Sub-agents return results to the main agent;
6. The main agent consolidates, evaluates, and organizes the results into the final output.

The advantage of this pattern is that the routing is clear and responsibilities are well-defined, making it more suitable for engineering project implementation. When problems occur, it is also easier to trace: whether the main agent decomposed the task incorrectly, whether a sub-agent executed the task incorrectly, or whether the problem arose during final consolidation.

Its disadvantage is also obvious: the main agent is extremely critical. If the main agent misunderstands the goal from the start, or assigns the wrong sub-tasks, the subsequent execution will go off track. Additionally, all tasks must be orchestrated through the main agent, so when tasks are extremely complex, the main agent can become a bottleneck.

DeepAgents leans toward this pattern. It emphasizes: **the main agent handles planning and orchestration, and sub-agents handle specialized execution.**

**Second: Collaborative pattern, also known as the mesh pattern.**

The core logic of the collaborative pattern (Collaborative Network) is: **multiple agents share information, complement each other, and advance together around the same problem.**

It is more like several experts in a meeting. Each agent can express opinions based on its own role and context, and can also supplement, question, or correct based on other agents' output. There may not necessarily be an absolute "leader"; the system relies more on interaction between agents to gradually converge on a result.

![Diagram of collaborative workflow Collaborative Network showing iterative feedback between generator and evaluator](../../../%E5%AE%9E%E6%88%98%E9%A1%B9%E7%9B%AE-%E6%B7%B1%E5%BA%A6%E7%A0%94%E6%90%9C/images/1/1-5-7-2.png)

The advantage of this approach is flexibility, making it suitable for open-ended exploration, proposal discussion, and viewpoint clash. For example, when multiple experts evaluate a business proposal together or discuss a technical direction, the collaborative pattern may generate more perspectives.

Its disadvantage is that it is more prone to losing control. Multiple agents may keep supplementing, rebutting, and supplementing again, ultimately discussing for a long time without a clear conclusion. Debugging is also more troublesome because it is hard to quickly determine which agent's judgment ultimately had the greatest influence on the final answer.

In the first phase of this course, we will first learn DeepAgents' hierarchical pattern: **the main agent handles orchestration, and sub-agents handle execution.**

### 5.8 Differences from Other Multi-Agent Frameworks

With the two architectures above in mind, looking at different multi-agent frameworks is no longer just about remembering names, but about seeing which "organizational approach" they lean toward.

**DeepAgents** is more like the hierarchical/orchestrator pattern: the main agent first plans, then dispatches tasks to sub-agents, and finally consolidates the results.

**AutoGen** is more like a decentralized/mesh collaborative pattern: multiple agents discuss problems as if in a group chat, freely picking up threads and complementing each other based on context.

**CrewAI** is more like role- and task-flow-driven team collaboration: developers typically define roles, tasks, and workflows first, then let different agents fulfill their responsibilities according to the setup. It can do hierarchical workflows or more flexible role-based collaboration.

| Framework | What it's more like | Primary organizational approach | How agents collaborate | More suitable tasks | Main risks |
| ---------- | -------------------------- | --------------- | ---------------------------------------------------------- | -------------------------------------------- | ---------------------------------------------- |
| DeepAgents | A project lead with multiple specialized assistants | Hierarchical orchestration | The main agent dispatches tasks through mechanisms like `task`, and sub-agents return results after completion | Deep research, long tasks, report generation, multi-step information organization | The main agent's judgment quality is critical; wrong task decomposition affects subsequent results |
| AutoGen | Multiple experts discussing in a group | Mesh collaboration | Multiple agents converse freely around context, complementing and correcting each other | Brainstorming, proposal discussion, open-ended exploration, complex problem solving | Prone to divergence; hard to trace where key judgments came from during debugging |
| CrewAI | A pre-defined team collaborating according to task workflows | Roles + task workflows | Define roles, goals, and tasks first, then let agents collaborate according to the workflow | Standard business processes, multi-role execution, clear team division of labor | Results depend on role and task design; poor workflow design leads to rigidity |

In short, the biggest difference among the three is not "which one is more advanced," but rather the way tasks are organized:

- If you want a main agent to handle global orchestration while other sub-agents complete local tasks, DeepAgents is more suitable;
- If you want multiple agents to discuss freely and inspire each other, AutoGen is more suitable;
- If you want to design team roles and task workflows in advance, CrewAI is more suitable.

This course focuses on DeepAgents. The reason is simple: its main path is clearer, making it more suitable for building engineering-oriented thinking first:

- Who is responsible for orchestration;
- Who is responsible for execution;
- Who stores intermediate information;
- Who outputs the final result.

This also fits the "Deep Research" project very well. After a user asks an open-ended question, the system needs to plan first, then search, then analyze, then supplement, and then generate a report. Such tasks are naturally suited to the hierarchical pattern: the main agent controls the big picture, while sub-agents respectively handle local work such as searching, reading, analyzing, and writing.

### 5.9 Sub-Agent Design Checklist

When actually configuring sub-agents later, you can use the following checklist:

| Check item | Ask yourself |
| ------------ | ------------------------------------------------- |
| Is the responsibility single? | Is it only responsible for one clear category of tasks? |
| Is the description clear? | After the main agent reads `description`, does it know when to call it? |
| Are the tools minimal enough? | Does it only have the tools it must use? |
| Is the output usable? | Does it return conclusions, or a pile of unprocessed process information? |
| Is the cost justified? | Is this task really worth one extra agent call? |
| Are the logs traceable? | When something goes wrong, can you see what task it received and what it did? |

If a sub-agent cannot clearly specify: when to call it; what the input should be; what the output should be; what it cannot do. Then it is not yet a good sub-agent—it is just a name that sounds impressive.

---

**Chapter Summary:**

In this chapter, we started from the project background and understood why DeepAgents appeared after ordinary agents. Regular LLMs mainly solve "answering questions," tool-using agents further solve "calling tools," while DeepAgents focuses more on "how complex tasks are planned, divided, executed, and continuously advanced."

Next, we distinguished the positioning of `LangChain`, `LangGraph`, and `DeepAgents`:

- `LangChain` leans more toward foundational abstraction;
- `LangGraph` leans more toward deterministic workflow orchestration;
- `DeepAgents` leans more toward autonomous planning and multi-agent organization.

Then, we sorted out DeepAgents' four core capabilities: task planning, context management, sub-agents, and long-term memory. Together they serve one goal: enabling agents to handle longer, more complex, and more open-ended tasks.

Finally, we focused on building the cognitive foundation for sub-agents: sub-agents are not just about writing a few more role prompts, but rather independent execution units delegated by the main agent through the `task` tool. Their core value lies in context isolation, capability specialization, and controllable parallelism. At the same time, we established an important engineering judgment: more multi-agents are not always better. Only when tasks are sufficiently open-ended, involve domain conflicts, or naturally require multi-directional parallelism is it worth bearing the cost and debugging complexity that multi-agent systems bring.

This chapter lays the cognitive foundation. The next chapter will formally enter the code level, creating the first DeepAgent and learning how to parse the execution results of `invoke()` and `stream()`; Chapter 3 will then specifically expand on sub-agent configuration, orchestration, and asynchronous execution.
