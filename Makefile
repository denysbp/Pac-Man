PY = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
SRC = src
USER := $(shell command whoami)
MODEL := Qwen/Qwen3-0.6B
HOME := /home/$(USER)
FOLDER = $(shell pwd)
PY = $(VENV)/bin/python3
SGOINFRE := $(HOME)/sgoinfre
VENV := $(SGOINFRE)/.venv
WGET := $(shell command -v wget 2> /dev/null)
CURL := $(shell command -v curl 2> /dev/null)


all: run


local:
	@test -f $(HOME)/.local/bin/env || mkdir -p $(HOME)/.local/bin && touch  $(HOME)/.local/bin/env

build_uv: local
ifdef WGET
		@wget -qO- https://astral.sh/uv/install.sh | sh
		@. $(HOME)/.local/bin/env
		@echo "We used wget to install the uv"
else ifdef CURL
			@curl -LsSf https://astral.sh/uv/install.sh | sh
			@. $(HOME)/.local/bin/env
			@echo "We used curl to install the uv"

endif

install: build_uv
	uv sync

run:
	@if [ ! -d ".venv" ]; then \
		uv sync; \
		uv add wheels/mazegenerator-2.1.0-py3-none-any.whl wheels/mlx-2.2-py3-none-any.whl; \
		uv run pac-man.py config.json; \
	else \
		uv run pac-man.py config.json; \
	fi

clean:
	rm -rf $(SRC)/__pycache__
	rm -rf $(SRC)/loader/__pycache__
	rm -rf $(SRC)/data_base/__pycache__
	rm -rf $(SRC)/exceptions/__pycache__
	rm -rf $(SRC)/helps/__pycache__
	rm -rf $(SRC)/models/__pycache__
	rm -rf $(SRC)/ui/__pycache__
	rm -rf __pycache__
	rm -rf .mypy_cache

fclean: clean
	rm -rf $(VENV) dist build

debug:
	uv -m pdb pac-man.py config.json

deploy:
	.venv/bin/python -m PyInstaller pac2.spec


lint:
	uv run -m flake8 .
	uv run mypy . --config-file pyproject.toml

help:
	@echo "\033[35mAvailable Make commands:\033[0m"
	@echo "\033[33mrun\033[0m          Execute the main script project."
	@echo "\033[33mdebug\033[0m        Run the main script in debug mode using Python’s built-in debugger."
	@echo "\033[33mclean\033[0m        Remove temporary files or caches (e.g., __pycache__, .mypy_cache) to keep the project environment clean."
	@echo "\033[33mdeploy\033[0m	   Install the project to go to the web!"
	@echo "\033[33mlint\033[0m         Execute flake8 . and mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs"
	@echo "\033[33mlint-strict\033[0m  Execute flake8 . and mypy . --strict"

.DEFAULT:
	@echo "\033[31mError: Unknown command.\033[0m"
	@echo "Use \033[33mmake help\033[0m to see all available commands."

.PHONY: run debug clean  lint  help .DEFAULT local build_uv all fclean deploy install