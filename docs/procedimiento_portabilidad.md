# Estructura del Procedimiento: Portabilidad en Salud (PR-AS-05)

## 1. Marco Institucional (Nivel Proceso)
* **Proceso Madre:** Aseguramiento.
* **Responsable del Proceso:** Subgerente Administrativo y Financiero.
* **Líder Técnico:** Coordinador de Aseguramiento.

## 2. El Procedimiento: Portabilidad (PR-AS-05)
La Portabilidad es la garantía de accesibilidad a los servicios de salud en cualquier municipio del territorio nacional para los afiliados de Capresoca EPS que emigren de su domicilio de afiliación.

### Alcance General
Comprende desde la radicación de la solicitud hasta la respuesta emitida informando la IPS asignada para servicios de baja complejidad.

---

## 3. Subprocedimiento en Desarrollo: Asignación de Red y Notificación
*Este es el primer módulo de automatización dentro del marco de Portabilidad.*

### A. Propósito del Subprocedimiento
Automatizar la identificación de usuarios, la asignación técnica de la red primaria en el municipio receptor y la notificación masiva a los prestadores (IPS).

### B. Insumos y Fuentes de Datos (Inputs)
Para la ejecución de los Notebooks de automatización, se requieren:
1. "**Base de Solicitudes:** Datos captados por canales presenciales, correo electrónico o página web.
2. **Maestros de Validación:** Base de Datos de Afiliados de Capresoca, BDUA (ADRES) y listados censales.
3. **Red de Servicios:** Listado de IPS de baja complejidad contratadas en municipios receptores."

### C. Actividades de Automatización (Pipeline)
"1. **Módulo de Validación:** Cruce automático de solicitudes vs. derechos en BDUA/ADRES.
2. **Módulo de Clasificación:** Categorización del tipo de emigración (Ocasional, Temporal o Dispersión Familiar).
3. **Módulo de Asignación:** Vinculación de usuarios a la red primaria disponible en el municipio receptor.
4. **Módulo de Salidas:** Generación de archivos para cargue en el sistema institucional (SIE) y bases de datos de notificación para IPS."

### D. Definición de Columnas para Normalización
* `ID_Usuario`: Documento de identidad (Llave para cruces BDUA).
* `Mun_Receptor`: Municipio donde se requiere la atención.
* `Vigencia_Desde/Hasta`: Periodo de la portabilidad (Máximo 12 meses para temporal).
* `NIT_IPS_Asignada`: Identificador del prestador de baja complejidad asignado.

---

## 4. Otros Subprocesos (Pendientes de Integración)
Este documento queda abierto para la normalización de futuros subprocesos de Portabilidad, tales como:
* Gestión de Prórrogas (Superiores a 12 meses).
* Gestión de Emigraciones Permanentes (Traslados de EPS).
* Auditoría de Prestación de Servicios en Red Externa.