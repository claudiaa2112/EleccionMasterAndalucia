# Herramientas para automatizar tareas

Hacía falta una forma común de preparar el proyecto y comprobar el código
([issue #23](https://github.com/claudiaa2112/EleccionMasterAndalucia/issues/23)).

## De qué parto

- Python define en un estándar cómo se describe un proyecto y sus dependencias: el fichero
  pyproject.toml ([PEP 621](https://peps.python.org/pep-0621/)), los grupos de dependencias
  para quien desarrolla ([PEP 735](https://peps.python.org/pep-0735/)) y el fichero que fija
  las versiones instaladas ([PEP 751](https://peps.python.org/pep-0751/)). Pero no dice qué
  programa tiene que usarlos.
- El código solo usa lo que trae Python, sin dependencias externas.
- La versión de Python ya la gestiona pyenv.
- Lo que se elija se usará después en contenedores y en integración continua, donde cada
  vez se parte de cero, así que importa cuánto tarda en instalarse, cuánto ocupa y cuánto
  tarda en preparar el proyecto y en comprobar el código.

## Criterios

- Que siga el estándar pyproject.toml.
- Que sirva para dependencias y tareas a la vez, o cuántas herramientas hacen falta en total.
- Lo que tarda en instalarse la herramienta y lo que ocupa.
- Lo que tarda en preparar el proyecto.
- Lo que tarda en comprobar la sintaxis.

## Cómo se mide

Cada herramienta se prueba en un contenedor limpio con la imagen oficial python:3.14-slim,
para partir siempre de cero, con el script [medir.sh](medir.sh), desde la carpeta del
repositorio:

    docker run --rm -v "$PWD":/src:ro python:3.14-slim bash /src/docs/objetivos/objetivo-3/medir.sh <herramienta>

Las herramientas que se instalan con pip se miden junto con el entorno en el que se
instalan, que ya incluye pip, así que su tamaño no se puede comparar directamente con el
de Make, que se instala con el sistema.

## Gestores de dependencias

- Pipenv: no se mide porque usa su propio fichero, Pipfile, en lugar del estándar
  pyproject.toml.
- pip con venv: vienen con Python, así que no hay que instalar nada. Crear el entorno
  (python -m venv .venv) tarda 10,95 s, porque copia pip dentro del entorno, y comprobar la
  sintaxis tarda 0,11 s. No fija las versiones instaladas ni define tareas, así que haría
  falta otra herramienta para ellas ([captura](capturas/pip.png)).
- uv: sigue el estándar pyproject.toml, pero no tiene tareas con nombre (la petición
  [#5903](https://github.com/astral-sh/uv/issues/5903) sigue abierta), así que haría falta
  otra herramienta para ellas. Se instala en 15,31 s y ocupa 51 MB; prepara el proyecto
  en 0,60 s y comprueba la sintaxis en 0,25 s ([captura](capturas/uv.png)).
- Poetry: sigue el estándar pyproject.toml, pero no tiene tareas sin añadir un plugin. Se
  instala en 32,38 s y ocupa 92 MB; prepara el proyecto en 3,08 s y comprueba la sintaxis
  en 1,43 s ([captura](capturas/poetry.png)).
- PDM: sigue el estándar pyproject.toml, fija las versiones en pdm.lock y permite definir
  las tareas dentro de pyproject.toml
  ([documentación](https://pdm-project.org/latest/usage/scripts/)), así que no hace falta
  otra herramienta. Se instala en 28,05 s y ocupa 59 MB; prepara el proyecto en 3,98 s y
  comprueba la sintaxis con su propia tarea en 1,76 s ([captura](capturas/pdm.png)).

## Gestores de tareas

## La tarea check

Se usa [ast.parse](https://docs.python.org/3/library/ast.html#ast.parse), que viene con
Python: lee cada fichero y comprueba que su sintaxis es correcta sin escribir nada en
disco. Se ha descartado
[compileall](https://docs.python.org/3/library/compileall.html), porque guarda el código
compilado en carpetas \_\_pycache\_\_, y comprobar la sintaxis no debe tener efectos
secundarios, como señaló el profesor en una
[revisión de este mismo objetivo](https://github.com/manuusnchz/gestor-ciclismo/pull/25).
