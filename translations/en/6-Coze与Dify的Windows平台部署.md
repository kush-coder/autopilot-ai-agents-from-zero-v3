# 6 - Deploying Coze and Dify on Windows

This chapter focuses on **hands-on deployment**: getting common low-code agent platforms running on Windows. Docker Desktop installation and general troubleshooting have been consolidated into Chapter 8, and this chapter goes directly into the deployment processes for **Coze Studio**, **Dify**, and **Coze Loop**.

---

**Chapter learning objectives:**

- Understand why Coze, after being open-sourced, has practical value in private deployment, B-end delivery, and intranet scenarios.
- Distinguish between the three deployment targets: **Coze Studio** handles development and debugging, **Dify** handles workflows, knowledge bases, and application publishing, and **Coze Loop** handles evaluation, experimentation, tracing, and operations.
- Complete a minimal deployment of **Coze Studio** on Windows: confirm the Docker environment -> get the code -> configure the model -> start with `docker compose` -> access via browser.
- Complete a minimal deployment of **Dify** on Windows: confirm the Docker environment -> get the code -> configure `.env` -> `docker compose up -d` -> access via browser.
- Understand two common model integration routes: **cloud API models** and **local Ollama models**, and know which scenarios each is suitable for.

**Study advice:** Don't try to absorb everything in this chapter at once; first pick one route and get it working end to end. If you haven't installed Docker Desktop yet, start with [Chapter 8: Windows Pre-installation Preparation](8-Docker%E5%BF%AB%E9%80%9F%E5%85%A5%E9%97%A8%E4%B8%8EDify%E9%83%A8%E7%BD%B2%E6%8E%92%E9%9A%9C.md#_22-windows-pre-installation-preparation). If you only want to try Coze, first complete Coze Studio and model configuration; if you only want to try Dify, first get the Dify service started and be able to log in. Coze Loop can wait until Studio is up and running. Model configuration is where things most easily get stuck: if you choose Volcano Ark, prepare your API Key and Endpoint in advance; if you choose Ollama, first confirm that the local model has been pulled successfully.

---

## 1. Overview

### 1.1 Why You Should Care About Local Deployment

Building agents on a cloud platform is convenient, but enterprise projects typically care about three additional things:

- **Data boundaries**: whether business data must remain in the intranet or in the enterprise's own environment.
- **Delivery method**: whether the platform, models, and business systems need to be delivered together to the customer.
- **Operational controllability**: whether you can control versions, logs, networks, and resources yourself.

After Coze was open-sourced, local deployment became another option. Previously, many B-end deliveries prioritized privately deployable platforms such as Dify and n8n; now, if a team is already familiar with Coze's agent, plugin, and workflow systems, the open-source version of Coze can also be included in the technology selection.

From a learning and delivery perspective, the appeal of the open-source Coze mainly lies in three points:

- **Friendly licensing**: It uses the Apache 2.0 license, which facilitates commercial use and secondary development.
- **More complete pipeline**: It covers Agent development, evaluation and operations, and deployment-related capabilities.
- **Lower hardware threshold**: An ordinary computer can complete a minimal experience; you don't necessarily need to start with high-spec GPU servers.

There is no need to frame this as "one replacing the other." A more appropriate understanding is: **cloud platforms are suitable for rapid validation, while local deployment is suitable for scenarios with higher requirements for security, integration, and delivery.**

### 1.2 Common Deployment Main Line in This Chapter

Whether you are deploying Coze Studio, Dify, or Coze Loop, getting through your first successful run revolves around the same main line:

| Stage          | What to accomplish                      | Common pitfalls                             |
| ------------- | ------------------------------- | ------------------------------------------ |
| 1. Environment preparation   | Confirm Docker; install Git and Go if necessary | Docker not started, network proxy or image source unavailable      |
| 2. Get the code   | Download or clone the official repository              | GitHub is slow, wrong directory level                    |
| 3. Modify configuration   | Configure model, port, or `.env`         | API Key, Endpoint, port, or file location entered incorrectly      |
| 4. Start the service   | Execute Docker Compose command        | Not executed in the correct directory, image pull failure, port occupied |
| 5. Browser verification | Open the local address and complete initialization        | Page opens but model unavailable, or service not fully started   |

The steps later in this chapter all unfold along this line. As long as this line goes smoothly, deployment issues become much easier to troubleshoot.

### 1.3 How to Choose Between Cloud Models and Local Models

Model configuration is the real core of this chapter. Getting Docker running is only the first step; only after the model is connected can the platform actually create and run agents.

| Configuration method         | Advantages                                 | Disadvantages                                             | Better suited for                           |
| ---------------- | ------------------------------------ | ------------------------------------------------ | ---------------------------------- |
| Cloud API model    | Strong capability, fast response, relatively straightforward configuration         | Requires internet access, usually incurs usage costs, data passes through cloud service providers   | Learning, testing, rapid validation               |
| Local Ollama model | More controllable data, usable offline, no dependency on external APIs | Higher requirements on local hardware; model capability and speed depend on local resources | Intranet, privacy-sensitive, and those who want full control over models |

If the goal is to get through the workflow as quickly as possible, prioritize cloud APIs; if you care more about privatization and data controllability, then consider Ollama.

> **Key reminder:** If the page opens but you cannot see models or cannot invoke applications, first check `api_key`, `model`, `endpoint` in the model configuration file, as well as whether the local Ollama service is running normally, rather than immediately suspecting the frontend page.

---

## 2. Installing and Configuring Coze Studio

![Overview diagram of the four-stage Coze Studio local deployment process](../../images/6/6-2-0-1.png)

### 2.1 Getting the Coze Studio Project

Coze Studio can be obtained either via Git clone or by directly downloading a ZIP package. Choose either method.

```bash
git clone https://github.com/coze-dev/coze-studio.git
```

Execute in the Docker Desktop terminal:

![Interface of cloning the Coze Studio repository in the Docker Desktop terminal](../../images/6/6-2-1-1.png)

> If Git is not installed on this machine, download and install it from https://git-scm.com/downloads. After installation, reopen the terminal and then run `git clone`.

### 2.2 Configuring the Model

Before starting the open-source version of Coze Studio for the first time, you need to configure the model service first. Otherwise, even if the page can be opened, no available models can be selected when creating Agents or workflows.

Go to the root directory of `coze-studio`, type `cmd` in the address bar, and press Enter:

![Interface of entering cmd in the Coze Studio root directory address bar](../../images/6/6-2-2-1.png)

First, copy the Volcano Ark Doubao model template file:

```bash
copy backend\conf\model\template\model_template_ark_doubao-seed-1.6.yaml backend\conf\model\ark_doubao-seed-1.6.yaml
```

The three key fields in the configuration file are:

| Field                       | Description                                                              |
| -------------------------- | ----------------------------------------------------------------- |
| `id`                       | Model ID in Coze Studio, defined by the developer; must be a non-zero integer and globally unique |
| `meta.conn_config.api_key` | API Key for the online model service                                            |
| `meta.conn_config.model`   | Model ID of the online model service; taking Volcano Ark as an example, fill in the Endpoint ID here       |

> Once a model is online, do not arbitrarily modify `id`. If you are only learning and testing, you can start by using the example and giving it a pure numeric value of 5 or more digits.

#### 2.2.1 Option 1: Cloud API Model (Volcano Ark Example)

The cloud API route is suitable for getting the platform's functionality working first. It does not consume local inference resources, but requires internet access and usually incurs usage fees.

**Step 1: Create an API Key**

Go to the Volcano Engine official website https://www.volcengine.com and open the console.

![Volcano Engine console homepage interface](../../images/6/6-2-2-2.png)

Search for and enter "Volcano Ark", then click "Create API Key" under "API Key Management".

![Volcano Ark interface for creating an API Key](../../images/6/6-2-2-3.png)

Click the small eye icon to view the API Key, and copy it for later use.

![Volcano Ark interface for viewing the API Key](../../images/6/6-2-2-4.png)

**Step 2: Create an Endpoint**

Enter the "Online Inference" page, select "Custom Inference Access Point", and click "Create Inference Access Point".

![Volcano Ark interface for creating an inference access point](../../images/6/6-2-2-5.png)

Enter a name for the access point; it is recommended to name it after the model, then click "Add Model".

![Volcano Ark interface for setting the inference access point name and adding a model](../../images/6/6-2-2-6.png)

Models can include Doubao, DeepSeek, Kimi, Qwen, and others. Here we use Doubao 1.6 as an example.

![Volcano Ark interface for selecting the Doubao model access point](../../images/6/6-2-2-7.png)

You can also add a model from another entry:

![Alternative entry interface for adding a model in Volcano Ark](../../images/6/6-2-2-8.png)

Check the agreement and click "Activate Model and Connect".

![Volcano Ark interface for checking the agreement and activating model connection](../../images/6/6-2-2-9.png)

If this is the first time activating the model, the platform may require real-name authentication; complete it according to the on-screen prompts.

After creation is complete, copy the Endpoint ID. Note: the ID below the model name is the Endpoint that will be filled into the configuration file later.

![Volcano Ark interface for copying the Endpoint ID](../../images/6/6-2-2-10.png)

**Step 3: Write into the Coze Studio Configuration File**

Open the `backend\conf\model\ark_doubao-seed-1.6.yaml` file copied earlier.

First change `id` to any pure numeric value of 5 or more digits.

![Interface for editing the Coze Studio model configuration file](../../images/6/6-2-2-11.png)

Then write the API Key and Endpoint into the corresponding positions, save and close the file.

![Interface for filling in the API Key and Endpoint in the Coze Studio model configuration file](../../images/6/6-2-2-12.png)

#### 2.2.2 Option 2: Local Ollama Model

The Ollama route is suitable for scenarios that place more emphasis on privatization, offline availability, and data controllability. However, it has higher requirements on local hardware, and the model's speed and effectiveness also depend on the model you pull and your computer's resources.

First install Ollama on this machine and pull a model, for example:

```bash
ollama pull qwen2.5:7b
```

![Interface for installing Ollama locally and preparing to pull a model](../../images/6/6-2-2-13.png)

Then find the Ollama model configuration template `model_template_ollama.yaml` in the Coze Studio project, copy and rename it to `model_ollama.yaml`, and place it in the `backend/conf/model/` directory.

![Interface for copying the Ollama model configuration template file](../../images/6/6-2-2-14.png)

Modify the following in the configuration file:

- `base_url`: usually fill in `http://host.docker.internal:11434`
- `model`: fill in the model name you pulled through Ollama, for example `qwen2.5:7b`

![Interface for modifying base_url and model in the Ollama model configuration file](../../images/6/6-2-2-15.png)

### 2.3 Starting Coze Studio

After model configuration is complete, enter the `docker` directory in the project.

![Interface showing the location of the docker directory in the Coze Studio project](../../images/6/6-2-3-1.png)

First type `docker` in the terminal and press Enter. If you see help-like information, it means the Docker command is available.

![Interface for verifying whether Docker is installed successfully in the terminal](../../images/6/6-2-3-2.png)

Next, copy the environment configuration file:

```bash
copy .env.example .env
```

> On Windows, use `copy`; on Linux / macOS, you can use `cp .env.example .env`.

![Interface for copying Coze Studio's .env.example to .env](../../images/6/6-2-3-3.jpeg)

Execute in the `coze-studio\docker` directory:

```bash
docker compose --profile '*' up -d
```

![Command-line interface for starting Coze Studio in Docker](../../images/6/6-2-3-4.png)

This command enables all profiles through Compose and starts the services in the background. The general meaning of `docker compose up -d` can be found in [Chapter 8: Compose](8-Docker%E5%BF%AB%E9%80%9F%E5%85%A5%E9%97%A8%E4%B8%8EDify%E9%83%A8%E7%BD%B2%E6%8E%92%E9%9A%9C.md#_32-compose).

The first startup may take 5-10 minutes, depending on the network and image pull speed. Seeing results similar to the following indicates that the services have started.

![Log interface after Coze Studio starts successfully](../../images/6/6-2-3-5.png)

After startup, check the running status:

```bash
docker compose ps
```

You can also open Docker Desktop and confirm in the container list whether the related services are running.

![Interface for viewing Coze Studio container running status](../../images/6/6-2-3-6.png)

### 2.4 Accessing Coze Studio

Access in the browser:

```text
http://localhost:8888/
```

![Login interface when accessing Coze Studio in the browser](../../images/6/6-2-4-1.png)

After logging in, you can enter the Coze Studio main interface.

![Coze Studio main interface after login](../../images/6/6-2-4-2.png)

The open-source version's features are not exactly the same as the commercial version. When learning, focus on: whether you can log in, whether you can see the models, and whether you can create an Agent or workflow.

---

## 3. Installing and Starting Dify

Dify's local deployment on Windows is more straightforward than Coze Studio. It does not require configuring model files in code first. The core workflow is: **get the project -> enter the `docker` directory -> copy `.env` -> start Compose -> access in the browser**.

This section covers only the minimal deployment process. Docker general concepts, image pull failures, container status anomalies, data locations, backup and upgrades, and database connections are all covered in [Chapter 8: Docker Quick Start and Dify Deployment Troubleshooting](8-Docker%E5%BF%AB%E9%80%9F%E5%85%A5%E9%97%A8%E4%B8%8EDify%E9%83%A8%E7%BD%B2%E6%8E%92%E9%9A%9C.md).

### 3.1 Pre-deployment Preparation

For local deployment of Dify on Windows, there are only two core dependencies:

- **Docker Desktop**: installed and verified as described in Chapter 8, and keep Docker Desktop in the Running state.
- **Dify project code**: what you actually work with later is the `docker` directory in the repository.

Dify is not a single program, but a whole set of coordinated services. After startup, it usually includes containers for the web frontend, API service, Worker, database, Redis, vector database, and more.

### 3.2 Getting the Dify Project

GitHub address: https://github.com/langgenius/Dify

> **Note:** The directory you actually work with later is not the repository root, but the `docker` directory inside the repository.

### 3.3 Copying .env.example to .env

The official Docker Compose deployment documentation also requires preparing `.env` first:

https://docs.dify.ai/zh-hans/getting-started/install-self-hosted/docker-compose

Enter the `docker` directory under the Dify repository, copy `.env.example` and rename it to `.env`.

Then modify the configuration in `.env` as needed, such as the port.

![Interface for modifying Dify .env port configuration](../../images/6/6-3-3-1.png)

The most common change for the first deployment is the port. If the local `80` port is occupied by another program, you can change it to `8100`, `8080`, or another unused port.

You can think of `.env` as the runtime parameter table for this deployment environment. The relationship between Docker / Compose / data volumes, as well as troubleshooting methods in Dify scenarios, can be found in [Chapter 8](8-Docker%E5%BF%AB%E9%80%9F%E5%85%A5%E9%97%A8%E4%B8%8EDify%E9%83%A8%E7%BD%B2%E6%8E%92%E9%9A%9C.md).

### 3.4 Starting Dify

The following operations can be done in the Windows command line, PowerShell, or the built-in terminal in Docker Desktop.

Enter the `docker` directory under the Dify repository:

![Interface for entering the Dify docker directory in the terminal](../../images/6/6-3-4-1.png)

Execute:

```bash
docker compose up -d
```

![Interface for executing docker compose up -d to start Dify](../../images/6/6-3-4-2.png)

On first startup, it automatically pulls images, creates containers, and initializes services. This process can be slow.

After installation is complete:

![Command line interface after Dify initial installation is complete](../../images/6/6-3-4-3.png)

Running `docker compose up -d` again later usually just starts the existing services.

You can also view the currently running containers on the Containers page in Docker Desktop.

![Interface for viewing Dify container running status in Docker Desktop](../../images/6/6-3-4-4.png)

### 3.5 Accessing Dify in the Browser

Access in the browser:

- Default port: `http://localhost`
- If you changed the port to `8100`: `http://localhost:8100`

On first access, you need to set an administrator username and password.

![Interface for setting up an administrator account when first accessing Dify](../../images/6/6-3-5-1.png)

Once inside, the local version works in basically the same way as the Dify cloud platform.

---

## 4. Coze Loop Guide

### 4.1 What Problems Does Coze Loop Solve

![Coze Loop product introduction interface](../../images/6/6-4-1-1.png)

Coze Loop is more oriented toward "performance management" and "runtime observation." It helps developers with prompt debugging, evaluation set management, experiment comparison, trace tracking, and automated evaluation.

If Coze Studio is about "building the agent," then Coze Loop is about "how to evaluate, track, and continuously optimize before and after going live." Therefore, it is not something you must install on day one, but it is very valuable in real projects.

### 4.2 Pre-deployment Preparation

Before installing the open-source version of Coze Loop, confirm the following environment:

**1. Go Language Environment**

You need to install the Go SDK, version 1.23.4 or above. After installation, configure GOPATH and add `${GOPATH}/bin` to the system environment variable PATH so that the system can find the binary tools installed by Go.

Go official website: https://go.dev/dl/

![Go official website download page](../../images/6/6-4-2-1.png)

After downloading, double-click to run the installer.

![Go installer launch interface](../../images/6/6-4-2-2.png)

Just click "Next" through the prompts.

After installation, make sure that the `bin` directory under the Go installation directory, or `GOPATH/bin`, has been added to the PATH environment variable.

![Schematic diagram of environment variable configuration after Go installation is complete](../../images/6/6-4-2-3.png)

**2. Docker Environment**

Install Docker and Docker Compose in advance, and start the Docker service.

**3. Model Services**

Prepare online model services such as OpenAI or Volcano Ark. You will need to fill in the API Key and model ID in the configuration file later.

### 4.3 Getting the Coze Loop Project

```bash
git clone https://gitee.com/shkstart/coze-loop.git
```

![Interface for cloning the Coze Loop repository via Gitee](../../images/6/6-4-3-1.png)

### 4.4 Configuring Models and Ports

Edit this file:

```text
coze-loop-main\release\deployment\docker-compose\conf\model_config.yaml
```

Taking Volcano Ark as an example, you need to modify:

- `api_key`: Volcano Ark API Key. You can refer to the creation method for Coze Studio mentioned earlier.
- `model`: the Endpoint ID of the Volcano Ark model access point.

![Interface for configuring Coze Loop model_config.yaml](../../images/6/6-4-4-1.png)

Next, open:

```text
coze-loop-main\release\deployment\docker-compose\.env
```

Change `COZE_LOOP_APP_OPENAPI_PORT` to `8889` or another unused port.

![Interface for modifying Coze Loop .env port configuration](../../images/6/6-4-4-2.png)

Then open `docker-compose.yml` in the same directory and confirm that the port referenced by `${COZE_LOOP_APP_OPENAPI_PORT}` is consistent with the one in `.env`.

![Interface for modifying Coze Loop docker-compose port mapping](../../images/6/6-4-4-3.png)

### 4.5 Starting and Accessing Coze Loop

Enter:

```text
coze-loop-main\release\deployment\docker-compose
```

Execute:

```cmd
docker compose -f docker-compose.yml --env-file .env --profile "*" up -d
```

If you want to view the full logs in the foreground, you can remove `-d`. For the first startup, it is recommended to run in the foreground first to better observe the startup process:

```cmd
docker compose -f docker-compose.yml --env-file .env --profile "*" up
```

The first startup needs to pull images and build local images, which may take a long time. Seeing the following logs indicates that the deployment is essentially complete.

![Log interface during Coze Loop initial startup](../../images/6/6-4-5-1.png)

![Log interface after Coze Loop startup is complete](../../images/6/6-4-5-2.png)

In the Docker Desktop container list, except for initialization containers like `xxx-init` that automatically exit after execution, the other service containers should remain running.

Access in the browser:

```text
http://localhost:8082
```

![Interface for viewing Coze Loop container running status in Docker Desktop](../../images/6/6-4-5-3.png)

After completing registration, you can enter the application details page.

![Interface when accessing the open-source version of Coze Loop in the browser](../../images/6/6-4-5-4.png)

### 4.6 Overview of Coze Loop's Main Features

Using the Demo space of the online version `https://www.coze.cn/loop` as an example, let's look at Coze Loop's core features. The open-source version and the online version may have slightly different interfaces, but the functional understanding is the same.

![Coze Loop online version Demo space interface](../../images/6/6-4-6-1.png)

#### 4.6.1 Prompt Development

Used for prompt preview and debugging.

![Interface of Coze Loop's Prompt Development module](../../images/6/6-4-6-2.png)

Click for details:

![Entry interface for Coze Loop Prompt Development details](../../images/6/6-4-6-3.png)

![Coze Loop Prompt Development details page interface](../../images/6/6-4-6-4.png)

#### 4.6.2 Playground

Playground is similar to Prompt Development, but is more suitable for free-form comparison.

![Interface of Coze Loop Playground module](../../images/6/6-4-6-5.png)

The free comparison mode cannot be enabled in the Demo space. You can switch to your personal space to use it.

![Interface of Coze Loop Playground in the Demo space](../../images/6/6-4-6-6.png)

![Interface for switching to the personal space in Coze Loop](../../images/6/6-4-6-7.png)

![Interface of Coze Loop free comparison mode](../../images/6/6-4-6-8.png)

#### 4.6.3 Evaluation Sets

Evaluation sets are used to manage test samples and serve as the foundation for subsequent experiments and automated evaluation.

![Interface of Coze Loop Evaluation Sets module](../../images/6/6-4-6-9.png)

![Coze Loop Evaluation Sets details interface](../../images/6/6-4-6-10.png)

![Interface for creating a new evaluation set in Coze Loop](../../images/6/6-4-6-11.png)

#### 4.6.4 Evaluators

This module is used to build tools for evaluating **Prompt Development** instances. It can be understood as a large language model with scoring prompts.

![Interface of Coze Loop Evaluators module](../../images/6/6-4-6-12.png)

![Interface for creating a new evaluator in Coze Loop](../../images/6/6-4-6-13.png)

![Coze Loop evaluator configuration details interface](../../images/6/6-4-6-14.png)

#### 4.6.5 Experiments

Experiments are used to connect evaluation sets, evaluation targets, and evaluators together for version comparison and performance analysis.

![Interface of Coze Loop Experiments module](../../images/6/6-4-6-15.png)

The Demo space does not have permission to create experiments. Switch to your personal space.

![Interface for switching to the personal space to create an experiment in Coze Loop](../../images/6/6-4-6-16.png)

Experiment details are as follows:

![Coze Loop experiment details page interface](../../images/6/6-4-6-17.png)

The metrics statistics module displays evaluation results in a visual way.

![Interface of Coze Loop experiment metrics statistics](../../images/6/6-4-6-18.png)

When creating a new experiment, simply configure the basic information, evaluation set, evaluation target, and evaluator in order.

![Coze Loop new experiment interface](../../images/6/6-4-6-19.png)

#### 4.6.6 Trace

Trace is used to record detailed information in the running pipeline, making it suitable for troubleshooting model calls, tool calls, and execution steps.

![Coze Loop Trace module interface](../../images/6/6-4-6-20.png)

![Coze Loop Trace details interface](../../images/6/6-4-6-21.png)

![Coze Loop Trace run details interface](../../images/6/6-4-6-22.png)

#### 4.6.7 Statistics and Automation Tasks

The Statistics module is used to view the overall operation status of the workspace; automation tasks are used to execute evaluations periodically.

![Coze Loop automation task module interface](../../images/6/6-4-6-23.png)

Details page:

![Coze Loop automation task details page interface](../../images/6/6-4-6-24.png)

![Coze Loop automation task configuration details interface](../../images/6/6-4-6-25.png)

---

## 5. Where to Check First When Deployment Fails

For deployment issues, don't just stare at the browser page. It is recommended to troubleshoot in the following order:

1. **Is the environment normal?**: Check whether Docker Desktop is Running, and whether `docker` and `docker compose` are available in the terminal.
2. **Is the directory correct?**: When executing commands, make sure you are in the corresponding project's `docker` or `release\deployment\docker-compose` directory.
3. **Is the configuration complete?**: Check whether `.env`, model configuration files, API Key, Endpoint, and ports are written correctly.
4. **Was the image pulled successfully?**: If it is stuck downloading images, prioritize handling proxies and image sources.
5. **Is the container running?**: Use `docker compose ps` or Docker Desktop to check the status.
6. **Are there clear errors in the logs?**: Focus on API, web, database, and model service-related logs.

This chapter only covers getting the minimal pipeline running. For more systematic Docker commands, Dify data locations, upgrade and backup, and database connections, continue to [Chapter 8 Docker Quick Start and Dify Deployment Troubleshooting](8-Docker%E5%BF%AB%E9%80%9F%E5%85%A5%E9%97%A8%E4%B8%8EDify%E9%83%A8%E7%BD%B2%E6%8E%92%E9%9A%9C.md).

---

**Chapter Review Questions:**

1. If Coze Studio, Dify, and Coze Loop can all run locally, why can't they still be understood as a single combined tool?

   **Reference ideas:** Coze Studio is more focused on agent and workflow building, Dify is more focused on an application platform and knowledge base/workflow delivery, and Coze Loop is more focused on evaluation, experiments, Trace, and lifecycle management. They may all depend on Docker, but they solve different problems.

2. When local deployment fails, will you first look at the browser page, or first check Docker and logs? Why?

   **Reference ideas:** First check Docker Desktop, container status, ports, `.env`, and service logs. The browser only tells you "access failed"; logs and container status can tell you whether the problem is with the image, database, configuration, model, or port.

3. What are the differences between cloud API models and Ollama local models in deployment troubleshooting?

   **Reference ideas:** For cloud APIs, mainly check Key, Endpoint, quota, network, and model name; for Ollama, also check whether the model has been pulled, whether local resources are sufficient, whether the service port is accessible, and whether the inference speed is acceptable. One is focused on connecting to a service, while the other is focused on hosting the model yourself.

**Chapter Summary:**

- **Significance of local deployment**: Local deployment of Coze and Dify enables agent platforms to move beyond cloud-only experiences and into scenarios that emphasize data security and private delivery.
- **Core components**: Coze Studio handles agent development, Dify handles workflows, knowledge bases, and application publishing, while Coze Loop is more focused on evaluation, experiments, Trace, and operations.
- **Hands-on main line**: The most important thing in this chapter is not remembering all the screenshots, but mastering a deployment logic: **Prepare environment -> Get code -> Modify configuration -> Start service -> Verify in browser**.

**Recommended next step:** If you want to continue learning about Docker concepts, data locations, upgrade and backup, and troubleshooting after deploying Dify, go to [Chapter 8 Docker Quick Start and Dify Deployment Troubleshooting](8-Docker%E5%BF%AB%E9%80%9F%E5%85%A5%E9%97%A8%E4%B8%8EDify%E9%83%A8%E7%BD%B2%E6%8E%92%E9%9A%9C.md); if you want to continue with a more complete enterprise deployment pipeline, go to [Chapter 7 Enterprise Large Model Deployment](7-%E4%BC%81%E4%B8%9A%E7%BA%A7%E5%A4%A7%E6%A8%A1%E5%9E%8B%E9%83%A8%E7%BD%B2.md).
