# Automatización de Gestión de Cartera y Recaudo (Cartera.ipynb)

## 1. Descripción General
Este documento detalla el funcionamiento del notebook `Cartera.ipynb`, diseñado para la **identificación, clasificación y gestión de la cartera de afiliados** al régimen contributivo de Capresoca EPS.

El sistema consolida información de múltiples fuentes (PILA Operador, PILA ADRES, Maestro de Afiliados y Bases Internas) para determinar el estado de pago de cada afiliado, clasificándolos en **Mora**, **Aviso** o **Sin Pagos**. El resultado final es un insumo crítico para las estrategias de cobro, notificación y depuración de base de datos.

### 🎯 Objetivo del Negocio
Optimizar el recaudo de aportes mediante la identificación precisa de deudores y la generación de bases de datos enriquecidas con información de contacto validada, cumpliendo con la normatividad vigente (Decreto 780 de 2016).

---

## 2. Stack Tecnológico
*   **Lenguaje:** Python 3.x
*   **Librerías Principales:**
    *   `pandas`: Manipulación y análisis de grandes volúmenes de datos.
    *   `numpy`: Operaciones numéricas eficientes.
    *   `glob`: Búsqueda de archivos en directorios.
    *   `re`: Expresiones regulares para validación de correos y teléfonos.
    *   `xlsxwriter`: Generación de reportes en Excel con formato avanzado.
    *   `openpyxl`: Lectura y escritura de archivos Excel.

---

## 3. Arquitectura del Pipeline

El flujo de datos sigue un proceso ETL (Extract, Transform, Load) robusto:

```mermaid
graph TD
    subgraph Fuentes [Fuentes de Datos]
        A[PILA Interna (I/IP)] -->|TXT| B(Unificación PILA)
        C[PILA ADRES (3047)] -->|TXT| B
        D[Maestro ADRES] -->|TXT| E(Filtrado Activos)
        F[SIE Relaciones Laborales] -->|CSV| G(Enriquecimiento)
        H[SIE Maestro] -->|CSV| G
    end

    subgraph Procesamiento [Transformación y Lógica]
        B --> I{Limpieza y Normalización}
        E --> I
        I --> J[Cruce de Información]
        J --> K[Identificación Sin Pagos]
        J --> L[Cálculo de Mora/Aviso]
        K --> M[Consolidación Final]
        L --> M
        M --> N[Validación Contacto]
    end

    subgraph Salida [Entregables]
        N --> O[Reporte Excel (.xlsx)]
        O --> P[Hoja: Cartera Consolidada]
        O --> Q[Hoja: Logs Auditoría]
        O --> R[Hoja: KPIs]
    end
```

---

## 4. Lógica de Negocio Detallada

### 4.1. Unificación de Fuentes PILA
El sistema integra dos flujos de información de pagos:
1.  **PILA Interna (SIE):** Archivos planos generados por el sistema de información de la EPS (`Pila I` y `Pila IP`).
2.  **PILA Conciliada (ADRES):** Archivo 3047 que contiene los pagos reconocidos por el ente rector.

**Regla de Negocio:** Se prioriza la estructura interna para el análisis, homologando los nombres de columnas del archivo ADRES para permitir una concatenación vertical perfecta.

### 4.2. Identificación de "Sin Pagos"
Se detectan afiliados que, estando **Activos** en el sistema, no registran pagos recientes.

*   **Universo:** Afiliados en Maestro ADRES con estado `AC` (Activo) y tipo `C` (Cotizante).
*   **Condición:** No cruzan con la base consolidada de PILA (ni interna ni ADRES).
*   **Acción:** Se marcan como "Sin Pagos" y se les imputa un origen de datos "MC_ADRES".

### 4.3. Clasificación de Cartera (Mora vs. Aviso)
La clasificación se basa en la comparación entre la fecha del último pago (`Periodo Pago`) y las fechas de corte definidas paramétricamente.

**Variables de Corte (Ejemplo):**
*   `V_Periodo_Actual`: Fecha de referencia del proceso (ej. 2025-06-01).
*   `Mora`: Fecha límite para considerar mora (ej. 2025-05-01).
*   `Dia`: Fecha límite para considerar al día (ej. 2025-06-01).

**Algoritmo de Clasificación:**

| Estado | Condición Lógica | Interpretación |
| :--- | :--- | :--- |
| **Sin Pagos** | `Periodo Pago` es Nulo/Vacío | Afiliado activo sin registro histórico de pago. |
| **Mora** | `Periodo Pago` < `Mora` | El último pago es anterior al mes de corte de mora (más de 30 días de retraso). |
| **Aviso** | `Mora` ≤ `Periodo Pago` < `Dia` | El pago es reciente pero no cubre el periodo actual (riesgo de entrar en mora). |
| **Al Día** | `Periodo Pago` ≥ `Dia` | El afiliado tiene sus pagos cubiertos hasta la fecha actual. |

### 4.4. Validación de Datos de Contacto
Para asegurar la efectividad de la gestión de cobranza, se aplican validaciones estrictas:

*   **Correos Electrónicos:**
    *   Se rechazan dominios falsos (`a@a.com`, `no@tiene.com`).
    *   Se validan sintaxis (`regex`) y longitud mínima.
    *   Se buscan palabras clave inválidas (`prueba`, `test`, `actualizar`).

*   **Teléfonos:**
    *   **Móviles:** Deben iniciar con `3` y tener 10 dígitos.
    *   **Fijos:** Deben iniciar con `60` + indicativo y tener 10 dígitos.
    *   **Líneas 01800:** Deben tener 11 dígitos.
    *   **Líneas de Emergencia:** Se descartan números como `123`, `112`, etc.

---

## 5. Estructura del Proyecto y Archivos

### 5.1. Entradas (Inputs)
| Variable | Descripción | Fuente |
| :--- | :--- | :--- |
| `R_Pila_I_SIE` | Carpeta con TXTs de PILA Interna. | Servidor NAS |
| `R_Pila3047` | Archivo TXT de PILA Conciliada ADRES. | Servidor NAS |
| `R_MaestroAdres` | Maestro de afiliados contributivos. | Servidor NAS |
| `R_Relaciones_Laborales_SIE` | CSV con vínculos laborales. | Servidor NAS |
| `R_Ms_SIE` | Maestro interno para enriquecimiento. | Servidor NAS |

### 5.2. Salidas (Outputs)
*   **Archivo Excel (`Proceso.xlsx`):**
    *   **Sheet `Cartera Consolidada`:** Base maestra con todos los afiliados y su estado.
    *   **Sheet `Logs_3047` / `Logs_PILA`:** Trazabilidad de los archivos insumo utilizados.
    *   **Sheet `Resumen_KPIs`:** Tablero de control con métricas de la ejecución.

---

## 6. Guía de Mantenimiento

### 6.1. Actualización de Fechas de Corte
Al inicio de cada mes, se deben actualizar las variables de tiempo en la **Celda 3**:
```python
V_Periodo_Actual = "2025-07-01" # Primer día del mes actual
Dia = "2025-07-01"              # Fecha de corte para estar al día
Mora = "2025-06-01"             # Fecha de corte para entrar en mora
```

### 6.2. Gestión de Rutas
Si cambian las ubicaciones de los archivos en el servidor, actualizar las variables en la **Celda 5** (`R_MaestroAdres`, `R_Pila3047`, etc.).

### 6.3. Ajuste de Reglas de Validación
*   Para agregar nuevos correos inválidos, editar la lista `CORREOS_INVALIDOS_EXACTOS` en la sección de validación de correos.
*   Para ajustar reglas de teléfonos, modificar la función `validar_telefono_co`.

### 6.4. Solución de Problemas Comunes
*   **Error de Memoria:** Si el volumen de datos crece, considerar usar `chunksize` en la lectura de pandas o procesar por lotes.
*   **Error de Codificación:** Si los archivos TXT cambian de origen, verificar si la codificación es `ANSI`, `UTF-8` o `UTF-16` y ajustar el parámetro `encoding` en `pd.read_csv`.
