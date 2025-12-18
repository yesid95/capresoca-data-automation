# Automatización de Gestión de No Movilidad (No_Movilidad_MSM)

## Descripción General
Este documento describe el proceso automatizado implementado en el notebook `No_Movilidad_MSM.ipynb`. El objetivo principal es gestionar y depurar los registros de afiliados que presentan bloqueos o inconsistencias en su estado de **Movilidad**, específicamente aquellos relacionados con el **Sisbén** (e.g., "Sin Sisbén", "Sisbén D").

El script toma el reporte de movilidad generado previamente, filtra los casos de interés y enriquece la información con datos demográficos del Maestro ADRES y datos de contacto del sistema SIE, facilitando la gestión administrativa y el contacto con el afiliado para subsanar la inconsistencia.

## Tecnologías Utilizadas
*   **Python 3.x**
*   **Pandas**: Para la manipulación, filtrado y cruce de datos.
*   **Regular Expressions (re)**: Para la limpieza y validación de teléfonos y correos electrónicos.
*   **OpenPyXL**: Para la exportación de archivos Excel con múltiples hojas.
*   **Módulos Personalizados**: `src.file_loader` y `src.data_cleaning` para carga y normalización de maestros.

## Entradas y Salidas

### Entradas (Inputs)
1.  **Dataframe Pila Movilidad (`R_Pila_movilidad`)**:
    *   Formato: `.xlsx`
    *   Contenido: Resultado del proceso de movilidad (probablemente de `S1_Movilidad.ipynb`) que contiene la columna `Movilidad`.
2.  **Reporte Validación SIE (`R_MS_SIe`)**:
    *   Formato: `.csv`
    *   Contenido: Base de datos de contacto (teléfonos, correos) del sistema de información.
3.  **Maestros ADRES (`R_Maestro__EPSC25`, `R_Maestro__EPS025`)**:
    *   Formato: `.TXT`
    *   Contenido: Información demográfica oficial de los afiliados.
4.  **Códigos DANE (`R_Cod_DANE`)**:
    *   Formato: `.txt`
    *   Contenido: Homologación de códigos de departamentos y municipios.

### Salidas (Outputs)
1.  **Archivo Movilidad No Efectiva (`S_Excel`)**:
    *   Formato: `.xlsx`
    *   Estructura: Un archivo Excel donde cada hoja corresponde a un tipo de inconsistencia de movilidad (e.g., una hoja para "Sin Sisben", otra para "Sisben D").

## Lógica del Proceso

### 1. Carga y Preparación
*   Se cargan los maestros ADRES (Contributivo y Subsidiado) y se normalizan los marcadores de población.
*   Se carga el archivo de Pila Movilidad y la base de contactos SIE.

### 2. Filtrado de Casos de Interés
*   Se filtra el DataFrame de Pila Movilidad para conservar únicamente los registros cuya columna `Movilidad` contenga:
    *   "sin sisben"
    *   "no sisben"
    *   "sisben D"
*   Esto aísla la población objetivo que requiere gestión prioritaria.

### 3. Enriquecimiento de Datos (Cruces)
*   **Datos Demográficos**: Se cruza con el Maestro ADRES para obtener:
    *   Nombres y Apellidos.
    *   Fecha de Nacimiento.
    *   Ubicación (Departamento y Municipio ID).
*   **Datos de Contacto**: Se cruza con la base SIE para obtener:
    *   Celular, Teléfono 1, Teléfono 2.
    *   Correo Electrónico.
*   **Nombres de Ubicación**: Se cruza con la tabla DANE para obtener los nombres legibles de Departamento y Municipio.

### 4. Limpieza de Contacto
*   **Teléfonos**: Se aplica una función de limpieza que:
    *   Elimina caracteres no numéricos.
    *   Valida que tenga 10 dígitos y empiece por '3' (formato móvil Colombia).
*   **Correos**: Se aplica una función de limpieza que:
    *   Valida estructura de email (Regex).
    *   Elimina correos "basura" o placeholders (e.g., "notiene", "sincorreo", "noaplica").

### 5. Exportación Agrupada
*   El DataFrame final se agrupa por el tipo de `Movilidad`.
*   Se itera sobre cada grupo y se exporta a una hoja separada en el archivo Excel de salida.
*   Se realiza una limpieza del nombre de la hoja para asegurar compatibilidad con Excel (eliminando caracteres especiales como `/`, `\`, `*`, etc.).

## Variables Clave
*   `Fecha`: Define la fecha de corte para el nombre del archivo de salida.
*   `hoja`: Nombre de la hoja a leer en el archivo de entrada de Pila.
