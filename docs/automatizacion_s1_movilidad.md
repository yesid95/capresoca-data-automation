# Automatización de Movilidad y S1 (S1_Movilidad)

## Descripción General
Este documento describe el proceso automatizado implementado en el notebook `S1_Movilidad.ipynb`. El objetivo principal es determinar el estado de **Movilidad** de los afiliados (e.g., "Mora", "Al día", "Relación laboral Reciente") cruzando información de pagos (Pila), base de datos de afiliados (ADRES), novedades (R1, S1, NC), relaciones laborales y compensaciones (ABX/ACX).

El resultado final es un archivo Excel consolidado que sirve como insumo para la gestión de aseguramiento y reporte de novedades.

## Tecnologías Utilizadas
*   **Python 3.x**
*   **Pandas**: Para la manipulación, limpieza y cruce de grandes volúmenes de datos.
*   **Glob/OS**: Para la lectura masiva de archivos en directorios.
*   **Datetime**: Para cálculos complejos de fechas (sumar días cotizados, ajustar periodos).
*   **Regular Expressions (re)**: Para la limpieza y normalización de campos de texto (e.g., Población).

## Entradas y Salidas

### Entradas (Inputs)
El script integra múltiples fuentes de información:

1.  **Pila SIE (Aportes)**:
    *   **Tipo I**: Planillas Integradas (`.txt`).
    *   **Tipo IP**: Planillas de Pensionados (`.txt`).
2.  **Maestros y Reportes ADRES**:
    *   `R_MS_ADRES`: Maestro de afiliados Contributivo.
    *   `R_R1` / `R_S1`: Archivos de respuesta automática de novedades.
    *   `R_NC`: Archivos de Novedades de Corrección.
3.  **Información Interna y Otros**:
    *   `R_Relaciones_Laborales`: Reporte de relaciones laborales activas.
    *   `R_ABX` / `R_ACX`: Archivos históricos de compensación.
    *   `R_UGPP`: Reporte de fiscalización de la UGPP.

### Salidas (Outputs)
1.  **Dataframe Pila Consolidado (`S_Excel`)**:
    *   Formato: `.xlsx`
    *   Contenido: Matriz detallada por afiliado con su estado de movilidad calculado, fechas ajustadas de pago, y validaciones de retiro.

## Lógica del Proceso

### 1. Carga y Unificación de Pila
*   Se cargan y concatenan todos los archivos de Pila I y Pila IP.
*   Se homologan estructuras y se limpian datos (e.g., convertir "X" a 1 en Pila IP).
*   Se agrupan los registros por cotizante para sumar "Días Cotizados" y unificar marcas de Ingreso (ING) y Retiro (RET).
    *   *Lógica de Retiro*: Si todos los aportantes marcan retiro, se etiqueta como "Todos Los Aportantes Marcan Retiro".

### 2. Procesamiento de Fuentes Secundarias
*   **ABX/ACX**: Se filtran por fecha máxima por serial BDUA y se suman días cotizados.
*   **R1, S1, NC, Relaciones Laborales**: Se filtran para mantener solo el registro con la fecha más reciente por afiliado.

### 3. Cruces de Información (Merges)
*   El DataFrame principal (Pila) se enriquece cruzando con:
    *   **ADRES**: Para obtener estado, tipo de afiliado y población.
    *   **R1, S1, NC**: Para obtener fechas de novedades reportadas.
    *   **Relaciones Laborales**: Para verificar fechas de ingreso.
    *   **ABX/ACX**: Para historial de compensación.

### 4. Cálculo de Fechas Ajustadas
*   **Fecha Ajustada Pila**: Se calcula sumando los días cotizados a la fecha base (Periodo Pago o Fecha R1). Se ajusta al primer día del mes siguiente si la suma cambia de mes.
*   **Fecha Ajustada ACX/ABX**: Lógica similar para proyectar la cobertura basada en días compensados.

### 5. Determinación de Movilidad
Se clasifica a cada afiliado en una categoría de movilidad usando reglas de negocio y fechas de corte (`mora_dt`, `Dia_dt`):

*   **Mora**:
    *   No marcan retiro.
    *   No tienen régimen especial.
    *   Fechas de pago/compensación son anteriores a la fecha de corte de mora.
*   **Relación Laboral Reciente**:
    *   Tienen una fecha de ingreso laboral reciente (posterior a la fecha de corte).
*   **Al Día**:
    *   Fechas de pago o compensación cubren el periodo actual (entre fecha mora y fecha día).
*   **Casos Especiales**:
    *   **Activo Régimen Especial**: `Estado_especial_BDUA == 1`.
    *   **Pensionado**: `Estado_especial_BDUA == 4`.
    *   **UGPP**: Coinciden con el listado de la UGPP.

### 6. Limpieza Final y Exportación
*   **Población**: Se normaliza la columna usando expresiones regulares para extraer códigos jerárquicos (e.g., LC, Sisben D).
*   **Fecha de Envío**: Se calcula la fecha óptima de envío asegurando que sea posterior a la última novedad o pago registrado.
*   Se exporta el resultado final a Excel.

## Variables Clave de Configuración
*   `mora`: Fecha de corte para considerar un pago en mora (e.g., "30/08/2025").
*   `Dia`: Fecha de referencia actual (e.g., "01/09/2025").
*   Rutas de archivos: Configuradas al inicio del script (se recomienda parametrizar para producción).
