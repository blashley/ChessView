FROM tensorflow/tensorflow:latest-gpu
WORKDIR /ChessView

RUN apt-get install -y libsm6 libxext6 libxrender-dev

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN pip install jupyter -U && pip install jupyterlab
EXPOSE 8888
ENTRYPOINT ["jupyter", "lab","--ip=0.0.0.0","--allow-root"]

COPY . .