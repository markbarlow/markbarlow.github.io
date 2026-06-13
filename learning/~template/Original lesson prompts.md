# Learning template initial prompt

A template for a self-contained interactive course as a single HTML file I can run locally in my browser. Requirements:

- One file, no install, no dependencies — just open in a browser
- Saves all progress automatically using localStorage
- I can close it and come back days later and pick up where I left off
- Each topic has: lesson, mental model, common mistakes, and a small exercise
- Show a progress bar and let me mark topics complete
- Works offline



# Detailed lesson prompt for LLM course

Your job is to teach me modern LLM engineering and fine-tuning concepts from beginner to advanced level using very simple daily-life language.

Teach me step-by-step like a real mentor. Assume I am smart but new to the topic.

Foundations:

- LLM basics
- How AI models work
- Tokens
- Tokenization
- Context windows
- Embeddings
- Transformers
- Attention mechanism
- Parameters
- Training vs inference
- Open-source vs closed-source models

Datasets & Training:

- SFT datasets
- Instruction tuning
- Preference datasets
- Synthetic datasets
- Data curation
- Dataset cleaning
- Dataset formatting
- Fine-tuning basics
- Continued pretraining
- Hallucination reduction

Fine-Tuning:

- LoRA
- QLoRA
- DPO
- RLHF
- Quantization
- Model checkpoints
- Adapter tuning
- GGUF models

Inference & Optimization:

- KV cache
- Flash Attention
- Speculative decoding
- Inference optimization
- Model serving
- Batch inference
- GPU basics
- VRAM basics
- Latency vs quality tradeoffs

Local AI Ecosystem:

- llama.cpp
- Ollama
- vLLM
- MLX
- Hugging Face
- Unsloth
- Axolotl
- PEFT
- TRL library

RAG & Memory:

- RAG
- Vector databases
- Chunking
- Retrieval pipelines
- AI memory systems
- Semantic search

Agents & Workflows:

- Prompt engineering
- System prompts
- Tool calling
- Function calling
- AI agents
- Agentic workflows
- Multi-agent systems
- Browser agents

Model Types:

- VLMs
- SLMs
- Dense models
- MoE models
- Coding models
- Reasoning models

Deployment:

- Local inference
- On-device AI
- API serving
- Cloud GPUs
- Edge AI basics

Evaluation:

- AI benchmarks
- Human evals
- Cost-per-token analysis
- Speed benchmarking
- Quality benchmarking

Real-World Skills:

- Building chatbots
- Building AI copilots
- AI automation
- AI SaaS workflows
- AI coding workflows
- AI orchestration systems
- AI product thinking

Start from the absolute basics and gradually make me advanced.

Rules:

- Use simple English only
- Avoid academic jargon unless necessary
- Explain every difficult word in plain language
- Use real-world analogies and daily-life examples
- Use small code snippets when useful
- Show practical use cases
- Compare concepts side-by-side when helpful
- Teach from fundamentals first, then advanced concepts
- At the end of each topic:
  - give a short summary
  - give a simple mental model
  - give beginner mistakes to avoid
  - give a small exercise/project
- structure: Grouped into modules/units, each with topics
- exercise_type: Multiple-choice quiz (auto-checked), Flashcard-style self-rated recall
- sections: Add a 'Key terms / glossary' section, Add a 'Recap / TL;DR' callout
- progress_features: Overall progress bar, Per-module progress, Mark topic complete button, Resume-where-you-left-off on open, Reset progress button, Search/filter topics
