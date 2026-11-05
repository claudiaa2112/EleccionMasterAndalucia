# Herramientas para los tests

Hacía falta una forma de comprobar automáticamente que la lógica hace lo que dicen los
issues del milestone 1
([issue #36](https://github.com/claudiaa2112/EleccionMasterAndalucia/issues/36)).

## De qué parto

- La lógica de la HU001 está dividida en issues (del #26 al #35) y cada uno tiene que tener
  sus tests, incluidos los que comprueban que se rechazan los datos incorrectos (del #32 al
  #35).
- El código solo usa lo que trae Python 3.14, sin dependencias externas.
- Las tareas del proyecto se lanzan con PDM
  ([justificación](../objetivo-3/automatizacion.md)), así que ejecutar los tests tiene que
  ser una tarea más de PDM, como `check`.
- Lo que se elija se usará después en un contenedor, donde no se puede escribir en la
  carpeta del código, y en integración continua, donde cada vez se parte de cero, así que
  importa qué ficheros deja, cuánto tarda en instalarse y cuánto tarda en ejecutar los
  tests.
- Hoy la lógica solo trabaja con datos que ya están en memoria y no depende de nada
  externo. Los dobles de prueba harán falta cuando tenga que leer los datos del DUA.

## Qué hay que elegir

- Biblioteca de aserciones: lo que se escribe dentro de cada test para comparar el
  resultado obtenido con el esperado y avisar, con un mensaje, si no coinciden.
- Test runner: lo que organiza los tests, permite preparar los datos que comparten y
  repetir un mismo test con varios casos.
- Orden para ejecutar los tests: la que encuentra los ficheros de test, los ejecuta y dice
  cuáles pasan y cuáles fallan.
- Dobles de prueba (mocks): objetos que se hacen pasar por otro durante un test, para no
  depender de algo externo.

Una misma herramienta puede cubrir varias de estas piezas, pero en cada opción se indica
cuál cubre.

## Criterios de búsqueda

- Dónde se buscan las opciones: la documentación oficial de Python, para lo que trae de
  serie; PyPI, el repositorio de paquetes de Python; y la encuesta anual de desarrolladores
  de Python (Python Developers Survey), para ver qué se usa.
- Entran en la comparación las que se pueden instalar desde PyPI o vienen con Python,
  funcionan con Python 3.14 y tienen alguna versión publicada en los dos últimos años. Las
  que no cumplen esto se nombran igualmente, con el motivo por el que se descartan.

## Criterios de elección

Biblioteca de aserciones:

- Que, cuando un test falla, el mensaje muestre el valor obtenido y el esperado sin
  escribir nada más.
- Que permita comprobar que se lanza un error y con qué mensaje.

Test runner:

- Que permita repetir un mismo test con varios casos, por ejemplo las cuatro prioridades o
  los límites de una nota, y si lo trae de serie o necesita un complemento.
- Que permita preparar una sola vez los datos que comparten varios tests, como una
  convocatoria de ejemplo.
- Qué ficheros deja en la carpeta del código al ejecutarse y si se puede evitar.

Orden para ejecutar los tests:

- Que termine con un código de error cuando algún test falla, para que la integración
  continua lo detecte.
- Que se pueda lanzar como tarea de PDM.

Dobles de prueba:

- Que se puedan usar con el test runner elegido, o qué haría falta añadir.
- Que permitan comprobar con qué datos se ha llamado al objeto sustituido, no solo qué
  devuelve.

Para todas las opciones que hay que instalar:

- Lo que tarda en instalarse y lo que ocupa.
- Cuántas dependencias necesita.
- Lo que tarda en ejecutar los tests.

## Cómo se mide

Cada opción se prueba en un contenedor limpio con la imagen oficial python:3.14-slim, para
partir siempre de cero, igual que en el [objetivo 3](../objetivo-3/automatizacion.md). Se
mide con el test del
[issue #32](https://github.com/claudiaa2112/EleccionMasterAndalucia/issues/32) (el código
de un máster tiene seis cifras), escrito con cada opción.
