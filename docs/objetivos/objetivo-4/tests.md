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

- Qué dice cuando falla el test de la HU001 que da la posibilidad en cada máster: si señala
  en qué máster la posibilidad no es la esperada.
- Cómo se escribe un test de rechazo, como el de una nota media fuera de 5 a 10: si la
  llamada se puede escribir tal como se hace a la convocatoria.

### Opciones

Para medir el primer criterio, en el test de posibilidades se espera a propósito que en el
492700 la posibilidad sea DEPENDE en vez de ENTRA_SEGURO.

- Métodos assert de unittest: assertEqual enseña todos los másteres y marca la línea del
  492700 con lo obtenido y lo esperado
  ([documentación](https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertEqual)).
  El rechazo se escribe con assertRaisesRegex alrededor de la llamada, tal cual
  ([documentación](https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertRaisesRegex)).
- assert de Python: ejecutado con python -m unittest solo dice AssertionError, sin señalar
  el máster ([documentación](https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement));
  solo lo señala si se ejecuta con pytest
  ([documentación](https://docs.pytest.org/en/stable/how-to/assert.html)). No tiene forma
  propia de comprobar que se lanza un error.
- assertpy 2.36.1: dice que esperaba DEPENDE en el 492700 y obtuvo ENTRA_SEGURO, sin enseñar
  el resto de másteres. El rechazo se escribe con raises(...).when_called_with(...), que
  separa el método de sus argumentos
  ([documentación](https://assertpy.github.io/assertpy/guides/errors/#expected-exceptions)).

### Elección

Los métodos assert de unittest y assertpy señalan el máster que falla, pero con assertpy el
test de rechazo ya no se escribe como la llamada que se hace a la convocatoria. Por eso
elijo los métodos assert de unittest.

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
