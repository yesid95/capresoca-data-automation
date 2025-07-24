
# Roadmap del Proyecto

Este documento describe la hoja de ruta para el desarrollo y la evolución del proyecto de automatización de datos de Capresoca. Su objetivo es proporcionar una visión clara de las prioridades y las futuras funcionalidades.

---


## Índice

- [Roadmap del Proyecto](#roadmap-del-proyecto)
  - [Índice](#índice)
  - [1. Fases de Desarrollo](#1-fases-de-desarrollo)
    - [Fase 1: Consolidación de la Lógica de Negocio (Corto Plazo - En curso)](#fase-1-consolidación-de-la-lógica-de-negocio-corto-plazo---en-curso)
    - [Fase 2: Desarrollo de la Aplicación de Escritorio (Mediano Plazo)](#fase-2-desarrollo-de-la-aplicación-de-escritorio-mediano-plazo)
    - [Fase 3: Implementación de Tareas Programadas y Pruebas (Largo Plazo)](#fase-3-implementación-de-tareas-programadas-y-pruebas-largo-plazo)
  - [2. Desglose de Tareas por Área](#2-desglose-de-tareas-por-área)
    - [2.1. Lógica de Negocio (Core / Back-end) ✅ 0/5 tareas completadas](#21-lógica-de-negocio-core--back-end--05-tareas-completadas)
    - [2.2. Interfaz de Usuario (UI / Front-end) ✅ 0/3 tareas completadas](#22-interfaz-de-usuario-ui--front-end--03-tareas-completadas)
    - [2.3. Automatización y Tareas Programadas ✅ 0/3 tareas completadas](#23-automatización-y-tareas-programadas--03-tareas-completadas)
    - [2.4. Pruebas y Calidad de Código ✅ 0/3 tareas completadas](#24-pruebas-y-calidad-de-código--03-tareas-completadas)

---

## 1. Fases de Desarrollo

El proyecto se desarrollará en fases, desde la consolidación de la lógica de negocio hasta la entrega de una aplicación de escritorio funcional.

### Fase 1: Consolidación de la Lógica de Negocio (Corto Plazo - En curso)

-   **Objetivo**: Refactorizar y estandarizar la lógica de negocio existente en los notebooks para crear una librería de `src` robusta y bien documentada.
-   **Estado**: En progreso.

### Fase 2: Desarrollo de la Aplicación de Escritorio (Mediano Plazo)

-   **Objetivo**: Construir la interfaz de usuario (GUI) y el motor de la aplicación que consumirá la librería de `src`.
-   **Estado**: Pendiente.

### Fase 3: Implementación de Tareas Programadas y Pruebas (Largo Plazo)

-   **Objetivo**: Añadir la funcionalidad de automatización (scheduler) y desarrollar un conjunto completo de pruebas unitarias y de integración.
-   **Estado**: Pendiente.

---

## 2. Desglose de Tareas por Área

A continuación se detallan las tareas específicas, agrupadas por área funcional.



### 2.1. Lógica de Negocio (Core / Back-end) ✅ 0/5 tareas completadas

- [ ] **Prioridad Alta**: Finalizar la refactorización de los notebooks de `Aseguramiento` más críticos a clases y funciones en `src`. <!-- tag:critical -->
  
  - [ ] **Proceso 1: Automatización Validación de Movilidad S1 (descendente a subsidiado)** <!-- tag:critical -->
      - [x] Fase 1: Fundamento del diagrama
          - [x] Definir objetivo del flujo
          - [x] Identificar actores involucrados (EPS, base de datos de relaciones laborales, usuario que ejecuta la revisión, etc.)
          - [x] Establecer el inicio y fin del proceso.
          - [x] Redactar estos puntos en texto para validar que estamos alineados antes de graficar
      - [ ] Fase 2: Mapeo de decisiones principales
          - [ ] Definir nodos tipo (¿Tiene relación laboral activa?, ¿más de una relación abierta?, ¿fecha de retiro?, ¿cotización reciente?)
          - [ ] Asociar cada nodo con una acción automatizable
          - [ ] Ordenar estas decisiones en un flujo lógico
      - [ ] Fase 3: Construcción progresiva del .puml
          - [ ] Crear plantilla base con @startuml y los actores
          - [ ] Agregar cada bloque de decisión usando sintaxis de PlantUML (if, else, endif, etc.)
          - [ ] Comentar cada sección en el .puml para facilitar mantenimiento
      - [ ] Fase 4: Revisión y cierre
          - [ ] Validar visualmente el flujo
          - [ ] Confirmar que no hay ambigüedades o condiciones mal cubiertas
          - [ ] Guardar el .puml en docs/diagramas (o mantenerlo en docs/ si aún hay pocos)
  
  - [ ] **Proceso 2: Validador de inconsistencias entre Sistema EPS y Maestro ADRES** <!-- tag:important -->
    - [ ] Fase 1: Definir tipos de inconsistencias detectables
    - [ ] Fase 2: Diagramar flujo de validación
    - [ ] Fase 3: Prototipo notebook con validaciones
    - [ ] Fase 4: Refactorización como módulo `src/validador`
    - [ ] Fase 5: Exportar reportes de alertas o correcciones sugeridas

  - [ ] **Proceso 3: Generación automática de archivo NS Subsidiado (Resolución 762 de 2023)** <!-- tag:important -->
      - [ ] Fase 1: Entendimiento normativo y estructura del archivo NS
      - [ ] Fase 2: Diseño del flujo de generación automática
      - [ ] Fase 3: Notebook funcional que genera archivo NS
      - [ ] Fase 4: Módulo `src/ns_subsidiado` y validaciones
      - [ ] Fase 5: Preparación para integración en ejecutable

  - [ ] **Proceso 4: Pipeline de ETL de archivos desde FTPs de ADRES a DataWarehouse** <!-- tag:automatizacion -->
      - [ ] Fase 1: Conexión y descarga automatizada desde FTPs
      - [ ] Fase 2: Organización en carpetas de servidor y DWH
      - [ ] Fase 3: Refactorización como módulo `src/etl_adres`
      - [ ] Fase 4: Verificación de integridad de datos descargados
      - [ ] Fase 5: Programación de ejecución automática

- [ ] **Prioridad Media**: Integrar un sistema de logging centralizado para registrar eventos y errores en toda la aplicación. <!-- tag:critical -->
- [ ] **Prioridad Baja**: Investigar y añadir soporte para nuevas fuentes de datos si es necesario.



### 2.2. Interfaz de Usuario (UI / Front-end) ✅ 0/3 tareas completadas

- [ ] **Prioridad Media**: Definir la tecnología a utilizar para la GUI (ej. PyQt, Tkinter, CustomTkinter). <!-- tag:gui -->
- [ ] **Prioridad Media**: Diseñar los mockups y el flujo de la interfaz de usuario. <!-- tag:gui -->
    - Vista para seleccionar y ejecutar una tarea. <!-- tag:gui -->
    - Vista para configurar parámetros (rutas de archivos, fechas). <!-- tag:gui -->
    - Panel para visualizar logs o estado del proceso. <!-- tag:gui -->
- [ ] **Prioridad Baja**: Implementar la primera versión funcional de la GUI. <!-- tag:gui -->



### 2.3. Automatización y Tareas Programadas ✅ 0/3 tareas completadas

- [ ] **Prioridad Alta**: Investigar e integrar una librería de scheduling (ej. `schedule`, `APScheduler`). <!-- tag:critical --><!-- tag:automatizacion -->
- [ ] **Prioridad Media**: Desarrollar la interfaz para que el usuario pueda programar tareas recurrentes (diarias, semanales, mensuales). <!-- tag:automatizacion -->
- [ ] **Prioridad Baja**: Implementar el servicio de fondo que gestionará la ejecución de las tareas programadas. <!-- tag:automatizacion -->



### 2.4. Pruebas y Calidad de Código ✅ 0/3 tareas completadas

- [ ] **Prioridad Media**: Implementar pruebas unitarias (`unittest` o `pytest`) para las funciones críticas en `src`. <!-- tag:critical -->
- [ ] **Prioridad Media**: Configurar un linter (como `flake8` o `pylint`) y un formateador de código (como `black`) para mantener la consistencia. <!-- tag:critical -->
- [ ] **Prioridad Baja**: Desarrollar pruebas de integración para los flujos de trabajo completos.
