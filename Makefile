init:
	docker-compose up -d --build
setup:
	docker-compose exec web pip install -r ../requirements/requirements.txt
clean: 
	rm -rf __pycache__