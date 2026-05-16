# Informe de simulación Happy Computing

## 1. Descripción del modelo

Happy Computing es un taller de reparaciones electrónicas modelado como una simulación basada en eventos discretos.

El sistema considera:

- 2 vendedores.
- 3 técnicos.
- 1 técnico especializado.

Los clientes pueden solicitar:

1. Reparación por garantía.
2. Reparación fuera de garantía.
3. Cambio de equipo.
4. Venta de equipos reparados.

### Refactor del tipo 4

En la versión actual del modelo, el tipo 4 se atiende en dos fases consecutivas con el mismo vendedor:

1. recepción o clasificación;
2. venta del equipo reparado.

El vendedor no se libera entre ambas fases.

---

## 2. Supuestos principales

- La jornada laboral dura 480 minutos.
- Las llegadas de clientes solo se generan dentro de la jornada.
- Los clientes que llegan antes del cierre pueden terminar después del minuto 480.
- La atención del vendedor sigue una distribución normal truncada `N(5, 2)`.
- Los tiempos de reparación siguen una exponencial con media 20 minutos.
- Los tiempos de cambio de equipo siguen una exponencial con media 15 minutos.

---

## 3. Resultados experimentales

Se ejecutaron 1000 réplicas independientes con semilla base `12345`.

### Resumen

| Métrica | Valor |
|---|---:|
| Ganancia promedio | $6894.45 |
| Ganancia mínima | $1700.00 |
| Ganancia máxima | $13100.00 |
| Desviación estándar | $2019.82 |
| Clientes generados promedio | 23.87 |
| Clientes completados promedio | 23.87 |
| Espera promedio en vendedor | 0.09 min |
| Espera promedio en reparación | 0.03 min |
| Espera promedio en cambio | 0.94 min |
| Utilización promedio de vendedores | 14.71% |
| Utilización promedio de técnicos | 22.37% |
| Utilización promedio del técnico especializado | 8.71% |

### Clientes completados promedio por tipo

| Tipo | Promedio |
|---|---:|
| Tipo 1 | 10.69 |
| Tipo 2 | 6.01 |
| Tipo 3 | 2.36 |
| Tipo 4 | 4.81 |

---

## 4. Conclusiones

La configuración de personal sigue siendo suficiente para la demanda promedio simulada.

El refactor del tipo 4 incrementa la ocupación de los vendedores y hace más realista el flujo de ventas, pero no genera saturación crítica en el escenario experimental evaluado.

