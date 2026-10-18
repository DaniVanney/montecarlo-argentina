# Decisiones del proyecto

Este archivo resume las decisiones vigentes y los puntos pendientes.
La referencia completa es el documento Bases_del_proyecto_Monte_Carlo_v1_0.docx,
versión 1.0, del 16 de octubre de 2026.

## Decisiones aprobadas

### Alcance

- El proyecto tiene fines de investigación, aprendizaje y portfolio.
- La primera etapa incluye todas las acciones de los paneles Líder y General,
  distinguiendo sus clases.
- CEDEAR se incorporará después de completar y validar la etapa de acciones.
- No se ejecutarán operaciones reales ni se ofrecerá asesoramiento personalizado.
- No se utilizarán suscripciones ni servicios pagos.

### Datos y herramientas

- El desarrollo se realizará en Python y los informes se prepararán en Power BI.
- La fuente inicial de datos será yfinance.
- El objetivo será el precio nominal de cierre en pesos argentinos.
- Los datos serán diarios y se utilizarán después de confirmar el cierre.
- Cada origen de pronóstico utilizará como máximo los últimos doce meses.
- Se exigirán al menos 140 ruedas válidas conocidas en ese momento.
- Los dividendos y desdoblamientos deberán tratarse sin duplicar ajustes.
- Las empresas sin datos suficientes permanecerán en el catálogo.

### Simulación y evaluación

- Monte Carlo será el método de simulación.
- Los horizontes serán de una a diez ruedas futuras.
- La separación inicial será cronológica: 70 % para entrenamiento y 30 % para prueba.
- Se necesitarán al menos 200 observaciones para obtener inicialmente
  140 en entrenamiento. Esto no garantiza suficientes ejemplos para cualquier modelo.
- La selección del procedimiento se realizará dentro del entrenamiento.
- La información futura no podrá utilizarse para construir ni elegir el pronóstico.
- La referencia obligatoria será mantener el último cierre observado.
- Cada pronóstico se evaluará cuando esté disponible su cierre objetivo.

### Registro e informes

- Los pronósticos originales se conservarán; las correcciones quedarán registradas.
- La generación y la evaluación serán diarias.
- El informe se actualizará semanalmente y mostrará las fechas correspondientes.
- Cuando no corresponda emitir un pronóstico, se mostrará
  “Estimación no disponible” junto con el motivo.
- La primera versión no incluirá comisiones ni rentabilidad neta de impuestos.

## Objetivo provisional

Evaluar si al menos el 90 % de los pronósticos publicados y maduros,
a diez ruedas, tiene un error porcentual absoluto no superior al 5 %.

Este objetivo no representa una precisión demostrada ni una garantía.
El porcentaje de error se calcula respecto del precio observado.

## Decisiones pendientes

- P01: elegir los modelos de rendimientos, volatilidad e innovaciones,
  sus parámetros y el tratamiento matemático de los eventos.
- P02: definir la frecuencia y la política de reentrenamiento.
- P03: definir la estimación puntual, los intervalos y los eventos
  cuyas probabilidades se informarán.
- P04: definir la evidencia mínima, cómo medir la incertidumbre
  y las reglas para habilitar o suspender estimaciones.

También deben concretarse el calendario, los criterios de liquidez,
la cantidad de simulaciones, las semillas, las tolerancias y los detalles
de ejecución y almacenamiento. No tienen valores aprobados por omisión.

## Control de cambios

Las propuestas pendientes no se implementarán como decisiones aprobadas.
Cada resolución deberá registrarse y reflejarse en una actualización
de la especificación, conservando la versión anterior.