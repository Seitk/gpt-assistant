.PHONY: start

build:
	@docker build -t gpt-assistant .

run_docker:
	@docker run -it --name gpt-assistant --network host gpt-assistant	

run_api:
	@poetry run gunicorn api:app

run:
	@poetry run python main.py
