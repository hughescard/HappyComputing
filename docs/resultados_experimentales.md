# Resultados experimentales y análisis

## 1. Configuración experimental

Se ejecutaron 1000 réplicas independientes del simulador Happy Computing con semilla base `12345` y jornada laboral de `480` minutos.

Los resultados se generaron usando la implementación manual de variables aleatorias del proyecto. Los uniformes base fueron producidos mediante un generador congruencial lineal propio, y las distribuciones exponencial y normal fueron construidas mediante transformada inversa y Box-Muller, respectivamente.

Cada réplica utilizó una semilla distinta según la regla:

```text
seed_i = seed_base + i
```

donde `i` representa el número de la réplica. Esta estrategia permite reproducibilidad y, al mismo tiempo, evita repetir la misma trayectoria aleatoria en cada corrida.

El modelo considera que el servicio tipo 4, venta de equipos reparados, requiere dos fases consecutivas con el mismo vendedor:

1. atención inicial o clasificación;
2. venta del equipo reparado.

El vendedor no se libera entre ambas fases. Esto aumenta la ocupación del recurso vendedor y puede modificar las esperas, aunque los precios de los servicios se mantienen iguales.

---

## 2. Resultados principales

### Ganancia bruta

| Métrica | Valor |
|---|---:|
| Ganancia promedio | $6417.00 |
| Ganancia mínima | $1550.00 |
| Ganancia máxima | $13200.00 |
| Desviación estándar | $1856.18 |

### Clientes

| Métrica | Valor |
|---|---:|
| Clientes generados promedio | 22.61 |
| Clientes completados promedio | 22.61 |

### Tiempos promedio de espera

| Cola / etapa | Tiempo promedio |
|---|---:|
| Vendedor | 0.09 min |
| Reparación | 0.05 min |
| Cambio de equipo | 1.11 min |

### Utilización promedio de recursos

| Recurso | Utilización promedio |
|---|---:|
| Vendedores | 13.94% |
| Técnicos | 21.21% |
| Técnico especializado | 8.64% |

### Clientes completados promedio por tipo de servicio

| Tipo de servicio | Descripción | Promedio |
|---|---|---:|
| Tipo 1 | Reparación por garantía | 10.29 |
| Tipo 2 | Reparación fuera de garantía | 5.64 |
| Tipo 3 | Cambio de equipo | 2.26 |
| Tipo 4 | Venta de equipos reparados | 4.42 |

---

## 3. Coherencia de la ganancia

La ganancia bruta promedio obtenida fue de **$6417.00** por jornada simulada.

La ganancia se determina únicamente por la cantidad de clientes completados por tipo de servicio y por los precios definidos para cada tipo. La segunda fase del tipo 4 afecta la utilización del vendedor y la dinámica de esperas, pero no modifica el ingreso unitario de la venta de equipos reparados.

Una verificación aproximada usando los promedios por tipo es:

```text
Tipo 2: 5.64 x 350 ≈ 1974.00
Tipo 3: 2.26 x 500 ≈ 1130.00
Tipo 4: 4.42 x 750 ≈ 3315.00

Total aproximado ≈ 6419.00
```

La diferencia respecto al valor exacto de **$6417.00** se explica por el redondeo de los promedios presentados en la tabla. Las reparaciones por garantía no aportan ingreso directo porque su precio es $0.

Los resultados obtenidos dependen de la variabilidad aleatoria propia del sistema y de la dinámica del calendario de eventos.

---

## 4. Análisis de clientes atendidos

En promedio se generaron **22.61 clientes** por jornada y se completaron también **22.61 clientes**.

Este resultado indica que, bajo la demanda modelada, el sistema logra completar todos los clientes que llegan antes del cierre de la jornada. Aunque algunos servicios pueden finalizar después del minuto 480, la simulación continúa hasta vaciar el calendario de eventos pendientes.

---

## 5. Análisis de tiempos de espera

Los tiempos promedio de espera son bajos:

```text
Vendedor: 0.09 min
Reparación: 0.05 min
Cambio de equipo: 1.11 min
```

Convertidos a segundos:

```text
Vendedor: 0.09 min ≈ 5.4 segundos
Reparación: 0.05 min ≈ 3.0 segundos
Cambio de equipo: 1.11 min ≈ 66.6 segundos
```

La espera más alta corresponde al cambio de equipo. Esto es coherente con el modelo, porque solo el técnico especializado puede atender ese servicio.

La espera del vendedor se mantiene baja aun cuando los clientes tipo 4 ocupan al vendedor durante una segunda fase de venta. El valor promedio no muestra congestión significativa.

---

## 6. Análisis de utilización de recursos

La utilización promedio fue:

```text
Vendedores: 13.94%
Técnicos: 21.21%
Técnico especializado: 8.64%
```

La utilización promedio de vendedores fue de 13.94%. Este valor incorpora tanto la atención inicial de todos los clientes como la segunda fase comercial requerida por los clientes tipo 4. Por tanto, el servicio de venta de equipos reparados aumenta el tiempo de ocupación del vendedor, aunque no cambia el precio del servicio.

Los técnicos normales presentan la mayor utilización promedio, lo cual es consistente con la alta proporción de clientes tipo 1 y tipo 2.

El técnico especializado mantiene una utilización promedio baja, pero sigue siendo un recurso crítico desde el punto de vista estructural porque es el único que puede atender cambios de equipo. Si la proporción de clientes tipo 3 aumentara, este recurso podría convertirse en cuello de botella.

---

## 7. Interpretación general

Con el modelo final del servicio tipo 4, no se observa saturación del sistema. Las esperas promedio son bajas y todos los clientes generados se completan dentro de la simulación.

La configuración actual de recursos parece suficiente para la tasa promedio de llegada utilizada en el modelo. Sin embargo, el análisis también muestra que los vendedores pasan a tener un papel más relevante al modelar la venta de equipos reparados como una segunda fase real de atención.

---

## 8. Conclusiones experimentales

1. La ganancia bruta promedio por jornada fue de **$6417.00**.

2. El sistema generó y completó en promedio **22.61 clientes por jornada**.

3. La segunda fase del servicio tipo 4 forma parte de la utilización promedio de vendedores, que fue de **13.94%**.

4. La espera promedio del vendedor fue de **0.09 minutos**, equivalente a aproximadamente **5.4 segundos**.

5. La mayor espera promedio se observó en cambio de equipo, con **1.11 minutos**.

6. No se observa saturación bajo la demanda promedio modelada.

7. El técnico especializado sigue siendo crítico porque es el único recurso capaz de atender cambios de equipo.
