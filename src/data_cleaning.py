# -*- coding: utf-8 -*-
"""
data_cleaning.py

Módulo para el procesamiento y limpieza de datos para reportes.

Este módulo contiene la clase BduaReportProcessor, diseñada para encapsular
la lógica de negocio específica para la preparación y validación de archivos
de la Base de Datos Única de Afiliados (BDUA) en Capresoca EPS;
# y la clase DataCleaner, diseñada
para realizar operaciones comunes de limpieza de datos en DataFrames de Pandas.
particularmente para los reportes enviados a ADRES.
En el futuro se ira generando mas funciones y clases que permitan automatizar procesos
de limpieza y validación de datos, asegurando que los reportes cumplan
# con los requicitos de ADRES
o de gestion interna de la EPS

Autor: Ingeniero Yesid
Fecha de creación: 2025-07-15
"""

from pandas.api.types import is_datetime64_any_dtype as is_datetime
import pandas as pd

import re


class BduaReportProcessor:
    """
    Agrupa la lógica de negocio para la preparación de archivos BDUA.

    Esta clase toma un DataFrame de Pandas y aplica una serie de
    transformaciones específicas del proceso BDUA, como la limpieza
    y priorización de marcas de población (censos, SISBEN).

    **Uso:**
    >>> import pandas as pd
    >>> data = {'afiliado_id': [1, 2, 3],
    ...         'marcas_poblacion': ['LC(9|17)-SIV(C08)', 'SIV(D01)', 'LC(0)']}
    >>> df = pd.DataFrame(data)
    >>>
    >>> processor = BduaReportProcessor(df=df)
    >>> df_limpio = processor.prioritize_population_markers(col_name='marcas_poblacion')
    >>> print(df_limpio)
       afiliado_id marcas_poblacion
    0            1            LC(9)
    1            2         Sisben D
    2            3
    """

    def __init__(self, df: pd.DataFrame, population_hierarchy: list = None):
        """
        Inicializa el procesador con los datos y la configuración necesaria.

        Args:
            df (pd.DataFrame): El DataFrame con los datos de afiliados a procesar.
            population_hierarchy (list, optional): Una lista de strings que define
                el orden de prioridad para los listados censales (LC). Si no se
                provee, se utilizará una jerarquía estándar.
        """
        if not isinstance(df, pd.DataFrame):
            raise TypeError("El input 'df' debe ser un DataFrame de Pandas.")

        self.df = df.copy()

        # Se establece la jerarquía de población como un atributo de la instancia
        if population_hierarchy is None:
            self.hierarchy = ["9", "17", "28", "2", "1"]
        else:
            self.hierarchy = population_hierarchy

    def prioritize_population_markers(self, col_name: str) -> pd.DataFrame:
        """
        Limpia y prioriza las marcas de población según las reglas de negocio.

        Este método procesa una columna que contiene múltiples marcas de población
        concatenadas (p. ej., "LC(9|16)-SIV(C08)") y devuelve solo la marca de
        mayor prioridad según la jerarquía definida.

        Args:
            col_name (str): El nombre de la columna que contiene las marcas de
                            población a procesar.

        Returns:
            pd.DataFrame: Un nuevo DataFrame con la columna de marcas procesada y
                          limpia. El DataFrame original no es modificado.
        """
        processed_df = self.df.copy()

        # Se define la lógica de limpieza como una función interna para mayor claridad.
        def _process_value(value: str) -> str:
            """Función auxiliar que procesa un único valor de la columna."""
            if pd.isna(value):
                return value

            # Aseguramos que el valor es un string para aplicar regex
            original_value = str(value)

            # Regla 1: Reemplazar si es exactamente SIV(Dnn) -> Sisben IV Grupo D
            if re.fullmatch(r"SIV\(D\d{2}\)", original_value.strip()):
                return "Sisben D"

            # Regla 2: Eliminar sufijos de SISBEN III y IV que acompañan a un listado
            # censal
            processed_value = re.sub(
                r"-SIV\([^\)]*\)|-SIII\([^\)]*\)", "", original_value
            )

            # Regla 3: Si después de limpiar solo queda una marca de SISBEN III, se
            # elimina
            if re.fullmatch(r"SIII\([^\)]*\)", processed_value.strip()):
                return ""

            # Regla 4: Eliminar el prefijo 'LC(0)-' que indica sin clasificación
            if processed_value.startswith("LC(0)-"):
                processed_value = processed_value.replace("LC(0)-", "")

            # Regla 5: Si el único valor es 'LC(0)', se considera sin marca
            if processed_value.strip() == "LC(0)":
                return ""

            # Regla 6: Normalizar y priorizar listados censales múltiples
            # (p. ej., "LC(9|17)")
            def _prioritize_lc(match: re.Match) -> str:
                """Función interna para aplicar la jerarquía a los códigos LC."""
                codes_str = match.group(1)
                codes = [c.strip() for c in codes_str.split("|")]

                if len(codes) == 1:
                    return f"LC({codes[0]})"

                # Iterar sobre la jerarquía para encontrar la mayor prioridad
                for priority_code in self.hierarchy:
                    if priority_code in codes:
                        return f"LC({priority_code})"

                return ""  # Si ningún código coincide con la jerarquía, se elimina

            processed_value = re.sub(r"LC\(([^\)]*)\)", _prioritize_lc, processed_value)

            return processed_value.strip()

        # Aplicar la función de procesamiento a toda la columna
        processed_df[col_name] = processed_df[col_name].apply(_process_value)

        return processed_df


class DataCleaner:
    """
    Clase para encapsular operaciones comunes de limpieza de datos.

    Se inicializa con un DataFrame y sus métodos aplican transformaciones
    devolviendo un nuevo DataFrame modificado.
    """

    def __init__(self, df: pd.DataFrame):
        """
        Inicializa el limpiador con un DataFrame.

        Args:
            df (pd.DataFrame): El DataFrame que se va a procesar.
        """
        if not isinstance(df, pd.DataFrame):
            raise TypeError("El input debe ser un DataFrame de Pandas.")
        self.df = df.copy()

    def process_date_column(self, column_name: str) -> pd.DataFrame:
        """
        Convierte de forma robusta una columna a formato datetime.

        Maneja columnas que ya son datetime y formatos con distintos
        separadores (dd/mm/yyyy o dd-mm-yyyy), priorizando el día primero.

        Args:
            column_name (str): El nombre de la columna a convertir.

        Returns:
            pd.DataFrame: Un nuevo DataFrame con la columna ya convertida.
        """
        print(f"INFO: Procesando la columna de fecha '{column_name}'...")

        # Copiamos el df para no modificar el original de la instancia
        df_copy = self.df.copy()
        column_series = df_copy[column_name]

        # 1. Verificar si ya es formato datetime
        if is_datetime(column_series):
            print(
                "INFO: La columna ya es datetime. No se requiere conversión."
            )
            return df_copy

        # 2. Convertir la columna
        converted_series = pd.to_datetime(column_series, errors="coerce", dayfirst=True)

        # 3. Reportar errores y actualizar el DataFrame
        original_nulls = column_series.isna().sum()
        new_nulls = converted_series.isna().sum()
        errors_found = new_nulls - original_nulls

        if errors_found > 0:
            print(
                f"ADVERTENCIA: {errors_found} fechas no válidas se convirtieron a NaT."
            )

        df_copy[column_name] = converted_series
        print("INFO: Conversión finalizada.")

        return df_copy
