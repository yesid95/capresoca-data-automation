# Automatización de Notificaciones y Mensajes de Texto

## Descripción General
Este documento describe el proceso automatizado implementado en el notebook `Mensajes_Texto.ipynb`. El objetivo principal es generar bases de datos depuradas y segmentadas para realizar campañas de notificación masiva (SMS o Correo Electrónico) a los afiliados.

El script identifica grupos específicos de usuarios que requieren realizar trámites administrativos, tales como actualización de datos de contacto, renovación de documentos de identidad, o gestión de encuestas Sisbén.

## Tecnologías Utilizadas
*   **Python 3.x**
*   **Pandas**: Para la manipulación, limpieza y cruce de datos.
*   **Numpy**: Para operaciones vectorizadas.
*   **Scikit-learn**: Se utiliza `TfidfVectorizer` y `KMeans` para análisis y validación de patrones en correos electrónicos.
*   **XlsxWriter**: Para la generación de reportes en Excel con formato avanzado y gráficos.
*   **Matplotlib**: Para visualización de análisis de clusters (correos).
*   **Regular Expressions (re)**: Para validación de formatos de correo y limpieza de teléfonos.

## Entradas y Salidas

### Entradas (Inputs)
1.  **Reporte Validación SIE (`R_MS_SIe`)**:
    *   Formato: `.csv`
    *   Contenido: Información de contacto (teléfonos, correos) del sistema de información.
2.  **Maestro ADRES (`R_MS_ADRES`)**:
    *   Formato: `.TXT`
    *   Contenido: Base de datos maestra de afiliados (Subsidiado).
3.  **Códigos DANE (`R_Cod_DANE`)**:
    *   Formato: `.txt`
    *   Contenido: Homologación de códigos de departamentos y municipios.
4.  **Presuntos Duplicados (`R_PR`)**:
    *   Formato: `.xlsx`
    *   Contenido: Listado de documentos duplicados para exclusión.
5.  **Base Sisbén (`R_Sisben`)**:
    *   Formato: `.xlsx`
    *   Contenido: Resultados de encuestas Sisbén con ubicación.

### Salidas (Outputs)
El proceso genera múltiples archivos Excel, cada uno enfocado en una campaña específica:

1.  **Actualización de Datos (`Ruta_Salida_Actualización_Datos`)**:
    *   Usuarios activos que les falta teléfono o correo.
    *   Hojas: `Sin_Datos`, `Telefonos` (falta correo), `Correo` (falta teléfono), `OK`, `Resumen`.
2.  **Actualización de Documento (`Ruta_Salida_Actualización_Documento`)**:
    *   Usuarios que por edad deben cambiar su tipo de documento.
    *   Hojas: `evolucion CN a RC`, `evolución RC a TI`, `evolución de TI a CC`, `Resumen`.
3.  **Sin Sisbén IV (`Ruta_Salida_No_Sisben`)**:
    *   Usuarios activos sin encuesta Sisbén válida.
    *   Hojas: `Datos`, `Resumen`.
4.  **Sisbén Otro Municipio (`R_Sisben_OtroMunicipio`)**:
    *   Usuarios cuyo municipio de afiliación difiere del municipio de la encuesta Sisbén.
    *   Hojas: `Datos`, `Resumen`.
5.  **Reportes de Calidad**:
    *   `R_resumen_SIE`: Estadísticas de completitud de datos de contacto.
    *   `R_MS_SIE_Corre`: Archivo SIE con correos y teléfonos validados.

## Lógica del Proceso

### 1. Limpieza y Validación de Contacto
*   **Teléfonos**: Se eliminan caracteres no numéricos, se valida longitud (10 dígitos) y prefijo móvil ('3').
*   **Correos Electrónicos**:
    *   Validación por Regex estándar.
    *   Lista negra de correos inválidos conocidos (e.g., "notiene@gamil.com").
    *   *Análisis Avanzado*: Se aplica clustering (K-Means) sobre vectores TF-IDF de los correos para identificar patrones anómalos o grupos de correos inválidos masivos.

### 2. Unificación de Fuentes
*   Se cruza el Maestro ADRES con los Códigos DANE para obtener nombres de municipios.
*   Se enriquece el Maestro ADRES con la información de contacto validada del SIE.

### 3. Segmentación de Campañas

#### A. Notificar Actualización de Datos
*   **Filtro**: Usuarios Activos (`AC`) y no suspendidos.
*   **Clasificación**:
    *   *Sin Datos*: No tienen ni celular ni correo.
    *   *Solo Teléfono*: Tienen celular pero falta correo.
    *   *Solo Correo*: Tienen correo pero falta celular.
    *   *OK*: Tienen ambos.

#### B. Notificar Actualización de Documento
*   **Filtro**: Usuarios Activos, tipos de documento CN, RC, TI.
*   **Cálculo de Edad**: Se calcula la edad exacta a la fecha actual.
*   **Reglas de Evolución**:
    *   `CN` -> `RC`: Todos los CN.
    *   `RC` -> `TI`: Mayores de 7 años.
    *   `TI` -> `CC`: Mayores de 18 años.
*   **Exclusión**: Se eliminan registros presentes en la base de Presuntos Duplicados (`R_PR`).

#### C. Usuarios Sin Sisbén IV
*   **Filtro**: Usuarios Activos, excluyendo poblaciones especiales (e.g., indígenas, desplazados si aplica).
*   **Validación**: Se excluyen aquellos que ya tienen marcas de clasificación Sisbén (A, B, C, D) o LC (Listado Censal) válidas en el maestro.

#### D. Sisbén en Otro Municipio
*   **Filtro**: Usuarios Activos.
*   **Cruce**: Se compara el código de municipio del maestro ADRES con el código de municipio reportado en la base Sisbén (`cod_mpio`).
*   **Condición**: `municipio_afiliacion != municipio_sisben`.

### 4. Generación de Reportes
*   Se utiliza `xlsxwriter` para crear archivos Excel con múltiples hojas.
*   Se agregan hojas de "Resumen" con tablas dinámicas y gráficos de barras incrustados para facilitar la lectura gerencial de las cifras.

## Consideraciones Adicionales
*   **Rutas Estáticas**: Las rutas de los archivos de entrada y salida están definidas en el código y deben actualizarse periódicamente (fechas en nombres de archivo).
*   **Validación de Correos**: El modelo de clustering requiere supervisión o ajuste de parámetros (`n_clusters`, `valid_clusters`) si cambian drásticamente los patrones de datos de entrada.
