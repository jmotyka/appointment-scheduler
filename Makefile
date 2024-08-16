IMAGE_NAME := appointment-scheduler
DOCKERFILE := Dockerfile
PORT := 8000

.PHONY: build run

build:
	docker build -t $(IMAGE_NAME) -f $(DOCKERFILE) .

run:
	docker run -p $(PORT):$(PORT) $(IMAGE_NAME)