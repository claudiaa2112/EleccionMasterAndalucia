# EleccionMasterAndalucia
## Descripción

Soy estudiante de último curso de Ingeniería Informática y el año que viene me gustaría seguir formándome cursando un máster. 
Lo único que tengo decidido es que quiero hacerlo en alguna universidad de Andalucía, pero tengo que averiguar qué másteres son afines al grado que he estudiado y en cuáles de ellos tengo opciones reales de entrar. 
Me recomendaron ver las opciones en la web del Distrito Único Andaluz (DUA), pero me salen cientos de resultados y tardo mucho en ir viendo la ficha de cada máster y en calcular si es, o no, una opción viable para mí, ya que tengo que tener en cuenta la prioridad que tiene mi carrera con respecto a cada máster, la nota de corte de la última adjudicación y, además, al abrir varias fichas de algunos másteres que me han llamado la atención, me he dado cuenta de que la nota de corte no siempre es comparable a la que tengo en mi expediente, porque algunos másteres tienen en cuenta otros criterios, como, por ejemplo, si tengo algún certificado de idiomas o formación complementaria (como cursos u otras titulaciones).

Para saber si tengo opciones en un máster, los únicos datos que tengo que aportar yo son mi
titulación, mi nota media y mis certificados de idiomas u otros méritos, si los tengo. Todo lo
demás está publicado en la web del DUA.

## Fuentes de datos

Todos los datos los saco del portal del Distrito Único Andaluz (DUA), la web oficial de la
Junta de Andalucía para acceder a los másteres de las universidades públicas andaluzas. La
información aparece escrita directamente en cada página, ordenada en tablas, así que se
puede leer y procesar sin herramientas especiales. Además, en todas las páginas cada máster
aparece con el mismo código de seis cifras, y eso me permite juntar lo que dice cada una
sobre un mismo máster.

- Catálogo de másteres para mi grado: en el [buscador de másteres](https://www.juntadeandalucia.es/economiaconocimientoempresasyuniversidad/sguit/mo_catalogo_top.php),
  eligiendo mi titulación, Grado en Ingeniería Informática, sale la lista de másteres que la
  admiten y con qué prioridad (alta, media o baja). Si la prioridad aparece en rojo, hay que
  cumplir un requisito adicional que se explica en la ficha del máster. Por ejemplo, el
  máster en Ingeniería Informática de Granada, con código 492700, tiene prioridad alta para
  mi grado.
- Notas de corte: en [esta página](https://www.juntadeandalucia.es/economiaconocimientoempresasyuniversidad/sguit/convocatorias/master_consulta_adj/notas_corte_adj.php)
  están las notas de corte de la última adjudicación, la de la admisión al curso 2026/2027.
  Para cada máster aparece la prioridad y la puntuación del último estudiante que entró.
  Cuando pone 0,01 con dos asteriscos, quiere decir que entraron todos los que lo pidieron
  con esa prioridad o una mayor. En el máster 492700, el último que entró tenía prioridad
  "resto" y 5 puntos.
- Ficha de cada máster: cada máster tiene su ficha, por ejemplo
  [la del máster 492700](https://www.juntadeandalucia.es/economiaconocimientoempresasyuniversidad/sguit/mo_catalogo_ficha.php?c_peticion=492700).
  En ella se explica qué se tiene en cuenta para puntuar a cada estudiante y cuánto pesa
  cada cosa, además de los requisitos adicionales. En el 492700 solo cuenta la nota media
  del expediente.

Según su [aviso legal](https://www.juntadeandalucia.es/informacion/legal.html), los
contenidos del portal de la Junta de Andalucía, del que forma parte el DUA, se pueden
reutilizar con licencia Creative Commons Reconocimiento 3.0, indicando que la información se
ha obtenido del Portal de la Junta de Andalucía.

## La clase Master

La clase Master, en [master/master.py](master/master.py), reúne lo que el DUA publica sobre
un máster y que hace falta para saber si tengo opciones de entrar:

- con qué prioridad admite cada titulación y qué requisitos adicionales le pide;
- qué criterios usa para puntuar y cuánto pesa cada uno, distinguiendo los que puedo
  calcular yo de los que dependen de la comisión;
- la nota de corte de la última adjudicación.

En el servicio web que se desplegará más adelante, cuando alguien indique su titulación, su
nota media y sus méritos, se comparará con cada máster para decirle si entra seguro, si
depende de la valoración de la comisión o si no entra ni con la máxima puntuación.

## Cómo preparar el proyecto y comprobar el código

Hace falta tener Python 3.14 y [PDM](https://pdm-project.org/latest/#installation).
Desde la carpeta del proyecto:

```bash
pdm install   # crea el entorno del proyecto e instala lo que necesita
pdm check     # comprueba que la sintaxis del código es correcta
```

pdm check compila todos los ficheros de la carpeta master y avisa si alguno tiene un error
de sintaxis, indicando el fichero y la línea. No revisa el estilo ni los tipos.

## Por qué PDM

Hacía falta una forma común de preparar el proyecto y comprobar el código
([issue #23](https://github.com/claudiaa2112/EleccionMasterAndalucia/issues/23)). Para
elegir la herramienta he partido de esto:

- Python define en un estándar cómo se describe un proyecto y sus dependencias: el fichero
  pyproject.toml ([PEP 621](https://peps.python.org/pep-0621/)), los grupos de dependencias
  para quien desarrolla ([PEP 735](https://peps.python.org/pep-0735/)) y el fichero que fija
  las versiones instaladas ([PEP 751](https://peps.python.org/pep-0751/)). Pero no dice qué
  programa tiene que usarlos.
- El código solo usa lo que trae Python, sin dependencias externas, así que la rapidez
  instalando muchas dependencias no es un criterio que pese aquí.
- La versión de Python ya la gestiona pyenv, así que no hace falta que la herramienta
  también instale Python.
- Se prefiere una sola herramienta para dependencias y tareas, para no añadir otra más.
- Que esté bien mantenida, para no acumular deuda técnica.

Las opciones que he mirado, con datos de GitHub del 31-10-2026:

- uv sigue el estándar y está muy activo, pero no tiene tareas con nombre (la petición
  [#5903](https://github.com/astral-sh/uv/issues/5903) sigue abierta), así que haría falta
  otra herramienta para ellas. Además instala versiones de Python, lo que se solapa con
  pyenv. Tiene más de 3000 issues y PR abiertos.
- Poetry sigue el estándar, pero tampoco tiene tareas sin añadir un plugin. Tiene unos 620
  issues y PR abiertos.
- Hatch tiene tareas, pero no tiene fichero que fije las versiones
  ([#749](https://github.com/pypa/hatch/issues/749) sigue abierta) e instala versiones de
  Python. Tiene unos 450 issues y PR abiertos.
- Pipenv usa su propio fichero, Pipfile, en lugar del estándar pyproject.toml.
- pip con venv viene con Python, pero no fija versiones ni tiene tareas, y haría falta
  añadir otra herramienta como Make.
- PDM sigue el estándar, fija las versiones en pdm.lock y permite definir las tareas dentro
  de pyproject.toml ([documentación](https://pdm-project.org/latest/usage/scripts/)). Usa el
  Python que ya hay instalado. Sacó su última versión el 30-10-2026 y tiene 45 issues y PR
  abiertos.

He elegido PDM porque es la única que cumple todo con una sola herramienta. Sus puntos
débiles son que su comunidad es más pequeña que la de uv o Poetry y que el formato estándar
de fichero de versiones, pylock.toml, todavía es experimental en PDM, por eso se usa el suyo
propio, pdm.lock.

Para la tarea check uso el compilador que trae Python (compileall), porque se pide comprobar
solo la sintaxis. Herramientas como Ruff o mypy revisan además estilo y tipos, que es más de
lo que se pide.

## Documentación de los objetivos
- [Objetivo 0: tarjeta del juego de rol y configuración del repositorio](docs/objetivos/objetivo-0/objetivo-0.md)
- Objetivo 1: [personas](docs/objetivos/objetivo-1/personas.md), [user journeys](docs/objetivos/objetivo-1/user-journeys.md), [historias de usuario](docs/objetivos/objetivo-1/historias-usuario.md) y [milestones](docs/objetivos/objetivo-1/milestones.md)