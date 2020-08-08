FROM python:3.8

RUN mkdir /usr/localrepo
WORKDIR /usr/localrepo

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt
RUN git clone https://github.com/markbrockettrobson/pydice.git

WORKDIR /usr/localrepo/pydice
RUN rm -rf ./python_dice
COPY .coveragerc ./
COPY pylintrc ./
COPY setup.py ./
COPY python_dice ./python_dice


RUN python -m pytest --black --isort --pylint --cov python_dice
RUN python -m codecov --token=808a466d-ee9a-43ff-b9eb-a863756030c7
