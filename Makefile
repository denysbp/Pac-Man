VENV = .venv
PY = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
SRC = src/

run:
	$(PY) pac-man.py config.json

install:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -U pyinstaller
	$(PIP) install -r requirements.txt

clean:
	rm -rf $(SRC)__pycache__
	rm -rf $(SRC)/loader/__pycache__
	rm -rf $(SRC)/data_base/__pycache__
	rm -rf $(SRC)/exceptions/__pycache__
	rm -rf $(SRC)/helps/__pycache__
	rm -rf $(SRC)/models/__pycache__
	rm -rf $(SRC)/ui/__pycache__

fclean: clean
	-rf $(VENV)

debug:
	$(PY) -m pdb pac-man.py config.json

deploy:
	.venv/bin/python -m PyInstaller pac2.spec


lint:
	@$(VENV)/bin/flake8 .
	@$(VENV)/bin/mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
	@echo "\033[32mEverything in the norm!!"

lint-strict: install
	@$(VENV)/bin/flake8 .
	@$(VENV)/bin/mypy . --strict
	@echo "\033[32mEverything in the norm!!"

help:
	@echo "\033[35mAvailable Make commands:\033[0m"
	@echo ""
	@echo "\033[33minstall\033[0m      Install project dependencies using uv."
	@echo "\033[33mrun\033[0m          Execute the main script project."
	@echo "\033[33mdebug\033[0m        Run the main script in debug mode using Python’s built-in debugger."
	@echo "\033[33mclean\033[0m        Remove temporary files or caches (e.g., __pycache__, .mypy_cache) to keep the project environment clean."
	@echo "\033[33mfclean\033[0m       Remove all temporary files, caches, output directory and also delete the virtual environment."
	@echo "\033[33mlint\033[0m         Execute flake8 . and mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs"
	@echo "\033[33mlint-strict\033[0m  Execute flake8 . and mypy . --strict"

.DEFAULT:
	@echo "\033[31mError: Unknown command.\033[0m"
	@echo "Use \033[33mmake help\033[0m to see all available commands."

.PHONY: run debug clean fclean lint lint-strict help .DEFAULT