# Automatización de Informe de Glosas, Traslados e Ingresos (Inf_Glosas_Tras_Ingre.ipynb)

## 1. Descripción General
Este documento detalla el funcionamiento del notebook `Inf_Glosas_Tras_Ingre.ipynb`, diseñado para la **generación automática de informes de calidad y efectividad** en los procesos de afiliación, traslados y movilidad.

El sistema analiza los registros validados (aprobados) y los registros con glosas (errores) para determinar la **calidad del dato "a la primera"**. Permite identificar qué usuarios tienen mayor efectividad en el ingreso de información y cuáles requieren refuerzo, generando métricas clave para la gestión del equipo.

### 🎯 Objetivo del Negocio
Medir y visualizar el desempeño del equipo de operaciones en cuanto a la calidad de la información ingresada, identificando la tasa de rechazos (glosas) frente a los registros aprobados limpiamente. Esto facilita la retroalimentación y mejora continua en los procesos de afiliación.

---

## 2. Stack Tecnológico
*   **Lenguaje:** Python 3.x
*   **Librerías Principales:**
    *   `pandas`: Procesamiento, cruce y agregación de datos.
    *   `matplotlib` / `seaborn`: Generación de gráficos estáticos para reportes.
    *   `plotly`: Visualizaciones interactivas para análisis exploratorio.
    *   `python-docx`: Generación automática de informes en Word.
    *   `numpy`: Cálculos numéricos.

---

## 3. Arquitectura del Pipeline

```mermaid
graph TD
    subgraph Insumos [Fuentes de Datos]
        A[df_ms_val (Validados/Aprobados)] --> P(Procesamiento)
        B[df_ms (Glosados/Errores)] --> P
        C[df_expedientes (Maestro Usuarios)] --> P
    end

    subgraph Procesamiento [Motor de Cálculo]
        P --> F{Filtrado por Fecha}
        F --> K[Generación Llave Única]
        K --> E[Identificación de Errores Previos]
        E --> C1[Cálculo de Éxitos Limpios]
        E --> C2[Conteo de Errores Únicos]
        C1 & C2 --> M[Cruce con Usuarios]
        M --> KPI[Cálculo de Efectividad %]
    end

    subgraph Salida [Entregables]
        KPI --> G[Gráfico de Barras (PNG)]
        KPI --> R[Reporte de Efectividad]
        G --> W[Informe Word / Anexos]
    end
```

---

## 4. Lógica de Negocio Detallada

### 4.1. Preparación y Limpieza
1.  **Filtrado Temporal:** Se seleccionan los registros correspondientes al mes y año de trabajo definidos.
2.  **Llave Única:** Se construye una llave compuesta (`Tipo Documento` + `Número Identificación`) para rastrear inequívocamente a cada afiliado a través de las diferentes bases de datos.

### 4.2. Clasificación de Registros
El sistema distingue entre dos tipos de resultados para medir la calidad real:
*   **Validados Limpios (Éxito a la primera):** Registros que fueron aprobados y **NO** existen en la base histórica de glosas para ese periodo. Es decir, pasaron la validación sin correcciones previas.
*   **Con Error (Glosados):** Registros que presentaron al menos una glosa. Se cuentan por afiliado único, independientemente de cuántos errores específicos tenga el registro.

### 4.3. Asignación de Responsables
*   Se utiliza la base de `df_expedientes` como maestro para asociar cada registro (a través de la llave única) con el `Usuario Grabado`.
*   Esto permite atribuir tanto los éxitos como los errores a operadores específicos.

### 4.4. Cálculo de Indicadores
Para cada usuario se calculan las siguientes métricas:
*   **Total Gestionados:** Suma de éxitos limpios + registros con error.
*   **Porcentaje de Efectividad:** 
    $$ \text{Efectividad} = \left( \frac{\text{Éxitos Limpios}}{\text{Total Gestionados}} \right) \times 100 $$

---

## 5. Estructura de Salidas

### 📊 Gráfico de Efectividad
Se genera un gráfico de barras horizontal (`Grafico_Efectividad_Calidad_MM_YYYY.png`) que muestra:
*   **Eje Y:** Usuarios ordenados por efectividad.
*   **Eje X:** Porcentaje de efectividad (0-100%).
*   **Etiquetas:** Porcentaje exacto y desglose (X errores / Y total).
*   **Líneas de Referencia:** Meta de calidad (ej. 95%).

### 📄 Archivos Generados
*   Gráficos en formato `.png` en la carpeta `anexos`.
*   Tablas de resumen de efectividad (impresas en consola o exportadas).
*   (Opcional) Integración con reporte en Word mediante `python-docx`.

---

## 6. Instrucciones de Uso
1.  Asegúrese de cargar los archivos insumo (`df_ms_val`, `df_ms`, `df_expedientes`) correctamente al inicio del notebook.
2.  Defina la variable `fecha_trabajo` con el periodo a analizar (ej. "01/12/2025").
3.  Ejecute las celdas secuencialmente.
4.  Revise la carpeta de salida para encontrar los gráficos generados y el reporte final.
