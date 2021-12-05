FROM pypy:3

RUN mkdir /usr/pydice
WORKDIR /usr/pydice

COPY requirements.txt ./
COPY requirements_test.txt ./
RUN pypy -m pip install --no-cache-dir -r requirements_test.txt

COPY setup.py ./
COPY run_formatter_and_tests.py ./
COPY pyproject.toml ./
COPY python_dice ./python_dice

RUN pypy -m pytest .

#docker build -t 38_pypy -f continuous_integration/38_pypy.dockerfile .