# Use Python 3.12 slim como base
FROM python:3.12-slim

# Instalar dependências do sistema para Playwright
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Definir diretório de trabalho
WORKDIR /app

# Copiar requirements primeiro (para cache do Docker)
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Instalar navegadores do Playwright
RUN playwright install chromium
RUN playwright install-deps chromium

# Copiar todo o código
COPY . .

# Criar diretório para downloads
RUN mkdir -p /app/download

# Definir variáveis de ambiente para otimização
ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Otimizações para Cloud Run "cold start"
ENV PYTHONDONTWRITEBYTECODE=1

# Comando para rodar a aplicação como servidor web otimizado
CMD ["python", "src/server.py"]
