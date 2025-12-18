# Automatización de Estructura S1 (S1 Estructura)

## Descripción General
Este documento describe el proceso automatizado implementado en el notebook `S1 Estructura.ipynb`. El objetivo principal es generar la estructura del archivo **S1** (Novedades de Traslado y Movilidad) para el reporte a ADRES, integrando información de afiliados que presentan movilidad en la Pila y sus respectivos beneficiarios.

El proceso toma como base los resultados del análisis de movilidad (Pila Validada) y cruza esta información con los Maestros de Afiliados (Contributivo y Subsidiado) para completar la estructura técnica requerida.

## Tecnologías Utilizadas
*   **Python 3.x**
*   **Pandas**: Para la manipulación de datos y construcción de estructuras.
*   **OpenPyXL**: Para la exportación a Excel.
*   **Módulos Personalizados**:
    *   `src.file_loader`: Para la carga optimizada de maestros ADRES.
    *   `src.data_cleaning`: Para la limpieza y normalización de datos (e.g., `BduaReportProcessor`, `DataCleaner`).

## Entradas y Salidas

### Entradas (Inputs)
1.  **Pila Validada (`R_Pila_Validada`)**:
    *   Formato: `.xlsx`
    *   Contenido: Resultado del proceso anterior (`S1_Movilidad.ipynb`) donde se identificaron los afiliados con movilidad ("S1").
2.  **Maestros ADRES**:
    *   `R_Maestro__EPSC25`: Maestro Contributivo (`.TXT`).
    *   `R_Maestro__EPS025`: Maestro Subsidiado (`.TXT`).
    *   Se cargan y combinan usando `cargar_maestros_ADRES`.

### Salidas (Outputs)
1.  **Archivo Estructura S1 (`S_Excel`)**:
    *   Formato: `.xlsx`
    *   Hojas:
        *   `S1`: Estructura final lista para reporte o validación.
        *   `maestro_ADRES`: Copia del maestro unificado (opcional/auditoría).

## Lógica del Proceso

### 1. Carga y Preparación de Datos
*   Se cargan los maestros de ADRES (Subsidiado y Contributivo) y se unifican.
*   Se carga el archivo de **Pila Validada**.
*   Se realiza una limpieza inicial de la población en el maestro ADRES usando `BduaReportProcessor` para priorizar marcadores de Sisbén IV y III.

### 2. Construcción de la Estructura S1 (Cabezas de Familia)
*   Se define la estructura de columnas estándar para el archivo S1 (e.g., `ENT_ID`, `TPS_IDN_ID`, `FECHA_AFILIACION_MOVILIDAD`, etc.).
*   Se filtran los registros de la Pila Validada donde la columna `Movilidad` contiene "S1".
*   Se mapean los datos básicos de la Pila a la estructura S1:
    *   Identificación del cotizante.
    *   Fecha de afiliación (tomada de `Fecha envio`).
    *   Población (tomada de `Población_2`).
*   Se marca el origen de estos registros como "Pila".

### 3. Incorporación de Beneficiarios
*   Se identifican las "cabezas de familia" en el S1 recién creado.
*   Se realiza un cruce (`merge`) con el **Maestro ADRES** para encontrar a los beneficiarios asociados a esas cabezas de familia.
    *   Llave de cruce: `TPS_IDN_ID_CF` y `HST_IDN_NUMERO_IDENTIFICACION_CF` (en Maestro) vs `TPS_IDN_ID` y `HST_IDN_NUMERO_IDENTIFICACION` (en S1).
*   Se agregan los beneficiarios encontrados al DataFrame S1, propagando la `FECHA_AFILIACION_MOVILIDAD` de su cotizante principal.
*   Se marca el origen de estos registros como "Beneficiarios Pila".

### 4. Enriquecimiento de Datos (Maestro -> S1)
*   Para completar la información faltante en S1 (que no viene de la Pila), se cruza nuevamente con el Maestro ADRES.
*   Se completan campos demográficos y de ubicación:
    *   Apellidos y Nombres.
    *   Fecha de Nacimiento y Sexo.
    *   País y Lugar de Nacimiento.
    *   Discapacidad, Etnia, etc.
    *   Ubicación (Departamento, Municipio, Zona).

### 5. Normalización de Sisbén y Población
*   Se aplica lógica para extraer y normalizar el Nivel de Sisbén (`TPS_NVL_SSB_ID`) y Metodología (`CND_AFL_SBS_METODOLOGIA`) a partir del subgrupo SIV.
    *   Reglas para grupos A, B, C del Sisbén IV.
    *   Reglas para Sisbén III (LC).

### 6. Validación y Ajuste de Fechas
*   Se valida la `FECHA_AFILIACION_MOVILIDAD` contra fechas de corte (`fecha_Minima`, `fecha_reporte`, `fecha_proxi_reporte`).
*   **Lógica de Ajuste**:
    *   Si fecha < mínima: Se ajusta a la fecha mínima y Tipo Traslado = 3.
    *   Si fecha > reporte actual pero < próximo reporte: Se ajusta al mes anterior y Tipo Traslado = 4.
    *   Si fecha > próximo reporte: Se marca para "proceso para proximos reportes".
    *   Por defecto: Tipo Traslado = 3.

### 7. Reglas de Negocio Finales
*   **Entidad**: Se asigna "EPS025" a `ENT_ID`.
*   **Lugar de Nacimiento**: Si está vacío y el país es Colombia ("COL"), se construye concatenando Departamento (`DPR_ID`) y Municipio (`MNC_ID`).

## Variables Clave
*   `fecha_archivo`: Fecha de corte para el nombre del archivo de salida.
*   `fecha_Minima`, `fecha_reporte`, `fecha_proxi_reporte`: Fechas de control para la validación de la movilidad.
