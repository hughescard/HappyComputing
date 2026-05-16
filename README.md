# Happy Computing - Simulación basada en eventos discretos

## 1. Problema seleccionado

Tema 4: **Happy Computing**

Happy Computing es un taller de reparaciones electrónicas que ofrece cuatro tipos de servicios:

1. Reparación por garantía.
2. Reparación fuera de garantía.
3. Cambio de equipo.
4. Venta de equipos reparados.

El objetivo del proyecto es desarrollar una simulación basada en eventos discretos que permita estimar la ganancia obtenida por el taller durante una jornada laboral, considerando la llegada aleatoria de clientes, el tipo de servicio solicitado, la disponibilidad de los empleados y las colas generadas cuando los recursos están ocupados.

---

## 2. Objetivo de la simulación

Simular el funcionamiento diario del taller Happy Computing para estimar la ganancia bruta obtenida durante una jornada laboral, teniendo en cuenta:

- La llegada aleatoria de clientes.
- El tipo de servicio solicitado por cada cliente.
- La atención inicial por parte de vendedores.
- La atención técnica requerida para reparaciones y cambios de equipo.
- La disponibilidad limitada de vendedores, técnicos y técnico especializado.
- Las colas generadas cuando los empleados disponibles están ocupados.
- La prioridad del técnico especializado para atender cambios de equipo.

---

## 3. Alcance del modelo

El modelo simula el flujo de clientes dentro del taller desde su llegada hasta la finalización del servicio solicitado.

Cada cliente debe ser atendido inicialmente por un vendedor. Dependiendo del tipo de servicio solicitado, el cliente puede finalizar su proceso después de la atención del vendedor o requerir una atención adicional por parte de un técnico o un técnico especializado. En el caso del tipo 4, el mismo vendedor realiza una segunda fase de venta del equipo reparado antes de completar el servicio.

El sistema cuenta con los siguientes empleados:

- 2 vendedores.
- 3 técnicos.
- 1 técnico especializado.

---

## 4. Servicios disponibles

| Tipo de servicio | Descripción | Ingreso asociado |
|------------------|-------------|------------------|
| Tipo 1 | Reparación por garantía | $0 |
| Tipo 2 | Reparación fuera de garantía | $350 |
| Tipo 3 | Cambio de equipo | $500 |
| Tipo 4 | Venta de equipos reparados | $750 |

La ganancia considerada en este modelo corresponde al ingreso bruto generado por los servicios completados. No se consideran costos de operación, salarios, piezas, electricidad ni otros gastos, ya que el enunciado del problema no proporciona estos datos.

---

## 5. Supuestos del modelo

Para poder construir el modelo de simulación se establecen los siguientes supuestos:

1. La jornada laboral tiene una duración de 8 horas, equivalentes a 480 minutos.

2. Solo se generan llegadas de clientes durante la jornada laboral.

3. Los clientes que llegan antes del cierre de la jornada pueden terminar su servicio aunque la atención finalice después de los 480 minutos.

4. La ganancia se registra cuando el cliente termina completamente su servicio.

5. Todo cliente debe pasar primero por atención de un vendedor.

6. Para los clientes de tipo 4, la primera atención del vendedor representa recepción o clasificación. Una vez identificado que se trata de una venta de equipo reparado, el mismo vendedor continúa con una segunda fase de venta. El vendedor no se libera entre ambas fases y el cliente se completa únicamente al finalizar dicha venta.

7. Las reparaciones por garantía y fuera de garantía pueden ser realizadas por técnicos normales o por el técnico especializado.

8. Los cambios de equipo solo pueden ser realizados por el técnico especializado.

9. El técnico especializado siempre prioriza los cambios de equipo sobre las reparaciones.

10. El técnico especializado solo atiende reparaciones si no hay clientes esperando por cambio de equipo.

11. Si la distribución normal utilizada para el tiempo de atención del vendedor genera un valor negativo, el valor se descarta y se genera nuevamente.

12. La simulación usa minutos como unidad base de tiempo.

---

## 6. Entidades del sistema

### Cliente

El cliente es la entidad principal del sistema. Cada cliente representa una persona que llega al taller y solicita uno de los servicios disponibles.

A cada cliente se le deben almacenar, como mínimo, los siguientes datos:

- Identificador del cliente.
- Tiempo de llegada.
- Tipo de servicio solicitado.
- Tiempo de inicio de atención por vendedor.
- Tiempo de fin de atención por vendedor.
- Tiempo de inicio de venta del equipo reparado, si aplica.
- Tiempo de fin de venta del equipo reparado, si aplica.
- Tiempo de inicio de atención técnica, si aplica.
- Tiempo de fin de atención técnica, si aplica.
- Tiempo total de espera.
- Estado del cliente dentro del sistema.

---

## 7. Recursos del sistema

Los recursos son los empleados disponibles para atender a los clientes.

### Vendedores

Cantidad disponible: 2.

Los vendedores atienden inicialmente a todos los clientes, sin importar el tipo de servicio solicitado.

### Técnicos

Cantidad disponible: 3.

Los técnicos atienden únicamente servicios de reparación:

- Tipo 1: reparación por garantía.
- Tipo 2: reparación fuera de garantía.

### Técnico especializado

Cantidad disponible: 1.

El técnico especializado atiende obligatoriamente los cambios de equipo:

- Tipo 3: cambio de equipo.

Además, puede atender reparaciones de tipo 1 o tipo 2, pero solo cuando no existan clientes esperando por cambio de equipo.

---

## 8. Colas del sistema

El sistema utiliza las siguientes colas:

### Cola de vendedores

Contiene los clientes que esperan por la atención inicial de un vendedor.

### Cola de reparaciones

Contiene los clientes que ya fueron atendidos por un vendedor y esperan por una reparación.

Esta cola incluye clientes de:

- Tipo 1: reparación por garantía.
- Tipo 2: reparación fuera de garantía.

### Cola de cambios de equipo

Contiene los clientes que ya fueron atendidos por un vendedor y esperan por un cambio de equipo.

Esta cola incluye clientes de:

- Tipo 3: cambio de equipo.

La cola de cambios de equipo tiene prioridad para el técnico especializado.

---

## 9. Eventos del calendario

La simulación se basa en un calendario de eventos discretos. Los eventos principales son:

### 1. INICIO_SIMULACION

Marca el comienzo de la simulación.

Responsabilidades principales:

- Inicializar el reloj de simulación en cero.
- Inicializar recursos, colas y métricas.
- Programar la primera llegada de cliente.

### 2. LLEGADA_CLIENTE

Representa la llegada de un nuevo cliente al taller.

Responsabilidades principales:

- Crear un nuevo cliente.
- Determinar aleatoriamente el tipo de servicio solicitado.
- Verificar si hay vendedor disponible.
- Si hay vendedor disponible, iniciar atención inmediatamente.
- Si no hay vendedor disponible, colocar al cliente en la cola de vendedores.
- Programar la próxima llegada, siempre que ocurra dentro de la jornada laboral.

### 3. FIN_ATENCION_VENDEDOR

Representa el momento en que un vendedor termina de atender a un cliente.

Responsabilidades principales:

- Determinar el siguiente paso del cliente según el tipo de servicio:
  - Tipo 1: libera el vendedor y pasa a reparación.
  - Tipo 2: libera el vendedor y pasa a reparación.
  - Tipo 3: libera el vendedor y pasa a cambio de equipo.
  - Tipo 4: no libera el vendedor e inicia la segunda fase de venta con el mismo cliente.
- Si el vendedor fue liberado y hay clientes esperando, asignarlo al siguiente cliente de la cola de vendedores.

### 4. FIN_VENTA_EQUIPO_REPARADO

Representa el momento en que el vendedor termina la segunda fase de atención de un cliente tipo 4.

Responsabilidades principales:

- Liberar el vendedor.
- Sumar el ingreso correspondiente al servicio tipo 4.
- Completar el servicio del cliente.
- Si hay clientes esperando en la cola de vendedores, asignar el vendedor liberado al siguiente cliente.

### 5. FIN_REPARACION

Representa el momento en que finaliza una reparación.

Responsabilidades principales:

- Liberar el recurso que realizó la reparación.
- Sumar el ingreso correspondiente si aplica:
  - Tipo 1: $0.
  - Tipo 2: $350.
- Verificar si el recurso liberado puede atender otro cliente en espera.

### 6. FIN_CAMBIO_EQUIPO

Representa el momento en que finaliza un cambio de equipo.

Responsabilidades principales:

- Liberar el técnico especializado.
- Sumar el ingreso correspondiente al cambio de equipo.
- Verificar si hay clientes esperando por cambio de equipo.
- Si no hay cambios pendientes, verificar si hay reparaciones pendientes que puedan ser atendidas por el técnico especializado.

### Control de cierre de llegadas

El cierre de llegadas no se implementa como un `EventType` real en el código. Es una condición de control del algoritmo de llegadas.

Regla aplicada:

- No se programan nuevas llegadas si el próximo tiempo de llegada supera los 480 minutos de jornada laboral.
- Los eventos ya pendientes en el calendario se siguen procesando hasta que todos los clientes dentro del sistema terminan su servicio.

---

## 10. Acciones internas del modelo

No todos los cambios de estado se modelan como eventos independientes dentro del calendario. Algunas acciones ocurren de forma inmediata dentro del procesamiento de otros eventos.

Las principales acciones internas son:

- iniciar_atencion_vendedor()
- iniciar_reparacion()
- iniciar_cambio_equipo()
- finalizar_cliente()
- intentar_asignar_vendedor()
- intentar_asignar_tecnico()
- intentar_asignar_tecnico_especializado()

Estas acciones pueden generar nuevos eventos futuros, como el fin de una atención o el fin de una reparación.

---

## 11. Reglas de funcionamiento del sistema

1. Cuando llega un cliente, se determina aleatoriamente el tipo de servicio solicitado.

2. Todo cliente debe ser atendido primero por un vendedor.

3. Si hay al menos un vendedor libre, el cliente inicia atención inmediatamente.

4. Si no hay vendedores libres, el cliente entra en la cola de vendedores.

5. Cuando termina la atención del vendedor:
   - Si el cliente solicitó reparación por garantía, pasa a la etapa de reparación.
   - Si el cliente solicitó reparación fuera de garantía, pasa a la etapa de reparación.
   - Si el cliente solicitó cambio de equipo, pasa a la cola o atención del técnico especializado.
   - Si el cliente solicitó venta de equipo reparado, continúa con una segunda fase de atención del mismo vendedor.

6. Los clientes tipo 4 solo se completan al terminar la segunda fase de venta del equipo reparado.

7. Las reparaciones pueden ser atendidas por técnicos normales o por el técnico especializado.

8. Los cambios de equipo solo pueden ser atendidos por el técnico especializado.

9. El técnico especializado atiende primero a los clientes en cola de cambio de equipo.

10. El técnico especializado solo atiende reparaciones si no hay clientes esperando por cambio de equipo.

11. Cuando un recurso termina un servicio, queda libre y se revisa si puede atender a otro cliente en espera.

12. La ganancia se suma únicamente cuando el cliente termina completamente el servicio solicitado.

13. Las nuevas llegadas solo se programan si ocurren dentro del tiempo definido para la jornada laboral.

---

## 12. Variables aleatorias del modelo

La generación de variables aleatorias se implementa directamente en el módulo `src/random_generators.py`. No se utilizan funciones predefinidas de distribución ni librerías externas de generación aleatoria. Primero se genera una secuencia pseudoaleatoria uniforme `U(0,1)` mediante un generador congruencial lineal propio. A partir de estos valores uniformes se construyen las distribuciones requeridas por el modelo: la exponencial mediante transformada inversa, la normal mediante Box-Muller y la variable discreta del tipo de servicio mediante probabilidades acumuladas.

| Variable | Método de generación |
|---|---|
| Uniforme `U(0,1)` | Generador congruencial lineal Park-Miller MINSTD |
| Tiempo entre llegadas | Exponencial por transformada inversa |
| Tipo de servicio | Comparación contra probabilidades acumuladas |
| Atención inicial del vendedor | Normal por Box-Muller, con regeneración si el valor es menor o igual que 0 |
| Venta de equipo reparado | Normal por Box-Muller, igual que atención de vendedor |
| Reparación | Exponencial por transformada inversa |
| Cambio de equipo | Exponencial por transformada inversa |

### Tiempo entre llegadas de clientes

Se modela mediante una distribución exponencial con media de 20 minutos.

Esta interpretación se utiliza porque, aunque el enunciado indica que los clientes arriban con intervalo de tiempo Poisson con λ = 20 minutos, en una simulación de eventos discretos resulta conveniente modelar las llegadas como un proceso de Poisson, donde los tiempos entre llegadas siguen una distribución exponencial.

### Tipo de servicio solicitado

El tipo de servicio se genera usando una distribución discreta con las siguientes probabilidades:

| Tipo de servicio | Probabilidad |
|------------------|--------------|
| Tipo 1 | 0.45 |
| Tipo 2 | 0.25 |
| Tipo 3 | 0.10 |
| Tipo 4 | 0.20 |

### Tiempo de atención del vendedor

Se modela mediante una distribución normal:

- Media: 5 minutos.
- Desviación estándar: 2 minutos.

En caso de generarse un valor negativo, se descarta y se genera un nuevo valor.

### Tiempo de venta de equipo reparado

Se modela con la misma distribución normal que la atención del vendedor:

- Media: 5 minutos.
- Desviación estándar: 2 minutos.

El vendedor no se libera entre ambas fases.

### Tiempo de reparación

Se modela mediante una distribución exponencial con media de 20 minutos.

Aplica para:

- Reparación por garantía.
- Reparación fuera de garantía.

### Tiempo de cambio de equipo

Se modela mediante una distribución exponencial con media de 15 minutos.

Aplica para:

- Cambio de equipo.

---

## 13. Métricas de salida

La métrica principal del modelo es:

- Ganancia bruta total de la jornada.

Además, se calcularán métricas complementarias para analizar el comportamiento del sistema:

- Cantidad total de clientes generados.
- Cantidad total de clientes atendidos.
- Cantidad de clientes atendidos por tipo de servicio.
- Ganancia generada por tipo de servicio.
- Tiempo promedio de espera en la cola de vendedores.
- Tiempo promedio de espera en la cola de reparaciones.
- Tiempo promedio de espera en la cola de cambios de equipo.
- Utilización promedio de vendedores.
- Utilización promedio de técnicos.
- Utilización del técnico especializado.
- Cantidad de clientes que quedan pendientes al cierre de la jornada.
- Tiempo final de la simulación.

---

## 14. Cálculo de la ganancia

La ganancia bruta total se calcula a partir de los servicios completados:

```text
ganancia_total =
    0   * cantidad_servicios_tipo_1_completados
  + 350 * cantidad_servicios_tipo_2_completados
  + 500 * cantidad_servicios_tipo_3_completados
  + 750 * cantidad_servicios_tipo_4_completados
```

Donde:

- Tipo 1: reparación por garantía.
- Tipo 2: reparación fuera de garantía.
- Tipo 3: cambio de equipo.
- Tipo 4: venta de equipos reparados.

---

## 15. Uso de semillas aleatorias

Durante la etapa de desarrollo y verificación del simulador se utilizará una semilla fija para garantizar la reproducibilidad de los resultados.

Esto permite:

- Repetir una misma ejecución.
- Depurar errores.
- Comparar cambios en la lógica del simulador.
- Verificar que el calendario de eventos funcione correctamente.

Para el análisis experimental final se ejecutarán múltiples réplicas independientes, variando la semilla en cada corrida, con el objetivo de estimar el comportamiento promedio del sistema.

---

## 16. Estructura del proyecto

```text
happy-computing-simulation/
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── simulation.py
│   ├── entities.py
│   ├── events.py
│   ├── experiments.py
│   └── random_generators.py
│
├── docs/
│   ├── pseudocodigo_happy_computing.md
│   └── resultados_experimentales.md
│
├── results/
│   └── replications_1000.csv
│
├── report/
│   ├── informe_happy_computing.md
│   └── informe_happy_computing.pdf
│
├── tests/
│   └── manual_checks.py
│
├── README.md
└── requirements.txt
```