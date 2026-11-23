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
aparece con el mismo código, de seis cifras o, en los másteres de la Universidad
Internacional de Andalucía, una A seguida de cinco cifras, y eso me permite juntar lo que
dice cada una sobre un mismo máster.

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

## Qué responde

La clase ConvocatoriaMaster, en [master/convocatoria_master.py](master/convocatoria_master.py),
se crea a partir de las tres páginas del DUA: del catálogo de una titulación saca la
prioridad de esa titulación en cada máster, de las notas de corte el último admitido y de
la ficha de cada máster cuánto pesa la nota media, y lo junta todo por el código del
máster. Su método posibilidades recibe una
nota media y dice, para cada máster del catálogo, si se
entraría seguro, si depende de cómo valore la comisión el resto de méritos, si no se
entraría ni con la máxima valoración o si no se puede saber porque el máster no se
adjudicó. En el servicio web que se desplegará más adelante, será lo que responda cuando
alguien indique su titulación y su nota media.

Los tests usan recortes reales de las tres páginas, guardados en
[tests/paginas_dua](tests/paginas_dua), con la indicación de que la información se ha
obtenido del Portal de la Junta de Andalucía.

## Cómo preparar el proyecto, comprobar el código y ejecutar los tests

Hace falta tener [uv](https://docs.astral.sh/uv/getting-started/installation/), que
instala Python 3.14 si no está y las dependencias del proyecto, y Make. Desde la carpeta
del proyecto:

```bash
make install   # instala Python 3.14 si hace falta y las dependencias del proyecto
make check     # comprueba que la sintaxis del código es correcta
make test      # ejecuta los tests
```

make check lee todos los ficheros de la carpeta master y avisa si alguno tiene un error de
sintaxis, indicando el fichero y la línea, sin escribir nada en disco. No revisa el estilo
ni los tipos.

## Documentación de los objetivos
- [Objetivo 0: tarjeta del juego de rol y configuración del repositorio](docs/objetivos/objetivo-0/objetivo-0.md)
- Objetivo 1: [personas](docs/objetivos/objetivo-1/personas.md), [user journeys](docs/objetivos/objetivo-1/user-journeys.md), [historias de usuario](docs/objetivos/objetivo-1/historias-usuario.md) y [milestones](docs/objetivos/objetivo-1/milestones.md)
- [Objetivo 3: elección de las herramientas para automatizar tareas](docs/objetivos/objetivo-3/automatizacion.md)
- [Objetivo 4: elección de las herramientas para los tests](docs/objetivos/objetivo-4/tests.md)
