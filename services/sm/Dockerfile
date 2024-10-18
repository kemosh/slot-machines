FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /sm/

COPY pyproject.toml ./
COPY source ./source
RUN pip install uv
RUN uv pip install --system -e .

ENTRYPOINT ["uvicorn", "--host", "0.0.0.0", "--port", "8080", "--reload", "sm.main:app"]
