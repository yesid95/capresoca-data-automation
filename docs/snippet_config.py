# ============================================================================
# SNIPPET PARA COPIAR EN TUS NOTEBOOKS
# ============================================================================
# Copia este bloque al inicio de cualquier notebook para usar config.py
# sin hardcodear rutas de usuario

import sys
from pathlib import Path
from datetime import date

# Detectar automáticamente la raíz del proyecto
project_root = Path.cwd()
while not (project_root / 'config.py').exists() and project_root != project_root.parent:
    project_root = project_root.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import config

# ============================================================================
# CONFIGURAR FECHAS DE TRABAJO
# ============================================================================

# OPCIÓN 1: Configuración automática con retraso de maestros (RECOMENDADO)
fecha_proceso = date(2026, 1, 16)           # Fecha del proceso actual
dias_retraso_maestros = 4                    # Maestros de hace 4 días

# Obtener todas las rutas automáticamente
rutas = config.configurar_rutas_completas(fecha_proceso, dias_retraso_maestros)

# Asignar rutas
R_Ms_ADRES_EPSC25 = rutas['maestro_contributivo']
R_Ms_ADRES_EPS025 = rutas['maestro_subsidiado']
R_NS_NEG = rutas['ns_negado']
R_NS_SIE = rutas['ns_sie']
R_NS_No_Enviar = rutas['ns_no_enviar']
R_NS_Enviar = rutas['ns_enviar']
R_Ips = rutas['ips_codigo']
R_Salida = rutas['salida']

# ============================================================================
# VERIFICACIÓN
# ============================================================================
print(f"✅ Usuario: {config.CURRENT_USER}")
print(f"✅ Fecha proceso: {rutas['fecha_proceso'].strftime('%d/%m/%Y')}")
print(f"✅ Fecha maestros: {rutas['fecha_maestros'].strftime('%d/%m/%Y')}")
print(f"✅ Salida: {R_Salida}")

# Asegurar que el directorio de salida existe
config.ensure_dir(R_Salida)

# ============================================================================
# FIN DEL SNIPPET - Tu código va aquí abajo
# ============================================================================


# ============================================================================
# OTRAS OPCIONES DE USO
# ============================================================================

# OPCIÓN 2: Fechas separadas (si los maestros tienen fecha específica)
"""
fecha_proceso = date(2026, 1, 16)
fecha_maestro = date(2026, 1, 12)  # Fecha específica del maestro

R_Ms_ADRES_EPSC25 = config.get_maestro_contributivo_fecha(fecha_maestro)
R_Ms_ADRES_EPS025 = config.get_maestro_subsidiado_fecha(fecha_maestro)
R_NS_NEG = config.get_ns_negado_fecha(fecha_maestro)
R_NS_SIE = config.get_ns_sie_fecha(fecha_proceso)
R_NS_No_Enviar = config.get_ns_no_enviar_fecha(fecha_proceso)
R_NS_Enviar = config.get_ns_enviar_fecha(fecha_proceso)
R_Ips = config.IPS_CODIGO
R_Salida = config.get_traslados_dir_fecha(fecha_proceso)
"""

# OPCIÓN 3: Con parámetros individuales (compatibilidad con código anterior)
"""
year, month, day = 2026, 1, 16
dias_atras = 4

R_Ms_ADRES_EPSC25 = config.get_maestro_contributivo(year, month, day, dias_atras)
R_Ms_ADRES_EPS025 = config.get_maestro_subsidiado(year, month, day, dias_atras)
R_NS_NEG = config.get_ns_negado(year, month, day, dias_atras)
R_NS_SIE = config.get_ns_sie(year, month, day)
R_NS_No_Enviar = config.get_ns_no_enviar(year, month, day)
R_NS_Enviar = config.get_ns_enviar(year, month, day)
R_Ips = config.IPS_CODIGO
R_Salida = config.get_traslados_output_dir(year, month, day)
"""
