# Documentación Técnica: Automatización de Unificación de Archivos

**Archivo:** `notebooks/Aseguramiento/Unificar_Archivos.ipynb`  
**Nivel:** Técnico / Ingeniería de Datos  
**Audiencia:** Junior a Senior

---

## 1. Introducción y Contexto
Este documento detalla la arquitectura y lógica implementada en el notebook `Unificar_Archivos.ipynb`. Este script actúa como un pipeline ETL (Extract, Transform, Load) diseñado para consolidar, limpiar y estandarizar grandes volúmenes de archivos planos provenientes de diversas fuentes (Financiero, PILA, ADRES).

El objetivo principal es resolver la fragmentación de datos (archivos semanales o mensuales dispersos) y los problemas de evolución de esquemas (cambios en la normativa legal que alteran las columnas de los archivos), generando datasets unificados listos para análisis.

## 2. Stack Tecnológico y Requisitos
El proceso se basa en **Python** utilizando las siguientes librerías clave:

*   **`pandas`**: Motor principal para la manipulación de datos en memoria (DataFrames). Se utiliza extensivamente para lectura (`read_csv`), concatenación (`concat`), cruces (`merge`) y escritura (`to_csv`).
*   **`os`**: Para la interacción con el sistema de archivos (listado de directorios, construcción de rutas agnósticas al sistema operativo).
*   **`datetime`** y **`dateutil.relativedelta`**: Para la manipulación avanzada de fechas y cálculos de lógica de negocio (reglas de traslados).

### Consideraciones de Entorno
*   **Rutas Dinámicas:** El código maneja variables para rutas de entrada (`input_folder`) y salida (`output_file`). Se observa una práctica de comentar/descomentar rutas según el entorno de ejecución (Home vs. Office).
    *   *Recomendación Senior:* Externalizar estas rutas a un archivo de configuración (`config.yaml` o `.env`) para evitar modificar el código fuente al cambiar de entorno.

---

## 3. Arquitectura del Proceso
El notebook está modularizado en secciones secuenciales. Cada sección sigue un patrón similar:

1.  **Discovery:** Identificar archivos en una ruta específica.
2.  **Extraction:** Leer archivos iterativamente respetando codificaciones específicas (UTF-16, ANSI).
3.  **Transformation:**
    *   Inyección de metadatos (Nombre de archivo, Fecha de extracción).
    *   Validación de esquema (Conteo de columnas).
    *   Normalización de tipos de datos (Todo como `string` inicialmente para preservar formatos como ceros a la izquierda).
4.  **Loading:** Concatenación y guardado en un archivo maestro `.TXT`.

---

## 4. Detalle de Implementación por Módulo

### 4.1. Módulo Financiero (Secciones 1 y 1.1)
Este módulo procesa la información financiera semanal.

*   **Desafío Técnico (Encoding):** Los archivos financieros originales vienen codificados en **UTF-16**.
    *   *Por qué es importante:* Si se intenta leer con el default (UTF-8), fallará o generará caracteres corruptos (mojibake). El código especifica explícitamente `encoding='utf-16'`.
*   **Lógica de Extracción:**
    *   Se extrae la fecha directamente del nombre del archivo usando slicing de strings: `file[-10:-4]`. Esto asume una nomenclatura estricta en los archivos de entrada.
*   **Validación de Calidad de Datos:**
    *   Se verifica estrictamente que el DataFrame resultante tenga **15 columnas**. Si no, se lanza un `ValueError`. Esto actúa como un "Circuit Breaker" para detener el proceso si llega un archivo corrupto o mal formado.

### 4.2. Módulo PILA (Secciones 2 y 2.1)
Procesa la Planilla Integrada de Liquidación de Aportes.

*   **Manejo de Tipos (Dtype):** Se utiliza `dtype=str` en `pd.read_csv`.
    *   *Explicación Junior:* Pandas intenta adivinar si una columna es número o texto. Si una cédula o código empieza por '0' (ej. '0123'), pandas lo leería como el número 123. Al forzar `str`, garantizamos que '0123' se mantenga como '0123'.
*   **Esquema:** Se estandariza a **42 columnas**.
*   **Iteración:** Se recorre cada archivo, se carga en memoria, se etiqueta con su nombre de origen y se añade a una lista para una concatenación final eficiente (`pd.concat` una sola vez al final es más eficiente que hacer `append` en cada iteración).

### 4.3. Enriquecimiento de Datos (Sección 3: Join Financiero-PILA)
Esta es una etapa crítica de integración de datos.

*   **Operación:** `LEFT JOIN` (pd.merge con `how='left'`).
    *   **Tabla Izquierda (Base):** PILA Unificada.
    *   **Tabla Derecha (Enriquecimiento):** Financiero (solo columnas `Nit` y `Razon_Social`).
    *   **Llave de Cruce:** `Num_rad_planilla`.
*   **Limpieza de Llaves:**
    *   Antes del cruce, se asegura que la llave `Num_rad_planilla` sea del mismo tipo (`str`) en ambos lados.
    *   Se realiza una limpieza de la columna `Nit` usando Regex (`.str.replace(r'\.0$', '', regex=True)`) para eliminar decimales flotantes indeseados que a veces aparecen al leer números como texto.
*   **Transformación de Formato:**
    *   Se aplica `zfill` (relleno con ceros) a los códigos de departamento (2 dígitos) y municipio (3 dígitos) para cumplir con el estándar del DANE.

### 4.4. Gestión de Cambios Normativos (Secciones 4 y 5: ABX y ACX)
Este módulo demuestra un manejo avanzado de **Evolución de Esquemas**. La normativa colombiana cambió la estructura de los archivos de compensación (de Nota Externa 5215 a Resolución 03341).

*   **El Problema:**
    *   Archivos antiguos (2018-2021.01): Tienen columnas relacionadas con el FOSYGA.
    *   Archivos nuevos (2021.02+): Eliminan FOSYGA, agregan Departamento y Municipio.
*   **La Solución Algorítmica:**
    1.  **Detección de Versión:** El script detecta qué "norma" aplicar basándose en el nombre de la carpeta del año (`folder_name in norma_vieja_folders`).
    2.  **Adaptación de Esquema (Schema Mapping):**
        *   Si es norma vieja: Se eliminan las columnas obsoletas y se *inyectan* las columnas nuevas (`Departamento`, `Municipio`) con valores por defecto ('85', '001') para que coincidan con la estructura nueva.
    3.  **Unificación:** Al final, todos los DataFrames, independientemente de su origen temporal, terminan con la misma estructura de columnas, permitiendo un análisis histórico coherente.

### 4.5. Lógica de Negocio Compleja (Sección 6: R1 y R3)
Aquí se implementa lógica de negocio pura para calcular fechas de efectividad de traslados.

*   **Cálculo de `Fecha_Efectiva`:**
    Se utiliza una función personalizada `compute_fecha_efectiva` que aplica reglas condicionales sobre la columna `TIPO_TRASLADO`:
    *   **Tipo 1:** Efectivo el 1° del mes siguiente (`relativedelta(months=1)`).
    *   **Tipo 2:** Efectivo el 1° del mes subsiguiente (2 meses después).
    *   **Tipo 4:** Mismo día, mes siguiente.
    *   **Otros:** Fecha original.
    *   *Nota Técnica:* Se usa `dateutil.relativedelta` porque es más robusto que simplemente sumar 30 días (maneja correctamente años bisiestos y meses de diferente duración).
*   **Limpieza de "Basura":**
    *   Los archivos de entrada a veces contienen columnas vacías o generadas por error (`Columna34` a `Columna45`). El script detecta si el archivo tiene exceso de columnas y las elimina explícitamente (`df.drop`) para mantener el dataset limpio.

---

## 5. Resumen de Archivos Generados

| Proceso | Archivo de Salida (Ejemplo) | Codificación | Notas Clave |
| :--- | :--- | :--- | :--- |
| **Financiero** | `Financiero_2025.TXT` | UTF-16 | 15 Columnas. |
| **PILA** | `Pila_2025.TXT` | UTF-16 | 42 Columnas. Tipos forzados a string. |
| **Unificado** | `Pila_Unificado_Con_Aportante...TXT` | UTF-16 | Cruce de PILA + NIT/Razón Social. |
| **ABX** | `ABX_2025.TXT` | ANSI | Normalizado a Resolución 03341. |
| **ACX** | `ACX_2025.TXT` | ANSI | Normalizado a Resolución 03341. |
| **R1/R3** | `All-2025.TXT` | ANSI | Incluye columna calculada `Fecha_Efectiva`. |

## 6. Guía de Mantenimiento (Troubleshooting)

1.  **Error `UnicodeDecodeError`:**
    *   *Causa:* El archivo de entrada no coincide con la codificación esperada (ej. viene en UTF-8 pero el script espera UTF-16).
    *   *Solución:* Verificar el origen del archivo y ajustar el parámetro `encoding` en la función `read_csv`.
2.  **Error `ValueError: El DataFrame unificado no tiene X columnas`:**
    *   *Causa:* Un archivo de entrada tiene una estructura corrupta o diferente (ej. una columna extra o faltante).
    *   *Solución:* Identificar el archivo corrupto (el script suele imprimir cuál es antes de fallar o se puede agregar un print en el loop) y corregirlo en origen.
3.  **Cambio de Año:**
    *   Al iniciar un nuevo año, se deben crear las carpetas correspondientes y actualizar las listas de carpetas en las secciones de ABX/ACX (`norma_nueva_folders`) y R1/R3 (`folders_XX`) para incluir el nuevo año.
