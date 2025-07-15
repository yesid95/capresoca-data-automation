'''
data_cleaning.py

Módulo de limpieza y transformación de datos

Este módulo agrupa funciones y clases reutilizables para:
  - Limpieza de datos (imputación de valores faltantes, eliminación de duplicados)
  - Transformaciones comunes (normalización, encoding, formato de fechas)
  - Validaciones y reportes básicos de calidad de datos

Autor: Ingeniero Yesid
Fecha de creación: 2025-07-15
'''  

import pandas as pd
import numpy as np


class DataCleaner:
    """
    Clase para limpiar y transformar DataFrames de EPS.

    Entre sus responsabilidades también incluye **priorizar el tipo de población** 
    cuando un afiliado aparece en múltiples listados sensales y en SISBÉN
    (todo viene en una sola cadena, p. ej. "LC(9|16)-SIV(C08)").

    El método `prioritize_population(col_name)`:
      - Toma la cadena compuesta.
      - Extrae las etiquetas sensales (p.ej. “LC(9)”, “LC(16)”) y SISBÉN (“SIV(C08)”).
      - Devuelve solo la etiqueta de **mayor prioridad** (por negocio, p.ej. sensal > SISBÉN),
        por ejemplo “LC(9)”.

    Uso:
        # Añadir la carpeta raíz del proyecto al sys.path para importar módulos personalizados
        sys.path.append(os.path.abspath("c:/Users/osmarrincon/Documents/capresoca-data-automation"))

        from src.data_cleaning import PoblacionCleaner     # Clase para limpiar y normalizar población

        maestro_ADRES["MARCASISBENIV+MARCASISBENIII"] = maestro_ADRES["MARCASISBENIV+MARCASISBENIII"].apply(cleaner.limpiar)  # LLamado a la clase
    """

    def __init__(self, df: pd.DataFrame):
        """
        Inicializa el DataCleaner con un DataFrame.

        Args:
            df (pd.DataFrame): DataFrame original.
        """
        if not isinstance(df, pd.DataFrame):
            raise TypeError("df debe ser un pandas DataFrame")
        self.df = df.copy()

    def drop_null_fraction(self, threshold: float) -> pd.DataFrame:
        """
        Elimina columnas con proporción de valores nulos superior al umbral.

        Args:
            threshold (float): Proporción máxima de nulos permitida (0.0 - 1.0).

        Returns:
            pd.DataFrame: DataFrame filtrado.
        """
        null_frac = self.df.isna().mean()
        cols_to_drop = null_frac[null_frac > threshold].index
        return self.df.drop(columns=cols_to_drop)

    def fill_with_constant(self, columns: list, value) -> pd.DataFrame:
        """
        Rellena NA en columnas seleccionadas con un valor constante.

        Args:
            columns (list): Lista de nombres de columnas.
            value: Valor a usar en la imputación.

        Returns:
            pd.DataFrame: DataFrame con valores imputados.
        """
        df = self.df.copy()
        for col in columns:
            df[col] = df[col].fillna(value)
        return df

    def remove_duplicates(self, subset: list = None, keep: str = 'first') -> pd.DataFrame:
        """
        Elimina filas duplicadas.

        Args:
            subset (list, optional): Columnas a considerar para duplicidad. Por defecto None (todas).
            keep (str): {'first', 'last', False} Decide qué duplicados mantener.

        Returns:
            pd.DataFrame: DataFrame sin filas duplicadas.
        """
        return self.df.drop_duplicates(subset=subset, keep=keep)

    def normalize_columns(self, columns: list) -> pd.DataFrame:
        """
        Escala valores numéricos de columnas al rango [0,1].

        Args:
            columns (list): Columnas numéricas a normalizar.

        Returns:
            pd.DataFrame: DataFrame con columnas normalizadas.
        """
        df = self.df.copy()
        for col in columns:
            minval = df[col].min()
            maxval = df[col].max()
            df[col] = (df[col] - minval) / (maxval - minval)
        return df

    def parse_dates(self, columns: list, fmt: str = '%Y-%m-%d') -> pd.DataFrame:
        """
        Convierte strings a datetime usando el formato especificado.

        Args:
            columns (list): Columnas de fechas en formato string.
            fmt (str): Formato de fecha (por defecto "%Y-%m-%d").

        Returns:
            pd.DataFrame: DataFrame con columnas datetime.
        """
        df = self.df.copy()
        for col in columns:
            df[col] = pd.to_datetime(df[col], format=fmt, errors='coerce')
        return df




