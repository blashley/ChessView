FROM tensorflow/tensorflow:latest
WORKDIR /ChessView
RUN apt-get install -y libsm6 libxext6 libxrender-dev
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .