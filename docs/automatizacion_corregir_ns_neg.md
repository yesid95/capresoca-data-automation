# Automatización de Corrección de Glosas de Novedades (Corregir NS-NEG.ipynb)

## 1. Descripción General
Este documento detalla el funcionamiento del notebook `Corregir NS-NEG.ipynb`, una herramienta crítica para la **depuración y corrección automática de glosas** (rechazos) generadas por la ADRES en el proceso de reporte de Novedades (NS).

El sistema analiza el archivo de respuestas negativas (`.NEG`), interpreta los códigos de error (Glosas) y aplica reglas de negocio para corregir la información, reclasificar el registro o descartarlo justificadamente. El objetivo es maximizar la aceptación de novedades en el siguiente ciclo de reporte.

### 🎯 Objetivo del Negocio
Reducir la carga operativa manual en la corrección de errores de reporte a la ADRES, asegurando la consistencia de la Base de Datos Única de Afiliados (BDUA) y evitando sanciones o pérdidas de recursos por inconsistencias en la información de los afiliados.

---

## 2. Stack Tecnológico
*   **Lenguaje:** Python 3.x
*   **Librerías Principales:**
    *   `pandas`: Motor principal de procesamiento de datos.
    *   `numpy`: Operaciones vectorizadas.
    *   `re`: Expresiones regulares para extraer datos correctos de los mensajes de error (glosas).
    *   `datetime` / `dateutil`: Manipulación de fechas y cálculo de ventanas de tiempo (regla de los 2 meses).
    *   `xlsxwriter`: Generación del reporte final consolidado en Excel.

---

## 3. Arquitectura del Pipeline

```mermaid
graph TD
    subgraph Entradas
        A[Archivo .NEG (Glosas ADRES)] --> P(Procesamiento)
        B[Maestros ADRES (EPS025/EPSC25)] --> P
        C[Novedades SIE (Nuevas)] --> P
    end

    subgraph Motor de Reglas [Corrección de Glosas]
        P --> G1{Análisis de Glosa}
        G1 -->|Datos Básicos| H[Corrección Automática]
        G1 -->|Entidad/Régimen| I[Reclasificación]
        G1 -->|Fechas| J[Ajuste Temporal]
        G1 -->|Irrecuperable| K[Descarte Justificado]
    end

    subgraph Salidas
        H --> L[Df_NS_Envio (Corregidos)]
        I --> M[DF_NS_EPSC25 (Contributivo)]
        J --> L
        K --> N[DF_No_Enviar (Auditoría)]
        G1 --> O[Df_NS_NEG (Pendientes)]
    end
```

---

## 4. Lógica de Negocio: Gestión de Glosas

El núcleo del notebook es una serie de funciones especializadas (`process_gnXXXX`) que atacan códigos de error específicos.

### 4.1. Corrección de Datos Básicos (Identidad)
ADRES devuelve el dato correcto en el mensaje de error. El script extrae este dato usando **Regex** y actualiza el registro.

| Código | Descripción | Acción Automática |
| :--- | :--- | :--- |
| **GN0034** | Primer Apellido errado | Extrae valor correcto de `GN0034(VALOR)` y actualiza `AFL_PRIMER_APELLIDO`. |
| **GN0035** | Segundo Apellido errado | Extrae valor correcto y actualiza `AFL_SEGUNDO_APELLIDO`. |
| **GN0036** | Primer Nombre errado | Extrae valor correcto y actualiza `AFL_PRIMER_NOMBRE`. |
| **GN0037** | Segundo Nombre errado | Extrae valor correcto y actualiza `AFL_SEGUNDO_NOMBRE`. |
| **GN0049** | Fecha Nacimiento errada | Extrae fecha correcta y actualiza `AFL_FECHA_NACIMIENTO`. |

### 4.2. Validación de Entidad y Régimen
Errores donde el afiliado parece pertenecer a otra EPS o régimen.

| Código | Descripción | Acción Automática |
| :--- | :--- | :--- |
| **GN0009** | Cotizante en otra entidad | Si es `EPSC25`, mueve a Contributivo. Si es otra EPS, mueve a `No_Enviar`. |
| **GN0030** | No pertenece a la entidad | Si la fecha de condición lo permite, ajusta fecha y mueve a Contributivo o descarta. |
| **GN0031** | No existe en BDUA | Si es novedad de entrada (`N01`) y no está en maestro, requiere validación manual. |

### 4.3. Reglas de Negocio Temporales
Validaciones de fechas según el Decreto 780 de 2016.

| Código | Descripción | Acción Automática |
| :--- | :--- | :--- |
| **GN0361** | Reporte extemporáneo (> 2 meses) | Ajusta la `FECHA_NOVEDAD` a la fecha mínima permitida (2 meses atrás). |
| **GN0084** | Fecha novedad < Fecha afiliación | Ajusta `FECHA_NOVEDAD` a `FechaInicioCondicion + 1 día`. |
| **GN0079** | Condición estudiante/discapacidad | Ajusta la fecha según el reporte de la glosa. |

### 4.4. Otras Validaciones Críticas
*   **GN0340 (IPS No Válida):** Mapea códigos internos de IPS a los códigos habilitados por REPS (ej. `001` -> `850010014401`).
*   **GN0059 / GN0169 (Datos RNEC):** Detecta inconsistencias graves con Registraduría. Se separan para auditoría manual (`DF_059_169`) o se limpian si es posible.

---

## 5. Estructura del Proyecto y Archivos

### 5.1. Entradas (Inputs)
Las rutas se configuran al inicio del script (Celda 2).
*   `R_Ms_ADRES_EPS025` / `_EPSC25`: Maestros de afiliados (Subsidiado/Contributivo).
*   `R_NS_NEG`: Archivo plano con las glosas recibidas de ADRES.
*   `R_NS_SIE`: Archivo plano con nuevas novedades generadas por el sistema interno.

### 5.2. Salidas (Outputs)
El script genera un archivo Excel consolidado (`DataFrames_Activos {Fecha}.xlsx`) con múltiples hojas:

1.  **Df_NS_Envio:** Registros corregidos y listos para generar el plano de envío.
2.  **Df_NS_NEG:** Registros que no pudieron corregirse automáticamente (requieren gestión humana).
3.  **DF_NS_EPSC25:** Registros identificados como pertenecientes al régimen Contributivo.
4.  **DF_No_Enviar:** Registros descartados definitivamente (fallecidos, otras EPS, duplicados).
5.  **DF_059_169:** Casos especiales de inconsistencia con Registraduría.

---

## 6. Guía de Mantenimiento

### 6.1. Actualización de Rutas y Fechas
Antes de cada ejecución, actualizar en la **Celda 2**:
```python
Fecha = "12/12/2025"  # Fecha del proceso
F_Envio = "12122025"  # Sufijo para el archivo de salida
R_NS_NEG = r"..."     # Ruta del archivo de glosas actual
```

### 6.2. Agregar Nuevas Reglas de Glosa
Para automatizar una nueva glosa (ej. `GN9999`):
1.  Crear una función `process_gn9999(df, ...)` siguiendo el patrón de las existentes.
2.  Implementar la lógica de extracción (Regex) o decisión.
3.  Invocar la función en el bloque principal de procesamiento.

### 6.3. Mapeo de IPS (GN0340)
Si se habilitan nuevas sedes o cambian los códigos REPS, actualizar el diccionario `ips_map` dentro de la función `process_gn0340`.

```python
ips_map = {
    "001": "850010014401",
    # Agregar nuevos mapeos aquí
}
```
