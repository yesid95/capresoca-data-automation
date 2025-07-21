# Convenciones de Código y Estructura

Este documento establece las convenciones de codificación, estilo y estructura que se seguirán en este proyecto. El objetivo es garantizar que el código sea limpio, consistente y fácil de mantener.

---

## 1. Estilo de Código

### 1.1. PEP 8

Todo el código Python debe adherirse a las guías de estilo de [PEP 8](https://www.python.org/dev/peps/pep-0008/).

### 1.2. Herramientas de Calidad de Código

Para garantizar la consistencia de forma automática, se recomienda el uso de las siguientes herramientas:

-   **`black`**: Para el formateo automático del código. Un código sin `black` no debería ser aceptado en un pull request.
-   **`flake8`**: Para la detección de errores de lógica, complejidad y estilo (linting).

### 1.3. Longitud de Línea

La longitud máxima de una línea de código será de **88 caracteres**, para ser compatible con el formateador `black`.

---

## 2. Convenciones de Nomenclatura

-   **Módulos**: Nombres cortos, en minúsculas y con guiones bajos si es necesario. Ejemplo: `file_loader.py`.
-   **Clases**: Nombres en `PascalCase`. Ejemplo: `BduaReportProcessor`.
-   **Funciones y Métodos**: Nombres en `snake_case`. Ejemplo: `cargar_maestro_adres()`.
-   **Variables**: Nombres en `snake_case`. Ejemplo: `df_maestro`.
-   **Constantes**: Nombres en `UPPER_SNAKE_CASE`. Ejemplo: `DEFAULT_HIERARCHY`.

---

## 3. Docstrings

Todos los módulos, funciones, clases y métodos públicos deben tener un `docstring` que explique su propósito y uso.

Se seguirá el **estilo de Google** para los docstrings, ya que es legible y completo.

### Ejemplo de Docstring (Función):

```python
def mi_funcion(param1, param2):
    """Descripción concisa de lo que hace la función.

    Args:
        param1 (str): Descripción del primer parámetro.
        param2 (int): Descripción del segundo parámetro.

    Returns:
        bool: Descripción de lo que retorna la función.

    Raises:
        ValueError: Si `param2` es negativo.
    """
    # ... código de la función
```

---

## 4. Estructura de Carpetas

El proyecto seguirá la siguiente estructura de directorios:

```txt
capresoca-data-automation/
│
├── data/         # Datos de entrada, salida e intermedios (no versionados)
├── docs/         # Documentación del proyecto (.md)
├── notebooks/    # Jupyter Notebooks para exploración y prototipado
├── src/          # Código fuente reutilizable de la aplicación
│   └── utils/    # (Opcional) Sub-módulos para utilidades genéricas
├── tests/        # Pruebas unitarias y de integración
├── venv/         # Entorno virtual de Python (no versionado)
├── .gitignore
├── requirements.txt
└── README.md
```
