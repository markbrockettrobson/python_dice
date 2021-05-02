FROM python:3.6

RUN mkdir /usr/pydice
WORKDIR /usr/pydice

COPY requirements.txt ./
COPY requirements_test.txt ./
RUN python -m pip install --no-cache-dir -r requirements_test.txt

COPY setup.py ./
COPY run_formatter_and_tests.py ./
COPY pyproject.toml ./
COPY python_dice ./python_dice

RUN python -m pytest .

#docker build -t 36_pytest -f continuous_integration/36_pytest.dockerfile .