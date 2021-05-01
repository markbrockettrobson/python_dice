FROM python:3.8

RUN mkdir /usr/pydice
WORKDIR /usr/pydice

COPY requirements.txt ./

RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY setup.py ./
COPY pyproject.toml ./
COPY python_dice ./python_dice

CMD python -m pytest --black --isort --pylint --cov python_dice

#docker build -t image_maker -f continuous_integration\CreateLinuxImages.dockerfile .
#docker run -v C:/Users/MarkB/PycharmProjects/python_dice/python_dice/test/test_image/linux:/usr/pydice/python_dice/test/test_image/linux image_maker
