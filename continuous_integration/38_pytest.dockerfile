FROM python:3.8

RUN mkdir /usr/pydice
WORKDIR /usr/pydice

COPY requirements.txt ./

RUN python -m pip install --no-cache-dir -r requirements.txt

COPY setup.py ./
COPY run_formatter_and_tests.py ./
COPY pyproject.toml ./
COPY python_dice ./python_dice

RUN python -m pytest .

#docker build -t 38_pytest -f continuous_integration/38_pytest.dockerfile .