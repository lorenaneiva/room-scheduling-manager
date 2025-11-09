FROM python:3.13-slim

WORKDIR /app

# Instalar Node.js
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# Verificar e instalar dependências do Tailwind
RUN if [ -f theme/static_src/package.json ]; then \
        echo "Instalando dependências do Tailwind..." && \
        cd theme/static_src && npm install; \
    else \
        echo "package.json não encontrado em theme/static_src/"; \
    fi

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]