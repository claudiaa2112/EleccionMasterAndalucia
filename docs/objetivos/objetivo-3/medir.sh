#!/usr/bin/env bash
# Uso, desde la carpeta del repositorio:
# docker run --rm -v "$PWD":/src:ro python:3.14-slim bash /src/docs/objetivos/objetivo-3/medir.sh <herramienta>
set -e
herramienta="$1"
CHECK="import ast, pathlib; [ast.parse(f.read_text(), str(f)) for f in pathlib.Path('master').rglob('*.py')]"
cp -r /src /proyecto
cd /proyecto
rm -rf .venv .pdm-python
export PIP_ROOT_USER_ACTION=ignore PIP_DISABLE_PIP_VERSION_CHECK=1

medir() { # medir "<descripción>" <orden...>
  echo "--- $1"
  local inicio=$EPOCHREALTIME
  "${@:2}" > /tmp/salida.log 2>&1 || { cat /tmp/salida.log; exit 1; }
  local fin=$EPOCHREALTIME
  python -c "print(f'    {$fin - $inicio:.2f} s')"
}

instalar_herramienta() { # crea /opt/herramienta con pip y mide su tamaño
  medir "Instalar $herramienta" bash -c "python -m venv /opt/herramienta && /opt/herramienta/bin/pip install -q $*"
  echo "--- Tamaño de $herramienta instalado"
  echo "    $(du -sh /opt/herramienta | cut -f1)"
  export PATH="/opt/herramienta/bin:$PATH"
}

echo "=== $herramienta en python:3.14-slim ($(python --version))"
case "$herramienta" in
  pip)
    echo "--- Instalar pip: viene con Python (0 s)"
    medir "Preparar el proyecto (python -m venv .venv)" python -m venv .venv
    medir "Comprobar la sintaxis" .venv/bin/python -c "$CHECK" ;;
  uv)
    instalar_herramienta uv
    medir "Preparar el proyecto (uv sync)" uv sync
    medir "Comprobar la sintaxis (uv run)" uv run python -c "$CHECK" ;;
  poetry)
    instalar_herramienta poetry
    medir "Preparar el proyecto (poetry install --no-root)" poetry install --no-root
    medir "Comprobar la sintaxis (poetry run)" poetry run python -c "$CHECK" ;;
  pdm)
    instalar_herramienta pdm
    medir "Preparar el proyecto (pdm install)" pdm install
    medir "Comprobar la sintaxis (pdm check)" pdm check ;;
  hatch)
    instalar_herramienta hatch
    printf '\n[tool.hatch.envs.default]\nskip-install = true\n' >> pyproject.toml
    medir "Preparar el proyecto (hatch env create)" hatch env create
    medir "Comprobar la sintaxis (hatch run)" hatch run python -c "$CHECK" ;;
  make)
    medir "Instalar make (apt-get)" bash -c "apt-get update -qq && apt-get install -y -qq make"
    echo "--- Tamaño de make"; echo "    $(du -sh /usr/bin/make | cut -f1)"
    printf 'check:\n\tpython -c "%s"\n' "$CHECK" > Makefile
    medir "Comprobar la sintaxis (make check)" make check ;;
  just)
    instalar_herramienta rust-just
    printf 'check:\n    python -c "%s"\n' "$CHECK" > justfile
    medir "Comprobar la sintaxis (just check)" just check ;;
  poethepoet)
    instalar_herramienta poethepoet
    printf '\n[tool.poe.tasks]\ncheck = "python -c \\"%s\\""\n' "$CHECK" >> pyproject.toml
    medir "Comprobar la sintaxis (poe check)" poe check ;;
  *) echo "Herramienta desconocida: $herramienta"; exit 1 ;;
esac
