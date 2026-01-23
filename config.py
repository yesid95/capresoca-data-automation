"""
Configuración centralizada de rutas del proyecto Capresoca.

Este archivo se versiona en Git y detecta automáticamente:
- El usuario actual del sistema
- La ruta del proyecto
- Las rutas base de OneDrive

Uso en notebooks:
    import sys
    from pathlib import Path
    
    # Detectar automáticamente la raíz del proyecto
    project_root = Path.cwd()
    while not (project_root / 'config.py').exists() and project_root != project_root.parent:
        project_root = project_root.parent
    sys.path.insert(0, str(project_root))
    
    import config
    
    # Usar rutas
    R_Ips = config.IPS_CODIGO
    R_Salida = config.get_traslados_output_dir(2026, 1, 16)
"""

import os
from pathlib import Path
from datetime import datetime, date, timedelta
from typing import Optional, Literal, Union


# ============================================================================
# DETECCIÓN AUTOMÁTICA DEL USUARIO Y RUTAS BASE
# ============================================================================

# Detectar usuario actual del sistema
CURRENT_USER = os.getenv('USERNAME') or os.getenv('USER')

# Ruta base de OneDrive (común para todos los usuarios)
ONEDRIVE_BASE = Path(f"C:/Users/{CURRENT_USER}/OneDrive - 891856000_CAPRESOCA E P S")

# Rutas base del proyecto
CAPRESOCA_BASE = ONEDRIVE_BASE / "Capresoca" / "AlmostClear"
ESCRITORIO_BASE = ONEDRIVE_BASE / "Escritorio"
YESID_BASE = ESCRITORIO_BASE / "Yesid Rincón Z"


# ============================================================================
# CONSTANTES
# ============================================================================

CONSTANTES_DIR = CAPRESOCA_BASE / "Constantes"
IPS_CODIGO = CONSTANTES_DIR / "IPS_CODIGO.txt"
DEPARTAMENTOS = CONSTANTES_DIR / "Departamentos.txt"
GLOSAS_ADRES = CONSTANTES_DIR / "Glosas ADRES 2025.xlsx"


# ============================================================================
# MAESTROS BDUA
# ============================================================================

BDUA_BASE = CAPRESOCA_BASE / "Procesos BDUA"

# Contributivo
BDUA_CONTRIBUTIVO = BDUA_BASE / "Contributivo"
MAESTRO_CONTRIBUTIVO_DIR = BDUA_CONTRIBUTIVO / "Maestro"

# Subsidiado
BDUA_SUBSIDIADO = BDUA_BASE / "Subsidiados"
MAESTRO_SUBSIDIADO_DIR = BDUA_SUBSIDIADO / "Maestro" / "MS"

# NS (Novedades Subsidiados)
NS_BASE = BDUA_SUBSIDIADO / "Procesos BDUA EPS" / "NS"
NS_NEGADO_DIR = NS_BASE / "NS Negado"


# ============================================================================
# TRASLADOS
# ============================================================================

TRASLADOS_BASE = YESID_BASE / "Traslados" / "Procesos BDUA"


# ============================================================================
# SIE
# ============================================================================

SIE_BASE = CAPRESOCA_BASE / "SIE"
SIE_ASEGURAMIENTO = SIE_BASE / "Aseguramiento"
SIE_EXPEDIENTES = SIE_ASEGURAMIENTO / "Expedientes" / "Años"


# ============================================================================
# FUNCIONES HELPER PARA RUTAS DINÁMICAS
# ============================================================================

def get_maestro_contributivo(year: int, month: int, day: int, dias_atras: int = 0) -> Path:
    """
    Obtiene la ruta del archivo maestro contributivo (EPSC25).
    
    Args:
        year: Año (ej: 2026)
        month: Mes (1-12)
        day: Día (1-31)
        dias_atras: Días a restar a la fecha (para maestros retroactivos)
    
    Returns:
        Path del archivo maestro contributivo
        Ejemplo: .../2026/EPSC25MC0014012026.TXT
    """
    # Aplicar días de retraso si se especifica
    if dias_atras > 0:
        fecha = date(year, month, day) - timedelta(days=dias_atras)
        year, month, day = fecha.year, fecha.month, fecha.day
    
    fecha_str = f"{day:02d}{month:02d}{year}"
    archivo = f"EPSC25MC00{fecha_str}.TXT"
    return MAESTRO_CONTRIBUTIVO_DIR / str(year) / archivo


def get_maestro_subsidiado(year: int, month: int, day: int, dias_atras: int = 0) -> Path:
    """
    Obtiene la ruta del archivo maestro subsidiado (EPS025).
    
    Args:
        year: Año (ej: 2026)
        month: Mes (1-12)
        day: Día (1-31)
        dias_atras: Días a restar a la fecha (para maestros retroactivos)
    
    Returns:
        Path del archivo maestro subsidiado
        Ejemplo: .../2026/EPS025MS0014012026.TXT
    """
    # Aplicar días de retraso si se especifica
    if dias_atras > 0:
        fecha = date(year, month, day) - timedelta(days=dias_atras)
        year, month, day = fecha.year, fecha.month, fecha.day
    
    fecha_str = f"{day:02d}{month:02d}{year}"
    archivo = f"EPS025MS00{fecha_str}.TXT"
    
    # Para años anteriores puede usar formato 2025-02
    if year < 2026:
        periodo = f"{year}-02" if month >= 7 else f"{year}-01"
        return MAESTRO_SUBSIDIADO_DIR / periodo / archivo
    
    return MAESTRO_SUBSIDIADO_DIR / str(year) / archivo


def get_ns_negado(year: int, month: int, day: int, dias_atras: int = 0) -> Path:
    """
    Obtiene la ruta del archivo NS Negado (.NEG).
    
    Args:
        year: Año (ej: 2026)
        month: Mes (1-12)
        day: Día (1-31)
        dias_atras: Días a restar a la fecha (para archivos retroactivos)
    
    Returns:
        Path del archivo NS negado
        Ejemplo: .../2026/NSEPS02509012026.NEG
    """
    # Aplicar días de retraso si se especifica
    if dias_atras > 0:
        fecha = date(year, month, day) - timedelta(days=dias_atras)
        year, month, day = fecha.year, fecha.month, fecha.day
    
    fecha_str = f"{day:02d}{month:02d}{year}"
    archivo = f"NSEPS025{fecha_str}.NEG"
    return NS_NEGADO_DIR / str(year) / archivo


def get_traslados_dir(year: int, month: int, day: int) -> Path:
    """
    Obtiene el directorio de traslados para una fecha específica.
    
    Args:
        year: Año (ej: 2026)
        month: Mes (1-12)
        day: Día (1-31)
    
    Returns:
        Path del directorio de traslados
        Ejemplo: .../2026/01_Enero/16
    """
    meses = {
        1: "01_Enero", 2: "02_Febrero", 3: "03_Marzo", 4: "04_Abril",
        5: "05_Mayo", 6: "06_Junio", 7: "07_Julio", 8: "08_Agosto",
        9: "09_Septiembre", 10: "10_Octubre", 11: "11_Noviembre", 12: "12_Diciembre"
    }
    
    mes_nombre = meses[month]
    return TRASLADOS_BASE / str(year) / mes_nombre / str(day)


def get_ns_sie(year: int, month: int, day: int) -> Path:
    """
    Obtiene la ruta del archivo NS desde SIE.
    
    Args:
        year: Año (ej: 2026)
        month: Mes (1-12)
        day: Día (1-31)
    
    Returns:
        Path del archivo NS SIE
        Ejemplo: .../16/SIE_NSEPS02516012026.txt
    """
    traslados_dir = get_traslados_dir(year, month, day)
    fecha_str = f"{day:02d}{month:02d}{year}"
    archivo = f"SIE_NSEPS025{fecha_str}.txt"
    return traslados_dir / archivo


def get_ns_no_enviar(year: int, month: int, day: int) -> Path:
    """
    Obtiene la ruta del archivo "No enviar".
    
    Args:
        year: Año (ej: 2026)
        month: Mes (1-12)
        day: Día (1-31)
    
    Returns:
        Path del archivo "No enviar"
        Ejemplo: .../16/No enviar 16-01-2026.txt
    """
    traslados_dir = get_traslados_dir(year, month, day)
    fecha_str = f"{day:02d}-{month:02d}-{year}"
    archivo = f"No enviar {fecha_str}.txt"
    return traslados_dir / archivo


def get_ns_enviar(year: int, month: int, day: int) -> Path:
    """
    Obtiene la ruta del archivo "Pendiente" (a enviar).
    
    Args:
        year: Año (ej: 2026)
        month: Mes (1-12)
        day: Día (1-31)
    
    Returns:
        Path del archivo "Pendiente"
        Ejemplo: .../16/Pendiente 16-01-2026.txt
    """
    traslados_dir = get_traslados_dir(year, month, day)
    fecha_str = f"{day:02d}-{month:02d}-{year}"
    archivo = f"Pendiente {fecha_str}.txt"
    return traslados_dir / archivo


def get_traslados_output_dir(year: int, month: int, day: int) -> Path:
    """
    Obtiene el directorio de salida para traslados.
    Es un alias de get_traslados_dir() para claridad.
    
    Args:
        year: Año (ej: 2026)
        month: Mes (1-12)
        day: Día (1-31)
    
    Returns:
        Path del directorio de salida
    """
    return get_traslados_dir(year, month, day)


def ensure_dir(path: Path) -> Path:
    """
    Asegura que un directorio exista, creándolo si es necesario.
    
    Args:
        path: ruta del directorio
    
    Returns:
        Path del directorio creado
    """
    path.mkdir(parents=True, exist_ok=True)
    return path


# ============================================================================
# FUNCIONES CON OBJETOS DATE (MÁS PYTHONIC)
# ============================================================================

def get_maestro_contributivo_fecha(fecha: date, dias_atras: int = 0) -> Path:
    """
    Obtiene la ruta del archivo maestro contributivo usando un objeto date.
    
    Args:
        fecha: Objeto date del proceso
        dias_atras: Días a restar a la fecha (para maestros retroactivos)
    
    Returns:
        Path del archivo maestro contributivo
        
    Ejemplo:
        >>> from datetime import date
        >>> fecha = date(2026, 1, 16)
        >>> ruta = get_maestro_contributivo_fecha(fecha, dias_atras=4)
    """
    if dias_atras > 0:
        fecha = fecha - timedelta(days=dias_atras)
    return get_maestro_contributivo(fecha.year, fecha.month, fecha.day)


def get_maestro_subsidiado_fecha(fecha: date, dias_atras: int = 0) -> Path:
    """
    Obtiene la ruta del archivo maestro subsidiado usando un objeto date.
    
    Args:
        fecha: Objeto date del proceso
        dias_atras: Días a restar a la fecha (para maestros retroactivos)
    
    Returns:
        Path del archivo maestro subsidiado
        
    Ejemplo:
        >>> from datetime import date
        >>> fecha = date(2026, 1, 16)
        >>> ruta = get_maestro_subsidiado_fecha(fecha, dias_atras=4)
    """
    if dias_atras > 0:
        fecha = fecha - timedelta(days=dias_atras)
    return get_maestro_subsidiado(fecha.year, fecha.month, fecha.day)


def get_ns_negado_fecha(fecha: date, dias_atras: int = 0) -> Path:
    """
    Obtiene la ruta del archivo NS Negado usando un objeto date.
    
    Args:
        fecha: Objeto date del proceso
        dias_atras: Días a restar a la fecha
    
    Returns:
        Path del archivo NS negado
    """
    if dias_atras > 0:
        fecha = fecha - timedelta(days=dias_atras)
    return get_ns_negado(fecha.year, fecha.month, fecha.day)


def get_traslados_dir_fecha(fecha: date) -> Path:
    """
    Obtiene el directorio de traslados usando un objeto date.
    
    Args:
        fecha: Objeto date del proceso
    
    Returns:
        Path del directorio de traslados
    """
    return get_traslados_dir(fecha.year, fecha.month, fecha.day)


def get_ns_sie_fecha(fecha: date) -> Path:
    """Obtiene la ruta del archivo NS SIE usando un objeto date."""
    return get_ns_sie(fecha.year, fecha.month, fecha.day)


def get_ns_no_enviar_fecha(fecha: date) -> Path:
    """Obtiene la ruta del archivo 'No enviar' usando un objeto date."""
    return get_ns_no_enviar(fecha.year, fecha.month, fecha.day)


def get_ns_enviar_fecha(fecha: date) -> Path:
    """Obtiene la ruta del archivo 'Pendiente' usando un objeto date."""
    return get_ns_enviar(fecha.year, fecha.month, fecha.day)


# ============================================================================
# CONFIGURACIÓN RÁPIDA PARA FECHA ACTUAL
# ============================================================================

def configurar_rutas_fecha(year: int, month: int, day: int) -> dict:
    """
    Configura todas las rutas para una fecha específica.
    Retorna un diccionario con todas las rutas necesarias.
    
    Args:
        year: Año (ej: 2026)
        month: Mes (1-12)
        day: Día (1-31)
    
    Returns:
        Dict con todas las rutas configuradas
    
    Ejemplo:
        rutas = configurar_rutas_fecha(2026, 1, 16)
        R_Ms_ADRES_EPSC25 = rutas['maestro_contributivo']
        R_Salida = rutas['salida']
    """
    return {
        'maestro_contributivo': get_maestro_contributivo(year, month, day),
        'maestro_subsidiado': get_maestro_subsidiado(year, month, day),
        'ns_negado': get_ns_negado(year, month, day),
        'ns_sie': get_ns_sie(year, month, day),
        'ns_no_enviar': get_ns_no_enviar(year, month, day),
        'ns_enviar': get_ns_enviar(year, month, day),
        'ips_codigo': IPS_CODIGO,
        'salida': get_traslados_output_dir(year, month, day)
    }


def configurar_rutas_completas(fecha_proceso: date, dias_retraso_maestros: int = 0) -> dict:
    """
    Configura todas las rutas con soporte para maestros retroactivos.
    
    Args:
        fecha_proceso: Fecha del proceso actual
        dias_retraso_maestros: Días de retraso de los maestros (ej: 4 si los maestros son de 4 días atrás)
    
    Returns:
        Dict con todas las rutas configuradas, incluyendo fechas usadas
    
    Ejemplo:
        >>> from datetime import date
        >>> rutas = configurar_rutas_completas(date(2026, 1, 16), dias_retraso_maestros=4)
        >>> R_Ms_ADRES_EPSC25 = rutas['maestro_contributivo']
        >>> R_Salida = rutas['salida']
        >>> print(f"Maestros del: {rutas['fecha_maestros']}")
    """
    fecha_maestros = fecha_proceso - timedelta(days=dias_retraso_maestros) if dias_retraso_maestros > 0 else fecha_proceso
    
    return {
        # Fechas de referencia
        'fecha_proceso': fecha_proceso,
        'fecha_maestros': fecha_maestros,
        'dias_retraso': dias_retraso_maestros,
        
        # Maestros (con fecha retroactiva)
        'maestro_contributivo': get_maestro_contributivo_fecha(fecha_proceso, dias_retraso_maestros),
        'maestro_subsidiado': get_maestro_subsidiado_fecha(fecha_proceso, dias_retraso_maestros),
        'ns_negado': get_ns_negado_fecha(fecha_proceso, dias_retraso_maestros),
        
        # Archivos de trabajo (fecha del proceso)
        'ns_sie': get_ns_sie_fecha(fecha_proceso),
        'ns_no_enviar': get_ns_no_enviar_fecha(fecha_proceso),
        'ns_enviar': get_ns_enviar_fecha(fecha_proceso),
        
        # Constantes y salida
        'ips_codigo': IPS_CODIGO,
        'salida': get_traslados_dir_fecha(fecha_proceso)
    }


# ============================================================================
# INFORMACIÓN DEL SISTEMA
# ============================================================================

def info():
    """Muestra información de configuración actual."""
    print("=" * 70)
    print("CONFIGURACIÓN DEL PROYECTO CAPRESOCA")
    print("=" * 70)
    print(f"Usuario actual: {CURRENT_USER}")
    print(f"OneDrive base: {ONEDRIVE_BASE}")
    print(f"Capresoca base: {CAPRESOCA_BASE}")
    print(f"")
    print("Rutas clave:")
    print(f"  - IPS_CODIGO: {IPS_CODIGO}")
    print(f"  - Maestros contributivo: {MAESTRO_CONTRIBUTIVO_DIR}")
    print(f"  - Maestros subsidiado: {MAESTRO_SUBSIDIADO_DIR}")
    print(f"  - Traslados: {TRASLADOS_BASE}")
    print(f"  - SIE: {SIE_BASE}")
    print("=" * 70)


if __name__ == "__main__":
    # Si ejecutas este archivo directamente, muestra la configuración
    info()
    
    # Ejemplo de uso con fecha
    print("\n" + "=" * 70)
    print("EJEMPLOS DE USO")
    print("=" * 70)
    
    print("\n1. Configuración básica (fecha 16-01-2026):")
    rutas = configurar_rutas_fecha(2026, 1, 16)
    for nombre, ruta in rutas.items():
        print(f"  {nombre}: {ruta}")
    
    print("\n2. Configuración con maestros retroactivos (4 días):")
    from datetime import date
    fecha = date(2026, 1, 16)
    rutas_completas = configurar_rutas_completas(fecha, dias_retraso_maestros=4)
    print(f"  Fecha proceso: {rutas_completas['fecha_proceso']}")
    print(f"  Fecha maestros: {rutas_completas['fecha_maestros']}")
    print(f"  Maestro EPSC25: {rutas_completas['maestro_contributivo']}")
    print(f"  Maestro EPS025: {rutas_completas['maestro_subsidiado']}")
    print(f"  NS SIE: {rutas_completas['ns_sie']}")
    print(f"  Salida: {rutas_completas['salida']}")
