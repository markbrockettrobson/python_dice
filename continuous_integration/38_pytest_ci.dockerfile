FROM python:3.8

RUN mkdir /usr/localrepo
WORKDIR /usr/localrepo

COPY requirements.txt ./

RUN python -m pip install --no-cache-dir -r requirements.txt
RUN git clone https://github.com/markbrockettrobson/pydice.git

WORKDIR /usr/localrepo/pydice
RUN rm -rf ./python_dice

COPY setup.py ./
COPY run_formatter_and_tests.py ./
COPY pyproject.toml ./
COPY python_dice ./python_dice

RUN python run_formatter_and_tests.py
RUN python -m codecov --token=808a466d-ee9a-43ff-b9eb-a863756030c7
