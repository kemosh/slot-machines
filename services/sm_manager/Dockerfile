FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /sm_manager/

COPY requirements.txt pyproject.toml ./
COPY source ./source
RUN pip install -r requirements.txt
RUN pip install -e .

ENTRYPOINT ["uvicorn", "--host", "0.0.0.0", "--port", "8080", "--reload", "sm_manager.main:app"]
