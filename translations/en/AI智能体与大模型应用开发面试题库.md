# AI Agent and Large Language Model Application Development Interview Question Bank

> Positioning: For **AI Agent / Large Language Model Application Development Engineers**, **AI Application Development Engineers**, and **Agent Development Engineers**.
> Style: Leaning toward **application implementation, architecture design, engineering governance, and real-world projects**, not pure algorithm research or pre-training details.

Document Features:

- Each question is marked with **importance** and **difficulty**, making it easier to distinguish must-review content, frequently tested content, and advanced content.
- **Corresponding chapters** are added below each question wherever possible, making it convenient to revisit knowledge points and practice while learning.
- A considerable number of questions come from **real interview experiences at major companies** and actual high-frequency follow-up questioning scenarios, bringing them closer to real interviews.
- The overall expression remains **professional yet accessible**, avoiding empty talk, clichés, and pure concept-stacking.
- Each second-level heading is categorized by topic, with a clear structure that facilitates systematic review by module.

Importance Marking Guide:

- `必刷`: Highly likely to be asked; failing to answer well directly exposes weaknesses.
- `高频`: Very common in interviews, usually a main question or a high-frequency follow-up.
- `中频`: Leans more toward engineering design, deep project exploration, and implementation details.
- `低频`: Bonus questions, extended questions, and role-specific deep-dive questions.

Difficulty Marking Guide:

- `基础`: Leans toward core concepts and standard answers, suitable for establishing a foundation in the first round.
- `中等`: Requires combining engineering understanding, layered explanations, or some project experience.
- `较难`: Leans more toward system design, complex governance, protocol details, or advanced architectural trade-offs.

## 1. Fundamentals and Technology Selection

### Q1-1. What is the core difference between RAG and Fine-tuning (SFT)? Can they be used together?

RAG addresses "where the knowledge comes from," while fine-tuning addresses "how the model should behave."

RAG does not modify model parameters; instead, it retrieves relevant materials at runtime and then hands them to the model to generate an answer. Therefore, it is better suited for knowledge that is highly time-sensitive, frequently updated, and needs to be traceable. Fine-tuning changes model parameters and is better suited for improving consistency of output style, structured output capability, classification ability, or stability of domain-specific behavior.

They can certainly be used together, and many enterprise projects are implemented this way: use RAG to supply knowledge, and use fine-tuning or strongly constrained output to improve behavioral stability. For example, in a customer service project, product policies are kept up to date through RAG, while reply format and field output are kept stable through fine-tuning or structured output.

**Common Follow-up Questions:**

- Why do most enterprise projects not prioritize continued pre-training?
- In what scenarios is the `RAG + 微调` combination suitable?
- If budget is limited, which one should be done first?

**Importance:** `必刷` (Occurrences: 3) | **Difficulty:** `中等`

**Assessment Focus:** Ability to distinguish knowledge enhancement from behavior optimization.

**Corresponding Chapters:** [1-3 RAG, Fine-tuning, Continued Pre-training, and Agent Selection §1. RAG](1-3-RAG%E3%80%81%E5%BE%AE%E8%B0%83%E3%80%81%E7%BB%AD%E8%AE%AD%E4%B8%8E%E6%99%BA%E8%83%BD%E4%BD%93%E9%80%89%E5%9E%8B.md#_1、rag); [1-3 RAG, Fine-tuning, Continued Pre-training, and Agent Selection §2. Fine-tuning](1-3-RAG%E3%80%81%E5%BE%AE%E8%B0%83%E3%80%81%E7%BB%AD%E8%AE%AD%E4%B8%8E%E6%99%BA%E8%83%BD%E4%BD%93%E9%80%89%E5%9E%8B.md#_2、微调%EF%BC%88fine-tuning%EF%BC%89)

### Q1-2. What is an AI Agent? What is the difference between it and a traditional AI application?

It can be summarized as: **Agent = Model + Toolset + Execution Loop + Current State**.

- The model is responsible for understanding the goal and deciding the next step.
- The toolset is responsible for providing external capabilities.
- The execution loop is responsible for making the system not just answer once, but be able to "think one step, do one step, observe the result, and then decide the next step."
- The current state is responsible for storing messages, tool results, and intermediate conclusions.

Traditional AI applications are closer to a single-turn system where "you input a request and get back a result." An Agent is closer to an operating mode of "continuously making decisions around a goal." Its key feature is not just using a large language model, but having tool invocation, state progression, and dynamic decision-making capabilities.

Therefore, not all AI applications should be called Agents. Fixed form generation, fixed knowledge Q&A, and fixed process approval are systems that often only need ordinary pipelines or a Workflow. Only when the path is not fixed and you need to continue selecting tools or adjusting the route based on intermediate results is an Agent truly appropriate.

Also note that many people treat "long-term memory, complex planning, and multi-agent collaboration" as mandatory requirements for an Agent. That is not true. For many entry-level scenarios, being able to "understand the goal, decide whether to invoke a tool, obtain the result, and continue making judgments" already constitutes an Agent.

**Importance:** `高频` (Occurrences: 2) | **Difficulty:** `基础`

**Assessment Focus:** Whether you understand the essence of an Agent and will not call any chatbot an Agent.

**Corresponding Chapters:** [21 Agent §1. Introduction to Agent](21-Agent%E6%99%BA%E8%83%BD%E4%BD%93.md#_1-introduction-to-agents); [1-3 RAG, Fine-tuning, Continued Pre-training, and Agent Selection §4. Agent Development](1-3-RAG%E3%80%81%E5%BE%AE%E8%B0%83%E3%80%81%E7%BB%AD%E8%AE%AD%E4%B8%8E%E6%99%BA%E8%83%BD%E4%BD%93%E9%80%89%E5%9E%8B.md#_4、智能体开发)

### Q1-3. When should you use Prompt, RAG, Fine-tuning, Workflow, or Agent?

The most reliable way to judge is to first determine whether the problem is fundamentally **a lack of knowledge, a lack of behavior, or a lack of process capability**.

- If the model already knows how but the task is simply not described clearly, start with Prompt.
- If what is missing is private knowledge, the latest knowledge, or external knowledge, prioritize RAG.
- If what is missing is stable behavior, such as a fixed format, fixed tone, or fixed classification habits, then consider fine-tuning.
- If the process is fixed, the nodes are clear, and stability and auditability are emphasized, prioritize Workflow.
- If the path is not fixed and you need to decide the next step while working and dynamically invoke tools, then consider an Agent.

This main line of technology selection can be compressed into one sentence:

- **Prompt** solves the problem of task expression.
- **RAG** solves the problem of knowledge sources.
- **Fine-tuning** solves the problem of behavioral stability.
- **Workflow** solves the problem of fixed processes.
- **Agent** solves the problem of dynamic decision-making.

In real projects, you usually would not say "we must build an Agent" from the start. Most requirements can be covered with `Prompt + RAG + Workflow` first. Only when the task openness is high, tool selection depends on intermediate results, and the process cannot be predetermined, does the value of an Agent truly emerge.

**Common Follow-up Questions:**

- Why do many projects not start with fine-tuning right away?
- Why are not all complex tasks suitable for an Agent?
- What is the dividing line between Workflow and Agent?

**Importance:** `必刷` (Occurrences: 1) | **Difficulty:** `中等`

**Assessment Focus:** Technology selection ability, boundary awareness, and whether you have engineering judgment.

**Corresponding Chapters:** [1-3 RAG, Fine-tuning, Continued Pre-training, and Agent Selection §1. RAG](1-3-RAG%E3%80%81%E5%BE%AE%E8%B0%83%E3%80%81%E7%BB%AD%E8%AE%AD%E4%B8%8E%E6%99%BA%E8%83%BD%E4%BD%93%E9%80%89%E5%9E%8B.md#_1、rag); [1-3 RAG, Fine-tuning, Continued Pre-training, and Agent Selection §4. Agent Development](1-3-RAG%E3%80%81%E5%BE%AE%E8%B0%83%E3%80%81%E7%BB%AD%E8%AE%AD%E4%B8%8E%E6%99%BA%E8%83%BD%E4%BD%93%E9%80%89%E5%9E%8B.md#_4、智能体开发)

### Q1-4. What are Tokens and the Context Window? What do they mean in engineering terms?

A Token can be seen as the basic unit of measurement for text processed by a model, and it is not equal to "character count" or "word count." What the model sees during training and inference is not raw text, but a sequence of tokens produced by the tokenizer.

The context window is the upper limit on how many tokens the model can see in a single inference pass. In engineering terms, `8K`, `32K`, and `128K` essentially all refer to "the maximum total number of tokens that can fit into this request, including the system prompt, conversation history, retrieved results, and user question."

Its engineering implications are very direct:

- The context window determines whether you can handle long-form Q&A, multi-turn conversations, and large-scale RAG context concatenation.
- The more tokens there are, the higher the cost usually is, and latency is also more likely to rise.
- Content beyond the window will be truncated, compressed, or may never even reach the model, so "cramming in as much as possible" is not necessarily better.

As a rough reference, `128K token` can be thought of as a very long piece of content. According to common empirical figures, 1 Chinese character is approximately `0.6` tokens, and 1 English character is approximately `0.3` tokens, so `128K token` can roughly be approximated to a scale of hundreds of thousands of Chinese characters. But this is only an estimate. The actual figures will vary depending on the tokenizer, language type, code, punctuation, and format.

**Common Follow-up Questions:**

- Roughly how many tokens are 1 Chinese character and 1 English word, and why should you not memorize a single fixed value?
- If the context is truncated, what would you prioritize handling first?

**Importance:** `高频` (Occurrences: 1) | **Difficulty:** `基础`

**Assessment Focus:** Whether you truly understand the relationship between tokens, context windows, and cost/truncation/long-text scenarios.

**Corresponding Chapters:** [1-1 Large Language Model Fundamentals and Engineering Overview §1. Understanding Large Language Models](1-1-%E5%A4%A7%E6%A8%A1%E5%9E%8B%E8%AE%A4%E7%9F%A5%E4%B8%8E%E5%B7%A5%E7%A8%8B%E6%A6%82%E8%A7%88.md#_1-getting-to-know-llms); [11 Model I/O and Model Integration §2. LangChain Model Categories, Parameters, and Returns](11-Model-I-O%E4%B8%8E%E6%A8%A1%E5%9E%8B%E6%8E%A5%E5%85%A5.md#_2-langchain-model-categories-parameters-and-returns)

**Source:** Tencent AI Backend Engineer First Round (Actual major company interview question)

### Q1-5. Which engineering metrics do you care about most before launching a large language model application?

Usually, I look at five dimensions: effectiveness, performance, cost, stability, and governance.

- Effectiveness: accuracy, faithfulness, task completion rate, citation correctness.
- Performance: time to first token, end-to-end latency, P95/P99.
- Cost: token consumption, retrieval cost, tool invocation cost.
- Stability: timeout rate, error rate, retry rate, fallback hit rate.
- Governance: logging, tracing, prompt versioning, index versioning, permission auditing.

If it is a RAG/Agent project, I would additionally look at retrieval recall quality, tool invocation success rate, manual fallback ratio, and badcase feedback efficiency, because these are the key metrics that truly affect the online experience.

**Common Follow-up Questions:**

- How do you design a fallback strategy?
- If costs exceed the budget, which layer would you optimize first?
- How do you roll back prompts/models/indexes?

**Importance:** `高频` (Occurrences: 1) | **Difficulty:** `中等`

**Assessment Focus:** Whether you have production environment awareness.

**Corresponding Chapters:** [1-1 Large Language Model Fundamentals and Engineering Overview §4. Engineering Implementation of Large Language Models (Overview)](1-1-%E5%A4%A7%E6%A8%A1%E5%9E%8B%E8%AE%A4%E7%9F%A5%E4%B8%8E%E5%B7%A5%E7%A8%8B%E6%A6%82%E8%A7%88.md#_4、大模型的工程实现%EF%BC%88概览%EF%BC%89); [7 Enterprise-level Large Language Model Deployment §1. Overview of Enterprise-level Large Language Model Deployment](7-%E4%BC%81%E4%B8%9A%E7%BA%A7%E5%A4%A7%E6%A8%A1%E5%9E%8B%E9%83%A8%E7%BD%B2.md#_1-overview-of-enterprise-level-large-model-deployment)

---

## 2. Prompt, Structured Output, and Guardrails

### Q2-1. How should System Message and User Message be divided?

System Message is responsible for holding stable constraints, while User Message is responsible for holding dynamic tasks.

System typically contains the role, objectives, boundaries, safety rules, output format requirements, and tool usage specifications. These contents should remain as stable as possible and be changed infrequently. User Message contains the user's current task, input data, supplementary context, and personalized requirements.

The benefit of this separation is a clearer structure, easier version management, and better suitability for subsequent templating, canary releases, and evaluation. If all content is mixed into a single prompt, troubleshooting performance fluctuations later will be very difficult.

**Importance:** `必刷` (Occurrences: 1) | **Difficulty:** `基础`

**Assessment Focus:** Prompt layered design capability.

**Corresponding Chapters:** [13 Prompts and Message Templates §3. Input Message Types](13-%E6%8F%90%E7%A4%BA%E8%AF%8D%E4%B8%8E%E6%B6%88%E6%81%AF%E6%A8%A1%E6%9D%BF.md#_3-message-types-for-input); [13 Prompts and Message Templates §7. Chat Prompt Templates](13-%E6%8F%90%E7%A4%BA%E8%AF%8D%E4%B8%8E%E6%B6%88%E6%81%AF%E6%A8%A1%E6%9D%BF.md#_7-chat-prompt-template-chatprompttemplate)

### Q2-2. What are the common approaches to structured output? What are their respective advantages and disadvantages?

From the perspective of Model I/O, structured output can broadly be divided into two categories: "post-processing parsing" and "pre-constrained structured output."

- Pure Prompt constraints: directly ask the model to return JSON. The advantage is that it is the simplest and fastest to get started; the disadvantage is that if the model says one extra word or misses a comma, the program is likely to crash, making it the least stable.
- Output Parser: for example `StrOutputParser`, `JsonOutputParser`, `PydanticOutputParser`. It is closer to "the model has already produced output, and I then convert the result into data usable by the program," making it suitable for the classic `prompt | model | parser` chain.
- Structured Output: for example `with_structured_output(TypedDict / Pydantic / JSON Schema)`. It is closer to "defining the schema before the model outputs," so that the model generates according to the structure and parses it automatically, providing stronger constraints.
- Function Calling / Tool Calling: essentially also a form of structured output, except that the goal is more focused on "generating call intent and parameters," which is especially suitable for tool invocation, external interface orchestration, and Agents.

If the model platform supports stricter structured output capabilities, the mode that only guarantees "returning valid JSON" is usually prioritized, because the former is closer to "generating according to schema," while the latter is often merely "looks like JSON."

To break it down further:

- `TypedDict` is suitable for scenarios where fields are fixed but strong runtime validation is not pursued.
- `Pydantic` is suitable for business scenarios with strict requirements on field types, ranges, and required fields.
- `JSON Schema` is more suitable for sharing structural protocols across languages and systems.

In engineering practice, "letting the model output JSON" is usually not treated as a true production solution. A more reliable order of preference is usually:

1. Prioritize native structured output whenever possible.
2. When strong validation is needed, prioritize schemas such as Pydantic.
3. Even when the model already produces structured output, still add business validation, default value handling, and failure retries.

Ultimately, a Prompt can only "try as much as possible to make it look like this." It is the Parser and Structured Output that truly help you connect the model's output into your program system.

**Importance:** `高频` (occurrences: 1) | **Difficulty:** `中等`

**Examination focus:** the engineering awareness of going from "able to output JSON" to "able to stably integrate with a system."

**Corresponding sections:** [14 Output Parsers §1, Introduction to Output Parsers](14-%E8%BE%93%E5%87%BA%E8%A7%A3%E6%9E%90%E5%99%A8.md#_1-introduction-to-output-parsers); [14 Output Parsers §4, Structured Output](14-%E8%BE%93%E5%87%BA%E8%A7%A3%E6%9E%90%E5%99%A8.md#_4-structured-output)

### Q2-3. What is Prompt Injection? Why should you be even more careful in RAG / Agent scenarios?

Prompt Injection is essentially: **untrusted input attempting to rewrite system instructions, induce the model to exceed its authority, or cause an Agent to perform actions it should not perform.**

It does not only come from direct user input; it can also be hidden in web pages, PDFs, knowledge base documents, emails, and even images. As long as such content can be read by the model, it can form an "indirect injection." Therefore, in systems that read external content, such as RAG, browser Agents, and code interpreters, the risk is clearly higher.

Protection is usually implemented at five layers:

- Instruction layering: put stable rules in System, and treat both User and external documents as untrusted input that cannot have the same authority as system constraints.
- Content isolation: treat retrieved fragments, web content, and user-uploaded documents only as "materials to be analyzed," and do not assume by default that they can issue new instructions.
- Tool permissions: route all write operations and dangerous operations through whitelists, schema validation, and least privilege, rather than giving the model raw capabilities.
- Action validation: perform rule-based validation on critical outputs, and confirmation, approval, or HITL on critical actions, so that a single piece of malicious text cannot directly trigger side effects.
- Observation and fallback: record injection samples, failure traces, and anomalous calls, and promptly add them to evaluation sets and interception rules.

There is one particularly critical point here: **RAG is not a security layer, and knowledge base documents themselves can also carry malicious instructions.** As long as "retrieved content" is directly treated as "trusted prompt text," the system is very dangerous.

**Common follow-up questions:**

- If a document says "ignore all previous instructions," how would you handle it?
- How does a browser Agent defend against hidden prompt text in web pages?
- Why cannot fine-tuning and alignment fundamentally solve Prompt Injection?

**Importance:** `高频` (occurrences: 1) | **Difficulty:** `中等`

**Examination focus:** application-layer security awareness, and understanding of direct injection, indirect injection, and tool privilege escalation risks.

**Corresponding sections:** [13 Prompts and Message Templates §1, Introduction to Prompts](13-%E6%8F%90%E7%A4%BA%E8%AF%8D%E4%B8%8E%E6%B6%88%E6%81%AF%E6%A8%A1%E6%9D%BF.md#_1-introduction-to-prompts); [17 Tools Tool Calling §6, From Course Examples to Real Projects](17-Tools%E5%B7%A5%E5%85%B7%E8%B0%83%E7%94%A8.md#_6-from-course-examples-to-real-projects)

### Q2-4. In Prompt Engineering, how do you systematically optimize prompts and improve accuracy?

Prompt optimization is usually not understood as "repeatedly hand-editing a few prompt sentences," but rather as a small engineering loop. If you really want to improve accuracy stably, the core is not esoteric techniques, but **task decomposition, example-driven iteration, evaluation regression, and boundary convergence**.

A relatively reliable approach usually involves:

- First define task boundaries: make clear what counts as a correct answer, what counts as a wrong answer, and which situations require refusal to answer or clarification.
- Layer the inputs: put stable rules in `System` and dynamic tasks in `User`; do not knead all constraints into one long prompt.
- Fix major problems before wording: if the root issue is a lack of knowledge, tools, or process, do not try to force the effect upward with Prompt alone.
- Use examples and counterexamples: few-shot examples, counterexample constraints, and output format examples are usually more stable than abstract requirements.
- Apply structured constraints: wherever schema, parser, or structured output can be used, do not just write "please return JSON."
- Build a badcase set: accumulate online error cases into a fixed evaluation set, and run regression every time the Prompt is changed, rather than relying on intuition to judge that it "seems more accurate."
- Manage versions and canary releases: manage Prompt, model version, temperature, and output format requirements together, to avoid changing one point and then being unable to trace the impact.

If expressed from a more practical interview perspective, one more point should be added: the so-called "accuracy > 95%" must be tied to a specific task, such as classification, extraction, format generation, or customer service Q&A; it is not a universal promised value. The real engineering goal should be for a specific task to stably meet the standard on a fixed evaluation set, rather than chasing a number detached from the scenario.

**Common follow-up questions:**

- If the Prompt cannot be improved no matter how you change it, how do you decide whether to switch to RAG, Tool, Workflow, or fine-tuning?
- How should a badcase set be built so that it can truly guide iteration?
- If online performance suddenly drops, how do you determine whether the problem is the Prompt, the model version, or the external knowledge / tool chain?

**Importance:** `高频` (occurrences: 1) | **Difficulty:** `中等`

**Examination focus:** Prompt optimization methodology, awareness of evaluation loops, and whether the candidate knows that Prompt is not a universal repair tool.

**Corresponding sections:** [1-2 Prompt Engineering Fundamentals §2, How to Write Prompts](1-2-%E6%8F%90%E7%A4%BA%E8%AF%8D%E5%B7%A5%E7%A8%8B%E5%9F%BA%E7%A1%80.md#_2-how-to-write-prompts); [14 Output Parsers §8, Practical Development Choices](14-%E8%BE%93%E5%87%BA%E8%A7%A3%E6%9E%90%E5%99%A8.md#_8-practical-development-choices)

### Q2-5. What are the boundaries of Prompt Engineering? Why can't everything be left to Prompt?

Prompt is closer to a "means of task expression and constraint," but it cannot solve knowledge gaps, complex state management, or strong execution requirements.

For example, when there is too much material, relying only on Prompt to stuff the context will lead to high costs, more noise, and loss of key information; at that point, you should switch to RAG. If a complex multi-step process is fully orchestrated by Prompt alone, it will become an unmaintainable long instruction and should be converted to Workflow or LangGraph. When you need stable invocation of external systems, you should use Tools / Function Calling rather than letting the model "pretend to call an interface" in text.

Therefore, a more reasonable engineering approach is: Prompt is responsible for expressing rules, RAG is responsible for supplementing knowledge, Tools are responsible for execution capability, and Graph / Workflow is responsible for process control.

**Importance:** `中频` (occurrences: 1) | **Difficulty:** `基础`

**Examination focus:** whether the candidate understands that Prompt is not a cure-all.

**Corresponding sections:** [1-2 Prompt Engineering Fundamentals §4, Boundaries of Prompt Engineering](1-2-%E6%8F%90%E7%A4%BA%E8%AF%8D%E5%B7%A5%E7%A8%8B%E5%9F%BA%E7%A1%80.md#_4、提示词工程的边界); [13 Prompts and Message Templates §1, Introduction to Prompts](13-%E6%8F%90%E7%A4%BA%E8%AF%8D%E4%B8%8E%E6%B6%88%E6%81%AF%E6%A8%A1%E6%9D%BF.md#_1-introduction-to-prompts)

### Q2-6. How do you perform Prompt version management and regression?

Once a Prompt has entered production, it can no longer be treated as a "string to be casually modified," but should be managed as a configuration asset or code asset.

Four things are usually managed together:

- The Prompt template itself: System and User templates, few-shot examples, and output format requirements.
- Runtime parameters: model name, model version, temperature, top_p, max_tokens.
- Evaluation set: fixed golden questions, typical badcases, and failure examples.
- Release information: template version number, release time, owner, canary scope, and rollback version.

A more reliable approach usually involves:

1. Version the Prompt together with the code, or manage it centrally in a configuration center.
2. Run a fixed regression set every time the Prompt is changed, rather than relying only on subjective feeling.
3. Record the template hash, model version, and key parameters, to avoid being unable to trace the cause when "the effect changed even though the Prompt was not changed."
4. Conduct canary releases and sampled manual review before going live, and retain the ability to quickly roll back for high-risk chains.

There is also a point that is very easy to overlook: **after switching the underlying model, the old Prompt may not necessarily maintain its original effect.** Therefore, in many cases the object of regression is not "whether this Prompt is correct," but "whether the combination of the Prompt and the current model is still stable."

**Common follow-up questions:**

- How should a golden set be constructed?
- If online performance fluctuates, how do you determine whether the problem is the Prompt or the model version?
- When Prompt, model, and index are changed together, how do you design a rollback strategy?

**Importance:** `中频` (occurrences: 1) | **Difficulty:** `中等`

**Examination focus:** Prompt engineering governance capability, rather than merely being able to hand-edit prompts.

**Corresponding sections:** [13 Prompts and Message Templates §8, Loading Prompts from Files](13-%E6%8F%90%E7%A4%BA%E8%AF%8D%E4%B8%8E%E6%B6%88%E6%81%AF%E6%A8%A1%E6%9D%BF.md#_8-loading-prompts-from-files); [1-2 Prompt Engineering Fundamentals §5, Several Points to Note in Prompt Engineering](1-2-%E6%8F%90%E7%A4%BA%E8%AF%8D%E5%B7%A5%E7%A8%8B%E5%9F%BA%E7%A1%80.md#_5、提示词工程的几个注意点)

---

## 3. Full RAG Pipeline

### Q3-1. Please describe a complete RAG pipeline.

A complete RAG pipeline generally consists of an **indexing stage** and a **retrieval stage**.

The indexing stage includes document loading, cleaning, chunking, vectorization, writing to the vector database, and supplementing metadata. The retrieval stage includes receiving the question, performing query rewriting when necessary, retrieval and recall, reranking and filtering, context assembly, handing it to the model to generate an answer, and finally handling citations, desensitization, and formatted output.

In engineering, the real difficulty usually does not lie in "connecting the model," but in three things: whether documents are parsed correctly, whether chunking preserves semantics, and whether the retrieved results are actually helpful for the current question. When online performance is poor, most of the time the bottleneck is also in these three layers, not in the final generation round.

**Common follow-up questions:**

- How should chunks be split?
- Which fields should metadata store?
- Why add rerank?

**Importance:** `必刷` (occurrences: 3) | **Difficulty:** `中等`

**Examination focus:** whether the candidate truly understands RAG, rather than merely being able to say "retrieval-augmented generation."

**Corresponding sections:** [19 RAG Retrieval-Augmented Generation §1. Introduction to RAG](19-RAG%E6%A3%80%E7%B4%A2%E5%A2%9E%E5%BC%BA%E7%94%9F%E6%88%90.md#_1-introduction-to-rag); [19 RAG Retrieval-Augmented Generation §2. Core Knowledge of RAG Text Processing](19-RAG%E6%A3%80%E7%B4%A2%E5%A2%9E%E5%BC%BA%E7%94%9F%E6%88%90.md#_2-core-knowledge-of-rag-text-processing)

### Q3-2. How should text chunking be designed? What are the common pitfalls?

The goal of chunking is not to "split evenly" but to "preserve semantic units that are meaningful for retrieval as much as possible."

It is usually designed by combining fixed length, paragraph boundaries, heading hierarchy, and overlapping windows. If chunks are too large, they will introduce more noise and cause inaccurate hits; if too small, context will be lost, and even after retrieval, the model will be unable to answer. For manuals, FAQs, policy documents, and PDFs with mixed text and images, these documents often cannot be split by character count alone; layout structure, headings, tables, and semantic boundaries must also be considered.

Common pitfalls include: overly fragmented chunks, ignoring heading hierarchy, insufficient overlap, failing to clean dirty raw OCR text, breaking up table content, and cramming multiple topics into a single chunk, which causes vector semantic contamination.

**Importance:** `高频` (occurrences: 3 times) | **Difficulty:** `中等`

**Assessment focus:** Whether the candidate has solid RAG fundamentals.

**Corresponding sections:** [19 RAG Retrieval-Augmented Generation §2. Core Knowledge of RAG Text Processing](19-RAG%E6%A3%80%E7%B4%A2%E5%A2%9E%E5%BC%BA%E7%94%9F%E6%88%90.md#_2-core-knowledge-of-rag-text-processing); [2-RAG Building Enterprise Private & Personal Knowledge Bases §2. Overview of Knowledge Bases](2-RAG-%E6%90%AD%E5%BB%BA%E4%BC%81%E4%B8%9A%E7%A7%81%E6%9C%89&%E4%B8%AA%E4%BA%BA%E7%9F%A5%E8%AF%86%E5%BA%93.md#_2-overview-of-knowledge-bases)

### Q3-3. When RAG performs poorly, how do you troubleshoot it?

Troubleshooting can be carried out in three layers: "before retrieval, during retrieval, and after retrieval."

- Before retrieval: check whether the query is clearly expressed, and whether it needs rewriting, decomposition, or additional context.
- During retrieval: check whether chunking, embeddings, vector database index parameters, top_k, filtering conditions, and reranking are reasonable.
- After retrieval: check whether the context assembled for the model is too long, whether it contains noise, whether key information is being drowned out, and whether the generation prompt requires that the model "refuse to answer when there is no evidence."

If it is an enterprise knowledge base, you should also separately check document quality, whether versions are up to date, and whether permission filtering is mistakenly blocking content. Many so-called "the model is not smart enough" problems can ultimately be traced back to dirty document parsing, overly fragmented chunks, noisy recall, or poor context assembly.

**Common follow-up questions:**

- Is a larger top_k always better?
- How do you identify whether the problem is in retrieval or generation?
- What is Lost in the Middle?

**Importance:** `必刷` (occurrences: 1 time) | **Difficulty:** `中等`

**Assessment focus:** Troubleshooting ability, and whether the approach to localization is layered.

**Corresponding sections:** [19 RAG Retrieval-Augmented Generation §2. Core Knowledge of RAG Text Processing](19-RAG%E6%A3%80%E7%B4%A2%E5%A2%9E%E5%BC%BA%E7%94%9F%E6%88%90.md#_2-core-knowledge-of-rag-text-processing); [19 RAG Retrieval-Augmented Generation §3. Comprehensive RAG Case Study: Intelligent Operations Assistant](19-RAG%E6%A3%80%E7%B4%A2%E5%A2%9E%E5%BC%BA%E7%94%9F%E6%88%90.md#_3-comprehensive-rag-case-intelligent-operations-assistant)

### Q3-4. What problems do hybrid retrieval, reranking, and query rewriting each solve?

These three techniques solve problems at three different levels.

- Query rewriting solves the problem that "the user's question expression is not similar enough to a retrieval query."
- Hybrid retrieval solves the problem that "relying solely on dense vectors may miss keyword matches."
- Reranking solves the problem that "a batch of candidates has been recalled, but the ordering is still not accurate enough."

In real projects, especially for knowledge such as policies, product specifications, order fields, and error codes, keywords are often very important, so dense retrieval alone is often insufficient. A relatively reliable approach is usually "query rewriting + dense retrieval + sparse retrieval + rerank," combined with metadata filtering as a final constraint.

**Common follow-up questions:**

- What is the difference between dense retrieval and sparse retrieval?
- At which layer is it most appropriate to apply reranking?
- Will hybrid retrieval be more expensive?

**Importance:** `高频` (occurrences: 1 time) | **Difficulty:** `中等`

**Assessment focus:** Whether the candidate understands the division of responsibilities in retrieval optimization.

**Corresponding sections:** [18 Vector Databases and Embedding in Practice §6. Writing to and Retrieving from Vector Databases](18-%E5%90%91%E9%87%8F%E6%95%B0%E6%8D%AE%E5%BA%93%E4%B8%8EEmbedding%E5%AE%9E%E6%88%98.md#_6-writing-to-and-retrieving-from-a-vector-database-rags-underlying-capability); [19 RAG Retrieval-Augmented Generation §2. Core Knowledge of RAG Text Processing](19-RAG%E6%A3%80%E7%B4%A2%E5%A2%9E%E5%BC%BA%E7%94%9F%E6%88%90.md#_2-core-knowledge-of-rag-text-processing)

### Q3-5. How should RAG be integrated into an Agent execution pipeline?

Integrating RAG into an Agent cannot be understood simply as "first look up some materials and then answer." A more robust approach is usually to make the retrieval capability a component that the Agent can invoke on demand.

There are three common integration patterns:

- Pre-retrieval: retrieve uniformly as soon as the user question arrives, then hand the evidence to the Agent for further planning.
- On-demand retrieval: wrap the Retriever / Search as a tool, so the Agent actively invokes it when factual evidence is needed.
- Post-verification: generate the result first, then use retrieval for evidence checking or citation completion.

In real projects, it is usually more recommended to use "on-demand retrieval as the primary pattern, with pre-retrieval as a supplement," because not every step requires querying the knowledge base; some steps involve planning, routing, parameter confirmation, or tool execution. Making RAG a callable capability reduces ineffective retrieval and is more suitable for multi-step tasks. Post-verification can serve as an enhancement, but is usually not suitable as the main pipeline, since it increases latency, and if the earlier steps have already gone off track, subsequent verification and correction will be more costly.

**Common follow-up questions:**

- Are you familiar with multiple retrievals during generation, adaptive retrieval, or Agentic RAG? What is the difference between that and "retrieve once, then generate"?
- Under what circumstances should one upgrade from "single retrieval" to "multi-round retrieval + mid-process supplementary retrieval"?

**Importance:** `高频` (occurrences: 1 time) | **Difficulty:** `中等`

**Assessment focus:** Whether the candidate understands how to integrate Agentic RAG, rather than only treating RAG as a fixed pre-processing pipeline.

**Corresponding sections:** [19 RAG Retrieval-Augmented Generation §1. Introduction to RAG](19-RAG%E6%A3%80%E7%B4%A2%E5%A2%9E%E5%BC%BA%E7%94%9F%E6%88%90.md#_1-introduction-to-rag); [21 Agent §6. Summary: Differences and Connections among Agent, Tool, Function Calling, RAG, and MCP](21-Agent%E6%99%BA%E8%83%BD%E4%BD%93.md#_6-summary-differences-and-relationships-among-agent-tool-function-calling-rag-and-mcp)

### Q3-6. Why must enterprise RAG projects pay close attention to permissions, versions, and citations?

Because enterprise knowledge is not about "being able to retrieve something," but about "retrieving the right thing, within the right permission scope, with traceable sources."

On permissions: vector retrieval must implement tenant isolation, role-based filtering, and document-level or paragraph-level permission control. Security cannot be left to the model's "conscientious refusal to answer." On versions: indexes and source documents must be traceable, and after document updates you need to know which vectors require incremental rebuilding. On citations: if answers cannot be traced back to original text segments, business stakeholders will find it hard to build trust, and auditing and post-incident review will also be difficult.

Therefore, in enterprises, RAG is not only a retrieval effectiveness issue; it is also a data governance issue.

**Importance:** `中频` (occurrences: 1 time) | **Difficulty:** `中等`

**Assessment focus:** Awareness of enterprise deployment, not just staying at the demo level.

**Corresponding sections:** [2-RAG Building Enterprise Private & Personal Knowledge Bases §2. Overview of Knowledge Bases](2-RAG-%E6%90%AD%E5%BB%BA%E4%BC%81%E4%B8%9A%E7%A7%81%E6%9C%89&%E4%B8%AA%E4%BA%BA%E7%9F%A5%E8%AF%86%E5%BA%93.md#_2-overview-of-knowledge-bases); [19 RAG Retrieval-Augmented Generation §3. Comprehensive RAG Case Study: Intelligent Operations Assistant](19-RAG%E6%A3%80%E7%B4%A2%E5%A2%9E%E5%BC%BA%E7%94%9F%E6%88%90.md#_3-comprehensive-rag-case-intelligent-operations-assistant)

### Q3-7. What is Lost in the Middle? What implications does it have for RAG design?

Lost in the Middle refers to the phenomenon that when context becomes long, models often find it easier to use information at the beginning and the end, while the key evidence in the middle is "seen but not used well."

Its implication for RAG is very direct: cramming more chunks into the context is not necessarily better. If there is too much noise in the middle, the truly critical evidence is more likely to be drowned out.

Therefore, in engineering practice, the following approaches are usually adopted:

- First perform reranking and filtering, then decide what gets into the context.
- Minimize low-value segments as much as possible; do not stuff in everything that is "possibly relevant."
- Put important evidence near the front, and when necessary use summarization or lead with the conclusion.
- For complex questions, use staged retrieval rather than dumping large volumes of material into the context at once.

In summary: **Long context does not equal high-quality context. The core of RAG remains "placing the most useful evidence where the model can use it most easily."**

**Importance:** `中频` (occurrences: 1 time) | **Difficulty:** `中等`

**Assessment focus:** Understanding of long-context behavior, and awareness of the interplay among retrieval, reranking, and context assembly.

**Corresponding sections:** [19 RAG Retrieval-Augmented Generation §2. Core Knowledge of RAG Text Processing](19-RAG%E6%A3%80%E7%B4%A2%E5%A2%9E%E5%BC%BA%E7%94%9F%E6%88%90.md#_2-core-knowledge-of-rag-text-processing); [19 RAG Retrieval-Augmented Generation §3. Comprehensive RAG Case Study: Intelligent Operations Assistant](19-RAG%E6%A3%80%E7%B4%A2%E5%A2%9E%E5%BC%BA%E7%94%9F%E6%88%90.md#_3-comprehensive-rag-case-intelligent-operations-assistant)

### Q3-8. With ultra-long-context models available, do we still need RAG?

In most scenarios, yes, because "being able to fit it in" and "being right to fit it in" are completely different things.

Ultra-long-context models do make long-document understanding and reasoning over a small number of documents more convenient, but the more common problems in enterprise scenarios are not "the model's context window is too small," but rather:

- The total amount of knowledge is too large to stuff everything in every time.
- Long-context cost and latency are both higher.
- Permission filtering, tenant isolation, and version control cannot be solved simply by force-fitting things into the window.
- Auditing and citation tracing are better handled through a retrieval pipeline.

Therefore, a more reasonable understanding is usually: **Long context expands the range of what can be handled, but it does not eliminate the value of retrieval.** It is better suited for analysis of a small number of long documents, context integration, and complex reasoning; RAG is better suited for narrowing down massive knowledge, permission filtering, evidence citation, and continuous updating.

If compressed into one sentence, it can be summarized as: **Long context is not a replacement for RAG, but rather closer to a complementary capability to RAG.**

**Importance:** `中频` (occurrences: 1 time) | **Difficulty:** `中等`

**Assessment focus:** Whether the candidate understands that "long-window capability" and "the value of a retrieval system" are not problems at the same level.

**Corresponding sections:** [19 RAG Retrieval-Augmented Generation §1. Introduction to RAG](19-RAG%E6%A3%80%E7%B4%A2%E5%A2%9E%E5%BC%BA%E7%94%9F%E6%88%90.md#_1-introduction-to-rag); [1-1 Overview of Large Language Model Cognition and Engineering §1. Understanding Large Language Models](1-1-%E5%A4%A7%E6%A8%A1%E5%9E%8B%E8%AE%A4%E7%9F%A5%E4%B8%8E%E5%B7%A5%E7%A8%8B%E6%A6%82%E8%A7%88.md#_1-getting-to-know-llms)

### Q3-9. How should complex-document RAG or multimodal RAG be implemented?

The biggest pitfall in such scenarios is treating PDFs, scanned documents, tables, images, and web pages all as "ordinary plain text."

A more robust approach is usually to treat the parsing layer as a separate concern:

- First perform layout analysis, OCR, table extraction, and heading hierarchy recovery, rather than chunking by character count from the start.
- Chunks should be split by structural blocks as much as possible, such as headings, paragraphs, tables, and figure captions, rather than cutting a table into several incomplete text fragments.
- Metadata should retain page numbers, section headings, document versions, source files, coordinates, or structural position information to facilitate citation and tracing.
- At query time, use multi-route retrieval when necessary, for example text recall, table recall, and image-caption recall, followed by unified reranking and assembly.

If it is an enterprise knowledge base, complex-document RAG often affects the upper limit of performance more than "model selection" does. Because if parsing is wrong, tables are fragmented, or the text-image correspondence is lost, no matter how powerful the downstream model is, it will be very difficult to compensate.

**Common follow-up questions:**

- Why are many device manuals and policy PDFs especially difficult to use for RAG?
- What is the relationship between OCR accuracy and final Q&A quality?
- When is multimodal RAG worth using, and when is plain text sufficient?

**Importance:**`中频` (occurrences: 1) | **Difficulty:**`较难`

**Assessment focus:** Whether you realize that RAG is not just a retrieval problem, but also involves document parsing, structure recovery, and citation tracking.

**Relevant sections:** [19 RAG Retrieval-Augmented Generation §2, RAG Text Processing Core Knowledge](19-RAG%E6%A3%80%E7%B4%A2%E5%A2%9E%E5%BC%BA%E7%94%9F%E6%88%90.md#_2-core-knowledge-of-rag-text-processing); [2-RAG Building Enterprise Private & Personal Knowledge Bases §2, Overview of Knowledge Bases](2-RAG-%E6%90%AD%E5%BB%BA%E4%BC%81%E4%B8%9A%E7%A7%81%E6%9C%89&%E4%B8%AA%E4%BA%BA%E7%9F%A5%E8%AF%86%E5%BA%93.md#_2-overview-of-knowledge-bases)

### Q3-10. What is Agentic RAG? How does it differ from "retrieve once and then generate directly"?

Traditional RAG is closer to a fixed pipeline: retrieve once, then hand the results to the model to generate an answer. Agentic RAG is closer to a closed-loop process, where the model or agent decides based on current progress whether to retrieve, what to retrieve, whether to rewrite the query, whether to continue supplementary retrieval, and even proactively goes back to search again when it finds the evidence is insufficient.

The biggest difference between the two is not "whether retrieval happens," but **whether retrieval is managed as a dynamic decision-making process**.

- Traditional RAG: stable flow, more controllable cost, simple to implement, suitable for single-turn Q&A and most standard knowledge base scenarios.
- Agentic RAG: better suited for complex questions, multi-hop evidence, and scenarios requiring self-checking and supplementary retrieval, but the trade-offs are longer chains, higher costs, and higher risk of losing control.

So in engineering practice, you usually don't start with Agentic RAG right away; instead, you first check whether the bad cases are actually concentrated on these problems:

- A single retrieval often fails to obtain enough evidence.
- The question itself needs to be decomposed, verified across multiple rounds, or cross-validated across multiple sources.
- Before generation, you need to determine "whether to query the knowledge base, the web, or a business system."

If Agentic RAG really needs to be put into production, I would definitely also add step limits, budget limits, failure exit conditions, and observability. Otherwise, it can easily turn from "smarter retrieval" into "a more expensive random walk."

**Common follow-up questions:**

- Under what circumstances should you stick with fixed RAG instead of upgrading to Agentic RAG?
- Which bad cases do the benefits of Agentic RAG usually show up in?
- How do you prevent multiple rounds of supplementary retrieval from pushing latency and cost too high?

**Importance:**`中频` (occurrences: 1) | **Difficulty:**`较难`

**Assessment focus:** Whether you truly understand the boundaries and costs of RAG's evolution from a fixed pipeline to an intelligent retrieval closed loop.

**Relevant sections:** [19 RAG Retrieval-Augmented Generation §1, Introduction to RAG](19-RAG%E6%A3%80%E7%B4%A2%E5%A2%9E%E5%BC%BA%E7%94%9F%E6%88%90.md#_1-introduction-to-rag); [21 Agent §1, Introduction to Agent](21-Agent%E6%99%BA%E8%83%BD%E4%BD%93.md#_1-introduction-to-agents)

---

## 4. Retrieval Infrastructure and Retrieval Optimization

### Q4-1. What is a vector database? How is it different from a traditional database? Why can't you just use MySQL?

First, a definition: a vector database is a storage system specifically designed for "similarity retrieval." It stores vectors, original content, and metadata, and supports nearest-neighbor search, filtering, and recall.

Traditional databases excel at exact filtering, transactions, and structured queries, while vector databases excel at nearest-neighbor retrieval based on "semantic similarity." The two are not substitutes for each other; they have a division of labor.

If you only use MySQL, you can of course still store embeddings, but once the data volume grows, approximate vector retrieval, ANN indexes, hybrid retrieval, and large-scale recall will all become inefficient, and engineering complexity will increase significantly. A more common approach in enterprises is: structured conditions go through traditional databases, semantic recall goes through vector databases, and metadata is used to combine the two.

**Importance:**`高频` (occurrences: 2) | **Difficulty:**`基础`

**Assessment focus:** Understanding of underlying retrieval infrastructure.

**Relevant sections:** [18 Vector Databases and Embedding in Practice §2, Vector Databases](18-%E5%90%91%E9%87%8F%E6%95%B0%E6%8D%AE%E5%BA%93%E4%B8%8EEmbedding%E5%AE%9E%E6%88%98.md#_2-vector-databases); [18 Vector Databases and Embedding in Practice §6, Writing to and Retrieving from Vector Databases](18-%E5%90%91%E9%87%8F%E6%95%B0%E6%8D%AE%E5%BA%93%E4%B8%8EEmbedding%E5%AE%9E%E6%88%98.md#_6-writing-to-and-retrieving-from-a-vector-database-rags-underlying-capability)

### Q4-2. What is an Embedding? What is its core value in application development?

The essence of an embedding is to convert raw content such as text or images into a fixed-length vector, so that "semantic relationships" are mapped as faithfully as possible into "spatial relationships." In another engineering-oriented phrasing, it turns "similar meaning" into "close distance," which is what allows programs to perform similarity calculations.

Its core value in application development is not just "encoding text into numbers," but that it gives a system the ability to retrieve by semantics for the first time. That is why it is often used for semantic search, similarity matching, deduplication, clustering, recommendation, and RAG recall.

In RAG, the embedding determines whether "the question and the knowledge can correctly meet in vector space." If the wrong embedding is chosen, then no matter how much you compensate with the vector database, reranking, or prompts afterward, you are only optimizing on top of an already skewed recall foundation.

Two engineering details also need to be emphasized:

- Building the index and querying should ideally use the same embedding model; otherwise, the dimensions may not match, or even if they do, the similarity may be meaningless.
- An embedding only turns text into a "dense vector" layer. In actual retrieval, it is often combined with scalar field filtering and even sparse retrieval, so it should not be understood as the entirety of a retrieval system.

**Importance:**`高频` (occurrences: 1) | **Difficulty:**`基础`

**Assessment focus:** Whether you understand that embeddings are not an "auxiliary model" but part of the retrieval infrastructure.

**Relevant sections:** [18 Vector Databases and Embedding in Practice §1, Vectors and Vectorization](18-%E5%90%91%E9%87%8F%E6%95%B0%E6%8D%AE%E5%BA%93%E4%B8%8EEmbedding%E5%AE%9E%E6%88%98.md#_1-vectors-and-embedding); [18 Vector Databases and Embedding in Practice §4, Text Vectorization with Embeddings](18-%E5%90%91%E9%87%8F%E6%95%B0%E6%8D%AE%E5%BA%93%E4%B8%8EEmbedding%E5%AE%9E%E6%88%98.md#_4-embedding-text-vectorization)

### Q4-3. How do you choose an appropriate Embedding model? What should you look at to evaluate its quality?

Usually you don't look at leaderboards first; instead, you look at your own knowledge types and retrieval goals, and then work backward to model selection. A more reasonable approach is to first look at three things:

- Language and domain fit: Chinese, English, multilingual, code, legal, finance—the most suitable model may be completely different for each.
- Consistency between index building and querying: try to use the same embedding model for both index building and querying; this is the bottom line.
- Whether cost and latency are acceptable: higher dimensions are not always better, and larger models are not always better. You need to see whether the knowledge base scale and query volume can support it.

In actual evaluation, you should focus more on "whether it lifts the entire retrieval chain as a whole" rather than just looking at a leaderboard score. A practical judgment usually has three layers:

- Retrieval layer: are relevant passages easier to recall, have bad cases decreased, and is the gap before and after reranking large?
- Business layer: have the faithfulness of the final answer, citation accuracy, and task completion rate improved?
- Engineering layer: are latency, cost, and integration complexity acceptable?

In engineering, two points need special emphasis:

- Embedding selection is not an isolated issue; it determines the upper limit together with chunking strategy, index parameters, hybrid retrieval, and reranking.
- Public leaderboards can only be used for initial screening. What really determines whether to launch is your own knowledge samples and bad cases.

So a more stable approach is usually to first select two to three candidate models and run through them, then do a small-scale comparison on your own knowledge base samples, observing recall quality, final answer quality, cost, and latency before making a decision.

**Importance:**`高频` (occurrences: 1) | **Difficulty:**`中等`

**Assessment focus:** Embedding selection, evaluation awareness, and understanding of "model consistency + retrieval chain linkage."

**Relevant sections:** [18 Vector Databases and Embedding in Practice §4, Text Vectorization with Embeddings](18-%E5%90%91%E9%87%8F%E6%95%B0%E6%8D%AE%E5%BA%93%E4%B8%8EEmbedding%E5%AE%9E%E6%88%98.md#_4-embedding-text-vectorization); [18 Vector Databases and Embedding in Practice §6, Writing to and Retrieving from Vector Databases](18-%E5%90%91%E9%87%8F%E6%95%B0%E6%8D%AE%E5%BA%93%E4%B8%8EEmbedding%E5%AE%9E%E6%88%98.md#_6-writing-to-and-retrieving-from-a-vector-database-rags-underlying-capability)

### Q4-4. How do you balance approximate retrieval and exact retrieval?

Exact retrieval offers more controllable results, but at large scale it has high cost and high latency. Approximate retrieval sacrifices some accuracy in exchange for better throughput and response speed, so most production systems prefer approximate retrieval.

In engineering, this is not a simple either-or choice; it depends on business requirements. If it is high-risk retrieval, the data volume is not large, and result consistency requirements are extremely high, you can use exact or more conservative indexing strategies. If it is general knowledge Q&A, product search, or recall over massive documents, approximate retrieval is usually more realistic, supplemented by reranking as compensation.

**Importance:**`中频` (occurrences: 1) | **Difficulty:**`中等`

**Assessment focus:** Ability to trade off performance and effectiveness.

**Relevant sections:** [18 Vector Databases and Embedding in Practice §2, Vector Databases](18-%E5%90%91%E9%87%8F%E6%95%B0%E6%8D%AE%E5%BA%93%E4%B8%8EEmbedding%E5%AE%9E%E6%88%98.md#_2-vector-databases); [18 Vector Databases and Embedding in Practice §5, Computing Semantic Similarity with Vectors](18-%E5%90%91%E9%87%8F%E6%95%B0%E6%8D%AE%E5%BA%93%E4%B8%8EEmbedding%E5%AE%9E%E6%88%98.md#_5-calculating-semantic-similarity-through-vectors)

### Q4-5. In which scenarios are knowledge graphs or graph databases more valuable than pure vector retrieval?

When the core of the problem is not just "semantic similarity" but "entity relationships, path reasoning, multi-hop associations, and structured constraints," knowledge graphs or graph databases become more valuable.

For example, device troubleshooting, product attribute associations, organizational relationships, legal provision citations, and dependency chain analysis—these scenarios often depend more on "who has what relationship with whom" rather than just "which text looks most similar." In these cases, relying only on vector retrieval tends to recall content that is semantically close but relationally wrong.

In engineering, it is better to understand it as an enhancement rather than a simple replacement. A relatively stable approach is usually: vector retrieval handles semantic recall, while the knowledge graph handles structured constraints, entity disambiguation, and relational reasoning. Only when the problem itself is highly structured and the relational chain is especially critical does a graph database possibly become the primary path.

**Importance:**`中频` (occurrences: 1) | **Difficulty:**`较难`

**Assessment focus:** Understanding of the boundary between "semantic recall" and "relational reasoning," as well as retrieval architecture selection ability.

### Q4-6. What scenarios is GraphRAG suitable for? How do you choose between it and traditional vector RAG?

GraphRAG is more suitable for scenarios with dense entity relationships, requirements for multi-hop reasoning, community summarization, or very strong structured constraints.

For example, organizational relationship analysis, supply chain dependencies, device failure chains, legal provision correlations, and people-event networks—these problems are often not about "which passage of text is most similar," but rather "how are these entities related, and how many hops are needed to reach the answer." In such cases, the advantage of a knowledge graph or graph database is more obvious.

But in engineering, you usually don't default to GraphRAG at the beginning. A more common and stable path is:

- Start with traditional vector RAG as the foundation to solve most semantic recall problems.
- When bad cases clearly concentrate on multi-hop relationships, entity disambiguation, and structural constraints, introduce graph enhancement.
- In actual implementation, it is often not an either-or choice, but rather "vector recall + graph recall + fused reranking" working together.

A more accurate conclusion is: **only when the core of the problem lies in relational structure will the benefits of the graph approach outweigh its complexity.**

**Common follow-up questions:**

- What is the relationship between GraphRAG and knowledge graph databases?
- Under what circumstances is multi-route retrieval more practical than a purely graph-based main route?
- Won't the cost of updating and maintaining the graph be too high?

**Importance:** `中频` (occurrences: 1) | **Difficulty:** `较难`

**Assessment focus:** GraphRAG selection capability, and awareness of the trade-offs between complexity and benefit.

---

## 5. Tools, Function Calling, and Agent

### Q5-1. What is the ReAct pattern? What problem does it solve?

The value of ReAct lies in linking "reasoning" and "acting," so that the model not only thinks but can also continuously adjust its next step based on external observations.

It usually manifests as a loop of `Thought -> Action -> Observation`. The model first makes a current judgment, then decides which tool to call, and then updates its judgment based on the result returned by the tool, until the task is complete. Compared with relying solely on one-shot generation, ReAct is better suited to tasks with uncertain paths, multi-step decision-making, and heavy dependence on external information.

One important point should also be added here: modern Tool Calling Agents do not necessarily display `Thought` explicitly. What is more common in actual code is `AIMessage.tool_calls`, tool execution results, and the next round of messages. Therefore, a more accurate way to understand it is: **ReAct is closer to a working mechanism than just a fixed Prompt template.**

From an engineering perspective, it is important to note that ReAct's advantage is flexibility, but the cost is longer chains, higher expense, and more complex debugging, so not every scenario is worth implementing a full loop.

**Common follow-up questions:**

- What is Chain of Thought (CoT)? Why can it improve performance on complex reasoning questions?
- What is the difference between CoT and ReAct? When is CoT alone sufficient, and when should you upgrade to ReAct?

**Importance:** `高频` (occurrences: 3) | **Difficulty:** `基础`

**Assessment focus:** Understanding of Agent operating paradigms.

**Corresponding sections:** [21 Agent §3. How Agents Work (V0.3)](21-Agent%E6%99%BA%E8%83%BD%E4%BD%93.md#_3、agent-工作原理%EF%BC%88v0.3%EF%BC%89); [17 Tools §2. How Tool Calling Works](17-Tools%E5%B7%A5%E5%85%B7%E8%B0%83%E7%94%A8.md#_2-how-tool-calling-works)

### Q5-2. What is the relationship among Tool, Function Calling, and Agent?

Tool is the capability unit, Function Calling is the invocation mechanism, and Agent is the operating pattern that organizes the model, tools, state, and decision-making process.

Tool addresses "what can be done," Function Calling addresses "how to initiate a structured call," and Agent addresses "how to decide over multiple rounds, around a goal, whether to call, whom to call, and how many times to call." Therefore, Tool is not equivalent to Agent, and a single Tool Calling does not necessarily equal an Agent either.

In real projects, many requirements only need Tool Calling, and it is not always necessary to deploy a full Agent. Only when a task requires multi-step planning, repeated decision-making, and state progression is an Agent worth introducing.

**Common follow-up questions:**

- Does a single-tool assistant count as an Agent?
- What is the relationship between ReAct and Function Calling?
- What should be the minimum granularity of Tool design?

**Importance:** `必刷` (occurrences: 2) | **Difficulty:** `基础`

**Assessment focus:** Whether conceptual distinctions are clear.

**Corresponding sections:** [17 Tools §1. Introduction to Tools](17-Tools%E5%B7%A5%E5%85%B7%E8%B0%83%E7%94%A8.md#_1-introduction-to-tools); [21 Agent §6. Summary: Differences and Connections Among Agent, Tool, Function Calling, RAG, and MCP](21-Agent%E6%99%BA%E8%83%BD%E4%BD%93.md#_6-summary-differences-and-relationships-among-agent-tool-function-calling-rag-and-mcp)

### Q5-3. How should an Agent be designed? What core components does it usually consist of?

In the most minimal understanding, it can be summarized as: **Agent = model + tool set + execution loop + current state**.

- Model: responsible for understanding the goal, analyzing the current situation, and deciding the next step.
- Tool set: responsible for providing external capabilities, such as search, databases, file systems, and business APIs.
- Execution loop: responsible for ensuring that the system does not answer only once, but can "think one step, do one step, see the result, and then decide the next step."
- Current state: responsible for saving messages, tool returns, intermediate results, and thread context.

On top of this minimal skeleton, memory, planning, reflection, and multi-agent collaboration can all be added later, but they are better understood as "extended capabilities" rather than something every Agent must have from the very beginning.

From an engineering design perspective, a deployable Agent should focus on controlling five things:

- Goal and responsibility: the problem an Agent solves should be as singular as possible; it should not try to do everything.
- Tool boundaries: expose only the capabilities truly needed to complete the task, and avoid giving the model unrestricted permissions.
- State design: where to store current task progress, intermediate conclusions, and message history must be designed explicitly.
- Stopping conditions: when to continue, when to clarify, when to escalate to a human, and when to end must not be ambiguous.
- Governance capabilities: logging, tracing, retries, timeouts, auditing, and human takeover must all be in place.

In summary: the focus of Agent design is not "adding more capabilities," but making the system more controllable, more traceable, and more reliable in delivering results around the four main threads of **model, tools, loop, and state**.

**Common follow-up questions:**

- When building a complex Agent, what do you think is the biggest challenge?
- Why do many Agents fail not because of insufficient capability, but because state, boundaries, and governance were poorly designed?

**Importance:** `必刷` (occurrences: 2) | **Difficulty:** `中等`

**Assessment focus:** Agent architecture capability, rather than staying at the conceptual level.

**Corresponding sections:** [21 Agent §1. Introduction to Agents](21-Agent%E6%99%BA%E8%83%BD%E4%BD%93.md#_1-introduction-to-agents); [21 Agent §6. Summary: Differences and Connections Among Agent, Tool, Function Calling, RAG, and MCP](21-Agent%E6%99%BA%E8%83%BD%E4%BD%93.md#_6-summary-differences-and-relationships-among-agent-tool-function-calling-rag-and-mcp)

### Q5-4. What is the basic principle of Function Calling?

The core division of labor in Function Calling can be summarized in one sentence: the model is responsible for decision-making, and the program is responsible for execution.

More completely, the chain usually works like this:

1. The host program sends the tool's `name`, `description`, and parameter schema to the model together.
2. The model determines whether to call a tool and, if so, first returns a structured `tool_calls` rather than directly giving the final natural-language answer.
3. The host program reads the `AIMessage.tool_calls` and actually executes the Python function, HTTP API, database query, or business service.
4. The program wraps the execution result into a `ToolMessage` or equivalent message and sends it back to the model.
5. The model generates the final answer based on the tool result.

Therefore, Function Calling does not mean the model calls the API itself; it only generates the structured intent of "which tool to call and what parameters to pass." The actual authentication, parameter validation, timeout handling, idempotency, retries, and security control still all remain at the host program layer.

To answer in a more engineering-oriented way, one more sentence should be added: Function Calling solves "how the model expresses its invocation intent," but it does not solve problems such as "whether the tool is safe, whether invocation is allowed, and how to handle invocation failures."

**Common follow-up questions:**

- What is the difference between Function Calling and text-parsing-based invocation?
- Why is native Tool Calling more recommended in production environments?
- How should tool execution failures be handled?

**Importance:** `必刷` (occurrences: 1) | **Difficulty:** `中等`

**Assessment focus:** Whether the responsibility boundary between the model and the host program is understood.

**Corresponding sections:** [17 Tools §1. Introduction to Tools](17-Tools%E5%B7%A5%E5%85%B7%E8%B0%83%E7%94%A8.md#_1-introduction-to-tools); [17 Tools §2. How Tool Calling Works](17-Tools%E5%B7%A5%E5%85%B7%E8%B0%83%E7%94%A8.md#_2-how-tool-calling-works)

**Source:** Tencent AI backend engineer first-round interview (real Big Tech interview question)

### Q5-5. What are the most important engineering principles when designing a Tool?

The four most important points are: single responsibility, explicit schema, observability, and failability.

Single responsibility means one Tool does only one clear thing, avoiding an all-encompassing "universal tool." An explicit schema helps the model understand parameter meanings more stably. Observability means every invocation must be traceable in terms of request, parameters, duration, result, and errors. Failability means the Tool must have timeout handling, error codes, retry policies, and fallback logic, rather than assuming success is guaranteed.

If a Tool needs to connect to business systems, permission checks, idempotency controls, and audit logs must also be added. Because once a tool changes from "checking the weather" to "sending messages, creating work orders, or writing to a database," the risk level becomes completely different.

**Importance:** `高频` (occurrences: 1) | **Difficulty:** `中等`

**Assessment focus:** Whether the candidate has the experience and awareness of connecting tools to production systems.

**Corresponding sections:** [17 Tools §3. Custom Tools](17-Tools%E5%B7%A5%E5%85%B7%E8%B0%83%E7%94%A8.md#_3-custom-tools-start-with-the-simplest-tool); [17 Tools §4. Parameter Schema: Why Pydantic](17-Tools%E5%B7%A5%E5%85%B7%E8%B0%83%E7%94%A8.md#_4-parameter-schema-why-pair-it-with-pydantic)

### Q5-6. If you were asked to implement an AI assistant that can "check weather and check news," how would you design it?

For this type of question in an interview, it is more recommended to first assess the scenario and then discuss the approach. For requirements like checking weather and checking news, the core is not complex planning, but rather "intent recognition + tool invocation + result integration."

A relatively solid implementation usually consists of four layers:

- Input and routing layer: first determine whether the user wants weather, news, or both. If necessary, extract parameters such as city, time, and news topic.
- Tool layer: wrap weather query and news retrieval as clear Tools, with well-defined schemas, parameter descriptions, error returns, and timeout policies.
- Orchestration layer: use Function Calling or a lightweight Agent to let the model decide which tool to call, how to pass parameters, and whether multiple tools need to be chained.
- Output layer: uniformly organize tool results, for example key fields for weather and summaries plus sources for news, and finally have the model generate a natural-language reply.

If the requirement is only single-round weather or news queries, `Prompt + Function Calling` is often sufficient, and a full ReAct Agent is not necessarily required. Only when the requirement escalates to a multi-step dynamic chain such as "first check the weather, then recommend local news based on the weather, and then continue asking about details of a particular news item" does the value of an Agent become more apparent.

Three engineering points require special attention: tool descriptions must be clear to prevent the model from calling them arbitrarily; external APIs must have fallback and timeout handling; and output results should ideally include sources or key fields to prevent the model from fabricating the tool results a second time.

**Importance:** `高频` (occurrences: 1) | **Difficulty:** `中等`

**Assessment focus:** Whether the candidate can break down a simple assistant into the four layers of "intent, tools, orchestration, and output," rather than immediately jumping to saying "use an Agent."

**Corresponding sections:** [17 Tools §5. Weather Assistant Hands-On](17-Tools%E5%B7%A5%E5%85%B7%E8%B0%83%E7%94%A8.md#_5-weather-assistant-in-practice-running-tools-as-a-complete-business-loop); [21 Agent §5. Practice and Cases](21-Agent%E6%99%BA%E8%83%BD%E4%BD%93.md#_5-hands-on-practice-and-case-studies)

**Source:** Tencent AI backend engineer first-round interview (real Big Tech interview question)

### Q5-7. What is "tool hallucination"? How can it be mitigated in engineering?

Tool hallucination refers to the model calling tools that do not exist, passing unreasonable parameters, or attempting to trigger write operations when it should only be reading data.

This kind of problem is especially common when there are many tools, vague descriptions, and unclear schemas. Sometimes the model is not "unable to use tools," but rather "misunderstands the boundaries of the tools."

Engineering fallback measures usually include:

- Tool registry whitelist: directly reject non-existent tool names.
- Strong schema validation: parameter types, required fields, and enumeration values must all be validated at runtime; do not trust what the model returns.
- Tool set convergence: expose the minimal tool set according to the scenario; do not let the model guess among dozens of similar tools.
- Clear descriptions: tool names, descriptions, and parameter meanings must clearly distinguish read/write boundaries and applicable scenarios.
- High-risk confirmation: side-effect actions involving sending messages, writing to databases, creating work orders, or placing orders must require approval or a second confirmation.
- Failure feedback: return the error reason to the model so it has a chance to correct itself, but limit the number of retries to avoid infinite loops.

It can be summarized as: **Tool Calling is not about "just connecting it"—it's about enabling the model to "call accurately, call with restraint, and ensure that even when it calls incorrectly, nothing serious goes wrong."**

**Importance:**`高频` (occurrences: 1) | **Difficulty:**`中等`

**Examination focus:** Understanding of Tool Use stability and risk control.

**Corresponding sections:** [17 Tools for Tool Calling §6, From Course Examples to Real Projects](17-Tools%E5%B7%A5%E5%85%B7%E8%B0%83%E7%94%A8.md#_6-from-course-examples-to-real-projects); [17 Tools for Tool Calling §4, Parameter Schema: Why Pair with Pydantic](17-Tools%E5%B7%A5%E5%85%B7%E8%B0%83%E7%94%A8.md#_4-parameter-schema-why-pair-it-with-pydantic)

### Q5-8. What is the difference between Function Calling and "having the model output JSON and then parsing it yourself"?

On the surface, both look like "the model outputs structured results," but they differ significantly in stability and engineering boundaries.

- Having the model output JSON is closer to making a request at the prompt layer. It is simple, universal, and quick to start, but as soon as the model adds a bit of natural language, omits a field, or writes the wrong type, the application side has to handle the fallout on its own.
- Function Calling is closer to protocol-level structured output. The model does not return arbitrary text, but explicitly returns a tool name and parameters, and the host parses and executes them according to the agreement, which is generally more reliable.

Therefore, in production environments, the usual judgment is:

- If you only need to extract fields and return lightweight structured results, and the platform's native capabilities are limited, start with JSON + parser.
- If you need to enter real tool invocation, external system orchestration, and execution with side effects, prefer native Function Calling or an equivalent Tool Use protocol.

The more critical difference lies in the boundary of responsibilities. JSON parsing is closer to "you ask the model to try to fit this format"; Function Calling is closer to "there is a clear contract between the model and the host." The clearer this contract is, the easier subsequent validation, auditing, retries, and observability become.

**Common follow-up questions:**

- When is JSON + parser already sufficient?
- Why is Function Calling more suitable for connecting to production systems?
- If the platform does not have native Function Calling, how can you make the JSON approach as robust as possible?

**Importance:**`中频` (occurrences: 1) | **Difficulty:**`中等`

**Examination focus:** Understanding of the protocol-level difference between structured output and tool invocation.

**Corresponding sections:** [14 Output Parsers §4, Structured Output](14-%E8%BE%93%E5%87%BA%E8%A7%A3%E6%9E%90%E5%99%A8.md#_4-structured-output); [17 Tools for Tool Calling §2, How Tool Invocation Works](17-Tools%E5%B7%A5%E5%85%B7%E8%B0%83%E7%94%A8.md#_2-how-tool-calling-works)

### Q5-9. When there are many tools, how do you control context length and invocation stability?

Once there are many tools, the problem is usually no longer "whether the model can call tools," but "whether it will choose incorrectly, call incorrectly, and make increasingly chaotic calls among a pile of similar tools."

There are generally four reliable approaches:

- Layered exposure: first break tools down by business domain into search, data, execution, and write-operation categories, and do not expose all tools to the same Agent at once.
- Dynamic selection: perform Tool Retrieval or routing first, and only put the Top-N most relevant tool descriptions into the current context instead of listing all of them.
- Tool aggregation: wrap overly granular underlying APIs into higher-level business actions, reducing the need for the model to guess names among dozens of similar functions.
- Description governance: tool names, descriptions, and parameter documentation should clearly state "when to use it, when not to use it, and whether it has side effects."

To go one step further, in production you can also make "tool selection" itself an independent stage, such as first performing intent classification or subdomain routing before entering specific tool invocation. This can both control context length and reduce the probability of tool hallucination and incorrect invocation.

It can be summarized as: **Having many tools is not the problem; the key is not letting the model blindly choose from an unstructured sea of tools.**

**Common follow-up questions:**

- When there are too many tools, should you prioritize routing or adjusting tool granularity?
- What is the difference between Tool Retrieval and ordinary knowledge retrieval?
- Why are business-action-level tools generally more suitable for model invocation than atomic APIs?

**Importance:**`中频` (occurrences: 1) | **Difficulty:**`较难`

**Examination focus:** Context governance and tool orchestration capabilities in multi-tool scenarios.

**Corresponding sections:** [17 Tools for Tool Calling §6, From Course Examples to Real Projects](17-Tools%E5%B7%A5%E5%85%B7%E8%B0%83%E7%94%A8.md#_6-from-course-examples-to-real-projects); [21 Agents §5, Practice and Examples](21-Agent%E6%99%BA%E8%83%BD%E4%BD%93.md#_5-hands-on-practice-and-case-studies)

---

## 6. Agent Frameworks and Orchestration: LangChain, LCEL, LangGraph

### Q6-1. Compared with ordinary Workflow or chained invocation, what is the greatest value of LangGraph?

The greatest value of LangGraph is that it explicitly expresses the state, nodes, edges, and loops in complex processes, making dynamic processes driven by large language models truly designable, traceable, and recoverable.

Ordinary chained invocation is suitable for simple serial processes, Workflow is suitable for fixed paths, while LangGraph is more suitable for tasks involving branching, loops, human interruption, state persistence, and multi-Agent collaboration. It is not "just another way of writing code," but rather turning complex control flow from implicit logic into an explicit graph structure.

So when your system begins to face questions like "should it continue querying, when should it stop, where to recover after failure, how to preserve state across turns," the advantages of LangGraph become apparent.

**Common follow-up questions:**

- What is the relationship between LangGraph and Agent?
- In what scenarios is an ordinary Workflow sufficient?
- Will the maintenance cost of graph orchestration be higher?

**Importance:**`必刷` (occurrences: 1) | **Difficulty:**`中等`

**Examination focus:** Whether the necessity of graph orchestration is understood.

**Corresponding sections:** [22 LangGraph Overview and Quick Start §1, Introduction to LangGraph](22-LangGraph%E6%A6%82%E8%BF%B0%E4%B8%8E%E5%BF%AB%E9%80%9F%E5%85%A5%E9%97%A8.md#_1-introduction-to-langgraph); [23 LangGraph API: Graph and State §1, Graph API: Graph](23-LangGraphAPI%EF%BC%9A%E5%9B%BE%E4%B8%8E%E7%8A%B6%E6%80%81.md#_1-graph-api-the-graph)

### Q6-2. In LangGraph, what do State, Node, and Edge represent respectively?

State is shared state, Node is processing logic, and Edge is the flow rule.

State determines what the "context that everyone operates on together" is in the graph; Node determines what each step specifically does, such as calling a model, querying a database, or executing a tool; Edge determines where to go next after the current node completes, which can be a fixed transition or conditional routing.

In real projects, whether LangGraph is well designed often depends on whether the State is clear, whether the Node granularity is reasonable, and whether the Edge conditions are explainable. Many graphs are difficult to maintain not because the graph itself is complex, but because too much implicit logic has been crammed into a single node.

**Importance:**`高频` (occurrences: 1) | **Difficulty:**`基础`

**Examination focus:** The basic mental model of LangGraph.

**Corresponding sections:** [23 LangGraph API: Graph and State §2, Graph API: State](23-LangGraphAPI%EF%BC%9A%E5%9B%BE%E4%B8%8E%E7%8A%B6%E6%80%81.md#_2-graph-api-state); [24 LangGraph API: Nodes, Edges, and Advanced Topics §2, Graph API: Edge](24-LangGraphAPI%EF%BC%9A%E8%8A%82%E7%82%B9%E3%80%81%E8%BE%B9%E4%B8%8E%E8%BF%9B%E9%98%B6.md#_2-graph-api-edge)

### Q6-3. What is the value of LangChain today? Why is writing an SDK directly not enough?

The value of LangChain lies not in "whether it can call a model," but in the fact that it unifies common capabilities such as model input and output, Prompt, Parser, Retriever, Tools, Memory, and Callbacks into a composable set of interfaces.

If you are only building a minimal demo, writing an SDK directly is of course fine. But once you enter the stages of multi-model integration, chained orchestration, structured output, observability, and long-term maintenance, unified abstraction will significantly reduce code fragmentation. What it really solves is the problem of "application-layer orchestration and ecosystem integration," not "sending an HTTP request for you."

**Importance:**`高频` (occurrences: 1) | **Difficulty:**`中等`

**Examination focus:** Framework selection judgment, rather than blind worship of frameworks.

**Corresponding sections:** [9 LangChain Overview and Architecture §2, Positioning of LangChain](9-LangChain%E6%A6%82%E8%BF%B0%E4%B8%8E%E6%9E%B6%E6%9E%84.md#_2-positioning-of-langchain); [9 LangChain Overview and Architecture §4, Core Modules of LangChain](9-LangChain%E6%A6%82%E8%BF%B0%E4%B8%8E%E6%9E%B6%E6%9E%84.md#_4-langchain-core-modules)

### Q6-4. How do you develop an Agent using LangChain?

A minimally viable LangChain Agent is usually explained along two routes.

- Classic route: model, tools, Prompt, `create_tool_calling_agent(...)`, `AgentExecutor(...)` are assembled layer by layer, which is more suitable for understanding the internal structure.
- 1.x route: directly use `create_agent(...)`, with the runtime based on LangGraph driving loops, state, and tool invocation behind the scenes, which is closer to the current official mainstream.

Whichever route you take, the underlying main line is the same:

- First define Tools, wrapping external capabilities into clear capability units.
- Then select an LLM, and let the model know the available tool schema.
- Then design the Prompt, clarifying the role, tool usage rules, stopping conditions, and output boundaries.
- Finally, let the system form a closed loop of "model decision -> tool execution -> result return -> continue or stop."

For simple scenarios, you can directly use high-level wrappers; for complex scenarios, you still need to be able to clearly explain the underlying main line. What really earns points in an interview is not memorizing API names, but being able to explain why the Agent calls a tool, when it stops, and how to handle failures.

**Importance:**`高频` (occurrences: 1) | **Difficulty:**`中等`

**Examination focus:** Whether the candidate understands that an Agent is not "just call create_agent and be done," but rather clearly understands the underlying composition.

**Corresponding sections:** [21 Agents §5, Practice and Examples](21-Agent%E6%99%BA%E8%83%BD%E4%BD%93.md#_5-hands-on-practice-and-case-studies); [17 Tools for Tool Calling §5, Weather Assistant Hands-On](17-Tools%E5%B7%A5%E5%85%B7%E8%B0%83%E7%94%A8.md#_5-weather-assistant-in-practice-running-tools-as-a-complete-business-loop)

### Q6-5. What is the value of LCEL? Why is it said to be more than just syntactic sugar?

The core value of LCEL is abstracting Prompt, Model, Parser, Retriever, and function logic all into Runnable, and then composing and invoking them through a unified approach.

It is not just about shorter syntax, but about enabling sequential chains, branching chains, parallel chains, and function chains to be assembled, debugged, and replaced through the same interface. This is very valuable for real projects, because later when you implement logging, streaming, batch processing, callbacks, and local replacement, a unified interface makes the system more maintainable.

**Importance:**`中频` (occurrences: 1) | **Difficulty:**`中等`

**Examination focus:** Whether the unified interface concept of chained orchestration is understood.

**Corresponding sections:** [15 LCEL and Chained Invocation §1, Runnable and Unified Invocation](15-LCEL%E4%B8%8E%E9%93%BE%E5%BC%8F%E8%B0%83%E7%94%A8.md#_1-runnable-and-the-unified-invocation-style); [15 LCEL and Chained Invocation §2, Introduction to LCEL](15-LCEL%E4%B8%8E%E9%93%BE%E5%BC%8F%E8%B0%83%E7%94%A8.md#_2-introduction-to-lcel)

### Q6-6. Among the advanced features of LangGraph, which do you think have the greatest engineering value?

Prioritize four categories of capabilities: streaming, persistence, time travel, and subgraphs. These four also happen to be the main line of LangGraph's advanced features.

First look at streaming. LangGraph's streaming is not just about "the model spitting out tokens bit by bit"; more importantly, it can stream the execution process of the entire graph. The commonly used `stream_mode` in real projects include:

- `values`: view the complete state snapshot after each step.
- `updates`: see which fields were actually changed in the current step.
- `messages`: view model message fragments or token streams.
- `custom`: actively push business progress within a node, such as "searching the knowledge base."

Next look at persistence. The `checkpointer` in LangGraph is closer to short-term memory within a thread or session, suitable for saving graph state by `thread_id`, used for checkpoint recovery, human-machine collaboration, and carrying over multi-turn tasks; if you need to save longer-term information across threads and sessions, that is closer to the Store direction.

The engineering value of time travel lies mainly in troubleshooting, post-incident review, and replay. Many complex Agents don't produce a wrong final result; rather, the state at some intermediate step gets contaminated. Time Travel lets you look back from a specific node or even rerun it.

Subgraphs, on the other hand, are valuable because they break a complex system into reusable modules. For example, a "retrieval subgraph," an "approval subgraph," and a "report generation subgraph" can each be encapsulated independently, while the main graph only handles higher-level orchestration.

These four capabilities can be summarized in one sentence: streaming addresses observability, persistence addresses recoverability, time travel addresses reviewability, and subgraphs address maintainability. Only with all four together does LangGraph truly resemble production infrastructure, rather than just a demo graph that can run end to end.

**Common follow-up questions:**

- What is the difference between a checkpointer and long-term memory?
- What scenarios are suitable for time travel?
- When should you break out a subgraph?

**Importance:**`中频` (occurrences: 1) | **Difficulty:**`较难`

**What is being assessed:** whether you care about real production capability, not just knowing how to write a HelloWorld.

**Corresponding sections:** [25 LangGraph Advanced Features §1. Streaming](25-LangGraph%E9%AB%98%E7%BA%A7%E7%89%B9%E6%80%A7.md#_1-streaming); [25 LangGraph Advanced Features §2. State Persistence](25-LangGraph%E9%AB%98%E7%BA%A7%E7%89%B9%E6%80%A7.md#_2-state-persistence); [25 LangGraph Advanced Features §3. Time Travel](25-LangGraph%E9%AB%98%E7%BA%A7%E7%89%B9%E6%80%A7.md#_3、时间回溯%EF%BC%88time-travel%EF%BC%89); [25 LangGraph Advanced Features §4. Subgraphs](25-LangGraph%E9%AB%98%E7%BA%A7%E7%89%B9%E6%80%A7.md#_4、子图%EF%BC%88subgraphs%EF%BC%89)

### Q6-7. How can Checkpoint, HITL, and Time Travel be explained in a more engineering-oriented way during interviews?

These three concepts are best understood together, because they jointly address the fact that **a complex Agent is not just about "getting it to run"; it also needs to be able to pause, observe, review, and continue.**

- Checkpoint: addresses whether a task can recover after being partially completed, and is suitable for long-running tasks, resuming from a checkpoint, and failure replay.
- HITL: addresses whether high-risk actions require human approval, and is suitable for human confirmation before actions such as payments, data deletion or modification, and sending messages externally.
- Time Travel: addresses how to look back and review after something goes wrong, and is suitable for troubleshooting, debugging, and rerunning specific stages.

If we summarize this in a very engineering-oriented way, it is:

> Checkpoint is responsible for recoverability, HITL for controllability, and Time Travel for reviewability.

When these three capabilities are presented together, interviewers usually get the impression that what you understand is not just "whether you can draw a graph," but "how to govern the system after it goes live."

**Common follow-up questions:**

- Which nodes would you definitely add human approval to?
- How do you explain the boundary between a checkpointer and long-term memory / Store?
- When is time travel merely a debugging tool, and when is it already a production necessity?

**Importance:**`中频` (occurrences: 1) | **Difficulty:**`较难`

**What is being assessed:** understanding of LangGraph production capability, as well as the ability to summarize the three categories of recovery, approval, and review.

**Corresponding sections:** [25 LangGraph Advanced Features §2. State Persistence](25-LangGraph%E9%AB%98%E7%BA%A7%E7%89%B9%E6%80%A7.md#_2-state-persistence); [25 LangGraph Advanced Features §3. Time Travel](25-LangGraph%E9%AB%98%E7%BA%A7%E7%89%B9%E6%80%A7.md#_3、时间回溯%EF%BC%88time-travel%EF%BC%89)

---

## 7. Memory, MCP, and Multi-Agent

### Q7-1. What is the relationship among context window, short-term memory, and long-term memory?

The context window is the upper limit of content the model can see in a single inference, short-term memory is session-level state, and long-term memory is user or task information retained across sessions.

In engineering terms, these three cannot be conflated. The window is an expensive resource and cannot be endlessly stuffed with history. Short-term memory generally retains task-relevant history, summaries, and thread state for the current task. Long-term memory is better suited for storing preferences, profiles, historical conclusions, and reusable facts, and needs to be retrieved on demand rather than being dumped into the prompt in full every time.

Therefore, a mature system usually works like this: only high-signal context goes into the window, short-term memory ensures continuity within the current thread, and long-term memory is recalled on demand from a database or vector store.

**Common follow-up questions:**

- What is the difference between memory and RAG?
- Why is memory not the same as training the model?
- What is Redis suitable for in a memory system?
- If the context becomes too long and gets truncated, would you choose a sliding window, summary compression, or retrieval-based supplementation? How do you decide?

**Importance:**`必刷` (occurrences: 3) | **Difficulty:**`中等`

**What is being assessed:** state design capability for conversational systems and Agents.

**Corresponding sections:** [16 Memory and Conversation History §1. Introduction to Memory](16-%E8%AE%B0%E5%BF%86%E4%B8%8E%E5%AF%B9%E8%AF%9D%E5%8E%86%E5%8F%B2%EF%BC%88%E5%90%ABRedis%E5%9F%BA%E7%A1%80%EF%BC%89.md#_1-introduction-to-memory); [25 LangGraph Advanced Features §2. State Persistence](25-LangGraph%E9%AB%98%E7%BA%A7%E7%89%B9%E6%80%A7.md#_2-state-persistence)

### Q7-2. How do you design short-term memory and long-term memory systems for an Agent? How are they typically implemented technically?

First, split "memory" into two layers; otherwise it is very easy to stuff all information into the context, which ultimately becomes both expensive and messy.

- Short-term memory: addresses continuity within the current session or current thread. Its core is "read history -> assemble into prompt -> call model -> write history back."
- Long-term memory: addresses retaining user preferences, profiles, historical conclusions, and reusable facts across sessions. Its core is "store structured information and recall it on demand," rather than stuffing everything into the prompt every round.

Technically, a common approach to short-term memory is to persist message history or thread state in memory, Redis, or a checkpointer, and then re-inject it in the next round through `MessagesPlaceholder` or graph state. Long-term memory is better placed in a database, vector store, or, in scenarios where relationships matter a great deal, a knowledge graph. A relatively solid engineering approach is: short-term memory serves continuity for the current task, long-term memory serves reuse across tasks, and the two are designed separately.

In the LangChain / LangGraph ecosystem, `RunnableWithMessageHistory + BaseChatMessageHistory` is better understood as "conversation history injection," while LangGraph persistence / checkpointer is better understood as thread-level state persistence. The former is better for first explaining clearly "how historical messages are read and written," while the latter is better suited for Agents, graph orchestration, and thread-level state management.

Therefore, in actual implementation, the division is usually as follows:

- Chat assistants or lightweight multi-turn Q&A: prefer the message history approach.
- Complex Agents or LangGraph: prefer the `thread_id + checkpointer` approach.
- Cross-session preferences, facts, and user profiles: use long-term storage and retrieve on demand, rather than directly forcing them into the context.

If the follow-up question is "how do you maintain continuity while saving tokens in very long multi-turn conversations," four common techniques are usually added:

- Sliding window: keep only the most recent N turns of original text. Simple and direct, but it is easy to lose early constraints.
- Periodic summarization: compress history into a structured summary every few turns, preserving goals, confirmed facts, pending items, and preferences.
- Retrieval-based supplementation: write old conversations into a vector store or long-term storage, and recall relevant fragments based on the current question, rather than stuffing all old messages back into the window.
- Structured memory slots: fixed information such as city, membership tier, preferences, and key states should be stored directly in key-value stores or databases, so the model does not have to "recall" them every time.

Therefore, a memory system is not about "the more history is saved, the better," but about distinguishing what should be kept as-is, what should be summarized, what should be structured, and what should be retrieved on demand.

**Common follow-up questions:**

- How do you understand the respective positioning of `RunnableWithMessageHistory` and LangGraph persistence / checkpointer?
- Is Redis better suited for short-term memory persistence or long-term memory?

**Importance:**`高频` (occurrences: 2) | **Difficulty:**`较难`

**What is being assessed:** memory layering design capability, as well as understanding of the boundaries among short-term state, long-term knowledge, and external storage.

**Corresponding sections:** [16 Memory and Conversation History §4. RunnableWithMessageHistory and BaseChatMessageHistory](16-%E8%AE%B0%E5%BF%86%E4%B8%8E%E5%AF%B9%E8%AF%9D%E5%8E%86%E5%8F%B2%EF%BC%88%E5%90%ABRedis%E5%9F%BA%E7%A1%80%EF%BC%89.md#_4、实现类介绍：runnablewithmessagehistory-与-basechatmessagehistory); [25 LangGraph Advanced Features §2. State Persistence](25-LangGraph%E9%AB%98%E7%BA%A7%E7%89%B9%E6%80%A7.md#_2-state-persistence)

### Q7-3. What is MCP? What core problem does it solve? How does it differ from Tool, RAG, and Agent?

If we start with a definition, MCP is the Model Context Protocol. It is an open standard that specifies how AI applications can connect to external tools, resources, and prompt templates in a unified way.

In essence, MCP is a "unified protocol layer for accessing model capabilities." The problem it solves is not "whether a model can call tools," but "how different AI applications can access external tools, resources, and context in a unified way."

To understand it more intuitively, MCP is best viewed as a unified socket for the AI world. What it unifies is not the model itself, but the way Host, Client, and Server discover, expose, and invoke capabilities. MCP Server does not only expose Tools; it can also expose Resources and Prompts.

- Tool / Function Calling: solves how the model expresses "which tool I want to call and what parameters to pass."
- RAG: solves how the model obtains external knowledge.
- Agent: solves who plans, decides, and invokes these capabilities.
- MCP: solves how these external capabilities are exposed and integrated in a standardized way.

Therefore, MCP is not equal to Agent, nor is it equal to Tool. It leans more toward the protocol and ecosystem layer, and its value lies in exposing once and reusing everywhere, unified schemas, and lower integration costs.

**Common follow-up questions:**

- What capabilities does an MCP Server typically expose?
- How do you choose between STDIO and HTTP transport?
- Why do enterprises care about MCP?

**Importance:**`高频` (occurrences: 1) | **Difficulty:**`中等`

**What is being assessed:** protocol-layer understanding.

**Corresponding sections:** [20 MCP Model Context Protocol §2. Introduction to MCP](20-MCP%E6%A8%A1%E5%9E%8B%E4%B8%8A%E4%B8%8B%E6%96%87%E5%8D%8F%E8%AE%AE.md#_2-introduction-to-mcp); [20 MCP Model Context Protocol §3. What MCP Can Do](20-MCP%E6%A8%A1%E5%9E%8B%E4%B8%8A%E4%B8%8B%E6%96%87%E5%8D%8F%E8%AE%AE.md#_3-what-mcp-can-do)

**Source:** Tencent AI backend engineer first-round interview (actual large-company interview question)

### Q7-4. What is the relationship between MCP and Function Calling?

Function Calling is closer to a "structured invocation mechanism" on the model side, while MCP is closer to a "unified capability integration protocol" on the application side.

The former solves how the model expresses "which function to call and what parameters to pass"; the latter solves how different external tools, resources, and prompt templates are exposed to clients under a unified standard. The two are not替代关系, but rather upper-layer and lower-layer relationship.

It can be understood simply as: Function Calling is closer to model decision-making, while MCP is closer to ecosystem integration and protocol standardization. In actual implementation, an Agent can absolutely continue to use Function Calling for invocation decisions on top of the capabilities exposed by MCP.

**Importance:**`高频` (occurrences: 1) | **Difficulty:**`中等`

**What is being assessed:** understanding of the boundary between the protocol layer and the invocation mechanism.

**Corresponding sections:** [20 MCP Model Context Protocol §2. Introduction to MCP](20-MCP%E6%A8%A1%E5%9E%8B%E4%B8%8A%E4%B8%8B%E6%96%87%E5%8D%8F%E8%AE%AE.md#_2-introduction-to-mcp); [17 Tools and Tool Calling §2. How Tool Calling Works](17-Tools%E5%B7%A5%E5%85%B7%E8%B0%83%E7%94%A8.md#_2-how-tool-calling-works)

### Q7-5. How does MCP achieve cross-platform compatibility?

MCP's cross-platform compatibility essentially comes from "unifying the protocol, not the implementation."

That is to say, different platforms, different languages, and different host programs can interoperate at the protocol layer as long as they all follow the same message structure, capability exposure method, and invocation conventions. In this way, clients do not need to write a separate private integration method for every external system, and servers can expose capabilities according to the standard.

Therefore, MCP's value does not lie in being tied to any particular technology stack, but in converging integration differences into a unified protocol surface.

**Importance:** `中频` (occurrences: 1 time) | **Difficulty:** `中等`

**Assessment point:** Understanding of protocol standardization.

**Corresponding section:** [20 MCP Model Context Protocol §5, MCP Architecture Knowledge](20-MCP%E6%A8%A1%E5%9E%8B%E4%B8%8A%E4%B8%8B%E6%96%87%E5%8D%8F%E8%AE%AE.md#_5-mcp-architecture-knowledge)

### Q7-6. What is the main content of the MCP technical protocol?

If expanded from the protocol layer, the main content of MCP is clearest when described in four layers:

- Participating roles: Host, Client, Server.
- Capability types: Tools, Resources, Prompts.
- Communication mechanisms: capability discovery, requests, responses, errors, notifications.
- Transport methods: stdio, Streamable HTTP, and other channels that carry the protocol.

One more detail needs to be added here:

- Tools lean more toward model-controlled, suitable for letting the model automatically decide whether to call them.
- Resources lean more toward application-driven, usually with the host deciding how to incorporate them into context.
- Prompts lean more toward user-controlled, suitable for reusing prompt templates or workflow templates.

By answering this way, interviewers can usually tell that you understand the protocol itself, rather than just treating MCP as some ready-made plugin marketplace.

**Importance:** `中频` (occurrences: 1 time) | **Difficulty:** `中等`

**Assessment point:** Whether you understand the basic composition of the MCP protocol layer.

**Corresponding section:** [20 MCP Model Context Protocol §5, MCP Architecture Knowledge](20-MCP%E6%A8%A1%E5%9E%8B%E4%B8%8A%E4%B8%8B%E6%96%87%E5%8D%8F%E8%AE%AE.md#_5-mcp-architecture-knowledge); [20 MCP Model Context Protocol §3, What MCP Can Do](20-MCP%E6%A8%A1%E5%9E%8B%E4%B8%8A%E4%B8%8B%E6%96%87%E5%8D%8F%E8%AE%AE.md#_3-what-mcp-can-do)

### Q7-7. What is the MCP server development process?

A typical development process for an MCP Server usually looks like this:

1. Clarify the capability boundary to expose: tools, resources, or prompt templates.
2. Define input/output schemas and error handling.
3. Choose the transport method, such as STDIO or HTTP.
4. Implement the server-side logic and fill in authentication, logging, timeout, and exception handling.
5. Complete registration, discovery, invocation, and integration testing on the client side.

In engineering terms, what is most easily overlooked is the capability boundary and error handling. An MCP Server is not simply wrapping an existing API with a shell; the capabilities must be designed as interfaces truly suitable for model consumption.

**Importance:** `中频` (occurrences: 1 time) | **Difficulty:** `中等`

**Assessment point:** Whether you understand that MCP is not only about "using it" but also includes server-side construction.

**Corresponding section:** [20 MCP Model Context Protocol §4, How to Use MCP](20-MCP%E6%A8%A1%E5%9E%8B%E4%B8%8A%E4%B8%8B%E6%96%87%E5%8D%8F%E8%AE%AE.md#_4-how-to-use-mcp); [20 MCP Model Context Protocol §6, Case Study: Local MCP Weather Service and Client](20-MCP%E6%A8%A1%E5%9E%8B%E4%B8%8A%E4%B8%8B%E6%96%87%E5%8D%8F%E8%AE%AE.md#_6-hands-on-case-study-local-mcp-weather-service-and-client)

### Q7-8. How should an Agent integrate MCP tools?

The core of integrating MCP tools into an Agent is incorporating the capabilities exposed by MCP into its own tool registration and scheduling system.

The usual approach is:

- First discover the tools or resources exposed by the MCP Server.
- Then convert these capabilities into tool descriptions and schemas that the Agent can consume.
- At execution time, let the model decide when to call them, with the host responsible for actually initiating the MCP request.
- Return the result to the Agent and enter the next round of decision-making.

The real key is not "getting connected", but "ensuring controllability after connection", including permissions, timeouts, retry on failure, observability, and auditing.

**Common follow-up questions:**

- In your architecture, does MCP only perform permission checks, or does it also work together with environment-level security sandboxes?
- If you already have MCP, why do you still need containers, read-only mounts, or system-level isolation?

**Importance:** `中频` (occurrences: 1 time) | **Difficulty:** `中等`

**Assessment point:** How Agent architecture combines with MCP.

**Corresponding section:** [20 MCP Model Context Protocol §4, How to Use MCP](20-MCP%E6%A8%A1%E5%9E%8B%E4%B8%8A%E4%B8%8B%E6%96%87%E5%8D%8F%E8%AE%AE.md#_4-how-to-use-mcp); [20 MCP Model Context Protocol §6, Case Study: Local MCP Weather Service and Client](20-MCP%E6%A8%A1%E5%9E%8B%E4%B8%8A%E4%B8%8B%E6%96%87%E5%8D%8F%E8%AE%AE.md#_6-hands-on-case-study-local-mcp-weather-service-and-client)

### Q7-9. What is the core advantage of MCP's streaming HTTP transport?

The core value of streaming HTTP is that results can be returned incrementally as they are produced, rather than having to wait for the entire call to finish before returning everything at once.

This brings three direct benefits:

- Lower time-to-first-token latency, giving users faster feedback.
- Support for mid-progress reporting in long-running tasks, reducing the feeling of being stuck.
- Easier for the host to handle cancellation, timeouts, and partial result processing.

For Agent or research-oriented tasks, this capability is especially important, because many calls are not "instantaneous" by nature.

**Importance:** `中频` (occurrences: 1 time) | **Difficulty:** `中等`

**Assessment point:** Understanding of the value of streaming protocols in terms of experience and concurrency.

**Corresponding section:** [20 MCP Model Context Protocol §5, MCP Architecture Knowledge](20-MCP%E6%A8%A1%E5%9E%8B%E4%B8%8A%E4%B8%8B%E6%96%87%E5%8D%8F%E8%AE%AE.md#_5-mcp-architecture-knowledge)

### Q7-10. How does MCP invocation ensure concurrency?

MCP concurrency capability is not determined by the protocol alone; it depends more on how the host and server design the request processing model.

To ensure concurrency, you typically need to pay attention to:

- Whether requests have unique identifiers to avoid response mismatching.
- Whether the server supports parallel processing rather than serial blocking.
- Whether tool execution has timeout, rate limiting, and priority control.
- Whether the client can correctly manage multiple request contexts.

If the underlying tool itself is very slow, no matter how good the protocol is, it cannot save the situation, so concurrency governance must be designed across three layers together: "protocol layer + service layer + tool layer".

**Importance:** `中频` (occurrences: 1 time) | **Difficulty:** `较难`

**Assessment point:** Protocol and host design capability under high-concurrency invocation.

**Corresponding section:** [20 MCP Model Context Protocol §5, MCP Architecture Knowledge](20-MCP%E6%A8%A1%E5%9E%8B%E4%B8%8A%E4%B8%8B%E6%96%87%E5%8D%8F%E8%AE%AE.md#_5-mcp-architecture-knowledge)

### Q7-11. What is the difference between A2A and MCP? When do you need multi-agent systems?

MCP focuses more on "how models connect with external capabilities", while A2A focuses more on "how Agents collaborate with each other".

The former leans toward tool and resource access standards, while the latter leans toward multi-agent communication and division of labor. If the system only needs to connect to search, databases, or file systems, MCP's value is more obvious; if the system has already evolved into multiple Agents with clear roles and separated responsibilities, such as planning, retrieval, execution, and review as independent roles, then A2A or multi-agent orchestration becomes meaningful.

Multi-agent is not "the earlier the better". If a task can be clearly handled by a single Agent, multi-agent only increases communication, debugging, and governance costs. Splitting is worthwhile only when role boundaries are clear, a single Agent's prompt is already overloaded, and the process truly requires role-based division.

**Common follow-up questions:**

- How do you choose between Supervisor and Handoff?
- What are the most common failure points in multi-agent systems?
- Under what circumstances is a Skill more appropriate than an independent Agent?
- What exactly is the boundary between A2A and in-application orchestration frameworks like LangGraph, or ordinary Agent frameworks?
- How should the boundary between Agent Skills, Tools, and independent Agents be understood? When is it more suitable to make something a Skill rather than splitting off another Agent?

**Importance:** `中频` (occurrences: 1 time) | **Difficulty:** `较难`

**Assessment point:** Protocol boundary and system decomposition capability.

**Corresponding section:** [26 LangGraph Multi-Agent and A2A §1, A2A Protocol and Multi-Agent Architecture](26-LangGraph%E5%A4%9A%E6%99%BA%E8%83%BD%E4%BD%93%E4%B8%8EA2A.md#_1、a2a-协议与多智能体架构); [26 LangGraph Multi-Agent and A2A §2, Supervisor and Handoff](26-LangGraph%E5%A4%9A%E6%99%BA%E8%83%BD%E4%BD%93%E4%B8%8EA2A.md#_2-supervisor-and-handoff); [26 LangGraph Multi-Agent and A2A §3, Skills and the Boundary of Multi-Agent](26-LangGraph%E5%A4%9A%E6%99%BA%E8%83%BD%E4%BD%93%E4%B8%8EA2A.md#_3-the-boundary-between-skills-and-multi-agent-systems); [27 Agent Skills: Agent Skills and AI Programming Tool Practices](../../27-Agent%20Skills%E6%99%BA%E8%83%BD%E4%BD%93%E6%8A%80%E8%83%BD%E4%B8%8EAI%E7%BC%96%E7%A8%8B%E5%B7%A5%E5%85%B7%E5%AE%9E%E8%B7%B5.md)

**Source:** Tencent AI Backend Engineer First Round (actual large-company interview question)

### Q7-12. What popular MCP tools are there?

Commonly discussed MCP tools typically fall into a few categories:

- Browser automation, such as Playwright.
- Data and backend, such as databases and services like Supabase.
- Files and code, such as local file systems and code repositories.
- Search and knowledge, such as web search and knowledge base retrieval.

In interviews, what matters more is not memorizing all the names, but knowing why these tools are popular: because they cover the most common external capability needs of Agents.

**Importance:** `低频` (occurrences: 1 time) | **Difficulty:** `基础`

**Assessment point:** Basic understanding of the MCP ecosystem, without requiring rote memorization.

---

## 8. Platform Practice and Framework Selection: Coze, Dify, RAGFlow

### Q8-1. How should we understand the relationship between platforms like Coze / Dify and LangChain / LangGraph?

Coze / Dify lean more toward the application layer, low-code, and visual delivery, while LangChain / LangGraph lean more toward code-level development frameworks. They are not substitutes for each other, but different layers on the same AI application chain.

If understood from this layered relationship:

- Dify / Coze are better suited for quickly assembling Agent, RAG, and Workflow, making it easier for business-side validation, collaboration, and delivery.
- LangChain is better suited for combining components such as Prompt, Model I/O, Parser, Retriever, and Tools in a code-based way.
- LangGraph is better suited for complex orchestration with explicit state, loops, conditional routing, human-in-the-loop collaboration, and multi-agent scenarios.

Therefore, platforms are closer to the "application building layer", while code frameworks are closer to the "underlying orchestration layer". A very common path in real projects is: first use a platform to validate business value, then migrate the core chain to a code framework; or let the platform handle upper-layer business orchestration while underlying complex capabilities are undertaken by self-built services.

**Importance:** `高频` (occurrences: 1 time) | **Difficulty:** `中等`

**Assessment point:** Selection judgment between platform capabilities and code capabilities.

**Corresponding section:** [3 Agent Development Based on Coze & Dify Platforms §1, Overview of Intelligent Agents (AI Agent)](3-%E5%9F%BA%E4%BA%8ECoze&Dify%E5%B9%B3%E5%8F%B0%E7%9A%84%E6%99%BA%E8%83%BD%E4%BD%93%E5%BC%80%E5%8F%91.md#_1、智能体ai-agent概述); [9 LangChain Overview and Architecture §2, LangChain Positioning](9-LangChain%E6%A6%82%E8%BF%B0%E4%B8%8E%E6%9E%B6%E6%9E%84.md#_2-positioning-of-langchain)

### Q8-2. How should one choose among various Agent development frameworks?

Framework selection should not be based on popularity, but on task complexity, team capability, and delivery requirements.

- If the goal is rapid prototyping, a rich ecosystem, and comprehensive common components, LangChain is very suitable.
- If the task involves explicit state, loops, conditional routing, human-in-the-loop collaboration, or multi-agent, LangGraph is more suitable.
- If low-code and rapid validation of business processes are needed, Coze / Dify are more suitable.
- If the system boundary is simple and requirements are very clear, writing an SDK directly may also be the lowest-cost option.

A more mature answer is not simply comparing "which is best", but explaining "what scenario makes which choice more cost-effective". Being able to state alternatives and migration paths is usually more persuasive than simply praising a particular framework.

**Common follow-up questions:**

- What metrics will you ultimately use to judge whether this framework selection was successful?
- If you use a platform in the early stage and later migrate to a self-developed framework, how should the migration boundary be drawn?

**Importance:** `高频` (occurrences: 1 time) | **Difficulty:** `中等`

**Assessment point:** Framework selection and engineering judgment.

**Corresponding section:** [9 LangChain Overview and Architecture §2, LangChain Positioning](9-LangChain%E6%A6%82%E8%BF%B0%E4%B8%8E%E6%9E%B6%E6%9E%84.md#_2-positioning-of-langchain); [22 LangGraph Overview and Quick Start §1, LangGraph Introduction](22-LangGraph%E6%A6%82%E8%BF%B0%E4%B8%8E%E5%BF%AB%E9%80%9F%E5%85%A5%E9%97%A8.md#_1-introduction-to-langgraph)

### Q8-3. When is a workflow more appropriate than an Agent?

When business steps are fixed, the output format is clear, and you need strong control and easy auditability, workflows are usually more suitable than agents.

For example, classification, summarization, content moderation, report generation, form filling, and fixed approval chains are scenarios where the process path is typically stable. Using a workflow allows you to define node responsibilities, failure retries, human intervention points, and SLAs more clearly. Agents are more suited to open-ended tasks and dynamic decision-making, while workflows are better suited to the large number of rule-based, accountable, and replayable process-oriented tasks in enterprises.

**Common follow-up questions:**

- Which nodes in a workflow are suitable to be handled by an LLM?
- Where should human review checkpoints be added?
- How can a workflow gradually evolve into an agentic workflow?

**Importance:**`高频` (Occurrences: 1) | **Difficulty:**`中等`

**Examination focus:** Process governance awareness.

**Corresponding sections:** [3 Agent Development Based on the Coze & Dify Platforms §6, Building Workflows](3-%E5%9F%BA%E4%BA%8ECoze&Dify%E5%B9%B3%E5%8F%B0%E7%9A%84%E6%99%BA%E8%83%BD%E4%BD%93%E5%BC%80%E5%8F%91.md#_6-building-workflows); [21 Agents §1, Introduction to Agents](21-Agent%E6%99%BA%E8%83%BD%E4%BD%93.md#_1-introduction-to-agents)

### Q8-4. When calling Dify / Coze workflows with Python, what engineering details deserve the most attention?

The key is to focus on five categories of issues: authentication, parameter alignment, streaming mode, timeout limits, and log tracing.

Let's start with Dify. The key fields of its workflow API are usually:

- `Authorization: Bearer {api_key}`
- The `inputs` in the request body
- `response_mode`
- `user`

There are two very easy pitfalls here: first, the API key is bound to the workflow, so you should not use a single global key everywhere; second, for long-running processes, try to use `streaming`, because `blocking` is easily interrupted by gateway timeouts. When actually implementing streaming, you need to be able to identify the `workflow_finished` in the SSE stream and correctly obtain the final `outputs`.

Now for Coze. You need to pay even closer attention to:

- `workflow_id`
- `app_id`
- `parameters`

Among these, `parameters` must strictly align with the input variables defined in the workflow. If any variable name does not match, the code may appear to run and the request may even succeed, but the business result will be wrong. For streaming, you need to be able to distinguish `PING`, `MESSAGE`, `DONE`, or the `MESSAGE / ERROR / INTERRUPT` events in the SDK.

To summarize from an engineering perspective, the key points to examine are:

- Whether the binding relationships among keys, workflows, and applications are clearly understood.
- Whether request parameter names strictly match the platform workflow inputs.
- Whether streaming is used by default instead of compressing long tasks into blocking calls.
- Whether platform logs, `workflow_run_id`, and business `request_id` are connected end to end.
- If the process has external side effects, whether idempotency, retries, and failure compensation are properly implemented.

What this question really tests is not "whether you can send a POST request," but whether you truly understand the real invocation chain of the platform API.

**Common follow-up questions:**

- How do you choose between streaming and blocking responses?
- What troubleshooting problems can platform logs solve?
- How do platform workflows and self-built backend services collaborate?

**Importance:**`中频` (Occurrences: 1) | **Difficulty:**`中等`

**Examination focus:** Whether you have looked at the real invocation chain of the platform API, rather than only being able to use the interface.

**Corresponding sections:** [4 Calling Dify Platform Workflows with Python §4, Request Format](4-Python%E8%B0%83%E7%94%A8Dify%E5%B9%B3%E5%8F%B0%E5%B7%A5%E4%BD%9C%E6%B5%81.md#_4、请求格式); [5 Calling Coze Platform Workflows with Python §3, Calling Workflows through Python Code](5-Python%E8%B0%83%E7%94%A8Coze%E5%B9%B3%E5%8F%B0%E5%B7%A5%E4%BD%9C%E6%B5%81.md#_3-通过-python-代码调用工作流)

### Q8-5. How should you choose an open-source RAG platform like RAGFlow? How does it compare with Dify or a self-built pipeline?

Do not answer this question as "which one is stronger." Instead, answer it as "what does the current knowledge base scenario need most?"

If the focus is document import, parsing, chunking, retrieval, and RAG orchestration experience, then platforms like RAGFlow are quite attractive; if the focus is multiple types of agents, workflows, plugin ecosystems, and business API orchestration, platforms like Dify / Coze have broader boundaries; if the core pipeline involves deep customization, complex state governance, compliance auditing, and tight coupling with internal systems, a self-built code pipeline is usually more stable.

When actually making a platform selection, prioritize four categories of factors: document import and parsing quality, permission and multi-tenant capabilities, ease of integration with business systems, and room for secondary development. Many projects do not get stuck on "whether RAG can be done," but on "whether parsing quality is stable, whether permissions can be enforced, and whether it can later be integrated into enterprise systems."

**Importance:**`中频` (Occurrences: 1) | **Difficulty:**`中等`

**Examination focus:** RAG platform selection judgment, as well as awareness of the boundary between platform capabilities and self-built capabilities.

---

## 9. Security, Evaluation, Deployment, and Observability

### Q9-1. How would you evaluate the effectiveness of a RAG or Agent system?

Evaluation should first be split into **offline evaluation** and **online evaluation**, and then the problem should be broken down to specific levels, rather than focusing only on a single overall score.

For RAG, it is usually viewed at two levels:

- Retrieval layer: whether relevant content was recalled, whether the cited passages are correct, and whether bad cases are stuck in chunking, recall, reranking, or filtering.
- Generation layer: whether the answer is faithful to the evidence, whether citations are correct, whether it can refuse to answer when there is no basis, and whether the final answer is actually helpful to the business.

For agents, evaluation should be divided into two categories:

- Trajectory-level evaluation: whether the right tools were selected, whether parameters were correct, whether there were ineffective loops, and whether it ended prematurely.
- Outcome-level evaluation: whether the final task was completed, and whether output quality and user experience met the standard.

Online evaluation looks at user satisfaction, escalation-to-human rate, task interruption rate, latency, and the distribution of bad case types. For agents, also look at tool invocation success rate, retry rate, loop count, and the proportion of human fallback.

For automated evaluation, you usually should not rely on only one approach. Instead, combine rule-based evaluation, `LLM-as-a-judge`, and manual sampling. Rule-based and LLM evaluation are suitable for scaling up and doing regression, while manual sampling is responsible for catching high-risk misjudgments and evaluation drift.

More importantly, evaluation should not only tell you that "the score went down," but also be able to identify which layer went wrong. For example, poor recall, poor context assembly, generation hallucinations, tool failures, and unreasonable termination conditions all require completely different fixes.

A more recommended evaluation loop is: **first build layered metrics, then accumulate bad cases, and finally let the bad cases drive iteration of prompts, retrieval, tools, and processes in return.**

**Common follow-up questions:**

- What are frameworks like RAGAS suitable for?
- How do you build a bad case dataset?
- How should automated evaluation and manual evaluation work together?

**Importance:**`必刷` (Occurrences: 2) | **Difficulty:**`较难`

**Examination focus:** Whether there is awareness of an evaluation feedback loop.

**Corresponding sections:** [19 RAG Retrieval-Augmented Generation §3, RAG Comprehensive Case: Intelligent Operations Assistant](19-RAG%E6%A3%80%E7%B4%A2%E5%A2%9E%E5%BC%BA%E7%94%9F%E6%88%90.md#_3-comprehensive-rag-case-intelligent-operations-assistant); [21 Agents §5, Hands-On Practice and Cases](21-Agent%E6%99%BA%E8%83%BD%E4%BD%93.md#_5-hands-on-practice-and-case-studies)

### Q9-2. What is "hallucination"? How should it be mitigated at the application layer?

Hallucination is not just "complete nonsense." More commonly, it is "things that look very real, but the details, citations, timestamps, permission scope, or tool results have already drifted."

Therefore, hallucination should not be treated purely as a model problem, but rather as a systemic problem across the entire pipeline. A relatively reliable mitigation approach usually has four layers:

- Knowledge layer: use RAG, external retrieval, citations, and refusal to answer without evidence, to make the model answer based on evidence as much as possible.
- Execution layer: hand over tasks such as calculations, database queries, sending messages, and checking orders to tools, and do not let the model fabricate results in plain text.
- Constraint layer: use structured output, schema validation, key field rule validation, and low-temperature strategies to reduce cases where "the format is correct but the content is wrong."
- Governance layer: implement bad case feedback loops, manual sampling, online monitoring, and degradation. Do not treat "the model will probably be fine" as a launch condition.

In summary: hallucination is very difficult to completely eliminate. The engineering goal is not to "guarantee that errors never occur," but to make it **discoverable, constrainable, rollback-able, and reviewable**.

**Common follow-up questions:**

- Why cannot RAG completely eliminate hallucination?
- What does "has citations but is still unfaithful" mean?
- Are hallucination and prompt injection the same thing?

**Importance:**`高频` (Occurrences: 2) | **Difficulty:**`中等`

**Examination focus:** Whether the boundary between "model capability issues" and "application pipeline governance issues" is understood.

**Corresponding sections:** [19 RAG Retrieval-Augmented Generation §1, Introduction to RAG](19-RAG%E6%A3%80%E7%B4%A2%E5%A2%9E%E5%BC%BA%E7%94%9F%E6%88%90.md#_1-introduction-to-rag); [14 Output Parsers §4, Structured Output](14-%E8%BE%93%E5%87%BA%E8%A7%A3%E6%9E%90%E5%99%A8.md#_4-structured-output)

### Q9-3. In multi-user scenarios, how do you implement security sandbox isolation for agents?

If an agent is only a single-machine demo, many risks will not surface; but once it enters a multi-user scenario, security isolation must be elevated from "tool permissions" to "execution environment isolation."

A more robust solution is usually divided into three layers:

- Environment layer: use Docker or other containers to isolate each task or tenant, and restrict CPU, memory, network, and file system access scope.
- System layer: combine seccomp, AppArmor, a read-only root directory, a temporary working directory, and a non-root user to avoid directly touching the host machine.
- Application layer: apply whitelists and auditing to tools, file access, system commands, and external connections, so that the model does not get raw permissions.

If code execution, commands, or file reading are required, you usually should not rely solely on prompts or business code for restrictions. Instead, mount the working directory as a least-privilege space, do not mount sensitive directories, and do not put database keys or host credentials into the container. MCP or tools are responsible for "whether it can be called," while the sandbox is responsible for "even if it is called, it cannot run out of bounds." The two have different responsibilities, and it is best to deploy both together.

**Importance:**`高频` (Occurrences: 2) | **Difficulty:**`较难`

**Examination focus:** Security isolation design for multi-user agents, as well as the division of labor between protocol-layer control and environment-layer isolation.

**Corresponding sections:** [7 Enterprise-Level LLM Deployment §1, Overview of Enterprise-Level LLM Deployment](7-%E4%BC%81%E4%B8%9A%E7%BA%A7%E5%A4%A7%E6%A8%A1%E5%9E%8B%E9%83%A8%E7%BD%B2.md#_1-overview-of-enterprise-level-large-model-deployment); [17 Tool Calling §6, From Course Cases to Real Projects](17-Tools%E5%B7%A5%E5%85%B7%E8%B0%83%E7%94%A8.md#_6-from-course-examples-to-real-projects)

### Q9-4. What metrics are involved in agent deployment and operations?

Agent operations should look at at least five categories of metrics:

- Effectiveness metrics: task completion rate, user satisfaction, citation accuracy.
- Performance metrics: first token latency, end-to-end latency, P95/P99.
- Stability metrics: invocation success rate, timeout rate, retry rate, failure rate.
- Cost metrics: token consumption, tool invocation cost, average cost per task.
- Governance metrics: human takeover rate, audit log completeness, efficiency of reviewing abnormal tasks.

For multi-tool, multi-step agents, also look at the success rate and bottleneck distribution of each step. Otherwise, you will only know that "it ultimately failed," without knowing at which layer the failure occurred.

**Importance:**`高频` (Occurrences: 1) | **Difficulty:**`中等`

**Examination focus:** An operations perspective from demo to production.

**Corresponding sections:** [7 Enterprise LLM Deployment §1, Enterprise LLM Deployment Overview](7-%E4%BC%81%E4%B8%9A%E7%BA%A7%E5%A4%A7%E6%A8%A1%E5%9E%8B%E9%83%A8%E7%BD%B2.md#_1-overview-of-enterprise-level-large-model-deployment); [21 Agent Intelligence §5, Hands-on and Case Studies](21-Agent%E6%99%BA%E8%83%BD%E4%BD%93.md#_5-hands-on-practice-and-case-studies)

### Q9-5. What challenges might a RAG system face in actual deployment?

Once RAG truly goes live, the difficulty is usually not whether it can retrieve, but whether this complete chain from indexing to answering can remain stable over the long term.

The first thing to emphasize here is that RAG is not a single-point capability, but an engineering chain consisting of an "indexing stage + retrieval and generation stage." Many online issues are essentially caused by a problem in one layer of these two stages.

First, break the challenges into six categories:

- Data side: document parsing quality, chunking strategy, table and PDF handling, knowledge update timeliness. If the source data is dirty and chunking is unreasonable, both downstream retrieval and generation will be dragged down.
- Retrieval side: embedding selection, recall quality, hybrid retrieval, reranking effectiveness, metadata filtering. Many systems seem able to answer offline, but once scaled online, the problems of "inaccurate recall, too much noise, missing key fragments" are exposed.
- Generation side: context assembly, citation traceability, faithfulness control, refusal strategies. RAG does not mean "no hallucination as long as retrieval is done." If context stitching is poor, the prompt is weak, and citations are unclear, the model will still make things up.
- Governance side: permission isolation, version management, citation traceability, knowledge rollback. What enterprises fear most is not a wrong answer, but answering content beyond permissions, or giving an answer without being able to explain where the basis came from.
- Evaluation side: badcase construction, offline evaluation, and closed-loop online metrics. Without evaluation, it is hard to know whether the problem actually lies in chunking, recall, reranking, or generation.
- Engineering side: latency, cost, caching, observability, index rebuilding, and online operations. For example, when the knowledge base is updated, should it be fully rebuilt or incrementally updated? If queries are slow, is the bottleneck in retrieval, reranking, or the model? These all need to be examined separately.

Therefore, a more solid answer in an interview is not to simply say "deployment will involve many engineering issues," but to explicitly state that RAG is a complete chain from data ingestion, index construction, retrieval recall, to answer generation, and if any layer fails, the final answer will also fail.

**Common follow-up questions:**

- If the online performance of RAG is poor, which layer would you prioritize for troubleshooting?
- When the knowledge base is frequently updated, how do you handle index rebuilding and version rollback?

**Importance:** `高频` (occurrences: 1) | **Difficulty:** `较难`

**Assessment focus:** Whether the candidate has production-system thinking.

**Corresponding sections:** [19 RAG Retrieval-Augmented Generation §2, Core Knowledge of RAG Text Processing](19-RAG%E6%A3%80%E7%B4%A2%E5%A2%9E%E5%BC%BA%E7%94%9F%E6%88%90.md#_2-core-knowledge-of-rag-text-processing); [7 Enterprise LLM Deployment §1, Enterprise LLM Deployment Overview](7-%E4%BC%81%E4%B8%9A%E7%BA%A7%E5%A4%A7%E6%A8%A1%E5%9E%8B%E9%83%A8%E7%BD%B2.md#_1-overview-of-enterprise-level-large-model-deployment)

### Q9-6. How do you ensure that Agent behavior is safe, controllable, and aligned with human intent?

This cannot rely solely on the model itself being "smart enough" or "already aligned." SFT, RLHF / RLAIF at the model layer can only provide a baseline safety boundary. When truly deployed in applications, application-layer governance must also be added.

It is usually done across four layers:

- Model and prompt layer: use the System Message to clearly define roles, boundaries, safety rules, and refusal strategies.
- Tool and permission layer: do not give the model raw permissions. All tools must have schema constraints, authentication, parameter validation, and least-privilege exposure.
- Execution and workflow layer: set maximum steps, timeouts, human approval, escalation to humans, and failure fallbacks to avoid infinite loops and dangerous actions being executed directly.
- Observability and audit layer: retain call logs, traces, inputs and outputs, key decision points, and human review workflows.

If I add another layer from a production perspective, I would also include budget control and circuit breakers:

- Budget control: maximum tool invocation count, time budget, token budget, and cost budget.
- Circuit breaker mechanism: stop after consecutive failures, alert on abnormal error rates, and exit when repeated attempts make no progress.

The value of these mechanisms is not just about saving money, but more importantly about containing the risk that "the model may keep trying indefinitely."

To summarize at a higher level: model alignment solves the problem of "keep basic behavior from being too outrageous," while application governance solves the problem of "make sure nothing goes wrong inside your business system." A truly stable Agent must combine "model capability + permission boundaries + workflow control + human-machine collaboration," rather than relying on any single layer.

**Common follow-up questions:**

- If the model has already been aligned, why does the application layer still need so much security governance?
- Which actions would you require human approval for, rather than letting the Agent execute them directly?

**Importance:** `高频` (occurrences: 1) | **Difficulty:** `较难`

**Assessment focus:** Whether the candidate understands that "model alignment" and "application-layer security governance" are two complementary mechanisms.

### Q9-7. When an Agent chain takes a very long time, how do you locate the performance bottleneck?

If an Agent chain takes several minutes to run, you cannot simply say "the model is too slow." You need to first break down the time cost.

It is usually decomposed across these layers:

- Model layer: single inference time, time-to-first-token latency, output token length.
- Retrieval layer: recall, reranking, external search, and knowledge base request time.
- Tool layer: API latency, browser actions, code execution, waiting for external system responses.
- Orchestration layer: routing decisions, Supervisor decisions, repeated retries, serial waiting.
- Result layer: post-processing, validation, storage, and log writing.

A more reliable approach is to instrument traces and spans for each step, first look at where the wall time is spent, and then decide whether to switch models, modify the chain, reduce steps, or change serial execution to parallel. If LangGraph is used, I would also look at node-level time consumption, whether the flow repeatedly enters the same node, and whether it keeps going back and forth due to a lack of a clear completion signal.

Many five-minute tasks end up not being bottlenecked by a single model call, but by overly long multi-step chains, tool waits, repeated judgment by supervisor nodes, or repeated checks in the middle due to the absence of a clear success signal. In other words, performance problems are often not "the model is too slow," but rather that **state transitions and execution loops were not well designed**.

**Importance:** `高频` (occurrences: 1) | **Difficulty:** `较难`

**Assessment focus:** Agent performance troubleshooting ability, as well as the ability to break down long-chain latency into the model, tool, retrieval, and orchestration layers.

### Q9-8. How should intent recognition / task routing be done?

It needs to be emphasized first that this question is not the same as "model routing." Model routing is closer to "should this time use a large model or a small model," while intent recognition / task routing is closer to "should this request go through FAQ, RAG, Tool, Agent, Workflow, or be directly transferred to a human."

A more solid design usually has three layers:

- The first layer is target classification: first clearly define what routing endpoints the system has, such as chitchat, FAQ, knowledge Q&A, status queries, action execution, complex tasks, and human fallback.
- The second layer is the routing mechanism: use rules and keywords as a fallback for high-certainty scenarios first, and use classification models or LLMs for semantic judgment in ambiguous scenarios.
- The third layer is confidence governance: do not force a decision when confidence is low. Allow clarification, downgrading, or transfer to a human, and do not let the system continue running with a misjudgment.

In engineering, a "single-layer universal router" is usually not built. Instead, multi-level routing is preferred:

- First do business intent routing: determine whether this is FAQ, RAG, Tool, or Agent.
- Then do subdomain routing: for example, in customer service, further distinguish orders, refunds, tickets, and complaints.
- Finally do model routing: within a specific chain, decide whether to use a strong model or a lightweight model.

The advantage of this approach is that it is easier to govern and easier to evaluate. During evaluation, focus on routing accuracy, the proportion of low confidence, the cost of misrouting, clarification hit rate, and the final task completion rate of each routing branch.

**Common follow-up questions:**

- When is rule-based routing alone sufficient, and when must semantic classification be introduced?
- If a question simultaneously resembles both FAQ and a Tool invocation, how do you handle it?
- How do you prevent incorrect routing from derailing all subsequent chains?

**Importance:** `高频` (occurrences: 1) | **Difficulty:** `较难`

**Assessment focus:** Layered routing capability, practical intent recognition implementation, and the awareness of system design that connects FAQ / RAG / Tool / Agent into a unified entry point.

**Corresponding sections:** [17 Tools and Tool Calling §6, From Course Cases to Real Projects](17-Tools%E5%B7%A5%E5%85%B7%E8%B0%83%E7%94%A8.md#_6-from-course-examples-to-real-projects); [19 RAG Retrieval-Augmented Generation §3, Comprehensive RAG Case Study: Intelligent O&M Assistant](19-RAG%E6%A3%80%E7%B4%A2%E5%A2%9E%E5%BC%BA%E7%94%9F%E6%88%90.md#_3-comprehensive-rag-case-intelligent-operations-assistant)

### Q9-9. How would you implement observability for LLM applications?

At a minimum, three things must be achieved: **logs, metrics, and traces.** That is, you need to see how requests flow through the system, how long each step takes, where failures occur, how many tokens were used, and what was ultimately output.

Specifically, trace_id / request_id should be connected end-to-end, linking the entry request, Prompt version, model version, index version, retrieval results, tool calls, exception information, time consumption, and token usage. If LangChain / LangGraph is used, special attention should also be paid to node flow, state updates, human interruption points, retry counts, and final exit reasons.

For Agent systems, observability is especially important because many problems occur in intermediate steps, not at the moment of final output. Truly useful observability is not just "it reported an error at the end," but can tell you: **which node it got stuck at, why it retried, why it ended, and what state it saw at that time.**

**Importance:** `中频` (occurrences: 1) | **Difficulty:** `中等`

**Assessment focus:** Awareness of tracing, logging, and metrics.

### Q9-10. When controlling the cost of LLM applications, which layers would you prioritize?

Usually start from four layers: model, context, retrieval, and workflow.

- Model layer: tier high-end and low-end models, using strong models for large tasks and lightweight models for small tasks.
- Context layer: compress prompts, reduce ineffective history, and control output length.
- Retrieval layer: optimize recall and reranking, and reduce meaningless content entering the context window.
- Workflow layer: reduce unnecessary LLM invocations, and use rules wherever possible instead of relying entirely on models.

Many systems have high costs not because the models are too expensive, but because the chain design is too wasteful, such as indiscriminate full retrieval, overly long history stitching, repeated invocations of large models, and blind retries after tool failures.

**Common follow-up questions:**

- When should model routing be introduced?
- How do you balance cost and effectiveness?
- Which is more worth optimizing first, token cost or tool cost?

**Importance:** `中频` (occurrences: 1) | **Difficulty:** `中等`

**Assessment focus:** Cost optimization thinking.

**Corresponding sections:** [1-1 LLM Cognition and Engineering Overview §4, Engineering Implementation of LLMs (Overview)](1-1-%E5%A4%A7%E6%A8%A1%E5%9E%8B%E8%AE%A4%E7%9F%A5%E4%B8%8E%E5%B7%A5%E7%A8%8B%E6%A6%82%E8%A7%88.md#_4、大模型的工程实现%EF%BC%88概览%EF%BC%89); [7 Enterprise LLM Deployment §1, Enterprise LLM Deployment Overview](7-%E4%BC%81%E4%B8%9A%E7%BA%A7%E5%A4%A7%E6%A8%A1%E5%9E%8B%E9%83%A8%E7%BD%B2.md#_1-overview-of-enterprise-level-large-model-deployment)

### Q9-11. How should model routing be done?

The core of model routing is not "automatically finding the strongest model for all requests," but routing requests of different complexity and risk levels to the most appropriate chain.

A common approach has three layers:

- Intent routing: first determine whether this is FAQ, RAG, tool invocation, complex Agent, or something that should be directly transferred to a human.
- Complexity routing: simple classification, formatted extraction, and lightweight summarization should go to small models; multi-step planning, open-ended generation, and complex decision-making should go to large models.
- Cost routing: check the cache first for hot questions; if something can be resolved with rules, don't send it to the LLM; high-value users or high-risk tasks should be given budget for stronger models.

In real-world implementation, "routing" is usually not built purely on subjective rules; instead, it is tuned together with evaluation and online data:

- Look at the completion rate, latency, and per-task cost of different routing branches.
- Check whether certain types of problems are being incorrectly demoted to smaller models.
- Check whether the routing rules need a fallback mechanism, such as escalating to a larger model after a smaller model fails.

So model routing is essentially a balancer among effectiveness, cost, and stability. A well-built system does not use the most expensive model every time; rather, it can "save where it should save and spend where it should spend."

**Common follow-up questions:**

- In which scenarios is it better to start with rule-based routing instead of model routing from the beginning?
- After a small model's routing fails, how should the upgrade and fallback strategy be designed?
- How can you avoid breaking the overall system effectiveness just to save cost?

**Importance:**`中频` (occurrences: 1) | **Difficulty:**`较难`

**Assessment focus:** cost governance, model tiering, and routing strategy design capability.

**Corresponding sections:** [11 Model I/O and Model Access §2, LangChain Model Categories, Parameters, and Returns](11-Model-I-O%E4%B8%8E%E6%A8%A1%E5%9E%8B%E6%8E%A5%E5%85%A5.md#_2-langchain-model-categories-parameters-and-returns); [7 Enterprise-level LLM Deployment §1, Overview of Enterprise-level LLM Deployment](7-%E4%BC%81%E4%B8%9A%E7%BA%A7%E5%A4%A7%E6%A8%A1%E5%9E%8B%E9%83%A8%E7%BD%B2.md#_1-overview-of-enterprise-level-large-model-deployment)

### Q9-12. How should an Agent / RAG system be designed in an intranet environment?

In an intranet environment, building Agent / RAG is not about "copying the public-cloud solution as is." The core is to first establish **data stays within the domain, models are controllable, dependencies are replaceable, and the pipeline is observable**.

If designed according to enterprise-level deployment thinking, it is usually divided into three layers:

- Application layer: privatized versions of platforms such as Dify and Coze, or self-developed backend services, responsible for workflows, Agent orchestration, permissions, and business interfaces.
- Inference layer: use a managed platform such as Xinference to centrally manage LLMs, Embedding, and Rerank, exposing OpenAI-compatible APIs externally.
- Data layer: the intranet vector database, relational database, object storage, knowledge base index, logs, and audit systems are all placed within a controllable domain.

The key points of this kind of architecture generally include:

- Unified model access: the upper layers should all use compatible APIs as much as possible, making it easy to replace online models, local models, and different inference engines.
- Network and permission isolation: which intranet systems the Agent can access must be opened according to least privilege; do not give the model a master key to the entire intranet.
- Knowledge governance: document parsing, index rebuilding, version rollback, tenant isolation, and citation tracking must all be built in, otherwise the intranet knowledge base will quickly become unmanageable.
- Observability and auditing: request traces, tool calls, retrieval results, model versions, token usage, and anomaly alerts must all be viewable in a closed loop within the intranet.
- Degradation capability: when intranet models fluctuate, there should be caching, rule-based pipelines, manual fallback, or backup models; otherwise the system will be very fragile.

In summary: an intranet solution is not an "offline demo," but a production architecture that places greater emphasis on security boundaries, operations governance, and model replaceability.

**Common follow-up questions:**

- Why do many enterprises choose to decouple the "application layer + inference layer" instead of mixing everything on one machine?
- In an intranet environment, why is it better to deploy and manage LLM, Embedding, and Rerank separately?
- If public web search cannot be accessed directly, how should dynamic information be supplemented?

**Importance:**`中频` (occurrences: 1) | **Difficulty:**`较难`

**Assessment focus:** understanding of enterprise private deployment, awareness of decoupling the application layer and inference layer, and capability in designing secure and operable intranet Agent / RAG systems.

**Corresponding sections:** [7 Enterprise-level LLM Deployment §1, Overview of Enterprise-level LLM Deployment](7-%E4%BC%81%E4%B8%9A%E7%BA%A7%E5%A4%A7%E6%A8%A1%E5%9E%8B%E9%83%A8%E7%BD%B2.md#_1-overview-of-enterprise-level-large-model-deployment); [7 Enterprise-level LLM Deployment §3, Model Deployment](7-%E4%BC%81%E4%B8%9A%E7%BA%A7%E5%A4%A7%E6%A8%A1%E5%9E%8B%E9%83%A8%E7%BD%B2.md#_3-model-deployment); [12 Ollama Local Deployment and Invocation §5, LangChain Integration with Ollama](12-Ollama%E6%9C%AC%E5%9C%B0%E9%83%A8%E7%BD%B2%E4%B8%8E%E8%B0%83%E7%94%A8.md#_5-integrating-ollama-with-langchain)

---

## 10. Typical Business Scenario Design Questions

### Q10-1. If you were asked to design an enterprise knowledge base Q&A system, how would you do it?

It is usually designed in four layers: "data ingestion, retrieval pipeline, generation pipeline, and governance capabilities."

First, set up document ingestion, parsing, chunking, vectorization, and index update mechanisms, then design the query pipeline, including query rewriting, hybrid retrieval, reranking, permission filtering, and context assembly. The generation layer should emphasize "answering based on evidence, refusing to answer when there is no basis, and providing citations as much as possible." The governance layer should then add permissions, versioning, monitoring, evaluation, and badcase feedback loops.

In enterprise scenarios, it is also common to reserve capabilities for transferring to human agents, knowledge revision, index rollback, and multi-tenant isolation, because these often affect long-term usability more than "getting the first answer right."

**Common follow-up questions:**

- How do you support knowledge updates?
- How do you prevent users from accessing documents outside their permissions?
- If the system gives irrelevant answers, where should you look first?

**Importance:**`必刷` (occurrences: 1) | **Difficulty:**`较难`

**Assessment focus:** complete expression capability from requirements to architecture.

**Corresponding sections:** [2-RAG Building Enterprise Private & Personal Knowledge Bases §5, Building a Knowledge Base with Dify](2-RAG-%E6%90%AD%E5%BB%BA%E4%BC%81%E4%B8%9A%E7%A7%81%E6%9C%89&%E4%B8%AA%E4%BA%BA%E7%9F%A5%E8%AF%86%E5%BA%93.md#_5-building-a-knowledge-base-with-dify); [19 RAG Retrieval-Augmented Generation §3, RAG Comprehensive Case: Intelligent Operations Assistant](19-RAG%E6%A3%80%E7%B4%A2%E5%A2%9E%E5%BC%BA%E7%94%9F%E6%88%90.md#_3-comprehensive-rag-case-intelligent-operations-assistant)

### Q10-2. If you were asked to design an NL2SQL Agent, which risks would you focus on controlling?

The focus should be on controlling four types of risks: schema injection, SQL security, execution validation, and ambiguity clarification.

First, do not stuff the entire database schema into the context; instead, tailor it to the question and perform schema linking. Second, restrict to read-only queries, prohibit dangerous statements, and add execution sandboxing and timeout controls. Third, perform syntax checking and pre-execution validation to avoid generating SQL that looks plausible but cannot actually run. Finally, for issues such as time ranges, metric definitions, and field ambiguity, support clarification rather than letting the model make assumptions on its own.

**Common follow-up questions:**

- Should a preview be shown before generating SQL?
- How do you perform self-correction?
- When should you give up on generating SQL and instead transfer to a human or use a report template?

**Importance:**`高频` (occurrences: 1) | **Difficulty:**`较难`

**Assessment focus:** structured queries and security awareness.

### Q10-3. If you were asked to design a customer service agent, which capabilities would you prioritize?

Prioritize intent recognition, knowledge retrieval, process execution, human-agent collaboration, and retrospective closed loops.

Customer service is not simple Q&A; it often involves FAQ, order queries, refund processes, ticket routing, and emotional soothing at the same time. Therefore, the system must be able not only to answer questions, but also to check statuses, call interfaces, and collect additional materials. It must also transfer to a human agent promptly when uncertain and hand over the full context completely.

After launch, it is also necessary to continuously review frequently unresolved issues, misjudged intents, knowledge gaps, and reasons for transferring to human agents. Only in this way will the system become increasingly stable, rather than looking good only in demos.

**Common follow-up questions:**

- How should the conditions for transferring to a human agent be designed?
- Why does the customer service scenario need long-term memory or user profiles even more?
- How do you evaluate satisfaction and closed-loop outcomes?

**Importance:**`高频` (occurrences: 1) | **Difficulty:**`较难`

**Assessment focus:** business-oriented Agent design capability.

**Corresponding sections:** [3 Agent Development Based on Coze & Dify Platforms §7, Project: Merchant Operations Manager](3-%E5%9F%BA%E4%BA%8ECoze&Dify%E5%B9%B3%E5%8F%B0%E7%9A%84%E6%99%BA%E8%83%BD%E4%BD%93%E5%BC%80%E5%8F%91.md#_7-project-merchant-operations-manager); [21 Agent Intelligence §5, Hands-on Practice and Cases](21-Agent%E6%99%BA%E8%83%BD%E4%BD%93.md#_5-hands-on-practice-and-case-studies)

### Q10-4. How should you design an Agent's completion judgment and termination conditions to avoid ending too early?

An Agent's "ending" cannot rely only on intuition, nor only on reading logs or a broad completion-rate score. A more robust approach is to design explicit completion conditions for it.

Termination logic is usually divided into four layers:

- Task layer: whether the user's goal has been achieved and whether the required artifacts or fields have been obtained.
- Tool layer: whether key tool calls succeeded and whether the returned results meet the expected constraints.
- State layer: whether the current state has entered a terminal state such as done / failed / need_human.
- Protection layer: maximum steps, timeout, repeated no-progress count, and abnormal exit conditions.

If there is a Supervisor or supervision node in the pipeline, it is better to treat it as a "secondary review" and "exception fallback" rather than the sole basis for ending. The truly robust approach is to allow entry into the final answer node only when key task results, tool returns, and state machine conditions are all satisfied. Otherwise, it is better to continue execution, ask for clarification, or transfer to a human rather than returning unfinished results to the user too early.

**Common follow-up questions:**

- Why is relying solely on a supervision node to calculate completion rate and check logs both slow and prone to misjudgment?
- Is there a more general judgment method, such as directly checking key tool call results and state fields?
- How can you prevent the Agent from returning results to the user before the task is actually finished?

**Importance:**`高频` (occurrences: 1) | **Difficulty:**`较难`

**Assessment focus:** Agent termination condition design, state machine thinking, and the ability to combine Supervisor / tool results / state fields.

**Corresponding sections:** [24 LangGraph API: Nodes, Edges, and Advanced Topics §2, Graph API - Edge](24-LangGraphAPI%EF%BC%9A%E8%8A%82%E7%82%B9%E3%80%81%E8%BE%B9%E4%B8%8E%E8%BF%9B%E9%98%B6.md#_2-graph-api-edge); [21 Agent Intelligence §4, How Agents Work (V1.0)](21-Agent%E6%99%BA%E8%83%BD%E4%BD%93.md#_4、agent-工作原理%EF%BC%88v1.0%EF%BC%89)

### Q10-5. How should a Code Agent be designed?

The core of a Code Agent is not "being able to write a few lines of code," but being able to complete a closed loop around a coding task: **read the codebase, make a plan, modify files, run verification, and continue correcting based on results**. From a system structure perspective, it is still essentially an execution system of **model + tool set + runtime loop + current state**, except that the tools and state are more oriented toward coding scenarios.

If broken down by module, it is usually designed as the following layers:

- Task understanding layer: first turn the requirement into a clear goal, and determine whether it is reading code, fixing a bug, adding tests, refactoring, or answering an architecture question.
- Codebase understanding layer: establish the minimal necessary context through code search, file tree, symbol index, dependency relationships, and commit history, rather than dumping the entire codebase into the model all at once.
- Planning and execution layer: first list a modification plan, then decide which files to read, which files to change, which commands to run, and what verification is needed.
- Tool layer: at minimum, it needs capabilities for search, reading files, editing files, running tests, executing commands, and viewing logs.
- Feedback loop layer: continue correcting based on lint, tests, runtime errors, and diff results, rather than ending after generating a patch once.
- Security governance layer: restrict execution permissions, isolate dangerous commands, and retain change and execution logs to prevent the Agent from making unconstrained arbitrary modifications in the codebase.

The real difficulty usually lies not in "whether it can generate code," but in three areas:

- Context governance: when the codebase is very large, how to obtain only the context most relevant to the current task.
- Verification closed loop: how to determine that a fix really worked, rather than just letting the model say "I have fixed it."
- Failure handling: when the Agent cannot fix a bug after repeated attempts, how to stop, how to expose intermediate diagnostics, and how to hand it back to a human.

Therefore, a mature Code Agent is closer to an "execution system for coding tasks" than an "enlarged version of a code autocomplete tool." Its key is not only being able to write code, but also being able to turn **codebase understanding, tool invocation, verification feedback, and stopping conditions** into a stable closed loop.

**Common follow-up questions:**

- In a codebase with tens of millions of lines, where is a Code Agent most likely to get stuck first?
- When an Agent can't fix a bug, how do you design stopping conditions and human handoff?
- In code scenarios, how do you distinguish between static knowledge and dynamic data? Which parts should rely on indexing, and which should rely on runtime feedback?

**Importance:**`高频` (occurrences: 1) | **Difficulty:**`较难`

**Assessment focus:** Agent design capabilities in code scenarios, codebase context governance, and awareness of the "modify-verify-continue fixing" loop.

### Q10-6. If you were to design a Deep Research system, how would it differ from ordinary RAG?

Ordinary RAG is closer to "retrieve first, then answer," while Deep Research is closer to "around a complex topic, first break down research tasks, then conduct multiple rounds of retrieval, cross-verification, comprehensive organization, and finally output a structured report."

Therefore, Deep Research typically requires capabilities such as query planning, subtask decomposition, multi-source retrieval, conflict detection, citation management, credibility assessment, and iterative supplementary retrieval. It is closer to a research assistant than a Q&A assistant. The output format also tends toward reports, summaries, and citation lists rather than a single direct answer.

If understood from an engineering implementation perspective, it is essentially closer to a combined capability of "**workflow / graph orchestration + multi-round retrieval + report generation**," rather than simply stuffing more context into ordinary RAG. The key is not just recall, but whether the research process has been decomposed, whether evidence has been repeatedly verified, and whether a structured conclusion with citations can ultimately be produced.

**Common follow-up questions:**

- How do you ensure the reliability of results?
- What does multi-source cross-verification mean?
- Why do such systems need human review checkpoints even more?

**Importance:**`中频` (occurrences: 1) | **Difficulty:**`中等`

**Assessment focus:** Understanding of complex retrieval and report generation.

### Q10-7. How do you design a Deep Research system?

The core of Deep Research is not "look up information once and then summarize," but "continuously research around a complex problem and form structured conclusions."

A relatively complete design typically includes:

- Query planner: breaks complex problems into sub-questions.
- Retrieval executor: performs multi-source retrieval across search, databases, and knowledge bases.
- Information fusion layer: handles deduplication, conflict detection, evidence alignment, and credibility weighting.
- Iteration controller: continues supplementary retrieval when evidence is found to be insufficient, rather than ending in one pass.
- Report generator: outputs summaries, main text, citations, and timestamps.

If expressed in a more engineering-oriented way, it can be understood as a research-oriented workflow:

- The front end is task decomposition and retrieval orchestration.
- The middle is multiple rounds of evidence collection, deduplication, and conflict handling.
- The back end is structured report generation and citation organization.

The biggest difference from ordinary RAG is the upgrade from "single-turn Q&A" to a "multi-turn research process." So the design focus is not just recall rate, but also planning quality, citation quality, credibility, and process replayability. In actual implementation, it is also usually more inclined to use explicit orchestration methods such as Workflow or LangGraph, rather than handing it entirely over to a black-box conversational Agent.

**Importance:**`中频` (occurrences: 1) | **Difficulty:**`较难`

**Assessment focus:** Ability to decompose modules in complex research-oriented systems.

### Q10-8. How do you design a Python code interpreter?

A Python code interpreter is essentially a closed-loop system of "model-generated code + secure execution + result return."

The core design typically includes:

- Code generation layer: the model converts user requirements into Python code.
- Sandbox execution layer: isolated environment, whitelist modules, timeout limits, resource limits.
- Result return layer: collects stdout, stderr, file artifacts, charts, and return values.
- State management layer: supports preserving variables or working directories across multiple execution rounds.
- Security governance layer: prohibits dangerous system calls, network access, and unauthorized reads/writes.

The real difficulty of such systems lies not in "whether Python can be run," but in "how to give it execution capability without exposing the host environment."

**Common follow-up questions:**

- If the Agent needs to execute system commands or access files, how do you prevent it from exceeding its authority to delete databases or read sensitive host files?
- Besides whitelisting, what other restrictions would you impose on host environment isolation?

**Importance:**`中频` (occurrences: 1) | **Difficulty:**`较难`

**Assessment focus:** Execution-oriented agents and secure sandbox design.

**Corresponding sections:** [17 Tools §6, From course cases to real projects](17-Tools%E5%B7%A5%E5%85%B7%E8%B0%83%E7%94%A8.md#_6-from-course-examples-to-real-projects); [21 Agent §5, Hands-on practice and cases](21-Agent%E6%99%BA%E8%83%BD%E4%BD%93.md#_5-hands-on-practice-and-case-studies)

### Q10-9. How do you design a Manus-like general-purpose agent?

Such systems should not emphasize "generality" first, but rather return to the minimal skeleton of an Agent: **model + tool set + execution loop + current state**. The so-called Manus-like system is essentially extending these four layers of capability to longer task chains and more complex task spaces.

The design typically needs:

- Task understanding and planning module: breaks goals into executable steps.
- Tool scheduling module: uniformly connects tools such as search, browser, code execution, and file system.
- State and memory module: maintains task context, to-do list, and stage results.
- Execution and reflection module: continues execution, correction, or retry based on intermediate results.
- Security and governance module: permission control, logging, failure recovery, and human handoff.

The difference between this type of system and an ordinary Agent is not that it has "more tools," but that it needs to advance tasks over the long term, handle intermediate artifacts, manage complex state, and maintain stability across longer chains. Therefore, it is closer to a general-purpose task execution framework than an enlarged version of a single-turn Q&A bot.

**Importance:**`中频` (occurrences: 1) | **Difficulty:**`较难`

**Assessment focus:** Ability to decompose systems for general-purpose task-oriented agents.

### Q10-10. How do you develop a browser automation Agent?

The core of a browser automation Agent is to turn "seeing the page, understanding the page, operating the page, and verifying results" into a stable closed loop.

A reasonably sound design typically includes:

- Page perception layer: obtains DOM, screenshots, and interactive element information.
- Decision layer: decides based on goals whether to click, input, scroll, wait, or go back.
- Execution layer: calls browser automation tools to complete actions.
- Verification layer: confirms whether actions took effect and whether the page entered the expected state.
- Governance layer: timeouts, retries, idempotency, prevention of misoperation, and log replay.

The biggest difficulty of this type of Agent is not "whether it can click buttons," but that web pages are unstable, asynchronous loading occurs, state drifts, and the cost of misoperation is high, so verification and rollback awareness must be built in.

**Importance:**`中频` (occurrences: 1) | **Difficulty:**`较难`

**Assessment focus:** Browser tools, task planning, and reliability design.

### Q10-11. When an Agent needs to execute tasks in a real or simulated environment, what is the essential difference from a pure software tool-type Agent?

The biggest difference is that software-type Agents primarily operate within digital systems, with more structured inputs and outputs and stronger replayability; whereas Agents in real or simulated environments face perceptual noise, incomplete state, real-time feedback, and physical-world side effects.

In other words, pure software tool-type Agents are closer to "calling APIs, reading and writing data, operating pages," with the focus on permissions, state machines, and tool orchestration; real-environment Agents add perception, localization, action execution, and safety constraints. In many cases, "successful invocation" does not mean completion—one must also determine whether the action actually took effect, whether the environment changed, and whether risks are controllable.

Therefore, such systems place greater emphasis on closed-loop perception, real-time performance, simulation verification, failure protection, and human handoff. In essence, it is not about adding a few more tools, but about advancing the Agent from an "information processing system" to a "perception-decision-action closed-loop system."

**Importance:**`中频` (occurrences: 1) | **Difficulty:**`较难`

**Assessment focus:** Understanding of the boundary between "software-type Agents" and "action-oriented / embodied environment Agents."

---

## 11. Project Presentation and Interview Practice

### Q11-1. When an interviewer asks you to introduce a RAG / Agent project you have worked on, how should you present it?

A more reliable order of presentation is `业务目标 -> 方案设计 -> 你负责的部分 -> 难点 -> 指标结果`.

Do not start by listing the tech stack; first explain what business problem the project solved, such as "reducing the cost of customer service document lookup" or "enabling operations staff to query data in natural language." Then talk about the architecture, such as whether RAG, Tools, LangGraph, or a platform workflow was used. Next, focus on what you specifically did yourself, such as indexing strategy, permission design, tool integration, evaluation system, and cost optimization. Finally, provide quantifiable results, such as hit rate, latency, rate of escalation to human agents, and labor hours saved.

If you want your presentation to be more stable, you can use a lightweight STAR structure suitable for application-oriented roles:

- Situation: what was the business problem and constraints.
- Task: which part you were responsible for and what the target metrics were.
- Action: what specific design, troubleshooting, and optimization work you did.
- Result: final metrics, deployment outcomes, and retrospective takeaways.

In project questions, the most common directions interviewers dig into are usually not "whether you have used a certain framework," but these areas:

- Which layer you were specifically responsible for—don't present the whole team's achievements as your own.
- What bad cases you encountered and how you ultimately fixed them.
- Why you made this technology choice rather than another solution.
- How the project's effectiveness was evaluated after launch, and how issues were diagnosed.

**Common follow-up questions:**

- What was the hardest part of this project?
- What trade-offs did you make?
- If you were to do it again, what would you change?

**Importance:**`必刷` (occurrences: 1) | **Difficulty:**`中等`

**Assessment focus:** Project presentation skills.

**Corresponding sections:** [19 RAG §3, RAG comprehensive case: intelligent operations assistant](19-RAG%E6%A3%80%E7%B4%A2%E5%A2%9E%E5%BC%BA%E7%94%9F%E6%88%90.md#_3-comprehensive-rag-case-intelligent-operations-assistant); [21 Agent §5, Hands-on practice and cases](21-Agent%E6%99%BA%E8%83%BD%E4%BD%93.md#_5-hands-on-practice-and-case-studies)

### Q11-2. If the interviewer asks, "Why didn't you use a more popular framework or model?" how should you answer more convincingly?

The key to answering is not to prove that "the current choice is always the best," but to explain that "the current choice matches the business constraints."

A relatively complete answer can be developed in four layers:

- Business complexity: whether the current problem actually requires a single Agent, a Workflow, or is already complex enough to require LangGraph / multi-agent.
- Engineering constraints: team familiarity, delivery timeline, observability, maintainability, and migration cost.
- Deployment conditions: whether to use online models directly, or to connect to OpenAI-compatible APIs, local models, Ollama, Xinference, or similar self-hosted inference layers.
- Cost and performance: latency, throughput, token cost, model version stability, and whether there is a risk of third-party version drift.

For example, if a heavier multi-agent framework was not chosen, it may be because the current task could already be handled by a single Agent or Workflow; if a larger model was not chosen, it may be because latency and cost were not worthwhile; if a certain managed platform was not chosen, it may be because we placed more value on unified OpenAI-compatible APIs, model control, and private deployment capability.

Taking it one step further, you should also naturally demonstrate two points:

- You are aware of the alternative solutions, not that you never researched them.
- You have left a migration path for the current solution and will not lock the system in.

**Common follow-up questions:**

- If future requirements become more complex, what is the migration path?
- How did you conduct technical validation?
- How do you avoid technology lock-in?
- If your MCP is self-developed based on Java, compared with mature Agent frameworks, where exactly does the extensibility advantage lie?

**Importance:** `高频` (occurrences: 1) | **Difficulty:** `中等`

**Assessment points:** Technical judgment and maturity of expression.

**Corresponding sections:** [9 LangChain Overview and Architecture §2, LangChain's Positioning](9-LangChain%E6%A6%82%E8%BF%B0%E4%B8%8E%E6%9E%B6%E6%9E%84.md#_2-positioning-of-langchain); [7 Enterprise-level LLM Deployment §1, Overview of Enterprise-level LLM Deployment](7-%E4%BC%81%E4%B8%9A%E7%BA%A7%E5%A4%A7%E6%A8%A1%E5%9E%8B%E9%83%A8%E7%BD%B2.md#_1-overview-of-enterprise-level-large-model-deployment)

### Q11-3. If online performance fluctuates significantly, how do you demonstrate your troubleshooting ability to the interviewer?

The most important thing is layered troubleshooting, along with a clear chain of evidence.

A more standardized answer is: first confirm whether there has been a change in input distribution, then check whether the model version or Prompt has changed, and then inspect retrieval recall, tool calls, context assembly, API timeouts, and log tracing. If it is RAG, sample queries to check whether the retrieved chunks and final answer are consistent; if it is an Agent, check whether each step of tool invocation and state progression is abnormal. Finally, consider whether the evaluation set is distorted or the cache is polluted.

This kind of answer is more persuasive than vaguely saying "tune parameters and optimize the prompt," because it demonstrates layered troubleshooting capability.

**Common follow-up questions:**

- Have you ever encountered intermittent errors?
- How do you reproduce an issue?
- How do you conduct an effective retrospective?
- How would you determine whether the problem mainly comes from model hallucination, or from the RAG, Prompt, or tool pipeline itself?

**Importance:** `中频` (occurrences: 1) | **Difficulty:** `中等`

**Assessment points:** Fault localization and retrospective capability.

---

## 12. Tool Ecosystem and Role Awareness

### Q12-1. Which AI development tools do you commonly use? What scenarios is each suitable for?

A relatively solid answer does not just list names, but instead layers them by scenario.

Generally, they can be divided into several categories:

- General conversation and research tools: for example, `ChatGPT`, `Claude`, and `Perplexity`, suitable for quickly validating ideas, organizing solutions, writing first drafts, and summarizing materials.
- AI coding collaboration tools: for example, `Cursor`, `Claude Code`, and `GitHub Copilot`, suitable for reading code, modifying code, adding tests, and explaining codebase structure. The key is whether they lean more toward in-IDE collaboration or toward terminal-based codebase-level agents.
- Low-code / workflow platform tools: for example, `Coze` and `Dify`, more suitable for rapid business validation, workflow orchestration, knowledge base integration, and multi-person collaboration.
- RAG / knowledge base platform tools: for example, `RAGFlow`, more suitable for document import, parsing, chunking, retrieval, and citation chain validation.

In a real project, you would rarely choose only one tool; instead, you would combine them by stage. For example, use a general conversation tool to organize the solution in the early stage, use a low-code platform for the POC, use an AI coding tool for core pipeline implementation, and then complete evaluation, deployment, and observability afterward.

If you need a sentence that sounds more like an actual interview response, you can summarize it directly like this: for solution planning and material summarization, common tools include `ChatGPT` and `Claude`; for code implementation and repository-level modifications, tools such as `Cursor`, `Claude Code`, and `Copilot` are more appropriate; for business validation and workflow orchestration, `Dify` and `Coze` are more common; and for knowledge base pipeline validation, platforms like `RAGFlow` are more suitable.

What this type of question really assesses is not "how many tools you have used," but whether you have formed your own mental model for tool layering and understand which problems each tool solves.

**Importance:** `中频` (occurrences: 1) | **Difficulty:** `基础`

**Assessment points:** Awareness of the tool ecosystem, and whether you can choose tools based on scenarios rather than popularity.

**Source:** Tencent AI Backend Engineer First Round (actual large-company interview question)

### Q12-2. How should the differences among AI coding tools such as Cursor, Claude Code, and Copilot be understood?

You can understand them as "all helping with development, but with different collaboration locations and interaction methods."

- Tools like Cursor lean more toward in-IDE collaboration, suitable for reading code while completing, partially rewriting, and editing based on the current file or workspace.
- Tools like Claude Code lean more toward terminal-based codebase-level agents, suitable for cross-file understanding, executing commands, modifying a set of files, and completing more complete task loops.
- Tools like Copilot lean more toward lightweight code completion and editing assistance, with advantages usually in low interruption and fitting into existing editor workflows.

Therefore, it is not appropriate to simply judge which one is stronger; instead, you should return to the task type itself. If it is "writing while completing, quickly modifying a piece of code," the in-IDE tool experience is smoother; if it is "understanding the entire codebase, running commands, making cross-file changes, and completing a more complete task," a terminal-based agent has more advantages; if the team already has stable IDE habits, lightweight completion tools also have lower integration costs.

You can also add one more point: tool capabilities will continue to change, so the truly stable criterion is not the name, but the depth of its understanding of codebase context, execution boundaries, controllability, and whether it fits the team's workflow.

**Importance:** `中频` (occurrences: 1) | **Difficulty:** `基础`

**Assessment points:** Ability to compare AI coding tools, and whether you have stable selection criteria.

**Source:** Tencent AI Backend Engineer First Round (actual large-company interview question)

### Q12-3. If you were asked to summarize the differences between an "AI Application Engineer" and an "Algorithm Research Role," what would you say?

It can be summarized as follows: an AI Application Engineer focuses more on "delivering model capabilities into business systems stably, safely, and at low cost," while an Algorithm Research Role focuses more on "how to push the boundaries of the model's own capabilities."

The former's core work typically includes technology selection, RAG / Agent architecture, tool and data integration, workflow orchestration, evaluation, deployment, monitoring, and business closure; the latter leans more toward model training, fine-tuning strategies, data construction, algorithm experiments, and metric breakthroughs. The two overlap, but the core competencies are different.

**Importance:** `低频` (occurrences: 1) | **Difficulty:** `基础`

**Assessment points:** Whether the understanding of the role is accurate.
