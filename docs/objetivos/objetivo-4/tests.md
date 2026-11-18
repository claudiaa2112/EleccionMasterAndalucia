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

- Métodos assert de unittest: assertEqual muestra el valor obtenido y el esperado, y
  assertRaisesRegex comprueba que se lanza un error y con qué mensaje
  ([captura](capturas/unittest-assert.png)).
- assert de Python: al fallar solo dice AssertionError, sin el valor obtenido ni el
  esperado ([captura](capturas/assert.png)); los muestra si se ejecuta con pytest
  ([documentación](https://docs.pytest.org/en/stable/how-to/assert.html)). No tiene forma
  propia de comprobar que se lanza un error.
- assertpy 2.36.0: al fallar muestra el valor obtenido y el esperado, y comprueba que se
  lanza un error con raises(...).when_called_with(...) ([captura](capturas/assertpy.png)),
  que también permite comprobar su mensaje
  ([documentación](https://assertpy.github.io/assertpy/guides/errors/#expected-exceptions)).

### Elección

Los métodos assert de unittest y assertpy cumplen los dos criterios; el assert de Python,
por sí solo, no muestra el valor obtenido y el esperado. Elijo los métodos assert de
unittest porque son parte del test runner elegido, así que los tests no necesitan otra
biblioteca para hacer las comprobaciones.

## Test runner

### Criterios

- Que permita repetir un mismo test con varios casos.
- Que permita preparar una sola vez los datos que comparten varios tests.

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

### Criterios

- Qué ficheros deja en la carpeta del código y si se puede evitar.
- Lo que tarda en ejecutar un test.

### Opciones

- python -m unittest: ejecuta un test en 0,32 s y deja \_\_pycache\_\_ en master y en tests
  ([captura](capturas/unittest.png)), que se evita con PYTHONDONTWRITEBYTECODE=1
  ([documentación](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONDONTWRITEBYTECODE)).
- nose2 0.16.0: ejecuta los tests escritos con unittest. Ejecuta un test en 0,49 s y solo
  deja \_\_pycache\_\_ en master y en tests ([captura](capturas/nose2.png)), que se evita
  igual.
- pytest 9.2.0: ejecuta un test en 1,45 s y deja \_\_pycache\_\_ en master y en tests y la
  carpeta .pytest\_cache ([captura](capturas/pytest.png)); .pytest\_cache se evita con
  -p no:cacheprovider
  ([documentación](https://docs.pytest.org/en/stable/how-to/plugins.html#deactivating-unregistering-a-plugin-by-name)).

### Elección

Los tres dejan solo ficheros que se pueden evitar, y python -m unittest es el que menos
tarda en ejecutar un test: 0,32 s, frente a los 0,49 s de nose2 y los 1,45 s de pytest. Por
eso elijo python -m unittest.

## Dobles de prueba

### Criterios

- Que se puedan usar con el test runner elegido.
- Que permitan comprobar con qué datos se ha llamado al objeto sustituido.

### Opciones

- unittest.mock: funciona con cualquier test runner y comprueba con qué datos se ha llamado
  al objeto sustituido con assert\_called\_with
  ([documentación](https://docs.python.org/3/library/unittest.mock.html)).
- flexmock 0.14.0: funciona con Python 3.14 ([captura](capturas/flexmock.png)), se integra
  con unittest y con pytest ([documentación](https://flexmock.readthedocs.io/)) y comprueba
  con qué datos se ha llamado al objeto sustituido con with\_args
  ([documentación](https://flexmock.readthedocs.io/en/latest/usage/call_count/)).
- mockito 2.0.4: funciona sin ningún test runner, y verify comprueba con qué datos se ha
  llamado al objeto sustituido: al fallar muestra la llamada que se esperaba y la que se
  hizo ([captura](capturas/mockito.png)).

### Elección

Las tres funcionan con unittest y comprueban con qué datos se ha llamado al objeto
sustituido. Elijo unittest.mock porque es parte del test runner elegido, así que no hace
falta otra biblioteca para sustituir objetos en los tests.
