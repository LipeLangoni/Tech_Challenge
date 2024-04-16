init:
	docker-compose up -d --build
setup:
	pip install -r requirements.txt
clean: 
	rm -rf __pycache__