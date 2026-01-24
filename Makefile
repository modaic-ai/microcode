clear-modaic-cache:
	rm -rf ~/.cache/modaic

clear-microcode-cache:
	rm -rf ~/.cache/microcode

clear-cache: clear-modaic-cache clear-microcode-cache

test:
	./microcode/.venv/bin/python -m pytest -q
