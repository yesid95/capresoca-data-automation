# Documentación de Funciones y Clases

Este documento detalla las funciones y clases reutilizables disponibles en el directorio `/src`. El objetivo es proporcionar una referencia clara para que los desarrolladores puedan utilizar estos componentes de forma efectiva.

---

## 1. Módulo: `file_loader.py`

Responsable de la carga de archivos de datos, especialmente los maestros de ADRES.

### 1.1. `cargar_maestro_ADRES(ruta_maestro)`

Carga un único archivo maestro en formato `.txt` separado por comas y sin encabezados.

-   **Parámetros**:
    -   `ruta_maestro` (str): Ruta completa del archivo a cargar.
-   **Retorna**:
    -   `pd.DataFrame`: Un DataFrame de Pandas con los datos y encabezados asignados.
    -   `None`: Si ocurre un error durante la carga (ej. archivo no encontrado, formato incorrecto).
-   **Ejemplo de uso**:

```python
from src.file_loader import cargar_maestro_ADRES

df_maestro = cargar_maestro_ADRES('data/input/MAESTRO_ADRES_202501.txt')

if df_maestro is not None:
    print(df_maestro.head())
```

### 1.2. `cargar_maestros_ADRES(ruta_maestro1, ruta_maestro2)`

Carga y combina dos archivos maestros de ADRES con las mismas características que la función anterior.

-   **Parámetros**:
    -   `ruta_maestro1` (str): Ruta del primer archivo.
    -   `ruta_maestro2` (str): Ruta del segundo archivo.
-   **Retorna**:
    -   `pd.DataFrame`: Un DataFrame combinado con los datos de ambos archivos.
    -   `None`: Si ocurre un error.
-   **Ejemplo de uso**:

```python
from src.file_loader import cargar_maestros_ADRES

df_combinado = cargar_maestros_ADRES('data/input/MAESTRO1.txt', 'data/input/MAESTRO2.txt')

if df_combinado is not None:
    print(f"Total de registros combinados: {len(df_combinado)}")
```

---

## 2. Módulo: `data_cleaning.py`

Contiene clases para la limpieza y transformación de datos según las reglas de negocio.

### 2.1. Clase `DataCleaner`

Encapsula operaciones comunes de limpieza de datos.

-   **Inicialización**:
    -   `DataCleaner(df: pd.DataFrame)`: Se instancia con un DataFrame de Pandas.

-   **Métodos**:
    -   `process_date_column(column_name: str)`: Convierte una columna a formato `datetime` de manera robusta, manejando múltiples formatos de entrada.
        -   **Retorna**: Un nuevo DataFrame con la columna convertida.

-   **Ejemplo de uso**:

```python
from src.data_cleaning import DataCleaner
import pandas as pd

data = {'fecha_nacimiento': ['25/12/1990', '1995-05-15', 'fecha_invalida']}
df = pd.DataFrame(data)

cleaner = DataCleaner(df)
df_limpio = cleaner.process_date_column('fecha_nacimiento')

print(df_limpio.dtypes)
```

### 2.2. Clase `BduaReportProcessor`

Agrupa la lógica de negocio específica para la preparación de archivos BDUA.

-   **Inicialización**:
    -   `BduaReportProcessor(df: pd.DataFrame, population_hierarchy: list = None)`: Se instancia con un DataFrame y una lista opcional que define la jerarquía de prioridad para los listados censales.

-   **Métodos**:
    -   `prioritize_population_markers(col_name: str)`: Limpia y prioriza una columna que contiene múltiples marcas de población (ej. `"LC(9|17)-SIV(C08)"`) basándose en una jerarquía predefinida.
        -   **Retorna**: Un nuevo DataFrame con la columna de marcas procesada.

-   **Ejemplo de uso**:

```python
from src.data_cleaning import BduaReportProcessor
import pandas as pd

data = {'marcas': ['LC(9|17)-SIV(C08)', 'SIV(D01)', 'LC(0)']}
df = pd.DataFrame(data)

# Usar jerarquía por defecto: ['9', '17', '28', '2', '1']
processor = BduaReportProcessor(df)
df_procesado = processor.prioritize_population_markers('marcas')

print(df_procesado)
#   marcas
# 0  LC(9)
# 1  Sisben D
# 2
```
