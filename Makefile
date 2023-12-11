all: default

clean: 


deps:
	pip install -r requirements.txt

dev_deps:
	pip install -r requirements-dev.txt

check-format: dev_deps
	yapf -rd pulpo_config

format: dev_deps
	yapf -ri pulpo_config

lint: check-format
	pylint -r n pulpo_config

lint-no-error: 
	pylint --exit-zero -r n pulpo_config

test: build dev_deps
	python3 -m pytest -v --cov=pulpo_config --cov-report html

build: deps
	# might re-add clean 
