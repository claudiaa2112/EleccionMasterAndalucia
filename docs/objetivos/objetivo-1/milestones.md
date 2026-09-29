# Milestones

## Milestone 0: modelado del problema de la HU001

Es un milestone interno, que corresponde al objetivo 2 de la asignatura, y trabaja solo
con la [HU001](historias-usuario.md#hu001-claudia-no-sabe-en-qué-másteres-tiene-posibilidades-objetivas-de-entrar).

### Qué se entrega

Un pull request a la rama principal del repositorio, asignado a este milestone, que
contiene:

- los issues que analizan el problema de la HU001, cada uno planteado como un problema y
  enlazado a ella;
- el código en el lenguaje de programación elegido, todavía sin lógica, organizado según
  las buenas prácticas de ese lenguaje en cuanto a directorios y nombres de ficheros y
  clases;
- el fichero `iv.yaml`, con la clave `entidad` apuntando al fichero donde está la entidad,
  y la justificación del lenguaje elegido.

### Cómo se sabe que es válido

Es válido si se ha seguido la metodología de diseño dirigido por el dominio (Domain Driven
Design) a partir de la HU001. Claudia lo comprobará en el pull request viendo que:

- los issues salen de la HU001 y de lo que enlaza (su journey y la definición de
  posibilidades objetivas) y plantean problemas, no tareas;
- en los issues se ha identificado el lenguaje ubicuo, es decir, el vocabulario del
  problema que entienden igual Claudia y quien programa;
- cada parte del código responde a uno de esos issues, y en él se justifica por qué es un
  objeto valor, una entidad o un agregado;
- se han tenido en cuenta los errores que pueden darse al crear cada parte;
- cada commit cierra o referencia un issue;
- el código es sintácticamente correcto.

## Milestone 1: lógica del problema de la HU001 comprobada con tests

Es un milestone interno, que corresponde al objetivo 4 de la asignatura. Parte de lo
entregado en el milestone 0 y sigue trabajando sobre el problema de la
[HU001](historias-usuario.md#hu001-claudia-no-sabe-en-qué-másteres-tiene-posibilidades-objetivas-de-entrar).

### Qué se entrega

Un pull request a la rama principal del repositorio, asignado a este milestone, que
contiene:

- los issues que dividen el problema de la HU001 en problemas más simples, cuya solución
  se pueda comprobar con un test, cada uno enlazado a ella;
- el código con la lógica de negocio, construido sobre el del milestone 0;
- los tests de esa lógica, incluidos los de los errores que puedan darse;
- la elección documentada de la biblioteca de aserciones y del ejecutor de tests, con los
  criterios fijados antes de elegirlos;
- la clave `test` en el fichero `iv.yaml` y el README actualizado explicando cómo se
  ejecutan los tests.

### Cómo se sabe que es válido

Es válido si todos los tests pasan al ejecutarlos con una sola orden, y esos tests
comprueban que se resuelve el problema de la HU001 tal como está descrito, incluidos los
distintos casos de la definición de
[posibilidades objetivas](user-journeys.md#qué-tiene-en-cuenta-para-saber-si-tiene-opciones-en-un-máster).
Claudia lo comprobará además viendo que:

- cada test responde a un issue, y cada issue a la HU001;
- los tests siguen los principios F.I.R.S.T. (rápidos, independientes, repetibles, que
  validan por sí mismos y hechos a tiempo);
- cada commit cierra o referencia un issue.
