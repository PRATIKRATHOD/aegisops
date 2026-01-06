Ollama is a local LLM runtime, similar to how:
    Docker runs containers locally
    JVM runs Java bytecode locally

Ollama runs Large Language Models (LLMs) on your own machine.

Why did we install Ollama?
✅ Fully local
✅ Open-source
✅ Free
✅ Enterprise-safe

When you run:
ollama run mistral

The model:
Runs on your CPU/RAM
Reads prompts from your system
Returns output without any network call

This is huge in enterprises where:
Logs contain sensitive data
Internet access is restricted


Pulled Mistral Model

What is Mistral?
Mistral is:
An open-source LLM
Lightweight compared to GPT-4
Very good at reasoning & explanations

Perfect for:
Incident summaries
RCA explanations
Technical reasoning

Why Mistral (and not others)?
We chose Mistral because:
Runs well on laptops
Fast responses
Open license
No GPU required
For production demos, simplicity beats size.