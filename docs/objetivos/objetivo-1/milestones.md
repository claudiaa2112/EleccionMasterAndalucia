# Milestones

## Milestone 0: modelado del problema de la HU001

Es un milestone interno, que corresponde al objetivo 2 de la asignatura, y trabaja solo
con la [HU001](historias-usuario.md#hu001-no-sé-en-qué-másteres-tengo-posibilidades-objetivas-de-entrar).
Para analizar su problema se sigue la metodología de diseño dirigido por el dominio
(Domain Driven Design).

### Qué se entrega

El código, todavía sin lógica, en el que cada objeto valor, entidad y agregado sale de un
issue en el que se ha aplicado esa metodología a la HU001.

### Cómo se sabe que es válido

Es válido si se ha seguido esa metodología. Claudia lo comprobará viendo que:

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
[HU001](historias-usuario.md#hu001-no-sé-en-qué-másteres-tengo-posibilidades-objetivas-de-entrar)
con la misma metodología, dividiéndolo en problemas más simples cuya solución se pueda
comprobar con un test.

### Qué se entrega

El código del milestone 0 con la lógica que resuelve el problema de la HU001, junto con
los tests que la comprueban, incluidos los de los errores que puedan darse, y que se
ejecutan con una sola orden.

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
