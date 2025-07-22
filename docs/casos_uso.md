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

#### 2.1.1. Caso de Uso: Automatización del Reporte de Movilidad S1

**Descripción**: Automatización del proceso de generación y validación del reporte de movilidad S1 descendente al régimen subsidiado, siguiendo la normativa y calendario de ADRES.

**Actores y Fuentes de Datos - Proceso Movilidad S1**

| Tipo      | Nombre/Descripción |
|-----------|--------------------|
| **Persona** | Profesional de apoyo del área de Aseguramiento de Capresoca EPS. Encargado de realizar el reporte de movilidad descendente S1 de acuerdo a la Resolución 762/2023 y de mantener actualizada la base de datos del régimen subsidiado. |
| **Sistema** | Sistema interno de la EPS (no se asigna nombre para evitar acoplamientos si el sistema cambia). Genera archivos y bases de datos de validación. |
| **Base de datos** | S1: Generado por el sistema interno de la EPS. |
| **Base de datos** | PILA del sistema interno de la EPS: Base de datos donde se validan pagos de los afiliados con novedades de ingreso, retiro o sin novedades, para identificar si deben o no bajar a subsidiado o para identificar si se deben reportar en S1. |
| **Base de datos** | PILA 3047 validada por ADRES: Para verificar pagos que no estén en PILA del sistema interno de la EPS. |
| **Base de datos** | Maestros ADRES: Lista de usuarios a validar o revisar pagos y novedades para definir si tienen o no que reportarse en el S1. |
| **Base de datos** | Dataset SAT unificado: Rastrea inicios y fin de relaciones laborales. Determina fecha efectiva de movilidad. |
| **Base de datos** | Dataset R1 unificado: Rastrea inicios de relaciones laborales. Determina fecha efectiva de movilidad. |
| **Base de datos** | Dataset NC (Novedades Contributivo): Rastrea inicios y fin de relaciones laborales. Determina fecha efectiva de movilidad. |
| **Base de datos** | Dataset ACX y ABX: Identifica máximos periodos comenzados de cada afiliado. |
| **Base de datos** | Dataset Expediente del sistema interno de la EPS: Determina si hay usuarios que deben bajar para compensar días porque terminaron una relación laboral y días después iniciaron otro, o para identificar usuarios que terminan relación laboral pero tienen continuidad con otra u otras relaciones laborales. |

> Nota: Estos actores y fuentes pueden ser modificados en fases posteriores si se detectan nuevas dependencias.


**Flujo Operativo y Condiciones de Uso - Automatización Movilidad S1**

> Para la visión técnica y estructural del sistema, consulta la sección de arquitectura en [`arquitectura.md`](arquitectura.md).

La automatización del reporte de movilidad S1 está alineada con el calendario de semanas de proceso definido por ADRES. Cada mes puede tener 2, 3, o 4 semanas hábiles, según la distribución de días hábiles y festivos. La última semana hábil suele reservarse para reportes de novedades por los entes territoriales "Alcaldias".

El proceso inicia cuando el profesional de apoyo del área de aseguramiento abre la automatización (inicialmente en un notebook) para preparar el reporte de movilidad S1, asegurando que la información utilizada esté actualizada al día del reporte. El reporte S1 se radica a ADRES el segundo día hábil de la semana de proceso, normalmente martes o miércoles si el lunes es festivo.

El proceso finaliza cuando el profesional de apoyo obtiene el archivo Excel ".xlsx" con la relación de usuarios categorizados, identificando correctamente a los afiliados que deben o no ser reportados en movilidad S1. Se documenta la trazabilidad de las decisiones tomadas por cada afiliado validado (relaciones laborales abiertas, pagos al día, moras, continuidad laboral con otro aportante, etc.), y se genera una hoja de informe/log que registra las bases de datos utilizadas y su fecha de actualización, facilitando la reproducibilidad y la identificación de errores.

**🧩 Resumen del Flujo de Validación – Proceso de Movilidad S1**
El flujo de validación de movilidad S1 tiene como objetivo identificar, con base en relaciones laborales y registros de pago, los afiliados que deben ser reportados como movilidad descendente al régimen subsidiado, según la Resolución 762 de 2023.

Este proceso se ejecuta en las llamadas "semanas de proceso" definidas por el calendario oficial de ADRES. Cada mes puede tener entre 2 y 4 semanas de proceso, dependiendo del número de semanas hábiles. La automatización debe correrse el mismo día del reporte para garantizar que las bases utilizadas estén actualizadas.

*🔹 Inicio del flujo:*
El proceso inicia manualmente cuando el profesional de apoyo del área de Aseguramiento ejecuta el notebook correspondiente.

*🔹 Validaciones centrales del flujo:*
Durante la ejecución, se realizan decisiones lógicas como:

¿El afiliado tiene relaciones laborales abiertas?

¿Tiene más de una relación activa?

¿Existe alguna relación sin pagos recientes?

¿Hay continuidad entre relaciones?

¿Debe compensar días o volver a subir al contributivo?

Estas validaciones se basan en diversas fuentes de datos como: PILA EPS, PILA 3047, Maestros ADRES, SAT, R1, NC, ACX/ABX y Expediente.

*🔹 Fin del flujo:*
El proceso finaliza cuando se ha generado:

Un archivo .xlsx con los afiliados categorizados como “reportables” o “no reportables”.

Una hoja de log con la trazabilidad de cada decisión, los nombres de las bases utilizadas y sus fechas de corte.

Este flujo garantiza la transparencia, reproducibilidad y calidad de la información usada para el reporte S1.

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

