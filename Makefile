install:
	docker run hello-world
	docker build --no-cache -f Dockerfile -t corona-festival .

dev:
	docker run -v $(PWD)/container/:/opt/container \
	--rm -ti --entrypoint=bash corona-festival:latest

pep8:
	docker run --rm -v $(PWD)/container/:/opt/container \
		--entrypoint=/usr/local/bin/python \
		corona-festival:latest \
		/usr/local/bin/pycodestyle /opt/container

unittest:
	docker run --rm -v $(PWD)/container/:/opt/container \
		-v $(PWD)/tests/:/opt/container/tests \
		--entrypoint=/bin/bash \
		corona-festival:latest \
		/opt/container/tests/test

test:
	make pep8
	make unittest


exec:
	docker run -v $(PWD)/container/:/opt/container \
	--rm --entrypoint=/bin/bash corona-festival:latest /opt/container/entrypoint

app: install test exec