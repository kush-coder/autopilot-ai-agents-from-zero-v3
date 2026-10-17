# 15 - Shopkeeper Data Q&A: API Interface Basics and Getting Started with FastAPI

---

**Chapter learning objectives:**

- Understand why a data Q&A agent ultimately needs to be wrapped as an HTTP API.
- Build a minimal, testable `/api/query` interface.
- Understand the relationship between regular responses, streaming responses, and the SSE protocol.
- Understand the three engineering foundations of FastAPI: `lifespan`, middleware, and `Depends`.
- Prepare for connecting the real `QueryService` in the next chapter.

**Study suggestion:** In this chapter, first learn the API skeleton; don't rush to connect the real data Q&A workflow. Focus on how requests come in, how responses go out, why streaming returns are needed, how each segment of SSE data is agreed upon, and what FastAPI's routing, dependencies, and lifecycle manage. Once these foundations are clear, connecting `QueryService` in the next chapter won't feel like the file relationships are scattered.

**Corresponding code branch:** `15-api-streaming-basics`

**Official documentation references:**

- FastAPI streaming responses: https://fastapi.org.cn/advanced/custom-response/#streamingresponse
- SSE protocol explanation: https://www.ruanyifeng.com/blog/2017/05/server-sent_events.html
- FastAPI lifespan events: https://fastapi.org.cn/advanced/events
- FastAPI middleware: https://fastapi.org.cn/tutorial/middleware
- FastAPI dependency injection: https://fastapi.org.cn/tutorial/dependencies

---

After Chapter 14, the core pipeline of the data Q&A agent can run internally on the backend, but at this point it is still not a real application. The current invocation method is more like internal debugging: a developer runs the graph in the command line and observes logs and output. When actually delivering to a frontend or other systems, this capability needs to be wrapped as an HTTP API.

This chapter only covers the first step: first clarifying the basic form of the API and the streaming protocol. Actually connecting `QueryService` will be left for the next chapter.

---

## 1. What Problems Does the Query Interface Solve

Ultimately, we need a query interface that receives a natural language question submitted by the frontend:

```json
{
  "query": "统计华北地区的销售总额"
}
```

After the backend receives the question, it needs to invoke the previously built LangGraph data Q&A agent and continuously return the execution process to the frontend.

This interface must meet at least four requirements:

| Requirement | Description |
| -------------- | ------------------------------------ |
| Receive user questions | The frontend passes `query` through the request body |
| Execute the data Q&A workflow | The backend calls `graph.astream(...)` |
| Return progress in real time | Push progress to the frontend whenever a key node is executed |
| Return the final result | After SQL execution is complete, return the query results to the frontend |

The most critical part here is "returning progress in real time." A data Q&A agent is not an ordinary CRUD interface; it goes through multiple steps in the middle. If the backend waits for all nodes to finish before returning everything at once, users can only watch the page spin endlessly, with no idea whether the system is running normally, stuck, or has already failed.

A better experience is:

```text
正在抽取关键词...
正在召回字段信息...
正在召回指标信息...
正在生成 SQL...
正在执行 SQL...
查询完成
```

This is the first core concept introduced in this chapter: **streaming responses**.

---

## 2. Build a Minimal FastAPI Interface First

FastAPI is a Python web framework for building API services. Simply put, it is responsible for exposing Python functions as HTTP interfaces so that frontends, Apifox, Postman, or other business systems can call backend capabilities through URLs.

A minimal FastAPI application looks roughly like this:

```python
from fastapi import FastAPI

# 创建 FastAPI 应用对象，后续所有路由、中间件、生命周期事件都会注册到 app 上
app = FastAPI()


@app.get("/health")
async def health_check():
    # 返回普通 dict 时，FastAPI 会自动把它序列化成 JSON 响应
    return {"status": "ok"}
```

There are three key pieces of information here:

| Code | Meaning |
| ------------------------- | ------------------------------- |
| `app = FastAPI()` | Create a FastAPI application instance |
| `@app.get("/health")` | Declare a GET endpoint |
| `return {"status": "ok"}` | Return a dictionary; FastAPI automatically converts it to JSON |

This project will not pile all interfaces into `main.py`, but instead will first split them according to the following structure:

```text
shopkeeper-agent/
├─ main.py
└─ app/
   └─ api/
      ├─ routers/
      │  └─ query_router.py
      └─ schemas/
         └─ query_schema.py
```

| File | Responsibility |
| ----------------- | --------------------------------- |
| `main.py` | Create the FastAPI application and mount routes |
| `query_router.py` | Define query endpoints, such as `/api/query` |
| `query_schema.py` | Define request body structures, such as `query: str` |

### 2.1 Define the Request Body QuerySchema

Corresponding project file path: `shopkeeper-agent/app/api/schemas/query_schema.py`

```python
from pydantic import BaseModel


class QuerySchema(BaseModel):
    # 前端请求体中的 query 字段，用来承载用户输入的自然语言问题
    query: str
```

The purpose of `QuerySchema` is to tell FastAPI that the current interface's request body should contain a string field `query`.

When the frontend sends:

```json
{
  "query": "统计华北地区的销售总额"
}
```

Inside the route function, the user question can be retrieved through `query.query`. The two `query` here have different meanings:

```text
第一个 query：函数参数名，是 QuerySchema 对象
第二个 query：请求体字段名，是用户问题字符串
```

### 2.2 Create the Query Router query_router

Corresponding project file path: `shopkeeper-agent/app/api/routers/query_router.py`

In this chapter, we use `fake_streamer()` to simulate streaming output first, without connecting the real data Q&A agent:

```python
import asyncio

from fastapi import APIRouter
from starlette.responses import StreamingResponse

from app.api.schemas.query_schema import QuerySchema

# 当前模块只负责查询相关接口，后续接口变多时可以继续拆分其他 router
query_router = APIRouter()


async def fake_streamer():
    # 先用 10 个 step 模拟智能体执行过程，方便验证流式响应是否可用
    for i in range(10):
        # 暂停 1 秒只是为了观察流式效果；真实项目中这里会被节点执行耗时代替
        await asyncio.sleep(1)

        # SSE 消息以 data: 开头，并以两个换行符结尾
        # 客户端会把每次 yield 的内容识别为一条独立事件
        yield f"data: step:{i}\n\n"


@query_router.post("/api/query")
async def query_handler(query: QuerySchema):
    # query 参数会由 FastAPI 根据请求体自动解析成 QuerySchema 对象
    # StreamingResponse 会把 fake_streamer() 每次 yield 的内容持续写给客户端
    return StreamingResponse(fake_streamer(), media_type="text/event-stream")
```

First, grasp two points from this code.

First, `APIRouter` is used to organize a group of endpoints. Although there is only one query endpoint currently, it is still placed in `query_router` so that when more endpoints are added later, everything will not be crammed into `main.py`.

Second, `fake_streamer()` is an asynchronous generator. It does not `return` a complete result all at once; instead, every 1 second it `yield` a segment of content. When connecting the real agent in the next chapter, it will be replaced with `QueryService.query(...)`.

### 2.3 Mount the Route in main.py

Corresponding project file path: `shopkeeper-agent/main.py`

```python
from fastapi import FastAPI

from app.api.routers.query_router import query_router

# 创建后端应用实例
app = FastAPI()

# 把 query_router.py 中定义的 /api/query 注册到应用上
# 如果没有这一行，/docs 页面里看不到该接口，客户端也访问不到它
app.include_router(query_router)
```

`app.include_router(query_router)` is critical. If the endpoint is only defined in `query_router.py` but not mounted on `app`, the FastAPI application will not know that the route exists. Opening `/docs` will also not show `/api/query`.

---

## 3. Why the Query Interface Needs Streaming Responses

An ordinary HTTP interface usually looks like this:

```text
客户端发起请求
  -> 服务端处理完整逻辑
  -> 服务端一次性返回响应
```

Using a Python analogy, an ordinary response is more like `return`:

```python
async def query():
    result = await run_all_steps()
    return result
```

Its characteristic is that the client must wait for all logic to complete before it can receive the response.

A streaming response is more like `yield`:

```python
async def query_stream():
    yield "抽取关键词"
    yield "召回字段信息"
    yield "生成 SQL"
    yield "执行 SQL"
```

Each time `yield` runs, the backend can write a segment of content to the client. Applied to the data Q&A interface, that is:

```text
客户端提交问题
  -> 后端返回：抽取关键词
  -> 后端返回：召回字段信息
  -> 后端返回：生成 SQL
  -> 后端返回：执行 SQL
  -> 后端返回：最终结果
```

Therefore, streaming responses do not solve the problem of "whether results can be returned," but rather the problem of "whether continuous feedback can be provided to users during long-running process execution."

---

## 4. Streaming Responses: How FastAPI Continuously Writes Data

Official documentation reference:

- FastAPI streaming responses (StreamingResponse): https://fastapi.org.cn/advanced/custom-response/#streamingresponse

In FastAPI, the core of implementing streaming returns is `StreamingResponse`. The official documentation explains that `StreamingResponse` can accept a generator, asynchronous generator, or other iterable object, and continuously writes the content produced from it into the response.

The example code in this chapter corresponds to this section:

```python
return StreamingResponse(
    # 传入异步生成器，StreamingResponse 会不断消费其中 yield 出来的内容
    fake_streamer(),
    # 声明为 SSE 事件流，客户端才会按流式事件来处理响应
    media_type="text/event-stream",
)
```

Here, three things need to be noted.

### 4.1 StreamingResponse Receives a Generator

`fake_streamer()` internally uses `yield`:

```python
async def fake_streamer():
    for i in range(10):
        # 放慢输出速度，方便在浏览器 Network 或 Apifox 中观察逐条返回
        await asyncio.sleep(1)

        # 每 yield 一次，后端就向客户端写出一条 SSE 消息
        yield f"data: step:{i}\n\n"
```

`return` ends the function, while `yield` pauses the function, hands over the current content first, and can continue execution the next time. This characteristic is naturally suited to a "output while executing" data Q&A workflow.

### 4.2 sleep Is Only for Observing the Streaming Effect

In the example:

```python
await asyncio.sleep(1)
```

is not business logic; it is only so that during testing you can visually see `step:0`, `step:1`, `step:2` returned one by one. Without the pause, ten messages would be output instantly, making it look like a one-time return. In a real project, this wait time will be replaced by actual node execution time, such as retrieval, calling the large language model, and executing SQL.

### 4.3 media_type Must Be Declared as text/event-stream

This line is also important:

```python
media_type="text/event-stream"
```

It tells the client that this is not ordinary JSON or plain text, but an SSE event stream. Without declaring this type, even if the backend keeps writing data, the frontend or API testing tool may not necessarily process it as an event stream.

---

## 5. SSE Protocol: The Streaming Format Agreed Between Frontend and Backend

`StreamingResponse` solves "how the server continuously writes responses." SSE solves "what format the continuously written text should be so that the frontend can easily parse it."

SSE stands for `Server-Sent Events`, which can be understood as "the server continuously sends events to the client." Its interaction method is:

```text
客户端发起一次 HTTP 请求
  -> 服务端保持连接
  -> 服务端持续发送多条事件消息
  -> 发送完成后关闭连接
```

This fits this project perfectly: the user first submits a question, and then the server mainly pushes execution progress and results back.

### 5.1 How to Choose Between SSE and WebSocket

Let's start with the conclusion: in the current project, the question submission is one-time, and subsequently the backend mainly returns progress and results continuously, so SSE fits the requirements better; WebSocket is more suitable for scenarios where both frontend and backend need to continuously send messages proactively.

![Choosing between SSE and WebSocket in a data Q&A interface: SSE is more suitable for continuous task progress and result returns, while WebSocket is more suitable for complex bidirectional real-time interaction](../../../%E5%AE%9E%E6%88%98%E9%A1%B9%E7%9B%AE-%E7%94%B5%E5%95%86%E9%97%AE%E6%95%B0/images/15/15-5-1-1.svg)

| Solution | Characteristics | Suitable Scenarios |
| --------- | ---------------------------------------- | ---------------------------- |
| WebSocket | Bidirectional communication; both client and server can continuously send messages | Online collaboration, chat, games |
| SSE | Mainly the server continuously pushes messages to the client | Task progress, log streams, model output streams |

In this project, the frontend only needs to submit a question once and then receive server pushes. Therefore, using SSE is lighter and more aligned with the current requirements.

### 5.2 The Minimal SSE Message Format

SSE messages are essentially UTF-8 text. The most common format is:

```text
data: 这里是要发送的内容

```

Note that a message must be followed by a blank line, that is, two newline characters:

```text
\n\n
```

Therefore, in Python it is usually written as:

```python
yield "data: step:0\n\n"
```

If you want to send JSON, you can also write:

```python
yield 'data: {"type": "progress", "step": "抽取关键词"}\n\n'
```

In the next chapter, `QueryService` will use a similar pattern:

```python
yield f"data: {json.dumps(chunk, ensure_ascii=False, default=str)}\n\n"
```

This line of code can be understood in three layers:

```text
data:        # SSE 的 data 字段
JSON 字符串  # 本项目自己的业务消息
\n\n         # 一条 SSE 消息结束
```

### 5.3 SSE Outer Layer and JSON Inner Layer

In this project, streaming messages will subsequently be designed into several types:

| Type | Purpose | Example |
| ---------- | ---------------- | -------------------------- |
| `progress` | Return node execution progress | `抽取关键词`, `生成SQL` |
| `result` | Return the final query result | Data queried by SQL |
| `error` | Return error information | SQL execution failure, model invocation failure |

In other words, the outer layer is SSE:

```text
data: ...\n\n
```

The inner layer is the project's own JSON protocol:

```json
{ "type": "progress", "step": "抽取关键词", "status": "running" }
```

This relationship must be clearly distinguished: **SSE is the transport format, and JSON is the business content.**

---

## 6. Test the Minimal Streaming Interface

Start the backend service:

```bash
uv run fastapi dev main.py
```

Then open: http://127.0.0.1:8000/docs

If you can see `POST /api/query`, it means `query_router` has been successfully mounted.

In Swagger UI, send:

```json
{
  "query": "test"
}
```

![Swagger UI](../../../%E5%AE%9E%E6%88%98%E9%A1%B9%E7%9B%AE-%E7%94%B5%E5%95%86%E9%97%AE%E6%95%B0/images/15/15-6-1-1.png)

In Swagger, you may notice that the page keeps loading and only displays the complete result once everything is finished. This does not mean the backend is not streaming; it is just that Swagger UI usually does not render SSE item by item.

To observe the real streaming effect, there are two methods:

| Tool | Observation Method |
| ---------------- | ----------------------------------------------- |
| Browser developer tools | Check the Network panel to see whether the response is continuously growing |
| Apifox / Postman | Select POST `/api/query` and observe whether SSE events appear one by one |

![Apifox](../../../%E5%AE%9E%E6%88%98%E9%A1%B9%E7%9B%AE-%E7%94%B5%E5%95%86%E9%97%AE%E6%95%B0/images/15/15-6-1-2.png)

If you see `step:0` to `step:9` appear roughly once per second, then the minimal streaming interface in this chapter is working.

---

## 7. The FastAPI Trio: lifespan, middleware, Depends

Earlier we already got the minimal query interface and the streaming protocol working. Next, let's add three more foundational FastAPI engineering pieces.

They each solve a different problem:

| Engineering problem | FastAPI capability | Usage in this project |
| ---------------------------- | ------------ | ---------------------------------------- |
| How to manage resources when the application starts and shuts down | `lifespan` | Initialize and close external clients |
| How to execute unified logic before and after each request | middleware | Generate `request_id` to aid log tracing |
| How the objects that route functions depend on are created | `Depends` | Assemble `QueryService`, Repository, Session |

For these three concepts, it is enough in this chapter to understand "what each one manages"; the concrete code will be expanded in the next two chapters.

### 7.1 lifespan: when application-level resources are initialized

FastAPI lifecycle events are used to run initialization logic before the application begins accepting requests, and cleanup logic when the application shuts down. The currently recommended approach is to pass an asynchronous context manager via `FastAPI(lifespan=...)`.

Why does this project need it? Because the data Q&A interface depends on many external resources:

- Embedding client;
- Qdrant client;
- Elasticsearch client;
- Metadata database MySQL connection;
- Data warehouse MySQL connection.

These resources should not be reinitialized for every incoming request. A more reasonable approach is:

```text
应用启动时：
  -> 初始化客户端和连接能力

请求处理期间：
  -> 复用已经初始化好的客户端

应用关闭前：
  -> 统一释放连接
```

The `lifespan` syntax in FastAPI looks roughly like this:

```python
from contextlib import asynccontextmanager

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    # yield 之前：应用启动时执行，适合初始化客户端、连接池等应用级资源
    init_clients()

    # yield 处：FastAPI 应用进入运行状态，开始接收和处理请求
    yield

    # yield 之后：应用关闭前执行，适合释放连接、关闭客户端
    await close_clients()


# 把生命周期函数交给 FastAPI，框架会在启动和关闭时自动调用
app = FastAPI(lifespan=lifespan)
```

You can think of `yield` as a dividing line:

```text
yield 前：应用启动时执行
yield 后：应用关闭时执行
```

In the next chapter, the real code will be written as:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 应用启动时初始化外部客户端，后续请求可以直接复用这些客户端
    qdrant_client_manager.init()
    embedding_client_manager.init()
    es_client_manager.init()
    meta_mysql_client_manager.init()
    dw_mysql_client_manager.init()

    # 应用运行期间停在这里，开始处理请求
    yield

    # 应用关闭前释放外部连接，避免连接泄漏
    await qdrant_client_manager.close()
    await es_client_manager.close()
    await meta_mysql_client_manager.close()
    await dw_mysql_client_manager.close()
```

### 7.2 middleware: unified logic that all requests pass through

The middleware here is not the messaging middleware of Kafka, RabbitMQ, and the like, but request middleware in a web framework. It can be understood as a piece of logic wrapped around the outside of all interfaces.

A request roughly goes through:

```text
客户端请求
  -> 中间件前半段
  -> 路由处理函数
  -> 中间件后半段
  -> 客户端响应
```

The basic way to define HTTP middleware in FastAPI is:

```python
from fastapi import Request


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    # call_next 之前：请求还没有进入具体路由，适合做鉴权、打 request_id 等统一处理
    response = await call_next(request)

    # call_next 之后：路由已经生成响应，适合补充响应头、记录耗时等
    return response
```

The two parameters here are very important:

| Parameter | Meaning |
| ----------- | ------------------------------------------ |
| `request` | The current request object; can read the path, method, request headers, etc. |
| `call_next` | Passes the request onward to the subsequent route handler function |

Middleware is suitable for cross-cutting logic required by all interfaces, such as:

- Unified authentication;
- Measuring request latency;
- Adding response headers;
- Recording access logs;
- Generating a `request_id` for each request.

In Chapter 17 of this project, middleware will be used to generate a unique `request_id` for each request, so that concurrent logs can be traced by request dimension.

### 7.3 Depends: declaring "what I need"

Dependency injection (Depends) can first be understood literally: the interface function only declares what objects it needs, and FastAPI is responsible for calling the dependency function when a request arrives, creating the object, and passing it in.

A simplified version of the official example is as follows:

```python
from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()


async def common_parameters(skip: int = 0, limit: int = 100):
    # 依赖函数可以像普通函数一样接收参数、组织数据，并返回给接口使用
    return {"skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(
    # Annotated[真实类型, Depends(依赖函数)]
    # 表示 commons 的类型是 dict，获取方式是调用 common_parameters
    commons: Annotated[dict, Depends(common_parameters)],
):
    return commons
```

In this code, `read_items()` does not manually call `common_parameters()`; it merely declares:

```text
我需要一个 commons
commons 的获取方式是 Depends(common_parameters)
```

When a request comes in, FastAPI automatically calls the dependency function.

Returning to this project, the query interface will ultimately be written like this:

```python
@query_router.post("/api/query")
async def query_handler(
    # 请求体参数：FastAPI 会把 JSON 请求体解析成 QuerySchema
    query: QuerySchema,
    # 业务服务参数：FastAPI 会调用 get_query_service 来创建 QueryService
    query_service: Annotated[QueryService, Depends(get_query_service)],
):
    return StreamingResponse(
        # 下一章会把真实问数工作流封装到 query_service.query(...) 中
        query_service.query(query.query),
        media_type="text/event-stream",
    )
```

This means:

```text
query 来自请求体
query_service 来自 get_query_service 这个依赖函数
```

The route layer does not need to care about which Repositories, Sessions, or Clients `QueryService` depends on internally. Those objects will be assembled in layers through `dependencies.py` in the next chapter.

---

## 8. Looking One Level Deeper into Dependency Injection

The previous section only covered the basic syntax of `Depends`. This section adds two more features that will be used immediately later: sub-dependencies and dependencies with `yield`.

### 8.1 Sub-dependencies

Dependencies can in turn depend on other dependencies. For example:

```text
query_router
  -> QueryService
      -> MetaMySQLRepository
          -> meta_session
      -> DWMySQLRepository
          -> dw_session
      -> Qdrant / ES / Embedding client
```

FastAPI automatically resolves this dependency tree. More importantly, within the same request, if multiple dependencies share the same sub-dependency, FastAPI performs request-level caching and will not create the same dependency object repeatedly within a single request.

Note that this cache is **request-level**, not a global singleton. With each new request, the dependency function will still run again.

### 8.2 Dependencies with yield

Request-level resources such as database Sessions are suited to dependencies with `yield`:

```python
async def get_meta_session():
    # 每次请求需要数据库 Session 时，先从 session_factory 创建一个请求级 Session
    async with meta_mysql_client_manager.session_factory() as meta_session:
        # yield 把 Session 交给 Repository 使用；请求结束后会回到这里并退出 async with
        yield meta_session
```

The execution order can be understood as:

```text
请求需要 meta_session
  -> 进入 async with，创建 session
  -> yield session 给 Repository 使用
  -> 请求结束
  -> 退出 async with，session 被关闭或归还
```

Here it is also necessary to distinguish between `lifespan` and dependencies with `yield`:

| Comparison item | `lifespan` | Dependencies with `yield` |
| ------------ | -------------------------------- | ---------------------------------------- |
| Lifecycle scope | Entire application | Single request |
| Typical resources | Clients, connection pools, global configuration | Database Session, request-level temporary resources |
| Example in this project | Initialize Qdrant, ES, MySQL manager | `get_meta_session()`, `get_dw_session()` |

A simple way to remember:

```text
lifespan 管应用级资源
yield 依赖项管请求级资源
```

---

**Chapter summary:**

- `/api/query` is not an ordinary JSON interface, but a streaming interface that needs to continuously return the execution process.
- In this chapter, `fake_streamer()` is first used to verify the API skeleton and streaming response; the real `QueryService` will be connected in the next chapter.
- FastAPI uses `StreamingResponse` to receive the asynchronous generator, and each `yield` writes a segment of content to the client.
- This project uses SSE as the frontend-backend streaming protocol, and the core format is `data: xxx\n\n`.
- `lifespan`, middleware, and `Depends` respectively solve application-level resource management, request-level unified logic, and dependency object assembly.

In the next chapter, `fake_streamer()` will officially be replaced with the real `QueryService.query(...)`, connecting `/api/query` to the LangGraph data Q&A workflow.
