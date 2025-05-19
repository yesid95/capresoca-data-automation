# Capresoca Data Automation

Automatización de procesos ETL, validación y análisis de la Base de Datos Única de Afiliados (BDUA) para CAPRESOCA EPS. Este proyecto está implementado en Python y utiliza Jupyter Notebooks para la exploración, transformación y análisis de datos, así como para la generación de reportes y validaciones automatizadas.

---

## 🚀 Objetivos
- Automatizar la extracción, transformación y carga (ETL) de datos BDUA.
- Validar y analizar la calidad de los datos provenientes de diferentes fuentes (SIE, ADRES, PILA, etc.).
- Generar reportes y estadísticas para la toma de decisiones.
- Facilitar la integración y trazabilidad de los datos de afiliados.
- Documentar y centralizar los procesos de análisis y aseguramiento de la información.

## 📦 Características principales
- Procesamiento y consolidación de archivos masivos (TXT, CSV, Excel).
- Validaciones cruzadas entre fuentes (SIE, ADRES, PILA, históricos, etc.).
- Automatización de reportes y generación de indicadores clave.
- Herramientas para la gestión documental (PDF, correos, unificación de archivos).
- Notebooks modulares para tareas específicas de aseguramiento y cartera.

## 📂 Estructura del proyecto

```txt
CAPRESOCA-DATA-AUTOMATION/
│
├── data/             ← Datos brutos y procesados
├── docs/             ← Documentación adicional
├── logs/             ← Archivos de log
├── notebooks/        ← Jupyter notebooks de exploración y automatización
│   ├── Aseguramiento/   ← Procesos de validación, indicadores y reportes
│   └── Generales/       ← Utilidades generales y herramientas de apoyo
├── src/              ← (Reservado para scripts Python reutilizables)
├── tests/            ← (Reservado para pruebas unitarias/integración)
├── venv/             ← Entorno virtual (no versionado)
├── .gitignore
├── requirements.txt  ← Dependencias del proyecto
└── README.md         ← Documentación principal
```

## 🛠️ Instalación

1. Clona el repositorio y accede a la carpeta del proyecto:
   ```powershell
   git clone <URL_DEL_REPOSITORIO>
   cd capresoca-data-automation
   ```
2. Crea y activa un entorno virtual (recomendado):
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate
   ```
3. Instala las dependencias:
   ```powershell
   pip install -r requirements.txt
   ```

## 📊 Uso básico

- Abre los notebooks en la carpeta `notebooks/` con Jupyter o VS Code.
- Ejecuta los notebooks según el proceso requerido (validación, indicadores, unificación, etc.).
- Personaliza las rutas de entrada/salida según tu entorno local.

## 📒 Organización de notebooks
- **Aseguramiento/**: Validaciones, indicadores, reportes y procesos de aseguramiento de la información (ej: `Validar SIE.ipynb`, `Indicadores_Traslados_ADRES.ipynb`, `Unificar_Archivos.ipynb`).
- **Generales/**: Utilidades para manejo de PDFs, correos, estructura de carpetas, etc.

## 🧩 Dependencias principales
- pandas, numpy, requests, SQLAlchemy, openpyxl, xlsxwriter, entre otras (ver `requirements.txt`).

## 🤝 Contribución
Las contribuciones son bienvenidas. Por favor, abre un issue o pull request para sugerencias, mejoras o corrección de errores.

## 📄 Licencia
Proyecto privado para uso interno de CAPRESOCA EPS.

## 📬 Contacto
**Responsable:** Osmar Rincón  
**Correo:** osmarrincon@uniminuto.edu

---

> Última actualización: mayo 2025
