FROM python:3.13.2

RUN pip install --no-cache-dir uv

WORKDIR /app

COPY . .

RUN uv sync

CMD ["uv", "run", "python", "fastapi-kgf/main.py"]