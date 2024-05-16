poetry flask test

    docker build -t "flask_test:24-05-16" .
    docker run -it --name flask -p 5555:5555 -d flask_test:24-05-16