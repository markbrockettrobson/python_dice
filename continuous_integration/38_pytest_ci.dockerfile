FROM python:3.8

RUN mkdir /usr/localrepo
WORKDIR /usr/localrepo

RUN git clone https://github.com/markbrockettrobson/python_dice.git

WORKDIR /usr/localrepo/pydice
RUN rm -rf ./python_dice
RUN rm -f pylintrc

RUN python -m venv venv
RUN . venv/bin/activate && -m pip install --upgrade pip

COPY requirements.txt ./
COPY setup.py ./
COPY run_formatter_and_tests.py ./
COPY pyproject.toml ./
COPY python_dice ./python_dice

RUN . venv/bin/activate && python -m pip install --no-cache-dir -r requirements.txt
RUN . venv/bin/activate && python -m pytest --black --isort --pylint --mypy --cov .
RUN python -m codecov --token=808a466d-ee9a-43ff-b9eb-a863756030c7

#DONT RUN DIRECTLY WITH CODCOV docker build -t 38_pytest_ci -f continuous_integration/38_pytest_ci.dockerfile .
#DONT RUN DIRECTLY WITH CODCOV docker run -it 38_pytest_ci bash
