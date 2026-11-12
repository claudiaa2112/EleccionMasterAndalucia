install:
	uv sync

check:
	uv run python -c "import ast, pathlib; [ast.parse(f.read_text(), str(f)) for f in pathlib.Path('master').rglob('*.py')]"
