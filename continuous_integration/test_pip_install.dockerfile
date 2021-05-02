FROM python:3.6

RUN mkdir /usr/pydice
WORKDIR /usr/pydice

COPY requirements.txt ./
COPY requirements_test.txt ./
RUN python -m pip install --no-cache-dir -r requirements_test.txt

COPY setup.py ./
COPY README.md ./
COPY run_formatter_and_tests.py ./
COPY pyproject.toml ./
COPY python_dice ./python_dice

RUN python setup.py sdist
RUN python -m venv venv

RUN venv/bin/python -m pip install dist/python_dice-2.0.1.tar.gz
RUN venv/bin/python -c "from python_dice import PythonDiceInterpreter; interpreter = PythonDiceInterpreter(); program = ['1d6']; roll = interpreter.roll(program)['stdout']; print(roll)"

#docker build -t test_pip_install -f continuous_integration/test_pip_install.dockerfile .
