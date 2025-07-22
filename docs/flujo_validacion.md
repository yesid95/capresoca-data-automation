# Documentación de Flujos de Validación

Este documento centraliza la lógica, nodos de decisión y acciones automatizables de los procesos de validación desarrollados en el proyecto. Cada sección corresponde a un proceso específico (ej. Movilidad S1, novedades NS, otros futuros), permitiendo mantener la trazabilidad y facilitar la evolución del sistema.

---

## Índice

- [Documentación de Flujos de Validación](#documentación-de-flujos-de-validación)
  - [Índice](#índice)
  - [Movilidad S1 (descendente a subsidiado)](#movilidad-s1-descendente-a-subsidiado)
    - [Descripción general](#descripción-general)
    - [Nodos de decisión principales](#nodos-de-decisión-principales)
    - [Acciones automatizables](#acciones-automatizables)
    - [Nodos de decisión principales](#nodos-de-decisión-principales-1)
  - [Otros procesos de validación](#otros-procesos-de-validación)

---

## Movilidad S1 (descendente a subsidiado)

### Descripción general
Automatización del reporte de movilidad S1 descendente al régimen subsidiado, siguiendo la normativa y calendario ADRES.

### Nodos de decisión principales
- ¿Tiene relación laboral activa?
- ¿Más de una relación abierta?
- ¿Fecha de retiro?
- ¿Cotización reciente?
- ¿Continuidad laboral?
- ¿Debe compensar días o volver a subir al contributivo?

### Acciones automatizables
- Clasificar afiliados según criterios de movilidad.
- Generar archivo Excel con categorización.
- Registrar trazabilidad de decisiones y fuentes de datos.

### Nodos de decisión principales

| ID  | Pregunta / Validación                           | Fuente de datos principal           | Tipo de respuesta | Acción asociada                         |
|-----|--------------------------------------------------|-------------------------------------|-------------------|------------------------------------------|
| N1  | ¿Tiene relación laboral activa?                 | SAT / R1 / NC / Expediente          | Sí / No           | Continuar o pasar a validación de pagos  |
| N2  | ¿Más de una relación abierta?                   | SAT / Expediente                    | Sí / No           | Evaluar continuidad o conflicto          |
| N3  | ¿Tiene cotización reciente?                     | PILA EPS / PILA 3047                | Sí / No           | Clasificar en mora o activo              |
| N4  | ¿Continuidad laboral entre relaciones?          | SAT / Expediente                    | Sí / No           | Evitar movilidad o reportar transición   |
| N5  | ¿Debe compensar días o volver a contributivo?   | SAT / ABX / ACX                     | Sí / No           | Reporte parcial o retorno                |

> Nota: Este flujo lógico será representado gráficamente en el diagrama `movilidad_s1.puml` ubicado en `docs/diagrams/workflow/`.

---

## Otros procesos de validación

*Esta sección se irá completando a medida que se desarrollen nuevos procesos.*

---
