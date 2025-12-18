# Documentación Técnica: Validación y Depuración SIE vs ADRES

**Archivo:** `notebooks/Aseguramiento/Validar SIE.ipynb`  
**Nivel:** Técnico / Ingeniería de Datos  
**Audiencia:** Junior a Senior

---

## 1. Introducción y Objetivo
Este notebook implementa un proceso ETL (Extract, Transform, Load) crítico para el aseguramiento de la calidad de datos en salud. Su objetivo principal es **cruzar, validar y auditar** la información del Sistema de Información de la EPS (SIE) contra la Base de Datos Única de Afiliados (BDUA/ADRES).

El resultado final es la generación automática de archivos planos de novedades (N01, N02, N03, etc.) listos para ser reportados a los entes de control, así como reportes de inconsistencias para gestión interna.

## 2. Stack Tecnológico
*   **Python 3.x**: Lenguaje base.
*   **Pandas**: Manipulación masiva de datos (DataFrames).
*   **Numpy**: Operaciones vectorizadas y lógica condicional (`np.select`).
*   **Zipfile / Shutil**: Manejo de archivos comprimidos y operaciones de sistema de archivos.
*   **Matplotlib**: Visualización básica de inconsistencias.

---

## 3. Arquitectura del Pipeline

### 3.1. Fase de Extracción (Carga de Datos)
El script ingesta múltiples fuentes de información, tanto archivos planos (`.TXT`, `.CSV`) como comprimidos (`.ZIP`).

**Fuentes Principales:**
1.  **Maestro SIE:** Reporte de validación de archivos maestros (`.csv`).
2.  **Maestro ADRES:** Archivos maestros del régimen subsidiado (EPS025) y contributivo (EPSC25).
3.  **Históricos ADRES:** Archivos comprimidos (`.ZIP`) que contienen el histórico de identificación y grupos familiares.
4.  **Tablas de Referencia:** Municipios DANE, códigos de parentesco, estados de afiliación, regímenes, etc.

**Técnicas Clave:**
*   **Lectura desde ZIP en memoria:** Se utiliza una función personalizada `load_txt_from_zip` para leer archivos `.TXT` directamente desde un `.ZIP` sin descomprimirlos en disco, optimizando I/O.
*   **Manejo de Codificación:** Se especifica `encoding='ANSI'` (cp1252) para la mayoría de archivos legacy, evitando errores de lectura (`UnicodeDecodeError`).
*   **Tipado Fuerte:** Se fuerza `dtype=str` en la lectura para preservar ceros a la izquierda en documentos de identidad y códigos DANE.

### 3.2. Fase de Transformación y Limpieza

#### 3.2.1. Limpieza de Expedientes SIE
*   **Filtrado:** Solo se conservan expedientes con estado 'Cerrado'.
*   **Deduplicación:** Se ordena por fecha de grabado y se mantiene el último registro (`keep='last'`) para tener la foto más reciente.

#### 3.2.2. Consolidación ADRES
*   Se concatenan los maestros de EPS025 (Subsidiado) y EPSC25 (Contributivo) en un único DataFrame `DF_ADRES`.
*   Se realiza un proceso similar para los históricos de identificación y grupos familiares.

#### 3.2.3. Enriquecimiento del Maestro SIE
El DataFrame principal `Df_SIE` se enriquece cruzando información:
1.  **Cruce con Histórico Identificación:** Para obtener el ID BDUA (`AFL_ID`).
2.  **Mapeo de Códigos:** Se traducen códigos internos del SIE a códigos estándar ADRES (Resolución 762/2023) usando diccionarios de mapeo (Parentesco, Estado, Régimen).
3.  **Normalización Geográfica:** Se cruza con la tabla de municipios para obtener códigos DANE estandarizados.
4.  **Cruce con Maestro ADRES:** Se trae toda la información de ADRES (`how='left'`) para comparar campo a campo.

---

## 4. Módulos de Validación (Lógica de Negocio)

El núcleo del script son las reglas de validación que detectan inconsistencias y generan novedades.

### 4.1. Detección de Duplicados (`Validar_Duplicidad`)
Identifica si un mismo `AFL_ID` aparece múltiples veces en el SIE.
*   **Lógica:** `Df_SIE.duplicated("AFL_ID", keep=False)`
*   **Categorías:** "Registro Duplicado SIE", "Registro unico SIE", "Registro Sin ID".

### 4.2. Novedad N14: Activo SIE, No Existe en ADRES
Usuarios que la EPS tiene activos pero ADRES no reconoce.
*   **Regla:** Estado SIE = 'AC', Régimen = 'EPS025', Estado Traslado = 'No Aplica', y no cruza con ADRES.
*   **Acción:** Genera novedad N14 (Retiro) con motivo "Activos SIE: RE, DS, SM O NO ADRES".
*   **Corrección de Fechas:** Rellena fechas nulas con la fecha actual (`pd.Timestamp.now()`).

### 4.3. Novedad N09: Fallecidos
Usuarios activos en SIE pero marcados como fallecidos (`TPS_EST_AFL_ID == 'AF'`) en ADRES.
*   **Acción:** Genera novedad N09 para actualizar el estado en el sistema.

### 4.4. Novedad I02: Inconsistencia de Serial
Verifica si el `serial_fosyga` coincide con el `AFL_ID`.
*   **Regla:** `Df_SIE["serial_fosyga"] != Df_SIE["AFL_ID"]`.
*   **Salida:** Archivo plano I02 para corrección de seriales.

### 4.5. Validación de Grupos Familiares
Compara la cabeza de familia reportada en SIE vs ADRES.
*   **Casos:**
    *   "Es Cabeza de familia" (Padre vacío).
    *   "Cabeza de familia igual/diferente".
    *   "SIE con cabeza, ADRES sin cabeza" (y viceversa).

### 4.6. Novedades de Datos Básicos (N01, N02, N03, N21)
Comparación campo a campo entre SIE y ADRES.
*   **N01 (Tipo Documento):** Detecta evoluciones (ej. TI -> CC). Incluye lógica para validar evoluciones permitidas ("CN"->"RC", "TI"->"CC") e intercambiar valores si es necesario.
*   **N02 (Nombres) y N03 (Apellidos):** Normaliza cadenas (trim, lower) y compara. Si difieren, genera novedad de actualización.
*   **N21 (Sisbén):** Valida inconsistencias en Grupo Poblacional y Nivel Sisbén IV. Implementa lógica compleja para asignar códigos de novedad (1, 2, 3, N) según el tipo de cambio.

### 4.7. Novedad I03: Traslados Pendientes
Identifica usuarios en proceso de traslado ("Pendiente Ingreso") que ya están activos en ADRES.

---

## 5. Generación de Salidas (Loading)

### 5.1. Archivos Planos (.TXT)
El script genera archivos planos separados por tipo de novedad y agrupados por Departamento (`DPR_ID`).
*   **Estructura:** Archivos sin encabezado, separador coma (`,`), codificación ANSI.
*   **Ruta:** `.../11_Noviembre/YESID/{TIPO_NOVEDAD}/{TIPO_NOVEDAD}_{DEPTO}.TXT`
*   **Automatización:** Itera sobre cada DataFrame de novedad (`df_N01`, `df_N02`, etc.) y agrupa por departamento para crear los archivos fragmentados requeridos por el validador.

### 5.2. Reporte Consolidado (.xlsx)
Genera un libro de Excel `Reporte SIE.xlsx` con múltiples hojas:
*   **Resumen:** Conteo de registros por tipo de novedad.
*   **Detalle:** Hojas individuales para cada DataFrame (`MS_SIE`, `DF_ADRES`, `N01`, `N02`, etc.) para auditoría manual.

---

## 6. Guía de Mantenimiento y Troubleshooting

1.  **Errores de Lectura (Encoding):**
    *   Si falla la carga de archivos planos, verificar si el archivo origen cambió de `ANSI` a `UTF-8`. Ajustar el parámetro `encoding` en `pd.read_csv`.
2.  **Cambios en Estructura de Archivos:**
    *   Si ADRES cambia el orden o nombre de columnas en los maestros, actualizar las listas `new_columns` en la sección de carga.
3.  **Fechas Inválidas:**
    *   El script maneja fechas inválidas (`errors='coerce'`) convirtiéndolas a `NaT` o strings "Fecha no validad". Revisar los logs de conteo de fechas inválidas si aumentan drásticamente.
4.  **Rutas de Archivos:**
    *   Las rutas están hardcodeadas (`C:\Users\osmarrincon\...`). Para producción, se recomienda usar rutas relativas o variables de entorno.

---

## 7. Glosario de Variables Clave
*   `AFL_ID`: Identificador único del afiliado (BDUA).
*   `ENT_ID`: Código de la entidad (EPS).
*   `TPS_IDN_ID`: Tipo de documento.
*   `HST_IDN_NUMERO_IDENTIFICACION`: Número de documento.
*   `DPR_ID`: Código Departamento.
*   `MNC_ID`: Código Municipio.
