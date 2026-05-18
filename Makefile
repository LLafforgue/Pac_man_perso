NAME	:= pac-man
TARGET	:= $(NAME).py
PY		:= python3
ENV		:= . venv/bin/activate
FILES	:= src/ tests/


all: install run

# Create a virual environment
venv:
	python -m venv venv

# Install dependencies
install: venv
	$(ENV) &&\
	python -m pip install --upgrade pip &&\
	pip install *.whl &&\
	pip install -e .[dev]

# Run a_maze_ing in venv
run:
	$(ENV) &&\
	$(PY) $(TARGET) config.json

# Build a package
package: install
	$(ENV) && pyinstaller pac-man.spec --clean
	cd dist && zip -r pac-man-$(shell uname -s).zip pac-man/

lint:
	$(ENV) &&\
	flake8 $(TARGET) $(FILES) &&\
	mypy $(TARGET) $(FILES) \
	--warn-return-any --warn-unused-ignores --ignore-missing-imports \
	--disallow-untyped-defs --check-untyped-defs

debug:
	$(ENV) && $(PY) -m pdb $(TARGET) config.json


clean:
	rm -rf build/ dist/ __pycache__
	rm -f *.pyc
	rm -rf .mypy_cache
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exe rm -rf {} +

.PHONY: all install run clean venv module lint package debug