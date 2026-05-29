# Documentación Técnica: Asignación y Validación de Red de Servicios

**Archivo Principal:** [PR_AS_05_Asignacion_Notificacion_IPS.ipynb](../notebooks/Aseguramiento/PR_AS_05_Asignacion_Notificacion_IPS.ipynb)  
**Nivel:** Técnico / Negocio / Aseguramiento en Salud  
**Audiencia:** Analistas de Aseguramiento y Líderes de TI  

---

## 1. Introducción y Objetivo
Esta automatización realiza la validación, cruce y corrección de la red de prestadores (IPS) asignada a los afiliados en el Sistema de Información de la EPS (SIE) frente a la red contratada vigente por municipio. 

El proceso consolida información de múltiples fuentes nacionales y locales, identifica inconsistencias (como IPS incorrectas o vacías en servicios básicos), y genera reportes analíticos junto con archivos planos estructurados para realizar cargues automáticos de corrección en el SIE.

---

## 2. Diagramas de Soporte y Flujos
Para entender la lógica funcional y técnica de la automatización, se han diseñado tres diagramas en formato PlantUML:

*   **Flujo del Proceso General:** [flujo_asignacion.puml](diagrams/flujo_asignacion.puml)  
    *Muestra la secuencia paso a paso desde el cargue de insumos, cruces de linajes, filtros de exclusión por certificación, asignación municipal y validación final de red.*
*   **Ciclo de Vida y Estados del Afiliado:** [estados_afiliado.puml](diagrams/estados_afiliado.puml)  
    *Ilustra las fases de validación por las que pasa un afiliado y en cuál de los cinco destinos o reportes finales (Auditoría, Casos Especiales, Red Consolidada, etc.) se clasifica.*
*   **Diagrama de Insumos y Salidas:** [insumos_cargue.puml](diagrams/insumos_cargue.puml)  
    *Esquematiza las bases de datos de entrada (.csv, .xlsx, .txt) requeridas para la ejecución y las carpetas/archivos planos generados como salida del proceso.*

---

## 3. Insumos del Proceso (Entradas)
El proceso integra 9 fuentes de información externas y locales:

1.  **Reporte Red SIE** *(Archivo .csv)*: Estado de la red asignada a cada afiliado en el sistema interno del SIE.
2.  **Maestro SIE** *(Archivo .csv)*: Reporte local del Maestro del SIE útil para comprobación interna de datos.
3.  **Portabilidad Regional y Nacional** *(Archivos .xlsx)*: Planillas de afiliados con portabilidades solicitadas y aprobadas.
4.  **LMA (Liquidación Mensual de Afiliados)** *(Archivo .xlsx)*: Base de datos nacional que reporta la población liquidada por el ADRES.
5.  **Compensados ADRES** *(Archivo .xlsx)*: Registro de cotizantes compensados mensualmente.
6.  **Censo Indígena Caño Mochuelo** *(Archivo .xlsx)*: Población indígena censada del resguardo con condiciones prestacionales especiales.
7.  **Maestros BDUA ADRES** *(Archivos .txt)*: Maestros nacionales de subsidiado (EPS025) y contributivo (EPSC25) para cruce oficial.
8.  **Maestro Alto Costo** *(Archivo .xlsx)*: Reporte de afiliados con patologías de alto costo.
9.  **Tabla de Contratos** *(Archivo .txt)*: Base de datos consolidada con contratos vigentes, NIT de prestadores, servicios habilitados y municipios de cobertura.

---

## 4. Reglas de Negocio Clave

### 4.1. Homologación de Documentos (Linajes de Evolución)
Debido a desfases en las fechas de corte de las bases de datos, un mismo afiliado puede figurar en una base con un documento antiguo (ej. Tarjeta de Identidad `TI` en LMA) y con uno nuevo en otra (ej. Cédula `CC` en SIE). 
*   **Lógica:** El notebook cruza los registros mediante el serial único de la BDUA (`AFL_ID`).
*   **Linajes:** Agrupa los documentos en familias evolutivas (`NACIONAL`: CN $\rightarrow$ RC $\rightarrow$ TI $\rightarrow$ CC; `EXTRANJERO_PT`: MS $\rightarrow$ AS $\rightarrow$ SC $\rightarrow$ PE $\rightarrow$ PT; `EXTRANJERO_CE`).
*   **Unificación:** Se arrastran y fusionan las variables históricas del afiliado y se conserva una sola fila bajo el tipo de documento de mayor jerarquía vigente (ej. `CC` sobre `TI`), evitando duplicados o perfiles divididos.

### 4.2. Población Certificada (Garantía de Pago)
Solo se autoriza la asignación de red a la **población certificada**.
*   **Regla:** El afiliado debe estar **Activo en el ADRES** y además figurar como liquidado en la **LMA** o registrado en la base de **Compensados** del mes evaluado. Afiliados sin estado activo y sin certificado de liquidación son excluidos del cargue general y se reportan en la pestaña de `Auditoria`.

### 4.3. Cobertura Regional y Portabilidad Nacional
Capresoca EPS cuenta con cobertura exclusiva en el departamento de Casanare (cuyo código DANE inicia con `85`).
*   **Regla:** Se busca asignar red en el municipio registrado en el SIE.
*   **Exclusión de Portabilidad Nacional:** Si un afiliado cuenta con Portabilidad Nacional activa (traslado temporal fuera del departamento), el sistema no le asigna red en este proceso, quedando sin servicios en el SIE local y reportando su registro en `Auditoria` como "Portabilidad Nacional".
*   **Portabilidad Regional:** Si tiene portabilidad activa dentro de Casanare (PR), se le asigna red en el municipio receptor registrado en la planilla de portabilidades.

### 4.4. Regla Especial Caño Mochuelo (Población Indígena)
La población perteneciente a la comunidad indígena de Caño Mochuelo cuenta con una red de servicios básicos exclusiva contratada con una IPS específica.
*   **Ubicación de Origen:** Hato Corozal (código DANE `85125`) y Paz de Ariporo (código DANE `85250`).
*   **Servicios Básicos:** Medicina General, Laboratorio Clínico, Odontología General y Medicamentos.
*   **Asignación:** 
    *   Si el afiliado pertenece a Caño Mochuelo y reside en sus municipios de origen, se le asigna obligatoriamente la **IPSI Caño Mochuelo (NIT 900827186)** para los servicios básicos.
    *   Servicios no básicos (como Optometría) se asignan con la red general del municipio.
    *   Si reside fuera de estos municipios sin portabilidad regional activa, se reporta en `Casos_Especiales_Indigenas` como **Anomalía Indígena**.
    *   Para la población general (no indígena) en Hato Corozal y Paz de Ariporo, se excluye del menú de contratos a la IPSI Caño Mochuelo para evitar asignaciones erróneas de esta red especial.

---

## 5. Arquitectura del Pipeline (Módulos del Notebook)

1.  **Cargue y Limpieza:** Lee dinámicamente las rutas físicas locales del proyecto. Limpia y remueve duplicados explícitos en los archivos de entrada (LMA, Compensados, etc.).
2.  **Cruce y Exclusiones (Linajes):** Realiza la fusión de datos BDUA-ADRES-SIE, aplica la regla de linajes y genera la tabla unificada de afiliados. Filtra y remueve los afiliados excluidos (fallecidos, suspendidos, no certificados o portabilidad nacional) enviándolos a la tabla de Auditoría.
3.  **Validación de Red:** Contrasta servicio por servicio (`MEDICINA GENERAL`, `LABORATORIO CLINICO`, `ODONTOLOGIA GENERAL`, `MEDICAMENTOS`, `OPTOMETRIA`, `IMAGENES DIAGNOSTICAS - IONIZANTES`) la IPS registrada en SIE contra los contratos válidos del municipio DANE asignado. Escribe los estados:
    *   `OK`: Coincide con contrato activo.
    *   `VACIO`: No tiene IPS asignada en el SIE.
    *   `INCORRECTO`: Tiene una IPS asignada en el SIE que no coincide con la red contratada.
    *   `SIN_CONTRATO`: No hay contratos vigentes para ese servicio en el municipio.
4.  **Exportación:** Escribe el libro consolidado de Excel y genera los planos `.txt` estructurados.

---

## 6. Estructura de Salidas (Entregables)

### 6.1. Excel de Consolidación
Libro consolidado generado dinámicamente (`Red_Asignada_Consolidada_[Fecha].xlsx`) que contiene 5 hojas:
*   `Red_Consolidada`: Listado general de afiliados aptos y procesados.
*   `Detalle_Inconsistencias`: Novedades con estado `VACIO`, `INCORRECTO` o `SIN_CONTRATO` para cada servicio evaluado.
*   `Casos_Especiales_Indigenas`: Afiliados indígenas Caño Mochuelo identificados en anomalía de portabilidad.
*   `Auditoria`: Registros excluidos del proceso (no activos, no liquidados, portabilidad nacional, fallecidos).
*   `Dashboard_Resumen`: Estadísticas globales de la validación.

### 6.2. Directorio de Cargues SIE
Para corregir los servicios en el SIE, se genera una carpeta consolidada con el timestamp (`Cargues_SIE_[Fecha]/`) estructurada de la siguiente manera:
*   Subcarpetas por **Código de Municipio** (ej. `85001`, `85125`).
*   Si un municipio tiene más de una IPS contratada para el mismo servicio básico, se crea una subcarpeta con el **NIT de la IPS** dentro de la carpeta del municipio.
*   Archivos planos correctivos con el nombre `{municipio}_{código_servicio}.txt`.
*   **Estructura del archivo plano (sin encabezados, codificación ANSI, separado por `|`):**
    ```text
    TIPO_DOCUMENTO|NUMERO_DOCUMENTO|CODIGO_SERVICIO_SALUD|NIT_PRESTADOR
    ```

---

## 7. Guía de Mantenimiento

1.  **Nombres de Archivo Mensuales:** Al inicio del notebook en el bloque de rutas, se deben actualizar los nombres de los archivos correspondientes a las bases de datos de entrada mensuales.
2.  **Códigos de Servicio:** La exportación utiliza mapeos fijos del nombre de servicio al código SIE del validador (ej: Medicina General $\rightarrow$ `328`, Medicamentos $\rightarrow$ `989`). Si se habilitan nuevos códigos en el catálogo SIE, deben añadirse en el diccionario `map_codigos`.
3.  **Codificación ANSI:** Al exportar los archivos `.txt`, se utiliza estrictamente `encoding='ansi'`. Esto asegura que caracteres especiales (como la Ñ en el tipo de documento o códigos especiales) se lean correctamente por el motor legacy del SIE de la EPS.
