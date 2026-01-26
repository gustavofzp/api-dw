FROM python:3.11-slim

# Variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

# Diretório de trabalho
WORKDIR /app

# Copia dependências primeiro (melhor cache)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do projeto
COPY . .

# Expõe a porta da API
EXPOSE 8000

# Comando de inicialização
CMD ["uvicorn", "api_dw.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]