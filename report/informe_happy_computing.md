# Informe del Proyecto

# Simulación basada en Eventos Discretos: Happy Computing

## 1. Datos generales

| Campo | Valor |
|---|---|
| Nombre del estudiante | Guillermo Hughes Cardona |
| Grupo | C311 |
| Asignatura | Simulación |
| Repositorio de GitHub | <https://github.com/hughescard/HappyComputing> |

---

## 2. Problema seleccionado

El problema seleccionado corresponde al Tema 4: Happy Computing.

Happy Computing es un taller de reparaciones electrónicas que ofrece cuatro tipos de servicios:

1. reparación por garantía;
2. reparación fuera de garantía;
3. cambio de equipo;
4. venta de equipos reparados.

El sistema debe representar el comportamiento operativo de una jornada laboral, considerando llegadas aleatorias de clientes, disponibilidad limitada de empleados, formación de colas y generación de ingresos por servicios completados.

---

## 3. Descripción general del sistema

El taller cuenta con tres tipos de recursos:

- 2 vendedores.
- 3 técnicos normales.
- 1 técnico especializado.

Todos los clientes pasan inicialmente por un vendedor. Esa primera atención representa recepción, consulta, identificación o clasificación de la solicitud.

Después de la atención inicial, el flujo depende del tipo de servicio:

- Tipo 1: pasa a reparación por garantía.
- Tipo 2: pasa a reparación fuera de garantía.
- Tipo 3: pasa a cambio de equipo.
- Tipo 4: continúa con una segunda fase de venta de equipo reparado.

Se decidió modelar el servicio tipo 4 en dos fases porque la venta de un equipo reparado no termina con la simple identificación de la solicitud. Después de la recepción inicial, el vendedor debe realizar acciones comerciales adicionales asociadas a la venta. Por ello, se programa un segundo evento de fin de venta y el vendedor permanece ocupado hasta completarlo.

---

## 4. Objetivo de la simulación

El objetivo de la simulación es estimar el comportamiento promedio del taller durante una jornada laboral de 480 minutos.

La métrica principal es la ganancia bruta total obtenida por jornada. Además, se analizan:

- clientes generados;
- clientes completados;
- clientes completados por tipo de servicio;
- tiempos promedio de espera;
- utilización promedio de vendedores, técnicos y técnico especializado.

---

## 5. Principales ideas seguidas para la solución

La solución se desarrolló mediante simulación basada en eventos discretos.

Las ideas principales fueron:

- Mantener un reloj de simulación.
- Usar un calendario de eventos ordenado por tiempo.
- Representar clientes mediante una entidad con tiempos de entrada, atención, espera y salida.
- Representar recursos mediante contadores de disponibilidad.
- Usar colas FIFO para vendedores, reparaciones y cambios de equipo.
- Programar eventos futuros cuando inicia una atención.
- Sumar ingresos solo cuando un cliente completa todo su servicio.
- Ejecutar múltiples réplicas independientes para obtener resultados agregados.

El calendario se implementa con una cola de prioridad. Cada evento tiene un contador incremental para resolver empates de tiempo y conservar un procesamiento determinista.

---

## 6. Supuestos del modelo

Los supuestos utilizados son:

1. La jornada laboral dura 480 minutos.

2. Solo se generan nuevas llegadas dentro de la jornada laboral.

3. Los clientes que llegaron antes del cierre pueden terminar su servicio después del minuto 480.

4. La simulación termina cuando ya no quedan eventos pendientes.

5. Todo cliente pasa primero por un vendedor.

6. Las reparaciones tipo 1 y tipo 2 pueden ser realizadas por técnicos normales o por el técnico especializado.

7. Los cambios de equipo tipo 3 solo pueden ser realizados por el técnico especializado.

8. El técnico especializado prioriza cambios de equipo sobre reparaciones.

9. Los servicios no son interrumpibles.

10. Para clientes tipo 4, la venta de equipo reparado requiere una segunda fase consecutiva con el mismo vendedor.

11. El vendedor no se libera entre la atención inicial y la venta del cliente tipo 4.

12. La ganancia se registra solo cuando el cliente termina completamente el servicio solicitado.

---

## 7. Variables aleatorias utilizadas

Las variables aleatorias del modelo son:

| Variable | Distribución |
|---|---|
| Tiempo entre llegadas | Exponencial con media 20 minutos |
| Tipo de servicio | Discreta: 0.45, 0.25, 0.10, 0.20 |
| Atención inicial del vendedor | Normal `N(5, 2)` truncada por regeneración si el valor es menor o igual que 0 |
| Venta de equipo reparado | Normal `N(5, 2)` truncada, igual a la atención del vendedor |
| Reparación | Exponencial con media 20 minutos |
| Cambio de equipo | Exponencial con media 15 minutos |

Las probabilidades por tipo de servicio son:

| Tipo | Probabilidad |
|---|---:|
| Tipo 1 | 0.45 |
| Tipo 2 | 0.25 |
| Tipo 3 | 0.10 |
| Tipo 4 | 0.20 |

---

## 8. Entidades, recursos y colas

### Entidad principal

La entidad principal es el cliente.

Cada cliente almacena:

- identificador;
- tiempo de llegada;
- tipo de servicio;
- inicio y fin de atención inicial con vendedor;
- inicio y fin de venta de equipo reparado, si aplica;
- entrada a cola técnica, si aplica;
- inicio y fin de servicio técnico, si aplica;
- tiempo de salida.

### Recursos

| Recurso | Cantidad | Función |
|---|---:|---|
| Vendedores | 2 | Atención inicial y venta de equipos reparados |
| Técnicos normales | 3 | Reparaciones tipo 1 y tipo 2 |
| Técnico especializado | 1 | Cambios de equipo y reparaciones si no hay cambios esperando |

### Colas

| Cola | Clientes que contiene |
|---|---|
| Cola de vendedores | Clientes esperando atención inicial |
| Cola de reparaciones | Clientes tipo 1 y 2 esperando reparación |
| Cola de cambios de equipo | Clientes tipo 3 esperando técnico especializado |

El cliente tipo 4 no vuelve a la cola de vendedores para la venta. La venta se realiza de forma consecutiva con el mismo vendedor.

---

## 9. Modelo de eventos discretos desarrollado

El modelo utiliza los siguientes eventos principales:

| Evento | Significado |
|---|---|
| `ARRIVAL` | Llegada de un cliente |
| `SELLER_SERVICE_END` | Fin de la atención inicial del vendedor |
| `SELLER_SALE_END` | Fin de la venta de equipo reparado para tipo 4 |
| `REPAIR_END` | Fin de reparación |
| `EQUIPMENT_CHANGE_END` | Fin de cambio de equipo |

El evento `SELLER_SALE_END` se agregó para representar correctamente el nuevo flujo del servicio tipo 4.

El cierre de llegadas no se modela como evento. Es una condición de control: si la próxima llegada ocurre después del minuto 480, no se programa. Los eventos ya agendados continúan procesándose hasta vaciar el calendario.

---

## 10. Reglas de asignación de recursos

Las reglas principales son:

1. Si llega un cliente y hay vendedor libre, inicia atención inicial.

2. Si no hay vendedor libre, espera en la cola de vendedores.

3. Al terminar la atención inicial:
   - tipo 1 y 2 liberan vendedor y pasan a reparación;
   - tipo 3 libera vendedor y pasa a cambio de equipo;
   - tipo 4 mantiene ocupado al vendedor e inicia la fase de venta.

4. Al terminar `SELLER_SALE_END`, el cliente tipo 4 se completa, se registra el ingreso de $750 y se libera el vendedor.

5. Técnicos normales solo atienden reparaciones.

6. El técnico especializado atiende primero cambios de equipo.

7. El técnico especializado solo atiende reparaciones cuando no hay cambios de equipo esperando.

8. Ningún servicio se interrumpe una vez iniciado.

---

## 11. Implementación del simulador

El simulador está organizado en módulos:

| Archivo | Responsabilidad |
|---|---|
| `src/events.py` | Definición de tipos de eventos, recursos y dataclass de evento |
| `src/entities.py` | Definición de la entidad cliente |
| `src/random_generators.py` | Generadores aleatorios del modelo |
| `src/simulation.py` | Núcleo de la simulación |
| `src/experiments.py` | Ejecución de múltiples réplicas y exportación CSV |
| `src/main.py` | Entrada por consola |
| `tests/manual_checks.py` | Pruebas manuales e invariantes |

La ejecución individual se realiza con:

```bash
python3 -m src.main --seed 12345
```

La ejecución experimental se realiza con:

```bash
python3 -m src.main --replications 1000 --output-csv results/replications_1000.csv
```

---

## 12. Validación del simulador

La validación se realizó mediante pruebas manuales que verifican:

- consistencia de ingresos;
- ausencia de colas pendientes al finalizar;
- comportamiento sin clientes;
- presión sobre vendedores;
- presión sobre reparaciones;
- presión sobre técnico especializado;
- segunda fase obligatoria para clientes tipo 4.

La prueba específica del tipo 4 verifica que:

- existe inicio y fin de atención inicial;
- existe inicio y fin de venta;
- `seller_sale_start == seller_service_end`;
- `departure_time == seller_sale_end`.

---

## 13. Configuración experimental

La configuración experimental fue:

| Parámetro | Valor |
|---|---:|
| Réplicas | 1000 |
| Seed base | 12345 |
| Jornada laboral | 480 minutos |
| Vendedores | 2 |
| Técnicos normales | 3 |
| Técnico especializado | 1 |

Cada réplica utiliza `seed_i = 12345 + i`.

---

## 14. Resultados obtenidos

### Ganancia

| Métrica | Valor |
|---|---:|
| Promedio | $6894.45 |
| Mínimo | $1700.00 |
| Máximo | $13100.00 |
| Desviación estándar | $2019.82 |

### Clientes

| Métrica | Valor |
|---|---:|
| Clientes generados promedio | 23.87 |
| Clientes completados promedio | 23.87 |

### Esperas promedio

| Etapa | Valor |
|---|---:|
| Vendedor | 0.09 min |
| Reparación | 0.03 min |
| Cambio de equipo | 0.94 min |

### Utilización promedio

| Recurso | Valor |
|---|---:|
| Vendedores | 14.71% |
| Técnicos | 22.37% |
| Técnico especializado | 8.71% |

### Clientes completados por tipo

| Tipo | Promedio |
|---|---:|
| Tipo 1 | 10.69 |
| Tipo 2 | 6.01 |
| Tipo 3 | 2.36 |
| Tipo 4 | 4.81 |

---

## 15. Análisis de resultados

La ganancia promedio se explica por los clientes completados por tipo y sus precios:

```text
Tipo 2: 6.01 x 350 ≈ 2103.50
Tipo 3: 2.36 x 500 ≈ 1180.00
Tipo 4: 4.81 x 750 ≈ 3607.50

Total aproximado ≈ 6891.00
```

La diferencia con **$6894.45** se debe al redondeo de los promedios presentados.

Los tiempos de espera en segundos son aproximadamente:

```text
Vendedor: 0.09 min ≈ 5.4 segundos
Reparación: 0.03 min ≈ 1.8 segundos
Cambio de equipo: 0.94 min ≈ 56.4 segundos
```

La espera más alta corresponde al cambio de equipo porque solo el técnico especializado puede realizar ese servicio.

La utilización promedio de vendedores fue de **14.71%**. Este valor incorpora tanto la atención inicial de todos los clientes como la segunda fase comercial requerida por los clientes tipo 4. Por tanto, el servicio de venta de equipos reparados aumenta el tiempo de ocupación del vendedor, aunque no cambia el precio del servicio. Aun así, esta utilización no indica saturación. Los técnicos normales presentan la mayor utilización promedio, con **22.37%**, debido a la alta proporción de servicios de reparación.

El técnico especializado mantiene una utilización baja, pero sigue siendo crítico estructuralmente, ya que es el único recurso que puede atender cambios de equipo.

---

## 16. Conclusiones

1. El modelo de eventos discretos representa el flujo operativo del taller Happy Computing durante una jornada laboral.

2. La modelación del servicio tipo 4 en dos fases representa con mayor detalle el proceso real de venta de equipos reparados.

3. La ganancia promedio obtenida fue de **$6894.45** por jornada.

4. El sistema completó en promedio **23.87 clientes** por jornada.

5. Los tiempos promedio de espera fueron bajos en todas las etapas.

6. No se observa saturación bajo la demanda promedio modelada.

7. El técnico especializado sigue siendo el recurso más crítico desde el punto de vista estructural.

8. Para análisis futuros, sería útil estudiar escenarios con mayor tasa de llegada o mayor proporción de cambios de equipo.

---

## 17. Repositorio de GitHub

El proyecto se encuentra en:

```text
https://github.com/hughescard/HappyComputing
```

---

## 18. Anexos

Archivos relevantes:

- `README.md`
- `docs/pseudocodigo_happy_computing.md`
- `docs/resultados_experimentales.md`
- Archivo CSV con resultados experimentales de 1000 réplicas.
- `tests/manual_checks.py`

Comandos de validación usados:

```bash
python3 tests/manual_checks.py
python3 -m src.main --seed 12345
python3 -m src.main --replications 100
```
