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
	rm -rf $(SRC)/loader/__pycache__
	rm -rf $(SRC)/data_base/__pycache__
	rm -rf $(SRC)/exceptions/__pycache__
	rm -rf $(SRC)/helps/__pycache__
	rm -rf $(SRC)/models/__pycache__
	rm -rf $(SRC)/ui/__pycache__

run:
	$(PY) -m src