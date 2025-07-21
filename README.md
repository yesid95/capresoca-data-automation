# Capresoca Data Automation

## 1. Descripción General

Este repositorio está destinado a la construcción de una aplicación para el **área de Aseguramiento de Capresoca EPS**. Su finalidad es automatizar tareas críticas del negocio, algunas de forma periódica y programada, y otras bajo demanda del usuario. El objetivo final es consolidar los prototipos actuales en una aplicación de escritorio robusta y ejecutable.

El público objetivo de este proyecto incluye ingenieros de datos, auditores y futuros colaboradores técnicos que necesiten comprender, utilizar o extender las funcionalidades existentes.

---

## 2. Estado del Proyecto

El proyecto se encuentra en una **fase de desarrollo activo**. Los componentes actuales están siendo migrados de notebooks exploratorios a módulos de código reutilizables.

- **Módulos Principales (`/src`)**:
  - `file_loader.py`: **(Estable)** Componente para la carga estandarizada de diversos tipos de archivos (CSV, TXT, Excel).
  - `data_cleaning.py`: **(Estable)** Funciones para la limpieza, validación y transformación de datos según las reglas de negocio.
  - `main.py`: **(Experimental)** Punto de entrada para futuras ejecuciones automatizadas.

- **Notebooks (`/notebooks`)**:
  - **(Prototipos funcionales)** Sirven como borradores y campo de pruebas para desarrollar y validar la lógica de negocio. Se dividen en:
    - `Aseguramiento`: Flujos de trabajo complejos (cruces, indicadores, reportes).
    - `Generales`: Utilidades para tareas auxiliares (manejo de PDFs, correos).

---

## 3. Requisitos del Entorno

- **Python**: `3.8` o superior.
- **Librerías Clave**: `pandas`, `numpy`, `openpyxl`, `sqlalchemy`.
- Para una lista completa de dependencias, consulta el archivo `requirements.txt`.

Para configurar el entorno, sigue estos pasos:

```powershell
# 1. Clona el repositorio
git clone https://github.com/yesid95/capresoca-data-automation.git
cd capresoca-data-automation

# 2. Crea y activa un entorno virtual
python -m venv venv
.\venv\Scripts\Activate

# 3. Instala las dependencias
pip install -r requirements.txt
```

---

## 4. Guía de Uso Básico

Actualmente, la funcionalidad del proyecto se ejecuta a través de los Jupyter Notebooks. Estos actúan como un **entorno de desarrollo controlado** que permite construir, validar y refinar la lógica de negocio antes de su integración final. Permiten entender los resultados a largo plazo y ajustar los procesos de forma iterativa.

- **Ejemplos de procesos complejos**: Reportes para ADRES según la normativa vigente (Resolución 762 de 2023).
- **Ejemplos de manejo de históricos**: El notebook `Unificar_Archivos.ipynb` consolida grandes volúmenes de datos en datasets únicos, facilitando análisis futuros o la alimentación de dashboards.

1.  **Inicia Jupyter Lab o VS Code** en el directorio raíz del proyecto.
2.  **Navega a la carpeta `/notebooks`** y abre el notebook correspondiente a la tarea que deseas realizar.
3.  **Ejemplo**: Para ejecutar el proceso de validación de archivos del Sistema de Información de Entidades (SIE), abre y ejecuta las celdas de `notebooks/Aseguramiento/Validar SIE.ipynb`.

**Nota**: Asegúrate de configurar las rutas de entrada y salida de archivos dentro de cada notebook según tu entorno local.

---

## 5. Futuras Funcionalidades

La visión a largo plazo es consolidar la lógica de negocio en una aplicación de escritorio para Windows que permita:

- **Tareas Programadas**: Ejecutar procesos de validación y reportería de forma automática (diaria, semanal, mensual).
- **Automatización por Demanda**: Permitir a los usuarios iniciar flujos de trabajo específicos a través de una interfaz gráfica sencilla.
- **Expansión de Módulos**: Fortalecer la biblioteca `src` con más componentes reutilizables y pruebas unitarias.

---

## 6. Contribuciones

Las contribuciones son bienvenidas. Para proponer mejoras, sigue estos lineamientos:

- **Estructura Modular**: Si desarrollas una nueva funcionalidad reutilizable, añádela como una función o clase en un módulo dentro de `/src`.
- **Estilo de Código**: Sigue las convenciones de `PEP 8` para mantener la consistencia y legibilidad del código.
- **Flujo de Trabajo**: Abre un *issue* para discutir el cambio propuesto y luego envía un *pull request* para su revisión.

---

## 7. Contacto y Licencia

- **Responsable**: Osmar Yesid Rincón
- **Correo**: rincon3259@gmail.com

Este proyecto está bajo la **Licencia MIT**. Consulta el archivo `LICENSE` para más detalles.

> *Última actualización: 19 de julio de 2025*
