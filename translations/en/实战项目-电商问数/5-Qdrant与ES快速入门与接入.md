# 5 - E-commerce Assistant: Qdrant and ES Quick Start and Integration

---

**Chapter Learning Objectives:**

- Understand the responsibility boundaries of `Qdrant` and `Elasticsearch` in "E-commerce Assistant," rather than mixing them together as generic "retrieval components."
- Master core concepts such as vector databases, full-text search, `mapping`, `collection`, and `payload`.
- Understand how `QdrantClientManager` and `ESClientManager` are encapsulated, initialized, and tested in the project.

**Study Advice:** Both Qdrant and ES are referred to as retrieval, but do not treat them as the same thing. When reading this article, first remember the division of labor: Qdrant is more suitable for semantic similarity recall, while ES is more suitable for full-text matching and precise filtering. The purpose of running the quickstart is not to become proficient in all APIs, but to see clearly what collections / points / payloads and indexes / documents / mappings correspond to respectively in the project.

**Corresponding Code Branch:** `05-qdrant-es`

---

When many students first see this project, they ask a very natural question:

> Since both are "retrieval," why do we need to integrate both `Qdrant` and `Elasticsearch` at the same time?

The answer is: **They do not solve the same type of problem.**

In "E-commerce Assistant," the division of labor among these infrastructure components can be summarized in the table below:

| Component            | Core Responsibility in the Project             | Problem It Excels At Solving                                 |
| --------------- | ------------------------------ | ------------------------------------------------ |
| `MySQL`         | Stores authoritative structured metadata and warehouse data | How to store structured information such as tables, fields, metrics, relationships, and sample values |
| `Qdrant`        | Stores vector indexes for fields and metrics       | "Which one is semantically more similar"                                   |
| `Elasticsearch` | Stores full-text indexes for field values         | "Which text can match"                               |

If we place them back into the question-answering pipeline, the responsibilities become clearer:

```text
用户自然语言问题
  -> Embedding 服务把文本转成向量
  -> Qdrant 召回语义相关的字段 / 指标
  -> Elasticsearch 检索可能相关的字段取值
  -> MySQL 补全表结构、字段定义、指标定义
  -> LLM 基于上下文生成 SQL
```

Therefore, what this chapter really covers is not two independent clients, but the **retrieval infrastructure layer** of "E-commerce Assistant": why they are needed, what they store respectively, how to integrate them in the project, and how they are called by the business layer later.

---

## 1. Qdrant Client Integration

### 1.1 Introduction to Qdrant

Official documentation: https://qdrant.tech/documentation/overview/what-is-qdrant/ (English)

In one sentence, `Qdrant` is: **A database specifically designed to store vectors and perform similarity retrieval.**

However, in the context of the current project, that sentence is still not specific enough. A more accurate description would be:

- Field information is vectorized and then written into `Qdrant`
- Metric information is also vectorized and then written into `Qdrant`
- When a user question arrives, it is also vectorized first
- Then the "question vector" is used to search for the most similar fields and metrics

In other words, `Qdrant` does not take on the responsibility of "storing all metadata" here, but rather: **quickly narrows down the semantic problem space among massive field and metric candidates.**

This is critical, because in enterprise data Q&A scenarios, there are usually many tables and fields. Without this semantic recall step, the LLM would be faced with a huge amount of candidate context, and the subsequent SQL generation would be more prone to veering off course.

When the current project builds vector indexes for fields and metrics, it does not just write one vector per entity. Instead, it vectorizes the name, description, and aliases separately and then writes them into the vector database. The purpose is to enable the system to understand both formal names and business aliases, as well as natural language expressions.

### 1.2 Distinguishing OLTP, OLAP, and Vector Databases

![Comparison chart of data organization methods for OLTP, OLAP, and vector databases](../../../%E5%AE%9E%E6%88%98%E9%A1%B9%E7%9B%AE-%E7%94%B5%E5%95%86%E9%97%AE%E6%95%B0/images/5/5-1-2-1.png)

Before understanding `Qdrant`, a common misconception is to simply think of it as "another kind of MySQL."

Looking directly at the diagram above, it essentially compares the **data organization methods** of three types of databases:

- **Left side: `OLTP database`**
  - Focuses on organizing data by "rows"
  - More suitable for supporting business systems that query, modify, and write one record at a time

- **Middle: `OLAP database`**
  - Focuses on organizing data by "columns"
  - More suitable for statistical analysis, because analysis scenarios often need to scan an entire column of data at once

- **Right side: `Vector database`**
  - The core unit is no longer "a row in a table," but a vector point
  - A point usually consists of `id`, `vector`, and `payload`

So what this diagram really conveys is: **Different data organization methods determine the problems they excel at solving.**

Let us first roughly understand the three types of databases as follows:

| Type          | Typical Representatives                        | Main Use               | Data Organization Method                                 |
| ------------- | ------------------------------- | ---------------------- | -------------------------------------------- |
| `OLTP` database | `MySQL`, `PostgreSQL`, `Oracle` | Supports daily business transactions       | Usually based on row-column table structures, with a bias toward row-based reads and writes         |
| `OLAP` database | `Hive`, `ClickHouse`, `Doris`   | Supports statistical analysis and report computation | Also table-structured, but more suitable for analytical queries, often columnar storage |
| Vector database    | `Qdrant`                        | Supports semantic similarity retrieval     | Vector points as the core data unit                       |

If compressed into one easy-to-remember sentence, the distinction can be made as follows:

- `OLTP（Online Transaction Processing）` is more of a **business database**, suitable for querying a single row
- `OLAP（Online Analytical Processing）` is more of an **analytical database**, suitable for querying a single column
- A vector database leans more toward **semantic similarity retrieval**

Mapping this diagram back to the "E-commerce Assistant" project makes the division of labor even clearer:

- `MySQL` is responsible for storing metadata and simulated warehouse data
- `Qdrant` is responsible for semantic similarity recall, recalling related fields and metrics based on vector similarity
- `Elasticsearch` is not equivalent to `OLAP` here. It leans more toward being a search engine and full-text retrieval system; in this project, it is mainly responsible for field-value retrieval.

You might ask, **Which of these three types of databases does `Elasticsearch` belong to?**

More specifically, `Elasticsearch` is not exactly equivalent to any single type here. It is better understood as a **search engine / full-text retrieval system**.

In the "E-commerce Assistant" project, its responsibilities are very clear:

- Based on natural language expressions in user questions
- Match real field values that actually exist
- Provide "value-domain" contextual information for subsequent SQL generation

Therefore, the most important conclusion here is not "who replaces whom," but: **structured storage, statistical analysis, semantic recall, and full-text retrieval often require different types of infrastructure services working together.**

### 1.3 Understanding Qdrant Core Concepts

![Example of metric metadata being vectorized separately by name, description, and alias and written into the vector database](../../../%E5%AE%9E%E6%88%98%E9%A1%B9%E7%9B%AE-%E7%94%B5%E5%95%86%E9%97%AE%E6%95%B0/images/5/5-1-3-1.png)

Qdrant's official description of `collection` is very clear: **points within the same collection use the same dimensionality and are compared using the same distance metric.**

If this is your first exposure to vector databases, start by mastering the following concepts:

| Concept         | How to Understand It                                   |
| ------------ | ---------------------------------------------- |
| `collection` | A collection of vector points, which can be analogized to "a table of vectors of the same type" |
| `point`      | A single record within the collection                               |
| `vector`     | The vector corresponding to this record                             |
| `payload`    | Business fields stored alongside the vector                     |
| `distance`   | How similarity is measured                         |

The most common structure of a `point` is as follows:

```json
{
  "id": "column-001",
  "vector": [0.12, 0.98, 0.44, 0.31],
  "payload": {
    "name": "region_name",
    "description": "地区名称"
  }
}
```

Two parameters are particularly important here:

- `size`: vector dimensionality, which must match the output dimensionality of the Embedding model
- `distance`: similarity / distance calculation method. The current project uses `COSINE`

### 1.4 Qdrant Quick Start Example

This quickstart demonstrates the four most basic steps:

```text
初始化客户端
  -> 创建 collection
  -> 写入 points
  -> query_points 查询相似向量
```

Turning this approach into a minimal runnable `.py` example:

Corresponding project file path: `shopkeeper-agent/examples/qdrant_quickstart_demo.py`

```python
import asyncio

from qdrant_client import AsyncQdrantClient, models

QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "quickstart_demo"
VECTOR_SIZE = 4


async def recreate_collection(client):
    """为了让示例可重复运行，先删除旧集合，再重新创建"""
    if await client.collection_exists(COLLECTION_NAME):
        await client.delete_collection(COLLECTION_NAME)

    # Create a collection：创建一个新的集合
    await client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(
            size=VECTOR_SIZE,
            distance=models.Distance.COSINE,
        ),
    )
    print(f"1. 已创建集合：{COLLECTION_NAME}")


async def add_vectors(client):
    """
    写入几个示例向量

    这里同时带上 payload，方便读者理解：
    在 Qdrant 里，一个 point 不只有 vector，还可以附带业务字段
    """
    await client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            models.PointStruct(
                id=1,
                vector=[0.05, 0.61, 0.76, 0.74],
                payload={"name": "订单分析", "type": "report"},
            ),
            models.PointStruct(
                id=2,
                vector=[0.19, 0.81, 0.75, 0.11],
                payload={"name": "销量趋势", "type": "metric"},
            ),
            models.PointStruct(
                id=3,
                vector=[0.36, 0.55, 0.47, 0.94],
                payload={"name": "区域销售额", "type": "dimension"},
            ),
        ],
    )
    print("2. 已写入 3 个向量点。")


async def run_query(client):
    """
    执行一次向量查询

    查询向量会和集合里的点做相似度计算，
    最终返回最相近的几个 point
    """
    query_vector = [0.2, 0.1, 0.9, 0.7]
    result = await client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=3,
        with_payload=True,
    )

    print(f"3. 查询向量：{query_vector}")
    print("4. 查询结果：")
    for i, point in enumerate(result.points, start=1):
        print(
            f"   {i}) id={point.id}, score={point.score:.4f}, payload={point.payload}"
        )


async def main():
    # 直接初始化客户端，方便单独学习 quickstart 的基本用法
    client = AsyncQdrantClient(url=QDRANT_URL)

    try:
        await recreate_collection(client)
        await add_vectors(client)
        await run_query(client)
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
```

Execute the file to verify, and it succeeds:

```bash
(shopkeeper-agent) didilili@DidililiMacBook-Pro shopkeeper-agent % python3 -m examples.qdrant_quickstart_demo

1. 已创建集合：quickstart_demo
2. 已写入 3 个向量点。
3. 查询向量：[0.2, 0.1, 0.9, 0.7]
4. 查询结果：
   1) id=1, score=0.8946, payload={'name': '订单分析', 'type': 'report'}
   2) id=3, score=0.8387, payload={'name': '区域销售额', 'type': 'dimension'}
   3) id=2, score=0.6660, payload={'name': '销量趋势', 'type': 'metric'}
```

What is most worth mastering here is not the sample data itself, but the three APIs:

- `create_collection(...)`: creates a collection and declares dimensionality and distance metric
- `upsert(...)`: updates or inserts points by `id`
- `query_points(...)`: returns the most relevant points based on a query vector

In Qdrant's official API documentation, `query_points` also supports parameters such as `score_threshold`, `limit`, `filter`, `with_payload`, and `with_vector`. The most commonly used ones in the current project are:

- `score_threshold`: controls the minimum recall score
- `limit`: controls the number of returned results
- `with_payload`: controls whether business fields are returned along with the results

`Qdrant` comes with a visualization page. You can usually open the console at http://localhost:6333/dashboard to see which `collection` exist and whether point data has been written successfully. This is convenient for troubleshooting during development.

![Qdrant console page for checking whether collections and point data have been written successfully](../../../%E5%AE%9E%E6%88%98%E9%A1%B9%E7%9B%AE-%E7%94%B5%E5%95%86%E9%97%AE%E6%95%B0/images/5/5-1-4-1.png)

### 1.5 Encapsulating the Qdrant Client

Once the basic concepts of `Qdrant` are understood, reading the encapsulation in the project code becomes much smoother.

In this project, we do not instantiate a new client on the fly in many places. Instead, we wrote a dedicated `QdrantClientManager`. The main purpose is to handle the following consistently: client initialization, client shutdown, reading the service address from configuration files, and ensuring the project uses only a single client instance.

Additionally, there is an important evolution point in this section: in the quick start earlier, the sample code first used a synchronous client to help understand the flow. However, when actually placed into the project, the more appropriate approach is to switch to an **asynchronous client**.

The reason is not complicated:

- Reading and writing to `Qdrant` is essentially network `I/O`
- After a network request is sent, the program usually needs to wait for the server response
- If an asynchronous client is used, this waiting time can yield `CPU` to other coroutines

Therefore, the project ultimately adopts `AsyncQdrantClient`, essentially to stay consistent with the entire asynchronous backend, reduce blocking, and improve overall concurrency utilization.

Corresponding project file path: `shopkeeper-agent/app/clients/qdrant_client_manager.py`

```python
import asyncio
import random
from typing import Optional

from qdrant_client import AsyncQdrantClient, models

from app.conf.app_config import QdrantConfig, app_config


class QdrantClientManager:
    def __init__(self, qdrant_config: QdrantConfig):
        # 保存配置对象，后面初始化客户端时要从这里读取 host 和 port
        self.qdrant_config = qdrant_config
        # 先把 client 声明出来，真正初始化放到 init() 中进行
        self.client: Optional[AsyncQdrantClient] = None

    def _get_url(self):
        # 根据配置文件拼出 Qdrant 服务地址
        return f"http://{self.qdrant_config.host}:{self.qdrant_config.port}"

    def init(self):
        # 创建异步客户端
        # 这里不在 __init__ 中直接初始化，是为了和项目的生命周期管理保持一致
        self.client = AsyncQdrantClient(url=self._get_url())

    async def close(self):
        # 项目关闭时统一关闭客户端连接
        await self.client.close()


# 创建一个全局的管理器对象
# 后续项目中的其他模块都通过它来获取同一套 Qdrant 客户端
qdrant_client_manager = QdrantClientManager(app_config.qdrant)


if __name__ == "__main__":
    # 先初始化客户端，后面的测试逻辑才能真正访问 Qdrant
    qdrant_client_manager.init()

    async def test():
        # 取出真正的 Qdrant 异步客户端
        client = qdrant_client_manager.client

        # 如果集合不存在，就先创建一个集合
        if not await client.collection_exists("my_collection"):
            await client.create_collection(
                collection_name="my_collection",
                vectors_config=models.VectorParams(
                    # 当前集合中的向量维度是 10
                    size=10,
                    # 使用余弦相似度作为距离计算方式
                    distance=models.Distance.COSINE,
                ),
            )

        # 向集合中写入 100 个随机 point
        # 每个 point 都有一个 id 和一个 10 维向量
        await client.upsert(
            collection_name="my_collection",
            points=[
                models.PointStruct(
                    id=i,
                    vector=[random.random() for _ in range(10)],
                )
                for i in range(100)
            ],
        )

        # 用一个随机生成的查询向量做相似度检索
        # limit=10 表示最多返回 10 条结果
        # score_threshold=0.8 表示只保留分数不低于 0.8 的结果
        res = await client.query_points(
            collection_name="my_collection",
            query=[random.random() for _ in range(10)],  # type: ignore
            limit=10,
            score_threshold=0.8,
        )

        # 打印查询结果，便于观察 point 的 id、score 等信息
        print(res)

    # 运行异步测试函数
    asyncio.run(test())
```

Execute the file to verify, and it succeeds:

```bash
(shopkeeper-agent) didilili@DidililiMacBook-Pro shopkeeper-agent % python3 -m app.clients.qdrant_client_manager
points=[ScoredPoint(id=33, version=4, score=0.9287777, payload={}, vector=None, shard_key=None, order_value=None), ScoredPoint(id=45, version=4, score=0.9019778, payload={}, vector=None, shard_key=None, order_value=None), ScoredPoint(id=58, version=4, score=0.90187067, payload={}, vector=None, shard_key=None, order_value=None), ScoredPoint(id=75, version=4, score=0.8799222, payload={}, vector=None, shard_key=None, order_value=None), ScoredPoint(id=66, version=4, score=0.87921834, payload={}, vector=None, shard_key=None, order_value=None), ScoredPoint(id=87, version=4, score=0.8753782, payload={}, vector=None, shard_key=None, order_value=None), ScoredPoint(id=73, version=4, score=0.86765623, payload={}, vector=None, shard_key=None, order_value=None), ScoredPoint(id=27, version=4, score=0.86216307, payload={}, vector=None, shard_key=None, order_value=None), ScoredPoint(id=16, version=4, score=0.8618801, payload={}, vector=None, shard_key=None, order_value=None), ScoredPoint(id=69, version=4, score=0.8546801, payload={}, vector=None, shard_key=None, order_value=None)]
```

**Code Analysis:**

#### 1.5.1 Understanding the Two Layers of Responsibility in the File

This section can be understood at two levels. The first level is encapsulating the `Qdrant` client into a foundational service within the project. The second level is using the test code at the bottom of the file to demonstrate a minimal runnable pipeline. Viewed this way, the file's responsibility is very clear: **the first half manages the client, and the second half explains how to use it**.

#### 1.5.2 Upper Half: What QdrantClientManager Does

Let's look at the manager code in the upper half first. The core goal here is not to "write one more class," but to consolidate the initialization and shutdown of the `Qdrant` client into a single place, so that every part of the project does not need to create and destroy connections on its own.

The most noteworthy parts of this section are the following locations:

- `self.qdrant_config`: stores the `Qdrant` configuration object, from which parameters such as `host` and `port` will later be read
- `_get_url()`: builds the complete service address from the configuration, for example `http://localhost:6333`
- `init()`: actually initializes `AsyncQdrantClient`
- `close()`: closes the client connection uniformly when the program exits
- `qdrant_client_manager = QdrantClientManager(app_config.qdrant)`: creates a globally reusable manager object when the module is loaded

#### 1.5.3 Lower Half: The Minimal Pipeline Demonstrated by the Test Code

Now look at the test code in the lower half. It is not meant to be a "temporary script," but rather to demonstrate the most basic usage flow once this client wrapper is complete. It corresponds to the following pipeline:

1. Check whether `collection` exists
2. If it does not exist, call `create_collection(...)`
3. Write a batch of vector points through `upsert(...)`
4. Perform a similarity query through `query_points(...)`

Once you understand these four steps, you have understood most of this file.

- `collection_name="my_collection"`: specifies which collection the current operation targets
- `models.VectorParams(size=10, distance=models.Distance.COSINE)`: specifies the vector dimension and distance calculation method
- `models.PointStruct(...)`: represents a single point record, which contains at least `id` and `vector`
- `limit=10`: indicates that at most the top 10 most similar results are returned
- `score_threshold=0.8`: indicates that only results with a score of no less than 0.8 are kept

#### 1.5.4 Async Syntax and Where Real Project Vectors Come From

Because an async client is used here, there are two points in the code syntax that would not appear in synchronous examples: all methods that interact with the server must be called via `await`; the test logic must first be placed inside an async function such as `async def test()`, and then executed through `asyncio.run(test())`.

Here, for the purpose of demonstrating the flow, the vectors are randomly generated. In a real project, the vectors written into `Qdrant` are not generated arbitrarily; they come from the encoding results produced by the `Embedding` model on field descriptions, metric descriptions, or user questions.

---

## 2. Elasticsearch Client Integration

### 2.1 Introduction to ES

`Elasticsearch` is not used in the current project to replace MySQL, nor to replace Qdrant.

Its core responsibility is: **to build a full-text index over field values, so that the system can map the user's natural language expressions to actual value ranges that really exist.**

For example:

- The user says "North China region"
- The user says "digital category"
- The user says "directly operated stores"

These expressions are not necessarily field names; they are more likely specific values within some dimension field. At this point, relying only on vector retrieval of fields and metrics is not enough; one more layer of "value domain retrieval" is needed. That is the role ES plays in the current project.

### 2.2 Basic ES Concepts

Official documentation: https://www.elastic.co/guide/en/elasticsearch/reference/8.19/documents-indices.html (English)

In Elasticsearch, first master four terms:

| Concept       | How to understand it                       |
| ---------- | ---------------------------------- |
| `index`    | A logical container for a group of similar documents             |
| `document` | A JSON document within an index           |
| `field`    | A field within a document              |
| `mapping`  | Defines field structure, field types, and indexing behavior |

If we draw an analogy with other infrastructure:

| System            | Structural analogy                                |
| --------------- | --------------------------------------- |
| `MySQL`         | table -> row -> column                          |
| `Qdrant`        | collection -> point -> vector / payload |
| `Elasticsearch` | index -> document -> field              |

In other words, although all three are "storing data," the way they organize data is different:

- MySQL is more oriented toward structured records
- Qdrant is more oriented toward vector points
- Elasticsearch is more oriented toward JSON documents

If we use the most familiar JSON format to understand it, an `document` roughly looks like this:

```json
{
  "id": "v_001",
  "value": "华北地区",
  "column_id": "dim_region.region_name"
}
```

In this example:

- The entire JSON object is an `document`
- `id`, `value`, and `column_id` are `field`
- These documents will be stored in some `index`

It will be easier to understand if we compare it again with the `Qdrant` discussed earlier:

- In `Qdrant`, we would say "write a `point` into a certain `collection`"
- In `Elasticsearch`, we would say "write a `document` into a certain `index`"

This also explains why it is particularly emphasized here: `index` is a **noun** here, meaning an index container; it is not the "write operation" used later in the API. In addition, the results returned by `Elasticsearch` often contain fields starting with an underscore, such as `_index`, `_id`, and `_source`. These are metadata fields that come with ES itself.

Here is a brief correspondence:

- `_index` indicates which index this piece of data belongs to
- `_id` indicates the unique identifier of this piece of data within the index
- What is stored in `_source` is the business data that we actually wrote in

### 2.3 Understanding mapping

`mapping` is essentially the "table structure description" in `Elasticsearch`.

If you have previously worked with relational databases, data modeling, or have seen the term `schema` in other technology stacks, you can directly map the two to each other here: `mapping` is the term used in `Elasticsearch`, while `schema` is the more common term in many databases or data systems.

The core meaning they express here is the same: **use a structural definition to describe what fields this type of data has, what types the fields are, and how they should be indexed and stored.**

Two common approaches should also be specially distinguished here:

- `dynamic mapping`: let `ES` infer field types automatically from the written data
- `explicit mapping`: we explicitly define the field structure and field types

From an engineering perspective, the current project is better suited to the **explicit definition** approach, because it is more controllable and makes it easier for us to precisely design retrieval behavior.

### 2.4 Difference Between text and keyword

`mapping` does not only define "what fields exist"; it also defines "what the data type of each field is." And `text` and `keyword` are two very common field types in `ES`, but they are handled in completely different ways.

That is to say,

1. First there is `index`
2. What is stored in `index` is `document`
3. There are many `field` in `document`
4. `mapping` needs to define the types of these `field`
5. When the field type is a string, the two most common types are `text` and `keyword`

The `text` type is more oriented toward **full-text retrieval**. It is suitable for storing a piece of text content that can be searched using natural language. To support this kind of search, `ES` often first tokenizes the text and then builds an inverted index. What does this mean? It means that what you store is not a string that "must be exactly identical as a whole," but a piece of text that can be split, searched, and matched.

For example: `"华北地区"`, `"数码品类"`, `"近三个月销售额"`. If such values are defined as `text`, users do not necessarily have to type the entire string exactly when querying; instead, they can match them through natural language.

In contrast, `keyword` is more oriented toward **exact matching**. It does not tokenize the way `text` does, and is more suitable for fields that "must be processed as a whole based on the original value."

For example: primary key `id`, field identifier `column_id`, status codes, category codes. These kinds of values are usually not used for full-text search; they are either equal or not equal, so they are better defined as `keyword`.

**Different field types lead to different ways ES later builds indexes and performs retrieval.** This is exactly why `mapping` matters. We are not casually declaring a field as some type; we are telling `ES` in advance: how this field is intended to be searched in the future.

In the "Shopkeeper Data Q&A" project, this distinction becomes very concrete: the `value` among field values is suitable for definition as `text`, because users will search for it using natural language, such as "North China region" or "digital category." `id` and `column_id` are more suitable for definition as `keyword`, because they are more like structured identifiers: they do not need tokenization and only need exact matching.

This point can also be seen in the actual code of the project, in the corresponding file: `shopkeeper-agent/app/repositories/es/value_es_repository.py`

The index mapping is roughly as follows:

```python
index_mappings = {
    "dynamic": False,
    "properties": {
        "id": {"type": "keyword"},
        "value": {
            "type": "text",
            "analyzer": "ik_max_word",
            "search_analyzer": "ik_max_word",
        },
        "column_id": {"type": "keyword"},
    },
}
```

One detail here is also worth noting: the `value` field uses `ik_max_word`, which shows that the project uses a Chinese tokenizer to improve matching performance when searching Chinese text. This setting also once again illustrates that the `value` field is not retrieved by "exact whole-string equality," but is processed according to the idea of full-text retrieval.

### 2.5 Common Ways to Use ES

There are roughly two common ways to use `Elasticsearch`:

1. Call the `REST API` directly
2. Use a language client within an application

If you are only doing testing or debugging, the first method is very convenient. For example, we can directly execute API requests in the `Dev Tools` of `Kibana` to verify whether the index was created successfully, whether documents were written successfully, and whether the query returns the expected results.

In this project, the more common real-world development method is the second one, that is, using the `elasticsearch` client library in Python code. This also explains why we will specifically wrap an `ESClientManager` next.

### 2.6 ES Quick Start Example

Official documentation: https://www.elastic.co/guide/en/elasticsearch/reference/8.19/full-text-filter-tutorial.html (English)

This tutorial is not about Python client wrapping, but rather about **walking through a typical Elasticsearch usage flow directly through the REST API**. It is usually best executed in the `Dev Tools` of `Kibana`, so it is very suitable for building intuition.

If we translate it into an easier-to-understand pipeline, it roughly looks like this:

```text
创建 index
  -> 定义 mapping
  -> 批量写入文档
  -> 使用 _search 做全文检索
  -> 再叠加 filter 做精确过滤
```

First look at the complete example code. It connects together "cleaning up the old index, creating the index, defining the mapping, writing documents in bulk, full-text retrieval, and adding filters on top."

```python
# 如果之前已经创建过 cooking_blog，可以删掉旧索引
DELETE /cooking_blog

# 创建索引
PUT /cooking_blog

# 定义字段结构
PUT /cooking_blog/_mapping
{
  "properties": {
    "title": { "type": "text" },
    "description": { "type": "text" },
    "author": { "type": "text" },
    "date": { "type": "date", "format": "yyyy-MM-dd" },
    "category": { "type": "text" },
    "tags": { "type": "text" },
    "rating": { "type": "float" }
  }
}

# 批量写入文档
POST /cooking_blog/_bulk?refresh=wait_for
{"index":{"_id":"1"}}
{"title":"Perfect Pancakes","description":"Fluffy pancakes for breakfast","author":"Maria Rodriguez","date":"2023-05-01","category":"Breakfast","tags":["pancakes","breakfast"],"rating":4.8}
{"index":{"_id":"2"}}
{"title":"Vegetarian Curry","description":"A spicy and comforting curry","author":"Aisha Khan","date":"2023-06-10","category":"Dinner","tags":["vegetarian","curry","spicy"],"rating":4.7}
{"index":{"_id":"3"}}
{"title":"Berry Smoothie Bowl","description":"A healthy breakfast with fresh berries","author":"Liam Turner","date":"2023-07-03","category":"Breakfast","tags":["smoothie","berries","healthy"],"rating":4.6}
{"index":{"_id":"4"}}
{"title":"Chocolate Lava Cake","description":"Rich chocolate cake with a gooey center","author":"Sophia Chen","date":"2023-08-12","category":"Dessert","tags":["chocolate","cake","dessert"],"rating":4.9}

# 全文检索
GET /cooking_blog/_search
{
  "query": {
    "match": {
      "description": "fluffy pancakes"
    }
  }
}

# 全文检索 + 过滤查询
GET /cooking_blog/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "description": "breakfast"
          }
        }
      ],
      "filter": [
        {
          "range": {
            "rating": {
              "gte": 4.7
            }
          }
        }
      ]
    }
  }
}
```

This example is most suitable for helping beginners master the following tasks:

1. Create an `index`
2. Define a `mapping`
3. Write `document` in bulk
4. Use `_search` for full-text retrieval
5. Add exact filtering on top of full-text retrieval

If we map this official example back to the current project, it will be easier to understand:

- `cooking_blog` is only a teaching-oriented `index`
- The recipe documents are only a teaching-oriented `document`
- `match`, `filter`, and `_search` are the real capabilities we need to master

In other words, although this example uses a cooking blog scenario, what it really aims to teach is the most basic and universal way of working with ES. Later, when we apply it to the "Shopkeeper Data Q&A" project, recipes will be replaced with field values, tags, or metadata, but the underlying approach will remain the same.

If this set of code runs successfully in `Dev Tools` and `_search` can retrieve results, it means you have already completed the minimal ES usage path.

![Response result of running the cooking_blog example in Kibana Dev Tools](../../../%E5%AE%9E%E6%88%98%E9%A1%B9%E7%9B%AE-%E7%94%B5%E5%95%86%E9%97%AE%E6%95%B0/images/5/5-2-6-1.png)

### 2.7 Understanding bulk and match

There are two more very commonly used APIs in the quick start that need to be understood separately.

#### 2.7.1 bulk

`bulk` is used for bulk writes, making it suitable for writing multiple documents at once. Its structure may seem a bit confusing at first because it uses an alternating pattern of "operation instruction + data body". For example:

```python
await client.bulk(
    operations=[
        {"index": {"_index": "my-books"}},
        {"name": "1984", "author": "George Orwell"},
        {"index": {"_index": "my-books"}},
        {"name": "Brave New World", "author": "Aldous Huxley"},
    ],
)
```

The structure here is actually very simple:

- First specify "I want to perform an `index` write"
- Then provide "the data for this write"
- Then continue to the next operation

#### 2.7.2 match

`match` is one of the most common full-text search query methods in ES. For example:

```python
await client.search(
    index="my-books",
    query={
        "match": {
            "name": "brave"
        }
    },
)
```

What this code means is:

- Search in the index `my-books`
- Focus on the `name` field
- The query term is `brave`

ES will perform text matching based on this query term and return the most relevant results. In the "Shopkeeper Data Q&A" project, this approach will later become: searching for `value` in the field value index; the query terms may be natural language like "North China region" or "digital category".

### 2.8 Wrapping the ES client

Just like the earlier `Qdrant`, the `Elasticsearch` client should not be created on the fly every time it is used. A more reasonable approach is to wrap it in a unified manager responsible for: reading the `host` and `port` from the configuration file, initializing the client, closing the client when the program exits, and allowing the entire project to share the same client object.

Corresponding project file path: `shopkeeper-agent/app/clients/es_client_manager.py`

```python
import asyncio
from typing import Optional

from elasticsearch import AsyncElasticsearch

from app.conf.app_config import ESConfig, app_config


class ESClientManager:
    def __init__(self, es_config: ESConfig):
        # 保存 ES 配置对象，后面初始化客户端时会从这里读取 host 和 port
        self.es_config = es_config
        # 先把 client 声明出来，真正初始化放到 init() 中进行
        self.client: Optional[AsyncElasticsearch] = None

    def _get_url(self):
        # 根据配置文件拼出 ES 服务地址
        return f"http://{self.es_config.host}:{self.es_config.port}"

    def init(self):
        # 创建异步 ES 客户端
        # hosts 之所以是列表，是为了兼容 ES 常见的集群连接方式
        self.client = AsyncElasticsearch(hosts=[self._get_url()])

    async def close(self):
        # 在程序退出时统一关闭客户端连接
        await self.client.close()


# 创建一个全局可复用的 ES 客户端管理器对象
es_client_manager = ESClientManager(app_config.es)

if __name__ == "__main__":
    # 先初始化客户端，后面的测试逻辑才能真正访问 ES
    es_client_manager.init()

    async def test():
        # 取出真正的 AsyncElasticsearch 客户端
        client = es_client_manager.client

        # 创建索引
        # 这里同时显式定义了字段结构
        # dynamic=False 表示关闭动态映射，要求写入数据必须符合当前定义
        await client.indices.create(
            index="my-books",
            mappings={
                "dynamic": False,
                "properties": {
                    # 书名和作者适合做全文检索，所以定义为 text
                    "name": {"type": "text"},
                    "author": {"type": "text"},
                    # 日期字段按日期类型处理
                    "release_date": {"type": "date", "format": "yyyy-MM-dd"},
                    # 页数字段按整数处理
                    "page_count": {"type": "integer"},
                },
            },
        )

        # 插入数据
        # bulk 采用“操作说明 + 数据本体”交替出现的格式
        # 适合一次性写入多条文档
        await client.bulk(
            operations=[
                {"index": {"_index": "my-books"}},
                {
                    "name": "Revelation Space",
                    "author": "Alastair Reynolds",
                    "release_date": "2000-03-15",
                    "page_count": 585,
                },
                {"index": {"_index": "my-books"}},
                {
                    "name": "1984",
                    "author": "George Orwell",
                    "release_date": "1985-06-01",
                    "page_count": 328,
                },
                {"index": {"_index": "my-books"}},
                {
                    "name": "Fahrenheit 451",
                    "author": "Ray Bradbury",
                    "release_date": "1953-10-15",
                    "page_count": 227,
                },
                {"index": {"_index": "my-books"}},
                {
                    "name": "Brave New World",
                    "author": "Aldous Huxley",
                    "release_date": "1932-06-01",
                    "page_count": 268,
                },
                {"index": {"_index": "my-books"}},
                {
                    "name": "The Handmaids Tale",
                    "author": "Margaret Atwood",
                    "release_date": "1985-06-01",
                    "page_count": 311,
                },
            ],
        )

        # 搜索
        # 在 name 字段上执行 match 查询
        # 这里演示的是最基础的全文检索能力
        resp = await client.search(
            index="my-books",
            query={"match": {"name": "brave"}},
        )

        # 打印查询结果，便于观察 hits 和返回结构
        print(resp)

        # 测试结束后关闭客户端连接
        await es_client_manager.close()

    # 运行异步测试函数
    asyncio.run(test())

```

Run the file to verify it succeeds:

```bash
(shopkeeper-agent) didilili@DidililiMacBook-Pro shopkeeper-agent % python3 -m app.clients.es_client_manager
{'took': 5, 'timed_out': False, '_shards': {'total': 1, 'successful': 1, 'skipped': 0, 'failed': 0}, 'hits': {'total': {'value': 1, 'relation': 'eq'}, 'max_score': 1.2067741, 'hits': [{'_index': 'my-books', '_id': 'SDB_np0BrzSqcXAMSMVk', '_score': 1.2067741, '_source': {'name': 'Brave New World', 'author': 'Aldous Huxley', 'release_date': '1932-06-01', 'page_count': 268}}]}}
```

![Result returned after successfully running the ESClientManager test code](../../../%E5%AE%9E%E6%88%98%E9%A1%B9%E7%9B%AE-%E7%94%B5%E5%95%86%E9%97%AE%E6%95%B0/images/5/5-2-8-1.png)

#### 2.8.1 What this layer of wrapping does

This file actually accomplishes two layers of work:

1. Wraps a globally reusable `ES` asynchronous client
2. Uses the test code at the bottom of the file to demonstrate the minimal usage flow of `ES`

#### 2.8.2 Explanation of \_get_url(), init(), and close()

First look at the manager code in the upper half. Its approach is consistent with the earlier `QdrantClientManager`, and its core is also three things:

1. Save the `ES` configuration
2. Create an asynchronous client in `init()`
3. Close the client in `close()`

Here you can focus on the following parts:

- `self.es_config`: saves the configuration object, which contains parameters such as `host`, `port`, and `index_name`
- `_get_url()`: combines the address in the configuration into a complete URL, for example `http://localhost:9200`
- `init()`: creates the `AsyncElasticsearch` client
- `close()`: closes the connection when the program exits or the lifecycle ends
- `es_client_manager = ESClientManager(app_config.es)`: creates a globally reusable client manager object

The most important conclusion here is actually the same as with `Qdrant`: **the entire project keeps only this one `ES` client manager, and all other places reuse it**. This avoids repeatedly creating connections and also keeps the management approach of the basic service layer consistent.

#### 2.8.3 What minimal path does the test code at the bottom demonstrate

Now look at the test code in the lower half, which corresponds to the minimal usage flow of `ES`:

```text
初始化客户端
  -> 创建 index
  -> 写入 document
  -> search 查询文档
```

If we break it down by actions, the main steps are as follows:

- `client.indices.create(...)`: create an index named `my-books` and explicitly specify the field structure
- `client.bulk(...)`: bulk write multiple documents
- `client.search(...)`: use `match` to search for `"brave"` in the `name` field
- `await es_client_manager.close()`: close the client after the test ends to avoid leaving unclosed connections behind

#### 2.8.4 Understanding key parameters

In addition, because an asynchronous client is used here, the test code must follow the same rules as the earlier `Qdrant`:

- The actual test logic is written inside `async def test()`
- When calling client methods, use `await`
- Use `asyncio.run(test())` at the outermost level to start the entire asynchronous process

Although this section is a demonstration example, it already connects the core usage pattern of `ES`: **first define the index structure, then write documents, and finally retrieve data based on query conditions.**

You may wonder why the official example sometimes passes `api_key`, while the code here only passes `hosts`. The reason is that the teaching project currently uses a local `Docker` environment with security authentication disabled, so only the connection address is needed for local development. In other words, this version of the code is closer to: a single-node local development environment with authentication disabled for convenient and rapid debugging.

In a more complete production environment, `ES` often involves:

- Deployment as a cluster rather than a single node
- Security authentication enabled
- Additionally providing `api_key` or other authentication information

We can understand this further:

- `hosts` is written in plural form not arbitrarily, but because `Elasticsearch` natively supports cluster deployment
- An `ES` cluster can contain multiple nodes, each usually running on a different server or container
- Data in an `index` can be distributed across multiple nodes in the form of **shards**
- To improve availability, **replicas** can also be prepared for these shards

Therefore, from an operations perspective, the `ES` client is not just "connecting to a single server", but may be interacting with **a cluster composed of a group of nodes**.

However, for the current project, it is enough at this layer to know the conclusion:

- This teaching environment is **single-node**
- Therefore, although `hosts` is a list, it usually contains only one address
- Capabilities such as sharding, replicas, and failover are inherent background capabilities of `ES` as a distributed search engine
- The focus of this chapter is still on "integrating the client into the project and completing basic usage", not on an in-depth discussion of cluster operations

Therefore, using `hosts=[self._get_url()]` here does not mean `ES` can only be connected this way, but rather that the current tutorial environment has been simplified.

We should also go one step further and understand its purpose in a real project. The `my-books` example above is mainly to help us quickly understand the client code style; in the actual "Shopkeeper Data Q&A" project, the more important role of `ES` is to build a full-text index for field values.

In other words, the data written in a real project will not be book titles and authors, but more likely a structure like this:

```json
{
  "id": "value_001",
  "value": "华北地区",
  "column_id": "dim_region.region_name"
}
```

In this way, when a user question contains natural language expressions such as "North China region", the system can find the real field value through `ES` and feed it back to the subsequent SQL generation process. That is to say, the `my-books` in the example is only a teaching dataset, and what the project really needs to reuse is this basic approach of **wrapping the client -> creating the index -> writing documents -> executing retrieval**. This connects with the Embedding service integration in [Chapter 6: MySQL, Embedding Integration, and Log Management](6-MySQL%E3%80%81Embedding%E4%B8%8E%E6%97%A5%E5%BF%97%E7%AE%A1%E7%90%86.md).

---

**Chapter summary:**

- **Qdrant** is responsible for vector storage and semantic similarity retrieval, with the core concept being `collection / point / vector / payload`.
- **Elasticsearch** is responsible for full-text retrieval and field value matching, with the core concept being `index / document / field / mapping`.
- In the project, these two are not an either-or choice; instead, they provide candidate results from the **semantic layer** and the **text layer** respectively for the subsequent data query flow.
- From a code organization perspective, the project manages asynchronous clients uniformly through `QdrantClientManager` and `ESClientManager`, which is fully consistent with the configuration system discussed in the previous article.

The next article will continue to cover the remaining basic services: **MySQL, Embedding, and log management**. Among them, MySQL handles structured storage, Embedding handles vector generation, and logs make the entire backend operation process observable and debuggable.
