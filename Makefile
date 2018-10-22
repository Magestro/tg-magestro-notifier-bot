IMAGE = tg-magestro-notifier-bot
CONTAINER = $(IMAGE)_container
PWD = $(shell pwd)

HOST=0.0.0.0
PORT=8888

.PHONY : image start stop

image :
	docker build -t $(IMAGE):latest .

start : | image
	docker run -d --name "$(CONTAINER)" -v $(PWD)/volume:/app/volume  "$(IMAGE):latest" -l "$(HOST):$(PORT)"
	sleep 10
	docker logs --tail 100 -f "$(CONTAINER)"

stop:
	docker stop "$(CONTAINER)" || echo
	docker rm -f "$(CONTAINER)" || echo

restart : | stop start
	echo
