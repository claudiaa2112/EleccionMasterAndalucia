# Herramientas para automatizar tareas

Hacía falta una forma común de instalar las dependencias y ejecutar las tareas
([issue #23](https://github.com/claudiaa2112/EleccionMasterAndalucia/issues/23)).

## Criterios

- Cuántas herramientas hacen falta en total para gestionar las dependencias y ejecutar las
  tareas.
- Que tenga lockfile, para que todo el mundo instale las mismas versiones.
- Lo que tarda en instalarse la herramienta.
- Lo que tarda en instalar las dependencias.
- Lo que tarda en ejecutar las tareas.

## Gestores de dependencias

- uv: no tiene tareas con nombre, así que hacen falta dos herramientas en total. Tiene
  lockfile, uv.lock. Se instala en 5,40 s, instala las dependencias en 0,16 s y ejecuta la
  comprobación con uv run en 0,25 s ([captura](capturas/uv.png)).
- Poetry: no tiene tareas sin añadir un plugin, así que hacen falta dos herramientas en
  total. Tiene lockfile, poetry.lock. Se instala en 17,52 s, instala las dependencias en
  2,71 s y ejecuta la comprobación con poetry run en 1,42 s ([captura](capturas/poetry.png)).
- PDM: define las tareas en pyproject.toml, así que basta con una herramienta. Tiene
  lockfile, pdm.lock. Se instala en 19,56 s, instala las dependencias en 5,19 s y ejecuta la
  tarea check en 1,24 s ([captura](capturas/pdm.png)).
- Hatch: define las tareas en pyproject.toml, así que basta con una herramienta, pero no
  tiene lockfile. Se instala en 25,08 s, instala las dependencias en 1,55 s y ejecuta la
  comprobación con hatch run en 0,57 s ([captura](capturas/hatch.png)).

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
