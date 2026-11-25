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

### Opciones

- Métodos assert de unittest: assertEqual muestra el valor obtenido y el esperado
  ([documentación](https://docs.python.org/3/library/unittest.html#distinguishing-test-iterations-using-subtests)),
  y assertRaisesRegex comprueba que se lanza un error y con qué mensaje
  ([documentación](https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertRaisesRegex)).
- assert de Python: al fallar solo lanza AssertionError, sin el valor obtenido ni el
  esperado ([documentación](https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement)); los muestra si se ejecuta con pytest
  ([documentación](https://docs.pytest.org/en/stable/how-to/assert.html)). No tiene forma
  propia de comprobar que se lanza un error.
- assertpy 2.36.0: al fallar muestra el valor obtenido y el esperado, y comprueba que se
  lanza un error con raises(...).when_called_with(...), que también permite comprobar su mensaje
  ([documentación](https://assertpy.github.io/assertpy/guides/errors/#expected-exceptions)).

### Elección

Los métodos assert de unittest y assertpy cumplen los dos criterios; el assert de Python,
por sí solo, no muestra el valor obtenido y el esperado. Elijo los métodos assert de
unittest porque son parte del test runner elegido, así que los tests no necesitan otra
biblioteca para hacer las comprobaciones.

## Test runner o framework

### Criterios

- Que permita agrupar los casos de un mismo test en subtests.
- Que tenga fixtures o funciones que preparen los datos que comparten varios tests.

### Opciones

- unittest: repite un test con varios casos con subTest
  ([documentación](https://docs.python.org/3/library/unittest.html#distinguishing-test-iterations-using-subtests))
  y prepara los datos compartidos en setUp
  ([documentación](https://docs.python.org/3/library/unittest.html#unittest.TestCase.setUp)).
- pytest 9.2.0: repite un test con varios casos con parametrize
  ([documentación](https://docs.pytest.org/en/stable/how-to/parametrize.html)) y prepara
  los datos compartidos con fixtures
  ([documentación](https://docs.pytest.org/en/stable/how-to/fixtures.html)).

### Elección

Los dos cumplen los dos criterios. Elijo unittest porque es el que ejecuta la orden elegida
en el apartado siguiente, python -m unittest, que solo ejecuta tests escritos con unittest.

## Orden para ejecutar los tests

### Criterio

- Lo que tarda en ejecutar un test.

### Opciones

- python -m unittest: ejecuta un test en 0,23 s ([captura](capturas/unittest.png)).
- nose2 0.16.0: ejecuta los tests escritos con unittest. Ejecuta un test en 0,51 s
  ([captura](capturas/nose2.png)).
- pytest 9.2.0: ejecuta un test en 0,84 s ([captura](capturas/pytest.png)).

### Elección

python -m unittest es el que menos tarda en ejecutar un test: 0,23 s, frente a los 0,51 s
de nose2 y los 0,84 s de pytest. Por eso elijo python -m unittest.
