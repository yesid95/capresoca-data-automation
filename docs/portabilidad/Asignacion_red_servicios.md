# Subprocedimiento: Asignación de Red de Servicios y Notificación (Portabilidad)

## 1. Contexto Institucional
Este subprocedimiento forma parte integral del proceso de **Aseguramiento** de **Capresoca EPS**. Se fundamenta en el procedimiento **PR-AS-05 Portabilidad en Salud (V.05)**, el cual busca garantizar la continuidad de la prestación del servicio de salud cuando un afiliado se traslada de su domicilio de afiliación original.

## 2. Descripción del Proceso Técnico (Data Pipeline)

El objetivo es transformar la extracción bruta del sistema institucional en una base de datos depurada, auditada financieramente y geográficamente consistente para la asignación de red primaria.

### Fase 1: Ingesta y Normalización del SIE
* "**Fuente:** Aplicativo SIE (formato `.txt`, codificación UTF-8).
* **Estructura Inicial:** `nit;razon_social;abreviatura;numero_identificacion;municipio;codigo;servicio;`.
* **Tratamiento:** Debido a que el archivo duplica registros por cada servicio asignado, se debe normalizar la columna `servicio` para consolidar un **registro único por afiliado**."

### Fase 2: Cruce y Clasificación de Portabilidad
Se integra la información del reporte de portabilidad para identificar el tipo de desplazamiento del usuario:
* **Estados a asignar:** 1. Portabilidad Nacional.
    1. Portabilidad Regional.
    2. Sin Portabilidad.
* **Atributos adicionales:** Para la portabilidad regional, se mapean las columnas de departamento y municipio receptor.

### Fase 3: Validación Financiera (ADRES - LMA/Compensados)
* **Objetivo:** Filtrar la base de datos para reportar únicamente a los afiliados reconocidos económicamente por la ADRES.
* **Lógica:** Se identifican los usuarios pagados en el proceso de **Liquidación Mensual de Afiliados (LMA)** y los compensados. Los registros no pagados son marcados para análisis interno.

### Fase 4: Auditoría de Consistencia (SIE vs. ADRES)
Cruce masivo contra los maestros de ADRES (Contributivo y Subsidiado):
1. **Validación de Estado:** Identificación de activos, retirados y otras novedades.
2. **Consistencia Geográfica:** Se comparan los campos de municipio y departamento entre SIE y ADRES.
3. **Gestión de Inconsistencias:** Los usuarios con diferencias se aislan para corrección por parte de los profesionales de bases de datos, pero la asignación de red se mantiene bajo el **municipio registrado en el SIE**.

## 3. Salidas y Entregables (Outputs)
El pipeline generará los siguientes archivos para la notificación formal a los prestadores:

* **Archivo Maestro (Excel/.txt):** Consolidado general de todo el proceso de asignación.
* **Reporte de Inconsistencias:** Listado de usuarios para actualización en bases de datos.
* **Paquete por IPS:**
    * Un archivo **Excel** por cada IPS con sus afiliados asignados.

## 4. Requerimientos de Automatización
* **Tecnología:** Python (Pandas/Polars) para el manejo de grandes volúmenes de datos de los maestros ADRES/SIE.
* **Normalización:** Funciones de pivotado para la columna de servicios.
* **Exportación:** Script automatizado para la generación de carpetas y archivos individuales por NIT de IPS.