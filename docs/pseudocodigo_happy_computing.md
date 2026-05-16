# Pseudocódigo del simulador Happy Computing

Este documento define el pseudocódigo formal para la simulación basada en eventos discretos del problema **Happy Computing**.

El objetivo del simulador es estimar la ganancia bruta generada durante una jornada laboral, considerando llegadas aleatorias de clientes, tipos de servicios, recursos limitados, colas y reglas de prioridad para el técnico especializado.

> Nota: Las operaciones auxiliares sobre estructuras de datos, como insertar eventos en el calendario, extraer el próximo evento, encolar y desencolar clientes, se consideran operaciones básicas de implementación y no se detallan individualmente en este pseudocódigo. El pseudocódigo se enfoca en la lógica del modelo de simulación.

---

## 1. Constantes del modelo

```pseudocode
JORNADA ← 480

NUM_VENDEDORES ← 2
NUM_TECNICOS ← 3
NUM_TECNICOS_ESPECIALIZADOS ← 1

PRECIO_TIPO_1 ← 0
PRECIO_TIPO_2 ← 350
PRECIO_TIPO_3 ← 500
PRECIO_TIPO_4 ← 750
```

---

## 2. Tipos de eventos

```pseudocode
EVENTO_LLEGADA_CLIENTE
EVENTO_FIN_ATENCION_VENDEDOR
EVENTO_FIN_VENTA_EQUIPO_REPARADO
EVENTO_FIN_REPARACION
EVENTO_FIN_CAMBIO_EQUIPO
```

---

## 3. Algoritmo principal

```pseudocode
ALGORITMO SimularJornada(seed)

    InicializarGeneradorAleatorio(seed)

    reloj ← 0
    calendario ← ColaPrioridadVacía()

    cola_vendedores ← ColaVacía()
    cola_reparaciones ← ColaVacía()
    cola_cambios ← ColaVacía()

    vendedores_libres ← NUM_VENDEDORES
    tecnicos_libres ← NUM_TECNICOS
    tecnico_especializado_libre ← VERDADERO

    ganancia_total ← 0
    clientes_generados ← 0
    clientes_completados ← 0

    estadisticas ← InicializarEstadisticas()

    tiempo_primera_llegada ← GenerarTiempoEntreLlegadas()

    SI tiempo_primera_llegada ≤ JORNADA ENTONCES
        InsertarEvento(
            calendario,
            EVENTO_LLEGADA_CLIENTE,
            tiempo_primera_llegada,
            cliente = NULO,
            recurso = NULO
        )
    FIN SI

    MIENTRAS calendario NO esté vacío HACER

        evento ← ExtraerProximoEvento(calendario)
        reloj ← evento.tiempo

        SEGÚN evento.tipo HACER

            CASO EVENTO_LLEGADA_CLIENTE:
                ProcesarLlegadaCliente(evento)

            CASO EVENTO_FIN_ATENCION_VENDEDOR:
                ProcesarFinAtencionVendedor(evento)

            CASO EVENTO_FIN_VENTA_EQUIPO_REPARADO:
                ProcesarFinVentaEquipoReparado(evento)

            CASO EVENTO_FIN_REPARACION:
                ProcesarFinReparacion(evento)

            CASO EVENTO_FIN_CAMBIO_EQUIPO:
                ProcesarFinCambioEquipo(evento)

        FIN SEGÚN

    FIN MIENTRAS

    resultados ← CalcularMetricasFinales(estadisticas)

    RETORNAR resultados

FIN ALGORITMO
```

---

## 4. Procesar llegada de cliente

```pseudocode
PROCEDIMIENTO ProcesarLlegadaCliente(evento)

    cliente ← CrearCliente()
    cliente.id ← clientes_generados + 1
    cliente.tiempo_llegada ← reloj
    cliente.tipo_servicio ← GenerarTipoServicio()

    clientes_generados ← clientes_generados + 1

    SI vendedores_libres > 0 ENTONCES

        vendedores_libres ← vendedores_libres - 1

        cliente.inicio_atencion_vendedor ← reloj
        cliente.espera_vendedor ← reloj - cliente.tiempo_llegada

        tiempo_atencion ← GenerarTiempoAtencionVendedor()

        InsertarEvento(
            calendario,
            EVENTO_FIN_ATENCION_VENDEDOR,
            reloj + tiempo_atencion,
            cliente,
            recurso = "VENDEDOR"
        )

    SINO

        Encolar(cola_vendedores, cliente)

    FIN SI

    proxima_llegada ← reloj + GenerarTiempoEntreLlegadas()

    SI proxima_llegada ≤ JORNADA ENTONCES

        InsertarEvento(
            calendario,
            EVENTO_LLEGADA_CLIENTE,
            proxima_llegada,
            cliente = NULO,
            recurso = NULO
        )

    FIN SI

FIN PROCEDIMIENTO
```

---

## 5. Procesar fin de atención del vendedor

```pseudocode
PROCEDIMIENTO ProcesarFinAtencionVendedor(evento)

    cliente ← evento.cliente

    cliente.fin_atencion_vendedor ← reloj

    SI cliente.tipo_servicio = 4 ENTONCES

        cliente.inicio_venta_vendedor ← reloj

        El vendedor permanece ocupado durante la fase de venta.

        tiempo_venta ← GenerarTiempoAtencionVendedor()

        InsertarEvento(
            calendario,
            EVENTO_FIN_VENTA_EQUIPO_REPARADO,
            reloj + tiempo_venta,
            cliente,
            recurso = "VENDEDOR"
        )

        RETORNAR

    FIN SI

    vendedores_libres ← vendedores_libres + 1

    SI cliente.tipo_servicio = 1 O cliente.tipo_servicio = 2 ENTONCES

        cliente.inicio_espera_tecnica ← reloj
        Encolar(cola_reparaciones, cliente)
        IntentarAsignarReparacion()

    SINO SI cliente.tipo_servicio = 3 ENTONCES

        cliente.inicio_espera_tecnica ← reloj
        Encolar(cola_cambios, cliente)
        IntentarAsignarTecnicoEspecializado()

    FIN SI

    IntentarAsignarVendedor()

FIN PROCEDIMIENTO
```

---

## 6. Procesar fin de venta de equipo reparado

```pseudocode
PROCEDIMIENTO ProcesarFinVentaEquipoReparado(evento)

    cliente ← evento.cliente

    vendedores_libres ← vendedores_libres + 1

    cliente.fin_venta_vendedor ← reloj

    ganancia_total ← ganancia_total + PRECIO_TIPO_4
    clientes_completados ← clientes_completados + 1

    RegistrarClienteCompletado(cliente)

    IntentarAsignarVendedor()

FIN PROCEDIMIENTO
```

---

## 7. Procesar fin de reparación

```pseudocode
PROCEDIMIENTO ProcesarFinReparacion(evento)

    cliente ← evento.cliente
    recurso ← evento.recurso

    cliente.fin_atencion_tecnica ← reloj

    SI recurso = "TECNICO" ENTONCES
        tecnicos_libres ← tecnicos_libres + 1
    SINO SI recurso = "TECNICO_ESPECIALIZADO" ENTONCES
        tecnico_especializado_libre ← VERDADERO
    FIN SI

    SI cliente.tipo_servicio = 1 ENTONCES
        ganancia_total ← ganancia_total + PRECIO_TIPO_1
    SINO SI cliente.tipo_servicio = 2 ENTONCES
        ganancia_total ← ganancia_total + PRECIO_TIPO_2
    FIN SI

    clientes_completados ← clientes_completados + 1
    RegistrarClienteCompletado(cliente)

    SI recurso = "TECNICO" ENTONCES
        IntentarAsignarReparacion()
    SINO SI recurso = "TECNICO_ESPECIALIZADO" ENTONCES
        IntentarAsignarTecnicoEspecializado()
    FIN SI

FIN PROCEDIMIENTO
```

---

## 8. Procesar fin de cambio de equipo

```pseudocode
PROCEDIMIENTO ProcesarFinCambioEquipo(evento)

    cliente ← evento.cliente

    tecnico_especializado_libre ← VERDADERO

    cliente.fin_atencion_tecnica ← reloj

    ganancia_total ← ganancia_total + PRECIO_TIPO_3
    clientes_completados ← clientes_completados + 1

    RegistrarClienteCompletado(cliente)

    IntentarAsignarTecnicoEspecializado()

FIN PROCEDIMIENTO
```

---

## 9. Intentar asignar vendedor

```pseudocode
PROCEDIMIENTO IntentarAsignarVendedor()

    MIENTRAS vendedores_libres > 0 Y cola_vendedores NO esté vacía HACER

        cliente ← Desencolar(cola_vendedores)

        vendedores_libres ← vendedores_libres - 1

        cliente.inicio_atencion_vendedor ← reloj
        cliente.espera_vendedor ← reloj - cliente.tiempo_llegada

        tiempo_atencion ← GenerarTiempoAtencionVendedor()

        InsertarEvento(
            calendario,
            EVENTO_FIN_ATENCION_VENDEDOR,
            reloj + tiempo_atencion,
            cliente,
            recurso = "VENDEDOR"
        )

    FIN MIENTRAS

FIN PROCEDIMIENTO
```

---

## 10. Intentar asignar reparación

```pseudocode
PROCEDIMIENTO IntentarAsignarReparacion()

    MIENTRAS cola_reparaciones NO esté vacía Y tecnicos_libres > 0 HACER

        cliente ← Desencolar(cola_reparaciones)

        tecnicos_libres ← tecnicos_libres - 1

        cliente.inicio_atencion_tecnica ← reloj
        cliente.espera_tecnica ← reloj - cliente.inicio_espera_tecnica

        tiempo_reparacion ← GenerarTiempoReparacion()

        InsertarEvento(
            calendario,
            EVENTO_FIN_REPARACION,
            reloj + tiempo_reparacion,
            cliente,
            recurso = "TECNICO"
        )

    FIN MIENTRAS

    SI cola_reparaciones NO esté vacía Y
       tecnico_especializado_libre = VERDADERO Y
       cola_cambios está vacía ENTONCES

        cliente ← Desencolar(cola_reparaciones)

        tecnico_especializado_libre ← FALSO

        cliente.inicio_atencion_tecnica ← reloj
        cliente.espera_tecnica ← reloj - cliente.inicio_espera_tecnica

        tiempo_reparacion ← GenerarTiempoReparacion()

        InsertarEvento(
            calendario,
            EVENTO_FIN_REPARACION,
            reloj + tiempo_reparacion,
            cliente,
            recurso = "TECNICO_ESPECIALIZADO"
        )

    FIN SI

FIN PROCEDIMIENTO
```

---

## 11. Intentar asignar técnico especializado

```pseudocode
PROCEDIMIENTO IntentarAsignarTecnicoEspecializado()

    SI tecnico_especializado_libre = FALSO ENTONCES
        RETORNAR
    FIN SI

    SI cola_cambios NO esté vacía ENTONCES

        cliente ← Desencolar(cola_cambios)

        tecnico_especializado_libre ← FALSO

        cliente.inicio_atencion_tecnica ← reloj
        cliente.espera_tecnica ← reloj - cliente.inicio_espera_tecnica

        tiempo_cambio ← GenerarTiempoCambioEquipo()

        InsertarEvento(
            calendario,
            EVENTO_FIN_CAMBIO_EQUIPO,
            reloj + tiempo_cambio,
            cliente,
            recurso = "TECNICO_ESPECIALIZADO"
        )

    SINO SI cola_reparaciones NO esté vacía ENTONCES

        cliente ← Desencolar(cola_reparaciones)

        tecnico_especializado_libre ← FALSO

        cliente.inicio_atencion_tecnica ← reloj
        cliente.espera_tecnica ← reloj - cliente.inicio_espera_tecnica

        tiempo_reparacion ← GenerarTiempoReparacion()

        InsertarEvento(
            calendario,
            EVENTO_FIN_REPARACION,
            reloj + tiempo_reparacion,
            cliente,
            recurso = "TECNICO_ESPECIALIZADO"
        )

    FIN SI

FIN PROCEDIMIENTO
```

---

## 12. Generar uniforme base

La generación aleatoria parte de un generador congruencial lineal propio. No se depende de funciones externas de distribución.

```pseudocode
CONSTANTE a ← 16807
CONSTANTE m ← 2147483647

FUNCIÓN GenerarUniforme()

    estado ← (a * estado) MOD m
    RETORNAR estado / m

FIN FUNCIÓN
```

---

## 13. Generar variable exponencial

La distribución exponencial se obtiene mediante transformada inversa.

```pseudocode
FUNCIÓN GenerarExponencial(media)

    u ← GenerarUniforme()
    RETORNAR -media * ln(u)

FIN FUNCIÓN
```

---

## 14. Generar variable normal

La distribución normal se obtiene mediante el método de Box-Muller.

```pseudocode
FUNCIÓN GenerarNormal(media, desviacion)

    u1 ← GenerarUniforme()
    u2 ← GenerarUniforme()

    z ← sqrt(-2 * ln(u1)) * cos(2 * pi * u2)

    RETORNAR media + desviacion * z

FIN FUNCIÓN
```

---

## 15. Generar tipo de servicio

```pseudocode
FUNCIÓN GenerarTipoServicio()

    u ← GenerarUniforme()

    SI u < 0.45 ENTONCES
        RETORNAR 1
    SINO SI u < 0.70 ENTONCES
        RETORNAR 2
    SINO SI u < 0.80 ENTONCES
        RETORNAR 3
    SINO
        RETORNAR 4
    FIN SI

FIN FUNCIÓN
```

---

## 16. Generar tiempo de atención del vendedor

```pseudocode
FUNCIÓN GenerarTiempoAtencionVendedor()

    REPETIR
        tiempo ← GenerarNormal(media = 5, desviacion = 2)
    HASTA QUE tiempo > 0

    RETORNAR tiempo

FIN FUNCIÓN
```

---

## 17. Generar tiempo entre llegadas

```pseudocode
FUNCIÓN GenerarTiempoEntreLlegadas()

    RETORNAR GenerarExponencial(media = 20)

FIN FUNCIÓN
```

---

## 18. Generar tiempo de reparación

```pseudocode
FUNCIÓN GenerarTiempoReparacion()

    RETORNAR GenerarExponencial(media = 20)

FIN FUNCIÓN
```

---

## 19. Generar tiempo de cambio de equipo

```pseudocode
FUNCIÓN GenerarTiempoCambioEquipo()

    RETORNAR GenerarExponencial(media = 15)

FIN FUNCIÓN
```

---

## 20. Registrar cliente completado

```pseudocode
PROCEDIMIENTO RegistrarClienteCompletado(cliente)

    cliente.tiempo_salida ← reloj
    cliente.tiempo_total_sistema ← cliente.tiempo_salida - cliente.tiempo_llegada

    ActualizarContadoresPorTipo(cliente.tipo_servicio)
    ActualizarTiemposDeEspera(cliente)
    ActualizarEstadisticasGenerales(cliente)

FIN PROCEDIMIENTO
```

---

## 21. Cálculo de métricas finales

```pseudocode
FUNCIÓN CalcularMetricasFinales(estadisticas)

    resultados.ganancia_total ← ganancia_total
    resultados.clientes_generados ← clientes_generados
    resultados.clientes_completados ← clientes_completados

    resultados.tiempo_promedio_espera_vendedor ←
        total_espera_vendedor / clientes_que_pasaron_por_vendedor

    resultados.tiempo_promedio_espera_reparacion ←
        total_espera_reparacion / clientes_que_requirieron_reparacion

    resultados.tiempo_promedio_espera_cambio ←
        total_espera_cambio / clientes_que_requirieron_cambio

    resultados.utilizacion_vendedores ←
        tiempo_ocupado_vendedores / (NUM_VENDEDORES * reloj)

    resultados.utilizacion_tecnicos ←
        tiempo_ocupado_tecnicos / (NUM_TECNICOS * reloj)

    resultados.utilizacion_tecnico_especializado ←
        tiempo_ocupado_tecnico_especializado / reloj

    RETORNAR resultados

FIN FUNCIÓN
```

---

## 22. Observaciones para la implementación

1. El calendario de eventos debe implementarse como una cola de prioridad ordenada por tiempo.
2. Las colas de clientes pueden implementarse como colas FIFO.
3. Los eventos de inicio de atención no necesitan estar en el calendario si ocurren inmediatamente dentro de otro evento.
4. El técnico especializado debe priorizar siempre la cola de cambios de equipo.
5. La ganancia se registra únicamente cuando el cliente termina completamente su servicio.
6. Las llegadas de nuevos clientes solo se programan si ocurren dentro de la jornada laboral.
7. El sistema puede seguir procesando eventos después del minuto 480 para terminar clientes que llegaron antes del cierre.
