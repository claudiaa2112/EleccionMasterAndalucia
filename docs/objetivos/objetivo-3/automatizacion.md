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
- Hatch: sigue el estándar pyproject.toml y tiene tareas, pero no tiene fichero que fije
  las versiones (la petición [#749](https://github.com/pypa/hatch/issues/749) sigue
  abierta). Se instala en 35,93 s y ocupa 111 MB; prepara el proyecto en 1,79 s y comprueba
  la sintaxis en 0,68 s ([captura](capturas/hatch.png)).

## Gestores de tareas

- Make: no depende de Python, pero no viene en la imagen y se instala con el sistema. Se
  instala en 15,07 s y ocupa 272 KB; comprueba la sintaxis en 0,31 s
  ([captura](capturas/make.png)).
- just: es un programa independiente. Se instala en 11,60 s y ocupa 20 MB, contando el
  entorno en el que se instala; comprueba la sintaxis en 0,12 s
  ([captura](capturas/just.png)).
- poethepoet: define las tareas dentro de pyproject.toml. Se instala en 11,17 s y ocupa
  19 MB, contando el entorno en el que se instala; comprueba la sintaxis en 0,60 s
  ([captura](capturas/poethepoet.png)).

## La tarea check

Se usa [ast.parse](https://docs.python.org/3/library/ast.html#ast.parse), que viene con
Python: lee cada fichero y comprueba que su sintaxis es correcta sin escribir nada en
disco. Se ha descartado
[compileall](https://docs.python.org/3/library/compileall.html), porque guarda el código
compilado en carpetas \_\_pycache\_\_, y comprobar la sintaxis no debe tener efectos
secundarios, como señaló el profesor en una
[revisión de este mismo objetivo](https://github.com/manuusnchz/gestor-ciclismo/pull/25).

## Decisión

Solo dos de las herramientas medidas gestionan a la vez las dependencias y las tareas, que
es lo que se buscaba para no tener que instalar y mantener una segunda herramienta: PDM y
Hatch. Hatch prepara el proyecto y comprueba la sintaxis más rápido que PDM, pero tarda
más en instalarse, ocupa casi el doble y no tiene fichero que fije las versiones
instaladas, así que no resuelve el problema de que cada persona acabe con versiones
distintas. PDM es la única que cumple todos los criterios con una sola herramienta.

uv es más rápido que PDM en todas las medidas, pero necesita otra herramienta para las
tareas. Sumando lo que cuesta instalar la herramienta, preparar el proyecto y comprobar la
sintaxis en un contenedor recién creado, PDM tarda unos 34 s y uv con just unos 28 s. La
comprobación de uv con just no se ha medido junta, así que su tiempo es una estimación a
partir de las dos medidas por separado. La diferencia es de unos 6 s, y la mayor parte
está en instalar la herramienta, que en un contenedor se hace una sola vez al construir la
imagen. Lo que se repite en cada uso, preparar el proyecto y comprobar la sintaxis, cuesta
unos 4 o 5 s más con PDM.

A cambio de esos segundos, con PDM hay una sola herramienta que instalar, actualizar y
mantener, y las dependencias y las tareas quedan en un único fichero, pyproject.toml, en
lugar de repartirse entre pyproject.toml y un fichero de tareas aparte. Como el proyecto no
tiene dependencias externas, una diferencia de segundos no compensa añadir una segunda
herramienta, que es más deuda técnica.

Por eso elijo PDM, sabiendo que tiene estas desventajas:

- Tarda casi 2 s en lanzar cualquier tarea, porque es un programa de Python que tiene que
  arrancar cada vez, así que si en integración continua se encadenan muchas tareas el
  tiempo se acumula.
- Su formato de fichero de versiones es el suyo propio, pdm.lock, porque el estándar
  pylock.toml todavía es experimental en PDM.
- Cada medida es de una sola ejecución y los tiempos de instalación dependen de la
  velocidad de descarga, así que las diferencias pequeñas entre herramientas no son
  concluyentes.

Si en los objetivos siguientes la velocidad llegara a ser un problema, la alternativa sería
uv con un gestor de tareas.
