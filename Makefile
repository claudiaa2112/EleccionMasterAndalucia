export UV_PROJECT_ENVIRONMENT ?= $(HOME)/.cache/eleccion-master-andalucia/venv
export PYTHONDONTWRITEBYTECODE = 1

install:
	uv sync

check:
	uv run python -c "import ast, pathlib; [ast.parse(f.read_text(), str(f)) for f in pathlib.Path('master').rglob('*.py')]"

test:
	uv run python -m unittest discover -s tests
