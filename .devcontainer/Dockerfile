FROM python:3.13.9-slim-trixie

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN apt update && apt install -y zstd    
RUN curl -fsSL https://claude.ai/install.sh | bash
RUN curl -fsSL https://ollama.com/install.sh | sh

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


COPY .devcontainer/start.sh .devcontainer/start.sh 
RUN chmod +x .devcontainer/start.sh

CMD ["sleep", "infinity"]


