FROM python:3.9.0a1

RUN mkdir /usr/pydice
WORKDIR /usr/pydice

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY .coveragerc ./
COPY pylintrc ./
COPY setup.py ./
COPY python_dice ./python_dice

RUN python -m pytest --black --isort --pylint --cov python_dice
