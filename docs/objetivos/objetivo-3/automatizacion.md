# Herramientas para automatizar tareas

Hacía falta una forma común de instalar las dependencias y ejecutar las tareas
([issue #23](https://github.com/claudiaa2112/EleccionMasterAndalucia/issues/23)).

## Gestor de dependencias

### Criterios

- Que siga el estándar pyproject.toml.
- Lo que tarda en instalarse.

### Opciones

- uv: sigue el estándar pyproject.toml. Se instala en 3,35 s ([captura](capturas/uv.png)).
- Poetry: sigue el estándar pyproject.toml. Se instala en 17,52 s
  ([captura](capturas/poetry.png)).
- PDM: sigue el estándar pyproject.toml. Se instala en 19,56 s ([captura](capturas/pdm.png)).
- Hatch: sigue el estándar pyproject.toml. Se instala en 25,08 s
  ([captura](capturas/hatch.png)).

## Gestor de tareas

### Criterios

- Lo que tarda en instalarse.
- Lo que tarda en ejecutar la tarea check.

### Opciones

- Make: las tareas se definen en un Makefile. Ya estaba instalado en el sistema, así que
  no hay tiempo de instalación, y ejecuta la tarea check en 0,09 s
  ([captura](capturas/make.png)).
- just: las tareas se definen en un justfile. Se instala en 3,14 s y ejecuta la tarea check
  en 0,10 s ([captura](capturas/just.png)).
- poethepoet: las tareas se definen dentro de pyproject.toml, y funciona con cualquier
  gestor de dependencias, no solo con Poetry. Se instala en 2,93 s y ejecuta la tarea check
  en 0,43 s ([captura](capturas/poethepoet.png)).
