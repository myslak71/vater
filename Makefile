black:  ## run black
	black .

black_check:  ## run isort check
	 black . --check

coverage:  ## create html coverage report and open it in the default browser
	coverage html
	xdg-open htmlcov/index.html

flake8:  ## run flake8
	flake8 src

isort:  ## run isort
	isort . -rc

isort_check:  ## run isort check
	isort . -rc --check

lint: mypy flake8 yamllint  isort_check black_check # run all linters

mypy:  ## run mypy
	mypy src --strict-optional

safety:  ## run safety check
	safety check -r requirements.txt -r requirements-dev.txt

unittests:  ## run pytest with coverage and -s flag for debugging
	 pytest --cov=src tests/ --cov-branch -s

yamllint:  ## run yamllint
	yamllint .
