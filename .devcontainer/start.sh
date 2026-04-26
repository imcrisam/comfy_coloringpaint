#!/bin/bash

ollama serve &
sleep 2

ollama launch claude --model qwen3-coder-next:cloud

wait