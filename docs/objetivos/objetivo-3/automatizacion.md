# Herramientas para automatizar tareas

Hacía falta una forma común de instalar las dependencias y ejecutar las tareas
([issue #23](https://github.com/claudiaa2112/EleccionMasterAndalucia/issues/23)).

## Criterios

- Que el gestor de dependencias siga el estándar pyproject.toml.
- Cuántas herramientas hacen falta en total para gestionar las dependencias y ejecutar las
  tareas.
- Que tenga lockfile, para que todo el mundo instale las mismas versiones.
- Lo que tarda en instalarse la herramienta.
- Lo que tarda en instalar las dependencias.
- Lo que tarda en ejecutar las tareas.

## Gestores de dependencias

- uv: sigue el estándar pyproject.toml. No tiene tareas con nombre, así que hacen falta dos
  herramientas en total. Tiene lockfile, uv.lock. Se instala en 5,40 s, instala las
  dependencias en 0,16 s y ejecuta la comprobación con uv run en 0,25 s
  ([captura](capturas/uv.png)).
- Poetry: sigue el estándar pyproject.toml. No tiene tareas sin añadir un plugin, así que
  hacen falta dos herramientas en total. Tiene lockfile, poetry.lock. Se instala en 17,52
  s, instala las dependencias en 2,71 s y ejecuta la comprobación con poetry run en 1,42 s
  ([captura](capturas/poetry.png)).
- PDM: sigue el estándar pyproject.toml. Define las tareas en pyproject.toml, así que basta
  con una herramienta. Tiene lockfile, pdm.lock. Se instala en 19,56 s, instala las
  dependencias en 5,19 s y ejecuta la tarea check en 1,24 s ([captura](capturas/pdm.png)).
- Hatch: sigue el estándar pyproject.toml. Define las tareas en pyproject.toml, así que
  basta con una herramienta, pero no tiene lockfile. Se instala en 25,08 s, instala las
  dependencias en 1,55 s y ejecuta la comprobación con hatch run en 0,57 s
  ([captura](capturas/hatch.png)).

## Gestores de tareas

- Make: no gestiona dependencias, así que hacen falta dos herramientas en total y el
  lockfile depende del gestor de dependencias que se use con él. Ya estaba instalado en el
  sistema, así que no hay tiempo de instalación, y ejecuta la tarea check en 0,09 s
  ([captura](capturas/make.png)).
- just: no gestiona dependencias, así que hacen falta dos herramientas en total y el
  lockfile depende del gestor de dependencias que se use con él. Se instala en 3,14 s y
  ejecuta la tarea check en 0,10 s ([captura](capturas/just.png)).
- poethepoet: funciona sin Poetry, con cualquier gestor de dependencias, pero no las
  gestiona, así que hacen falta dos herramientas en total y el lockfile depende del gestor
  de dependencias que se use con él. Se instala en 2,93 s y ejecuta la tarea check en 0,43 s
  ([captura](capturas/poethepoet.png)).
- uv con Make: dos herramientas en total, con el lockfile de uv, uv.lock. Make ya estaba
  instalado. make install descarga Python 3.14 e instala las dependencias en 6,78 s y make
  check ejecuta la tarea en 0,95 s ([captura](capturas/make-uv.png)).

## Decisión

PDM y Hatch son las únicas que gestionan las dependencias y ejecutan las tareas con una
sola herramienta, pero Hatch no tiene lockfile, así que con una sola herramienta la opción
sería PDM.

Con dos herramientas, uv tiene lockfile y es el gestor de dependencias más rápido en todas
las medidas. De los gestores de tareas, Make es el que menos tarda en ejecutar la tarea
check y ya estaba instalado en el sistema, así que no añade tiempo de instalación.

Comparando PDM con uv y Make medidos juntos:

- Instalar la herramienta: PDM tarda 19,56 s y uv 5,40 s.
- Instalar las dependencias: PDM tarda 5,19 s y uv con Make 6,78 s, porque además descarga
  Python 3.14; con Python ya instalado, uv tarda 0,16 s.
- Ejecutar la tarea check: PDM tarda 1,24 s y uv con Make 0,95 s.

En total, PDM tarda unos 26 s y uv con Make unos 13 s, la mitad aunque incluya la descarga
de Python. Por eso elijo uv con Make: la única ventaja de PDM es necesitar una sola
herramienta, y Make no añade nada que instalar.
