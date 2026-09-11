VENV = .venv
PY = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
SRC = src/
all: run

install:
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

clean:
	rm -rf $(SRC)__pycache__
run:
	$(PY) -m src