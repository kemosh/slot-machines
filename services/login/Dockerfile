FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /login/

COPY requirements.txt pyproject.toml ./
COPY source ./source
RUN pip install -r requirements.txt
RUN pip install -e .

# watchdog
RUN pip install watchdog

#ENTRYPOINT ["python", "-m", "login.main"]
ENTRYPOINT ["watchmedo", "auto-restart", "-p", "*.py", "-R", "python", "--", "-m", "login.main"]

