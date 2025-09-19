FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN adduser --disabled-password --gecos "" drini && \
    chown -R drini:drini /app

COPY . .

USER drini

ENV PORT=8000
ENV PATH="/home/drini/.local/bin:$PATH"

EXPOSE ${PORT}

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]