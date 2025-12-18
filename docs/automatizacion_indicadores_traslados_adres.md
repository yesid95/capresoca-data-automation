# Automatización de Indicadores de Traslados BDUA (Indicadores_Traslados_ADRES.ipynb)

## 1. Descripción General
Este documento detalla el funcionamiento del notebook `Indicadores_Traslados_ADRES.ipynb`, diseñado para la **generación automática de estadísticas e indicadores de gestión** relacionados con los procesos de traslado de afiliados (BDUA) ante la ADRES.

El sistema procesa los archivos de respuesta y validación (R4, S4, S1, S3, S5, S6) generados por la ADRES y por el validador interno, consolidando la información para determinar cuántos traslados fueron **solicitados, aprobados y negados** tanto para el régimen Subsidiado como para el Contributivo.

### 🎯 Objetivo del Negocio
Proveer una visión clara y cuantificable del desempeño de la EPS en los procesos de movilidad y traslado, facilitando la toma de decisiones y el reporte a entes de control mediante un tablero de mando (Dashboard) en Excel.

---

## 2. Stack Tecnológico
*   **Lenguaje:** Python 3.x
*   **Librerías Principales:**
    *   `pandas`: Procesamiento y filtrado de datos masivos.
    *   `os`: Gestión de rutas y lectura de directorios.
    *   `xlsxwriter`: Escritura eficiente de múltiples hojas en Excel.
    *   `openpyxl`: Manipulación avanzada de estilos de Excel (bordes, colores, celdas combinadas) para el reporte final.

---

## 3. Arquitectura del Pipeline

```mermaid
graph TD
    subgraph Insumos [Archivos de Respuesta ADRES]
        A[R4/S4 (Respuestas Traslados)] --> L(Carga Masiva)
        B[S1 (Validaciones Automáticas)] --> L
        C[S3/S5/S6 (Otras Respuestas)] --> L
    end

    subgraph Procesamiento [Motor de Cálculo]
        L --> F{Filtrado y Clasificación}
        F -->|Columna 3 = '1'| AP[Aprobados]
        F -->|Columna 3 = '0'| NG[Negados]
        F -->|Cruce de Bases| EX[Exclusión de Duplicados]
        EX --> CON[Consolidación de DataFrames]
    end

    subgraph Salida [Reporte Gerencial]
        CON --> E[Archivo Excel Multihola]
        E --> R[Hoja Resumen (KPIs)]
        R --> D[Dashboard con Estilos]
    end
```

---

## 4. Lógica de Negocio Detallada

### 4.1. Tipología de Archivos Procesados
El sistema ingesta archivos planos (TXT/VAL) que corresponden a la estructura de respuesta BDUA:

*   **R4 / S4:** Respuestas de traslados (Salida de afiliados hacia otras EPS).
*   **S1:** Validaciones de estructura y consistencia (Automático y Validador).
*   **S3:** Cruces de información.
*   **S5:** Respuestas de traslados (Entrada de afiliados a Capresoca).
*   **S6:** Novedades de traslado.

### 4.2. Reglas de Clasificación (Aprobados vs. Negados)
Para los archivos principales de respuesta (R4, S4), se aplica la siguiente lógica basada en la posición de las columnas (índices base 0):

*   **Aprobados:** Registros donde la **Columna 3** tiene el valor `"1"`.
*   **Negados:** Registros donde la **Columna 3** tiene el valor `"0"`.

### 4.3. Lógica de Depuración y Exclusión
Para evitar el doble conteo de registros que aparecen en múltiples archivos de respuesta, se aplica una jerarquía de exclusión:

1.  **Limpieza S1/S3/S6:** Se filtran registros con códigos de estado `0, 1, 2` y se excluyen aquellos cuya entidad de origen sea la propia EPS (`EPS025`, `EPSC25`).
2.  **Exclusión en Cascada:**
    *   Se eliminan de **S5** los registros que ya existen en **S1_Auto**.
    *   Se eliminan de **S3** los registros que ya existen en **S5** o **S1_Auto**.
    *   Se eliminan de **S6** los registros que ya existen en **S5** o **S1_Auto**.
    *   *Criterio de cruce:* Se comparan columnas clave (ej. Tipo y Número de Documento) para identificar duplicados.

### 4.4. Generación del Tablero de Control (Resumen)
El script no solo exporta los datos crudos, sino que construye una hoja de **"Resumen"** con formato ejecutivo:

*   **Secciones:**
    1.  Consolidado a Otra EPS (Subsidiado).
    2.  Consolidado a Otra EPS (Contributivo).
    3.  Consolidado a Capresoca EPS (Entradas).
*   **Métricas:**
    *   **Solicitados:** Total de registros procesados.
    *   **Aprobados:** Cantidad y Porcentaje (`Aprobados / Solicitados`).
    *   **Negados:** Cantidad y Porcentaje (`Negados / Solicitados`).
*   **Estilos:** Uso de `openpyxl` para aplicar colores corporativos, bordes, negritas y formatos de porcentaje.

---

## 5. Estructura del Proyecto y Archivos

### 5.1. Rutas de Entrada
Las rutas apuntan a carpetas específicas donde se depositan los archivos planos del periodo:
*   `ruta_R4_Sub`, `ruta_S4_Sub`
*   `ruta_R4_Cont`, `ruta_S4_Cont`
*   `ruta_S1_Auto`, `ruta_S1_Val`
*   `ruta_S3`, `ruta_S5`, `ruta_S6`

### 5.2. Salida (Output)
*   **Archivo:** `Estadisticas Traslado BDUA {Fecha}_CORRECCION.xlsx`
*   **Ubicación:** Carpeta `Indicadores` dentro de la ruta base.
*   **Contenido:**
    *   Hojas de detalle: `S4_Sub`, `R4_Sub`, `S4_Cont`, etc.
    *   Hoja `Resumen`: Tabla dinámica con los KPIs.

---

## 6. Guía de Mantenimiento

### 6.1. Actualización Mensual
Al cambiar de periodo, se debe modificar la variable `Fecha` en la **Celda 1**:
```python
Fecha = "11_Noviembre 2025" # Actualizar al mes de reporte
```

### 6.2. Gestión de Rutas
Si la estructura de carpetas en OneDrive cambia, actualizar la variable `Base`:
```python
Base = r"C:\Users\osmarrincon\OneDrive...\Colab_Notebooks"
```

### 6.3. Ajuste de Estructuras de Archivo
Si la ADRES cambia la estructura de los archivos planos (ej. agrega columnas o cambia el separador), se deben ajustar los parámetros en la función de carga:
```python
Separador_Archivo = ',' # Cambiar si es pipe (|) o punto y coma (;)
tiene_encabezado = False # Cambiar a True si los archivos traen header
```
