# Herramientas para automatizar tareas

Hacía falta una forma común de instalar las dependencias y ejecutar las tareas
([issue #23](https://github.com/claudiaa2112/EleccionMasterAndalucia/issues/23)).

## Gestor de dependencias

### Criterios

- Que siga el estándar pyproject.toml.
- Lo que tarda en instalarse.

### Opciones

- uv: sigue el estándar pyproject.toml. Se instala en 3,35 s ([captura](capturas/uv.png)).
- Poetry: sigue el estándar pyproject.toml. Se instala en 34,40 s
  ([captura](capturas/poetry.png)).
- PDM: sigue el estándar pyproject.toml. Se instala en 22,60 s ([captura](capturas/pdm.png)).
- Hatch: sigue el estándar pyproject.toml. Se instala en 4,51 s
  ([captura](capturas/hatch.png)).

## Gestor de tareas

### Criterios

- Lo que tarda en instalarse.
- Lo que tarda en ejecutar la tarea check.

### Opciones

- Make: las tareas se definen en un Makefile. Ya estaba instalado en el sistema
  ([captura](capturas/make-instalado.png)), así que no hay tiempo de instalación, y ejecuta
  la tarea check en 0,09 s ([captura](capturas/make.png)).
- just: las tareas se definen en un justfile. Se instala en 1,96 s
  ([captura](capturas/just.png)) y ejecuta la tarea check en 0,12 s
  ([captura](capturas/just1.png)).
- poethepoet: las tareas se definen dentro de pyproject.toml, y funciona con cualquier
  gestor de dependencias, no solo con Poetry. Se instala en 2,88 s y ejecuta la tarea check
  en 0,31 s ([captura](capturas/poethepoet.png)).
- PDM: las tareas se definen dentro de pyproject.toml. Se instala en 22,60 s
  ([captura](capturas/pdm.png)) y ejecuta la tarea check en 1,28 s
  ([captura](capturas/pdm1.png)).
- Hatch: las tareas se definen dentro de pyproject.toml. Se instala en 4,51 s
  ([captura](capturas/hatch.png)) y ejecuta la tarea check en 0,48 s
  ([captura](capturas/hatch1.png)).
