IMAGE_NAME=goit-pythonweb-hw-03
VERSION=1
PORTS=3000:3000

build:
	docker build -t $(IMAGE_NAME):$(VERSION) .

run:
	docker run -it --rm -p $(PORTS) $(IMAGE_NAME):$(VERSION)

compose:
	docker compose up --build
