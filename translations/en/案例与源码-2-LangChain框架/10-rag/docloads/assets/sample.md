# Introduction to Speculative Decoding

## Introduction

Speculative Decoding is an advanced inference optimization technique used to accelerate the autoregressive text generation process of Large Language Models (LLMs) while ensuring that output quality is not affected. Inspired by speculative execution in computer architecture, this technique aims to solve the latency problem caused by serial dependencies when LLMs generate long sequences. By introducing a small draft model to "guess" multiple future tokens, and then having the target large model verify these guesses in parallel, speculative decoding can significantly improve inference speed, typically achieving a 2x to 3x speedup without changing the model's output distribution.

## History and Development

The concept of speculative decoding can be traced back to the 2022 research paper "Fast Inference from Transformers via Speculative Decoding" (arXiv:2211.17192), proposed by a Google research team. Targeting the inference bottleneck of Transformer models, this paper introduced a mechanism that uses an approximate model to generate candidate tokens and has the target model verify them in parallel, achieving a 2x-3x speedup on the T5-XXL model.

In 2023, another key paper, "Accelerating Large Language Model Decoding with Speculative Sampling" (arXiv:2302.01318), extended this idea by proposing a speculative sampling algorithm that achieved a 2-2.5x distributed speedup on the Chinchilla 70B model. In the same year, variants such as Medusa (arXiv:2401.10774) introduced tree attention mechanisms and multiple decoding heads, further improving efficiency.

By 2024-2025, variants of speculative decoding emerged in abundance, including Self-Speculative Decoding, EAGLE, and Multimodal Speculative Decoding (MSD). A comprehensive survey titled "Unlocking Efficiency in Large Language Model Inference: A Comprehensive Survey of Speculative Decoding" (arXiv:2401.07851) systematically categorized existing methods and introduced the Spec-Bench benchmark. These developments have extended speculative decoding from text-only LLMs to multimodal models, and it has been widely applied in production environments, such as Google products and Groq chips.

## The Bottleneck of Autoregressive Decoding

Before understanding speculative decoding, it is necessary to analyze the limitations of traditional autoregressive decoding. LLMs such as the GPT series are based on the Transformer architecture, and the sequence generation process is autoregressive:

- **Process description**: In the traditional autoregressive generation process, the model generates only one token at a time: $P(x_t \mid x_{1:t-1})$. Each new token generation requires another round of forward propagation. This causes the computational cost of generation to grow linearly with the number of tokens, which is extremely inefficient especially for long text generation.
- **KV cache mechanism**: To avoid recomputation, the model maintains a Key-Value (KV) cache, but it still needs to be updated serially.

**Main bottlenecks**:

- **Serial dependency**: Each token generation requires a complete forward propagation, with parameters loaded from high-bandwidth memory (HBM) to accelerator cache, causing a memory bandwidth bottleneck.
- **Computational overhead**: Each propagation pass of a large model (such as 70B parameters) takes milliseconds. For a long sequence T, the total latency is approximately T times the single-step time.
- **Hardware limitations**: On GPUs/TPUs, batch support is limited, preventing full utilization of parallel capabilities.
- **Energy consumption**: Frequent memory access increases power consumption and affects deployment costs.

These problems are particularly prominent in real-time applications (such as chatbots), and speculative decoding alleviates them through parallel verification.

## Core Principles and Algorithm

The core of speculative decoding is to use a small draft model to quickly generate a draft sequence, which is then verified in parallel by the target model to ensure that the output distribution remains unchanged.

### Key Components

- **Draft Model**: Has a small number of parameters (1/10-1/5 of the target model), trained through knowledge distillation, and generates tokens quickly.
- **Target Model**: The original LLM, used for verification.
- **Speculation depth gamma**: The length of the draft sequence, usually 4-8.

### Detailed Algorithm Steps

1. **Initialization**: Current context $S = [x_1, \dots, y_{t-1}]$, KV cache ready.
2. **Draft generation phase**: Use the draft model to autoregressively generate gamma tokens: $d_1, d_2, \dots, d_\gamma$. This step is serial but fast.
3. **Verification phase**: Append the draft to S to form $S' = S + [d_1, \dots, d_\gamma]$. The target model computes logits for all positions in parallel: $p(y | S + [d_1, \dots, d_{i-1}])$ for i=1 to gamma.
4. **Rejection Sampling**:
   - For each position i, calculate the draft distribution q and target distribution p.
   - If $\frac{p(d_i | \cdot)}{q(d_i | \cdot)} > u$ (u ~ Uniform[0,1]), accept $d_i$.
   - Otherwise, reject and sample a new token from p.
5. **Acceptance and rollback**: Accept the first m consecutively matched tokens (m <= gamma), update S and the KV cache. Sample the (m+1)-th token from p as a correction.
6. **Iteration**: Repeat until generation is complete.

### Mathematical Foundation

Let p be the target distribution and q be the draft distribution. Speculative sampling ensures that generation follows p:

- Sampling probability: For a draft token d, the acceptance probability is $min(1, p(d)/q(d))$.
- Corrective sampling: If rejected, sample from $(p - q') / (1 - sum min(1, p/q))$, where $q' = min(q, p)$.
  This maintains distributional equivalence within hardware numerical precision.

## Variants and Extensions

Speculative decoding has many variants to adapt to different scenarios:

- **Tree-structured Speculation**: Such as Medusa, which uses multiple decoding heads to predict branches in parallel, improving hit rate. Medusa-1 is fine-tuned on a frozen backbone, achieving a 2.2x speedup; Medusa-2 uses joint fine-tuning, achieving a 2.3-3.6x speedup.
- **Self-Speculative Decoding**: Uses the same model to generate drafts through partial forward propagation or low-rank approximation, avoiding an additional model.
- **EAGLE**: Combines autoregressive and non-autoregressive methods, supported in vLLM, speculating 5 tokens.
- **Lookahead Decoding**: A draft-free variant that uses n-gram or Jacobian approximation for acceleration.
- **Multimodal Extension (MSD)**: For MLLMs such as LLaVA-7B, processes text/visual tokens separately, trains the draft model in two stages, achieving a 2.29x speedup.
- **Distributed Speculation**: Multi-GPU environments, suitable for extremely large-scale models.

These variants are evaluated through the Spec-Bench benchmark, demonstrating superiority across various tasks.

## Advantages and Limitations

### Advantages

- **Speed and efficiency**: 2-3x speedup, reducing inference latency and energy consumption.
- **Quality preservation**: Theoretically lossless, with an output distribution equivalent to the original model.
- **Flexibility**: Can be combined with quantization, FlashAttention, and others for further optimization.
- **Deployment-friendly**: Suitable for edge devices and cloud services, supporting real-time applications.

### Limitations

- **Draft accuracy dependency**: If the draft model is poor, frequent rollbacks reduce efficiency.
- **Additional preparation**: Requires training a draft model, or handling floating-point precision errors.
- **Batching limitations**: Standard implementations do not support high-throughput batching.
- **Not suitable for short sequences**: Benefits are limited for very short generation tasks.
