# Resultados experimentales y análisis

## 1. Configuración experimental

Se ejecutaron 1000 réplicas independientes del simulador Happy Computing con semilla base `12345` y jornada laboral de `480` minutos.

Cada réplica utilizó la semilla:

```text
seed_i = seed_base + i
```

donde `i` es el número de la réplica.

La versión analizada incorpora el refactor del servicio tipo 4, que ahora se procesa en dos fases consecutivas con el mismo vendedor:

1. atención inicial o clasificación;
2. venta del equipo reparado.

---

## 2. Resultados principales

### Ganancia bruta

| Métrica | Valor |
|---|---:|
| Ganancia promedio | $6894.45 |
| Ganancia mínima | $1700.00 |
| Ganancia máxima | $13100.00 |
| Desviación estándar | $2019.82 |

### Clientes

| Métrica | Valor |
|---|---:|
| Clientes generados promedio | 23.87 |
| Clientes completados promedio | 23.87 |

### Tiempos promedio de espera

| Cola / etapa | Tiempo promedio |
|---|---:|
| Vendedor | 0.09 min |
| Reparación | 0.03 min |
| Cambio de equipo | 0.94 min |

### Utilización promedio de recursos

| Recurso | Utilización promedio |
|---|---:|
| Vendedores | 14.71% |
| Técnicos | 22.37% |
| Técnico especializado | 8.71% |

### Clientes completados promedio por tipo de servicio

| Tipo de servicio | Descripción | Promedio |
|---|---|---:|
| Tipo 1 | Reparación por garantía | 10.69 |
| Tipo 2 | Reparación fuera de garantía | 6.01 |
| Tipo 3 | Cambio de equipo | 2.36 |
| Tipo 4 | Venta de equipos reparados | 4.81 |

---

## 3. Análisis de la ganancia

La ganancia bruta promedio obtenida fue de **$6894.45** por jornada.

El aumento respecto a la lógica anterior del tipo 4 se explica porque ahora ese servicio consume dos fases de vendedor, lo cual incrementa la ocupación del recurso vendedor y modifica la dinámica de colas y finalización.

La ganancia esperada por tipo se mantiene:

- Tipo 1: $0
- Tipo 2: $350
- Tipo 3: $500
- Tipo 4: $750

---

## 4. Análisis de clientes atendidos

En promedio se generaron y completaron **23.87 clientes por jornada**.

El sistema sigue terminando todos los clientes generados durante el horizonte laboral simulado, lo que indica capacidad suficiente bajo esta demanda promedio.

---

## 5. Análisis de tiempos de espera

Los tiempos promedio de espera fueron bajos:

- Vendedor: 0.09 minutos
- Reparación: 0.03 minutos
- Cambio de equipo: 0.94 minutos

El refactor del tipo 4 incrementa la carga sobre el vendedor, por eso la utilización del recurso aumenta respecto al modelo previo y la espera promedio del vendedor también sube ligeramente.

---

## 6. Análisis de utilización de recursos

La utilización promedio fue:

- Vendedores: 14.71%
- Técnicos: 22.37%
- Técnico especializado: 8.71%

El vendedor es ahora más demandado porque el tipo 4 utiliza dos fases consecutivas de atención. Aun así, el sistema conserva holgura operativa.

---

## 7. Conclusiones experimentales

1. La ganancia bruta promedio por jornada fue de **$6894.45**.
2. El sistema completó en promedio **23.87 clientes por jornada**.
3. El refactor del tipo 4 incrementó la utilización del vendedor.
4. El técnico especializado continúa siendo el recurso estructural más sensible del sistema.
5. La simulación sigue sin mostrar saturación crítica bajo la demanda promedio modelada.

