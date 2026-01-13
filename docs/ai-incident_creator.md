Why AI explanation is useful

Why GenAI is used only for reasoning

Why actions are not automated yet


Why subprocess?
Because Ollama runs as a CLI tool, not a Python library.
So instead of:
import ollama 

We do:
subprocess.run(["ollama", "run", "mistral"])


This means:
Python is orchestrating
Ollama is executing
LLM stays decoupled from our code


What actually happens under the hood(Code):
Python builds a prompt (string)
Python sends it to Ollama via stdin
Ollama runs the LLM
Output is returned via stdout
Python captures and processes it
Exactly like calling:
some-command < input.txt > output.txt