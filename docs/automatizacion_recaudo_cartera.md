# Automatización de Cruce Recaudo vs Pila SIE

## Descripción General
Este documento describe el proceso automatizado implementado en el notebook `Recaudo-Cartera.ipynb`. El objetivo principal es actualizar una matriz de **Relación de Recaudo** con la información de pagos (Cotización Obligatoria) proveniente de los archivos de **Pila SIE** (Tipos I e IP).

El script cruza la información de los cotizantes y aportantes para identificar los pagos realizados en diferentes periodos y diligenciar las columnas correspondientes en el archivo maestro de recaudo.

## Tecnologías Utilizadas
*   **Python 3.x**
*   **Pandas**: Para la manipulación y análisis de estructuras de datos (DataFrames).
*   **OpenPyXL**: Para la lectura y escritura de archivos Excel.
*   **Glob/OS**: Para la búsqueda y gestión de archivos en directorios.
*   **Datetime**: Para el manejo de fechas y generación de rangos de periodos.

## Entradas y Salidas

### Entradas (Inputs)
1.  **Archivo Maestro de Recaudo (`R_Recaudo`)**:
    *   Formato: `.xlsx`
    *   Hoja: "RELACION RECAUDO"
    *   Contenido: Información base de recaudo con columnas de identificación de aportantes y cotizantes.
2.  **Archivos Pila SIE Tipo I (`R_Pila_SIE_I`)**:
    *   Ubicación: Carpeta con archivos `.TXT`.
    *   Formato: Texto delimitado por `|`.
    *   Contenido: Planillas Integradas de Liquidación de Aportes (Tipo I).
3.  **Archivos Pila SIE Tipo IP (`R_Pila_SIE_IP`)**:
    *   Ubicación: Carpeta con archivos `.TXT`.
    *   Formato: Texto delimitado por `|`.
    *   Contenido: Planillas de Pensionados (Tipo IP).

### Salidas (Outputs)
1.  **Archivo de Recaudo Actualizado (`RS_Recaudo`)**:
    *   Formato: `.xlsx`
    *   Contenido: El mismo archivo maestro de entrada, pero con nuevas columnas para cada periodo (mes) detectado, diligenciadas con el valor de la "Cotización Obligatoria" si se encontró el pago en los archivos de Pila.

## Lógica del Proceso

### 1. Carga y Unificación de Fuentes Pila
*   Se leen todos los archivos `.TXT` de la carpeta de **Pila I** y se concatenan en un solo DataFrame.
*   Se leen todos los archivos `.TXT` de la carpeta de **Pila IP**.
    *   Se realiza una limpieza específica para Pila IP: convertir "X" a 1 y vacíos a 0.
    *   Se homologan los nombres de columnas con Pila I.
*   Se unen ambas fuentes (I e IP) en un único DataFrame `Df_Pila_SIE`.

### 2. Filtrado y Limpieza
*   Se filtran los registros de Pila SIE para excluir correcciones (`Correcciones != "A"`).
*   Se seleccionan únicamente las columnas relevantes:
    *   Identificación Aportante
    *   Periodo Pago
    *   Tipo y Número de Identificación Cotizante
    *   ING, RET, Días Cotizados
    *   Cotización Obligatoria
    *   Número y Fecha de Planilla

### 3. Generación de Columnas de Periodos
*   Se identifica el periodo mínimo presente en el archivo de Recaudo (`periodo_pago`).
*   Se genera un rango de fechas mensual desde ese mínimo hasta el mes actual.
*   Se crean columnas vacías en el DataFrame de Recaudo (`Df_Recaudo`) para cada uno de estos periodos (formato `YYYY-MM`).

### 4. Cruce de Información (Mapping)
*   Se crea un diccionario de mapeo (`mapping`) a partir de `Df_Pila_SIE` utilizando una llave compuesta por:
    *   `numero_identificacion_aportante`
    *   `tipo_identificacion_cotizante`
    *   `numero_identificacion_cotizante`
    *   `periodo_pago`
*   El valor almacenado en el diccionario es la `Cotización Obligatoria`.

### 5. Asignación de Valores
*   Se itera sobre cada fila del archivo de Recaudo.
*   Para cada fila, se busca en el diccionario si existen pagos para la combinación (Aportante + Cotizante) en los periodos generados.
*   Si existe coincidencia, se asigna el valor de la cotización en la columna del periodo correspondiente.

### 6. Exportación
*   El DataFrame resultante se exporta a Excel, sobrescribiendo o creando el archivo de salida definido.

## Consideraciones Adicionales
*   **Rutas de Archivos**: Las rutas están definidas estáticamente en el código (e.g., `C:\Users\osmarrincon\Downloads\...`). Para despliegue en otro entorno, estas deben actualizarse o parametrizarse.
*   **Rendimiento**: El uso de `apply` fila por fila (`assign_cotizacion_all`) puede ser lento si el volumen de datos en `Df_Recaudo` es muy grande. Se podría optimizar vectorizando la operación o usando `merge`/`pivot`.
