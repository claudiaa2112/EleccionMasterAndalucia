# Herramientas para los tests

Hacía falta una forma de comprobar automáticamente que la lógica hace lo que dicen los
issues del milestone 1
([issue #36](https://github.com/claudiaa2112/EleccionMasterAndalucia/issues/36)).

## Búsqueda de opciones

- Se buscan en la documentación de Python, en PyPI y en la encuesta de desarrolladores de
  Python de 2024 ([resultados](https://lp.jetbrains.com/python-developers-survey-2024/)).
- Entran las que vienen con Python o se instalan desde PyPI, funcionan con Python 3.14 y
  tienen alguna versión publicada en los dos últimos años (búsqueda del 5 de noviembre de
  2026).

## Biblioteca de aserciones

### Criterios

- Que, cuando un test falla, muestre el valor obtenido y el esperado.
- Que permita comprobar que se lanza un error y con qué mensaje.
- Lo que tarda en instalarse.

## Test runner

### Criterios

- Que permita repetir un mismo test con varios casos.
- Que permita preparar una sola vez los datos que comparten varios tests.
- Qué ficheros deja en la carpeta del código y si se puede evitar.
- Lo que tarda en instalarse.
- Lo que tarda en ejecutar un test.

## Dobles de prueba

### Criterios

- Que se puedan usar con el test runner elegido.
- Que permitan comprobar con qué datos se ha llamado al objeto sustituido.
- Lo que tarda en instalarse.
