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

### Opciones

- Métodos assert de unittest: vienen con Python, así que no hay que instalarlos.
  assertEqual muestra el valor obtenido y el esperado, y assertRaisesRegex comprueba que se
  lanza un error y con qué mensaje ([captura](capturas/unittest-assert.png)).
- assert de Python: viene con Python. Al fallar solo dice AssertionError, sin el valor
  obtenido ni el esperado ([captura](capturas/assert.png)); los muestra si se ejecuta con
  pytest ([documentación](https://docs.pytest.org/en/stable/how-to/assert.html)). No tiene
  forma propia de comprobar que se lanza un error.
- assertpy 2.36.0: se instala en 1,13 s. Al fallar muestra el valor obtenido y el esperado,
  y comprueba que se lanza un error con raises(...).when_called_with(...)
  ([captura](capturas/assertpy.png)), que también permite comprobar su mensaje
  ([documentación](https://assertpy.github.io/assertpy/guides/errors/#expected-exceptions)).

### Elección

Los métodos assert de unittest y assertpy cumplen los dos primeros criterios, pero los de
unittest vienen con Python y no hay que instalarlos, frente a los 1,13 s de assertpy. El
assert de Python, por sí solo, no muestra el valor obtenido y el esperado. Por eso elijo
los métodos assert de unittest.

## Test runner

### Criterios

- Que permita repetir un mismo test con varios casos.
- Que permita preparar una sola vez los datos que comparten varios tests.
- Qué ficheros deja en la carpeta del código y si se puede evitar.
- Lo que tarda en instalarse.
- Lo que tarda en ejecutar un test.

### Opciones

- unittest: viene con Python, así que no hay que instalarlo. Repite un test con varios
  casos con subTest
  ([documentación](https://docs.python.org/3/library/unittest.html#distinguishing-test-iterations-using-subtests))
  y prepara los datos compartidos en setUp
  ([documentación](https://docs.python.org/3/library/unittest.html#unittest.TestCase.setUp)).
  Ejecuta un test en 0,32 s y deja \_\_pycache\_\_ en master y en tests
  ([captura](capturas/unittest.png)), que se evita con PYTHONDONTWRITEBYTECODE=1
  ([documentación](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONDONTWRITEBYTECODE)).
- pytest 9.2.0: se instala en 2,20 s, con 5 paquetes. Repite un test con varios casos con
  parametrize ([documentación](https://docs.pytest.org/en/stable/how-to/parametrize.html))
  y prepara los datos compartidos con fixtures
  ([documentación](https://docs.pytest.org/en/stable/how-to/fixtures.html)). Ejecuta un
  test en 1,45 s y deja \_\_pycache\_\_ en master y en tests y la carpeta .pytest\_cache
  ([captura](capturas/pytest.png)); \_\_pycache\_\_ se evita como en unittest y
  .pytest\_cache con -p no:cacheprovider
  ([documentación](https://docs.pytest.org/en/stable/how-to/plugins.html#deactivating-unregistering-a-plugin-by-name)).
- nose2 0.16.0: se instala en 0,80 s, como un solo paquete. Ejecuta los tests escritos con
  unittest, así que prepara los datos compartidos en setUp como él, y repite un test con
  varios casos con params ([documentación](https://docs.nose2.io/en/latest/params.html)).
  Ejecuta un test en 0,49 s y solo deja \_\_pycache\_\_ en master y en tests
  ([captura](capturas/nose2.png)), que se evita como en unittest.

### Elección

Los tres permiten repetir un test con varios casos y preparar los datos compartidos.
unittest es el que menos tarda en los dos criterios que se miden: viene con Python, así que
no hay que instalarlo, frente a los 0,80 s de nose2 y los 2,20 s de pytest, y ejecuta un
test en 0,32 s, frente a los 0,49 s de nose2 y los 1,45 s de pytest. Además, como nose2,
solo deja \_\_pycache\_\_, mientras que pytest deja también .pytest\_cache. Por eso elijo
unittest.

## Dobles de prueba

### Criterios

- Que se puedan usar con el test runner elegido.
- Que permitan comprobar con qué datos se ha llamado al objeto sustituido.
- Lo que tarda en instalarse.

### Opciones

- flexmock 0.14.0: se instala en 1,01 s, como un solo paquete
  ([captura](capturas/flexmock.png)). Se integra con unittest y con pytest
  ([documentación](https://flexmock.readthedocs.io/)) y comprueba con qué datos se ha
  llamado al objeto sustituido con with\_args
  ([documentación](https://flexmock.readthedocs.io/en/latest/usage/call_count/)).
- mockito 2.0.4: se instala en 0,89 s, como un solo paquete. Funciona sin ningún test
  runner, y verify comprueba con qué datos se ha llamado al objeto sustituido: al fallar
  muestra la llamada que se esperaba y la que se hizo ([captura](capturas/mockito.png)).
