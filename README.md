# LLM Android Agent Evaluation

This project benchmarks Large Language Models (LLMs) such as GPT-4 and Claude on simulated Android UI tasks using the [`android_world`](https://github.com/qualgent-research/android_world) environment.

## Overview

The agent is prompted to perform multi-step actions to achieve goals (e.g., "Uninstall the Slack app") based on observed app UI elements. The models are evaluated in both **zero-shot** and **few-shot** settings.

## Setup

### 1. Clone This Repository

```bash
git clone https://github.com/your-username/llm_android_agent.git
cd llm_android_agent
```

### 2. Clone `android_world:

```bash
cd ..
git clone https://github.com/qualgent-research/android_world.git
cd llm_android_agent
```

### 3. Create Virtual Environment

```bash
conda create -n llm_agent_env python=3.11
conda activate llm_agent_env
pip install -r requirements.txt
```

### 4. API KEYS: 
You will need API keys for this.

```bash
export OPENAI_API_KEY=your-openai-key
export ANTHROPIC_API_KEY=your-anthropic-key
```

### 5. Run

To see results for GPT-4, Run:
```bash
python -m src.evaluate_gpt
```

To see results for Claude, Run:

```bash
python -m src.evaluate_claude
```



