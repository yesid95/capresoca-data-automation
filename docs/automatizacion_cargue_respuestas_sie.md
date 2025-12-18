# Documentación Técnica: Cargue de Respuestas al SIE

**Archivo:** `notebooks/Aseguramiento/Cargue respuestas al SIE.ipynb`  
**Nivel:** Técnico / Ingeniería de Datos  
**Audiencia:** Junior a Senior

---

## 1. Introducción y Objetivo
Este notebook automatiza el proceso de validación y clasificación de respuestas de aseguramiento (archivos S1, S3) para su posterior carga al Sistema de Información de la EPS (SIE).

El objetivo principal es cruzar la información de los archivos de respuesta automáticos con la base de datos interna (Expedientes y Relaciones Laborales) para determinar qué registros deben ser procesados como **S1 (Subsidios)** y cuáles como **R1 (Relaciones Laborales)**, generando un reporte consolidado en Excel.

## 2. Stack Tecnológico
*   **Python 3.x**: Lenguaje base.
*   **Pandas**: Manipulación de datos y cruces (Merges).
*   **Numpy**: Lógica condicional vectorizada (`np.where`).
*   **Glob/Pathlib**: Manejo de rutas y lectura masiva de archivos.

---

## 3. Arquitectura del Pipeline

### 3.1. Fuentes de Información (Inputs)
El proceso ingesta múltiples fuentes de datos:

1.  **Archivos de Respuesta (ADRES/Validador):**
    *   `R_S1_Automatico`: Archivo `.VAL` con respuestas automáticas S1.
    *   `R_S1_Val`: Archivo `.VAL` de validación S1.
    *   `R_S3`: Archivo `.TXT` con respuestas S3.
2.  **Fuentes Internas (SIE):**
    *   `R_MS_SIE`: Maestro del SIE (Validación Archivos Maestro).
    *   `R_Expedientes_SIE`: Histórico de expedientes (múltiples `.TXT`).
    *   `R_Relaciones_Laborales`: Reporte de relaciones laborales contributivas.

### 3.2. Limpieza y Transformación de Datos

#### 3.2.1. Expedientes SIE
*   **Filtrado de Estado:** Se eliminan registros con estado "Pendiente" o "Anulado".
*   **Filtrado de Procesos:** Se conservan solo procesos relevantes como:
    *   Ingreso Afiliado Contributivo (Cotizante, Nacimiento, Beneficiario).
    *   Afiliación por Adición Relación Laboral.
    *   Actualización de Beneficiarios o Relación Laboral.
*   **Deduplicación:** Se ordena por `Fecha Grabado` descendente y se mantiene el registro más reciente por `Tipo Documento` y `Número Identificación`.

#### 3.2.2. Relaciones Laborales
*   **Normalización de Fechas:** Conversión a formato `datetime`.
*   **Deduplicación:** Se mantiene la relación laboral más reciente (`fecha_ingreso`) por afiliado.

---

## 4. Lógica de Negocio y Validaciones

### 4.1. Validación S1 Automático
Esta es la lógica central del notebook. Se busca clasificar cada registro del archivo S1 Automático.

1.  **Enriquecimiento:**
    *   Se cruza con **Relaciones Laborales** para identificar si el afiliado tiene una relación laboral activa (`Relacion Laboral` = "SI"/"No").
    *   Se cruza con **Expedientes SIE** para obtener la `Fecha Grabado` y el `Usuario Grabado`.

2.  **Clasificación (S1 SIE vs. R1 no SIE):**
    Se crea la columna `Nueva Columna` aplicando reglas complejas sobre las fechas:
    *   **Fechas de Referencia:**
        *   `fecha_registro`: Fecha de grabado en SIE o fecha de ingreso laboral.
        *   `ref_col`: Fecha extraída de la columna 20 del archivo S1.
        *   `ref_var`: Fecha extraída del nombre del archivo S1.
    *   **Regla de Negocio:**
        Un registro se marca como **"R1 no SIE"** (posible novedad de relación laboral no registrada en SIE como subsidio) si:
        1.  La `fecha_registro` es posterior o igual a las fechas de referencia del archivo.
        2.  El usuario que grabó el registro **no** es 'Jhonatan.perez' (filtro de usuario específico).
        3.  Existe una fecha de ingreso laboral válida.
    *   En caso contrario, se clasifica como **"S1 SIE"**.

### 4.2. Generación de Reporte R1
Se extrae un subconjunto de datos para el reporte R1:
*   **Filtro:** Registros clasificados como "R1 no SIE" y que tengan el valor "F" en la columna 30 (indicador específico del archivo S1).
*   **Enriquecimiento:** Se añaden los datos del aportante (`tipo_documento_aportante`, `numero_identificacion_aportante`) desde la base de Relaciones Laborales.

---

## 5. Generación de Salidas (Outputs)

El script genera un archivo Excel consolidado (`Yesid-DD-MM-YYYY.xlsx`) con las siguientes hojas:

1.  **S1Automatico:** El archivo S1 completo con la clasificación "S1 SIE" / "R1 no SIE" y datos de cruce.
2.  **Df_R1:** Subconjunto de registros R1 con información de aportantes.
3.  **df_S1_Val:** Copia del archivo de validación S1 original.
4.  **df_S3:** Copia del archivo S3 original.

---

## 6. Guía de Mantenimiento

1.  **Rutas de Archivos:**
    *   Las rutas están definidas al inicio. Es crucial actualizarlas mensualmente o parametrizarlas, especialmente las rutas de red (`\\Servernas\...`).
2.  **Formatos de Fecha:**
    *   El script asume formatos específicos (`%Y/%m/%d %H:%M` para expedientes, `%Y-%m-%d` para relaciones laborales). Si los reportes fuente cambian de formato, el script fallará en la conversión `pd.to_datetime`.
3.  **Estructura de Archivos S1:**
    *   Se accede a columnas por índice (ej. `df_S1_Automatico.iloc[:, 20]`, `iloc[:, 30]`). Si la estructura del archivo plano S1 cambia (más o menos columnas), estos índices apuntarán a datos incorrectos. Se recomienda usar nombres de columnas si el archivo tiene encabezado, o definir un esquema fijo.
