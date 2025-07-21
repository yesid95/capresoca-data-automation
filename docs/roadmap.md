# Roadmap del Proyecto

Este documento describe la hoja de ruta para el desarrollo y la evolución del proyecto de automatización de datos de Capresoca. Su objetivo es proporcionar una visión clara de las prioridades y las futuras funcionalidades.

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

### 2.1. Lógica de Negocio (Core / Back-end)

-   [ ] **Prioridad Alta**: Finalizar la refactorización de los notebooks de `Aseguramiento` más críticos a clases y funciones en `src`.
-   [ ] **Prioridad Media**: Integrar un sistema de logging centralizado para registrar eventos y errores en toda la aplicación.
-   [ ] **Prioridad Baja**: Investigar y añadir soporte para nuevas fuentes de datos si es necesario.

### 2.2. Interfaz de Usuario (UI / Front-end)

-   [ ] **Prioridad Media**: Definir la tecnología a utilizar para la GUI (ej. PyQt, Tkinter, CustomTkinter).
-   [ ] **Prioridad Media**: Diseñar los mockups y el flujo de la interfaz de usuario.
    -   Vista para seleccionar y ejecutar una tarea.
    -   Vista para configurar parámetros (rutas de archivos, fechas).
    -   Panel para visualizar logs o estado del proceso.
-   [ ] **Prioridad Baja**: Implementar la primera versión funcional de la GUI.

### 2.3. Automatización y Tareas Programadas

-   [ ] **Prioridad Alta**: Investigar e integrar una librería de scheduling (ej. `schedule`, `APScheduler`).
-   [ ] **Prioridad Media**: Desarrollar la interfaz para que el usuario pueda programar tareas recurrentes (diarias, semanales, mensuales).
-   [ ] **Prioridad Baja**: Implementar el servicio de fondo que gestionará la ejecución de las tareas programadas.

### 2.4. Pruebas y Calidad de Código

-   [ ] **Prioridad Media**: Implementar pruebas unitarias (`unittest` o `pytest`) para las funciones críticas en `src`.
-   [ ] **Prioridad Media**: Configurar un linter (como `flake8` o `pylint`) y un formateador de código (como `black`) para mantener la consistencia.
-   [ ] **Prioridad Baja**: Desarrollar pruebas de integración para los flujos de trabajo completos.
