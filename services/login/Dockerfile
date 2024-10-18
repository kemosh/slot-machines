FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /login/

COPY pyproject.toml ./
COPY source ./source
RUN pip install uv
RUN uv pip install --system -e .

# watchdog
RUN pip install watchdog

ENTRYPOINT ["watchmedo", "auto-restart", "-p", "*.py", "-R", "python", "--", "-m", "login.main"]

