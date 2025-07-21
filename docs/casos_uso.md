# Casos de Uso y Prototipos en Notebooks

Este documento describe cómo los Jupyter Notebooks ubicados en la carpeta `/notebooks` actúan como prototipos funcionales y validadores de la lógica de negocio que, eventualmente, será integrada en la aplicación de escritorio final.

---

## 1. El Rol de los Notebooks como Prototipos

Cada notebook representa un **caso de uso** específico del área de Aseguramiento. Su propósito es servir como un entorno de desarrollo controlado donde se puede:

-   **Explorar los datos** para entender su estructura y calidad.
-   **Desarrollar y refinar la lógica de negocio** de forma iterativa.
-   **Validar los resultados** intermedios y finales antes de la implementación formal.
-   **Generar resultados inmediatos** para necesidades operativas mientras se construye la solución a largo plazo.

Una vez que la lógica en un notebook es estable y ha sido validada, se refactoriza e integra en los módulos de la carpeta `/src` para su posterior uso en la aplicación.

---

## 2. Mapeo de Notebooks a Funcionalidades Futuras

A continuación, se detallan los principales casos de uso y los notebooks que sirven como sus prototipos.

### 2.1. Caso de Uso: Módulo de Validación y Cruce de Información

-   **Descripción**: Funcionalidad de la aplicación que permitirá realizar validaciones cruzadas entre diferentes fuentes de datos (BDUA, ADRES, SIE, etc.) para garantizar la consistencia y calidad de la información del afiliado.
-   **Notebooks Prototipo**:
    -   `notebooks/Aseguramiento/Validar SIE.ipynb`: Prototipo para el proceso de validación de la estructura y contenido de los archivos del Sistema de Información de Entidades (SIE).
    -   `notebooks/Aseguramiento/Cruces Informacion.ipynb`: Base para el motor de cruce de datos entre múltiples fuentes.
    -   `notebooks/Aseguramiento/Corregir NS-NEG.ipynb`: Prototipo para la lógica de corrección de inconsistencias específicas detectadas durante los cruces.

### 2.2. Caso de Uso: Módulo de Reportería y Generación de Indicadores

-   **Descripción**: Característica de la aplicación que generará reportes normativos (ej. para ADRES) y de gestión interna de forma automática o bajo demanda.
-   **Notebooks Prototipo**:
    -   `notebooks/Aseguramiento/Indicadores_Traslados_ADRES.ipynb`: Prototipo para el cálculo y reporte de indicadores relacionados con traslados, según la normativa vigente.
    -   `notebooks/Aseguramiento/Cartera.ipynb`: Base para la generación de reportes de estado de cartera y recaudo.

### 2.3. Caso de Uso: Herramienta de Consolidación de Datos (ETL)

-   **Descripción**: Funcionalidad que permitirá unificar grandes volúmenes de datos históricos o de diferentes periodos en un único dataset maestro para facilitar análisis futuros o la carga a sistemas de Business Intelligence (BI).
-   **Notebooks Prototipo**:
    -   `notebooks/Aseguramiento/Unificar_Archivos.ipynb`: Prototipo central para la lógica de unificación de archivos masivos.
    -   `notebooks/Aseguramiento/HIstoricos estructura.ipynb`: Prototipo para la definición y estandarización de la estructura de los archivos históricos.

### 2.4. Caso de Uso: Módulo de Utilidades y Herramientas Auxiliares

-   **Descripción**: Conjunto de herramientas de apoyo integradas en la aplicación para facilitar tareas operativas diarias.
-   **Notebooks Prototipo**:
    -   `notebooks/Generales/Editar PDFs.ipynb`: Base para una futura herramienta de manipulación de documentos PDF.
    -   `notebooks/Generales/Correos_Maxivos 064.ipynb`: Prototipo para un módulo de comunicación y envío de notificaciones masivas.
