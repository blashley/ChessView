## Instructions to run notebooks on your system
1. Make sure you have Docker installed.
2. Clone the repo and navigate to the directory ChessView.
3. Run the command `sudo docker build -t chessview .`
4. After the docker image has been built, launch a container with 
`sudo docker run -v ${PWD}:/ChessView -p 8888:8888 --rm chessview`
5. Play around with the code and see what improvements you can come up with!