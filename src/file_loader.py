import pandas as pd


def cargar_maestros_ADRES(ruta_maestro1, ruta_maestro2):
    """
    Carga y combina dos archivos maestros .txt sin encabezados, separador
    coma, codificación ANSI.
    Asigna encabezados personalizados al final para evitar errores por nombres
    duplicados.

    Args:
        ruta_maestro1 (str): Ruta del primer archivo.
        ruta_maestro2 (str): Ruta del segundo archivo.

    Returns:
        pd.DataFrame | None: DataFrame combinado o None si ocurre un error.
    """
    encabezados = [
        "AFL_ID",
        "ENT_ID",
        "TPS_IDN_ID_CF",
        "HST_IDN_NUMERO_IDENTIFICACION_CF",
        "TPS_IDN_ID",
        "HST_IDN_NUMERO_IDENTIFICACION",
        "AFL_PRIMER_APELLIDO",
        "AFL_SEGUNDO_APELLIDO",
        "AFL_PRIMER_NOMBRE",
        "AFL_SEGUNDO_NOMBRE",
        "AFL_FECHA_NACIMIENTO",
        "TPS_GNR_ID",
        "AFL_PAIS_NACIMIENTO",
        "AFL_MUNICIPIO_NACIMIENTO",
        "AFL_NACIONALIDAD",
        "AFL_SEXO_IDENTIFICACION",
        "AFL_DISCAPACIDAD",
        "TPS_AFL_ID",
        "TPS_PRN_ID",
        "TPS_GRP_PBL_ID",
        "TPS_NVL_SSB_ID",
        "NUMEROFICHASISBEN",
        "TPS_CND_BNF_ID",
        "DPR_ID",
        "MNC_ID",
        "ZNS_ID",
        "AFL_FECHA_AFILIACION_SGSSS",
        "AFC_FECHA_INICIO",
        "NUMERO CONTRATO",
        "FECHADE INICIO DEL CONTRATO",
        "CNT_AFL_TPS_GRP_PBL_ID",
        "CNT_AFL_TPS_PRT_ETN_ID",
        "TPS_MDL_SBS_ID",
        "TPS_EST_AFL_ID",
        "CND_AFL_FECHA_INICIO",
        "CND_AFL_FECHA_INICIO",
        "GRP_FML_COTIZANTE_ID",
        "PORTABILIDAD",
        "COD_IPS_P",
        "MTDLG_G_P",
        "SUB_SISBEN_IV",
        "MARCASISBENIV+MARCASISBENIII",
        "CRUCE_BDEX_RNEC",
    ]

    try:
        # Cargar archivos sin encabezados
        df1 = pd.read_csv(
            ruta_maestro1, sep=",", encoding="ansi", header=None, dtype=str
        )
        df2 = pd.read_csv(
            ruta_maestro2, sep=",", encoding="ansi", header=None, dtype=str
        )

        # Combinar DataFrames
        df = pd.concat([df1, df2], ignore_index=True)

        # Validar longitud del encabezado
        if len(encabezados) != df.shape[1]:
            error_msg = (
                "Error: La cantidad de columnas no coincide con el número de "
                "encabezados definidos."
            )
            print(error_msg)
            return None

        # Asignar encabezados únicos
        df.columns = encabezados
        return df

    except FileNotFoundError as e:
        print(f"Error: Archivo no encontrado - {e.filename}")
    except pd.errors.ParserError as e:
        print(f"Error: Problema al parsear los archivos - {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")
    return None


def cargar_maestro_ADRES(ruta_maestro):
    """
    Carga un archivo maestro en formato .txt separado por comas.
    El archivo no tiene encabezados, por lo que se asignan encabezados personalizados.
    Maneja errores comunes como columnas faltantes, separador incorrecto o
    ruta inválida.
    Args:
        ruta_maestro (str): Ruta del archivo maestro.
    Returns:
        pd.DataFrame: DataFrame con los registros, o None si ocurre un error.
    """
    encabezados = [
        "AFL_ID",
        "ENT_ID",
        "TPS_IDN_ID_CF",
        "HST_IDN_NUMERO_IDENTIFICACION_CF",
        "TPS_IDN_ID",
        "HST_IDN_NUMERO_IDENTIFICACION",
        "AFL_PRIMER_APELLIDO",
        "AFL_SEGUNDO_APELLIDO",
        "AFL_PRIMER_NOMBRE",
        "AFL_SEGUNDO_NOMBRE",
        "AFL_FECHA_NACIMIENTO",
        "TPS_GNR_ID",
        "AFL_PAIS_NACIMIENTO",
        "AFL_MUNICIPIO_NACIMIENTO",
        "AFL_NACIONALIDAD",
        "AFL_SEXO_IDENTIFICACION",
        "AFL_DISCAPACIDAD",
        "TPS_AFL_ID",
        "TPS_PRN_ID",
        "TPS_GRP_PBL_ID",
        "TPS_NVL_SSB_ID",
        "NUMEROFICHASISBEN",
        "TPS_CND_BNF_ID",
        "DPR_ID",
        "MNC_ID",
        "ZNS_ID",
        "AFL_FECHA_AFILIACION_SGSSS",
        "AFC_FECHA_INICIO",
        "NUMERO CONTRATO",
        "FECHADE INICIO DEL CONTRATO",
        "CNT_AFL_TPS_GRP_PBL_ID",
        "CNT_AFL_TPS_PRT_ETN_ID",
        "TPS_MDL_SBS_ID",
        "TPS_EST_AFL_ID",
        "CND_AFL_FECHA_INICIO",
        "CND_AFL_FECHA_INICIO",
        "GRP_FML_COTIZANTE_ID",
        "PORTABILIDAD",
        "COD_IPS_P",
        "MTDLG_G_P",
        "SUB_SISBEN_IV",
        "MARCASISBENIV+MARCASISBENIII",
        "CRUCE_BDEX_RNEC",
    ]

    try:
        # Intentar cargar el archivo
        df = pd.read_csv(
            ruta_maestro,
            sep=",",
            encoding="ansi",
            dtype=str,
            header=None,
            names=encabezados,
        )
        # Verificar si las columnas coinciden con los encabezados esperados
        if list(df.columns) != encabezados:
            raise ValueError(
                "Las columnas del archivo no coinciden con los encabezados esperados."
            )
        return df
    except FileNotFoundError:
        print(f"Error: La ruta del archivo no es válida: {ruta_maestro}")
    except pd.errors.ParserError:
        print(
            (f"Error: El separador del archivo puede ser incorrecto o el archivo "
             f"está malformado: {ruta_maestro}")
        )
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"Error inesperado al cargar el archivo {ruta_maestro}: {e}")
    return None
