FROM python:3.9

RUN mkdir /usr/pydice
WORKDIR /usr/pydice

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY .coveragerc ./
COPY pylintrc ./
COPY setup.py ./
COPY python_dice ./python_dice

CMD python -m pytest --black --isort --pylint --cov python_dice

#docker run -v C:/Users/MarkB/PycharmProjects/python_dice/python_dice/test/test_image/linux:/usr/pydice/python_dice/test/test_image image_maker
#docker build -t image_maker -f continuous_integration\CreateLinuxImages.dockerfile .