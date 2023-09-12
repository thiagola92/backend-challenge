FROM python:3.11

RUN pip install -U pip setuptools wheel
RUN pip install pdm

WORKDIR /project

COPY pyproject.toml pdm.lock /project/
COPY src/ /project/src

RUN python -m pdm init --non-interactive
RUN python -m pdm install

CMD ["python", "-m", "pdm", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]