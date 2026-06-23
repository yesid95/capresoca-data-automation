# Capresoca Data Automation

Proyecto de automatización de procesos de datos para el área de Aseguramiento de
Capresoca EPS. El repositorio reúne notebooks operativos, módulos reutilizables
en Python y documentación técnica de los principales flujos.

## Estado del proyecto

El proyecto se encuentra en desarrollo activo. Actualmente, la mayoría de los
procesos se ejecutan desde Jupyter Notebooks y se migran progresivamente a
módulos reutilizables dentro de `src/`.

## Contenido

- [Índice de notebooks](notebooks/README.md): catálogo de los 76 notebooks del
  proyecto.
- [Arquitectura](docs/arquitectura.md): descripción general de componentes y
  decisiones técnicas.
- [Casos de uso](docs/casos_uso.md): procesos funcionales contemplados.
- [Funciones](docs/funciones.md): referencia de funcionalidades.
- [Convenciones](docs/convenciones.md): lineamientos para desarrollar y
  documentar.
- [Roadmap](docs/roadmap.md): evolución prevista del proyecto.

## Estructura del repositorio

```text
capresoca-data-automation/
├── data/                  # Archivos de entrada locales
├── docs/                  # Documentación funcional y técnica
├── notebooks/
│   ├── Aseguramiento/     # Procesos del área de Aseguramiento
│   ├── Generales/         # Utilidades transversales
│   └── README.md          # Índice de notebooks
├── out/                   # Resultados generados por los procesos
├── src/
│   ├── data_cleaning.py   # Limpieza y reglas de transformación
│   ├── file_loader.py     # Carga estandarizada de archivos
│   └── main.py            # Punto de entrada experimental
├── tests/                 # Pruebas automatizadas
├── config.py              # Configuración compartida
└── requirements.txt       # Dependencias del entorno
```

## Requisitos

- Python 3.8 o superior.
- JupyterLab o la extensión de Jupyter para Visual Studio Code.
- Dependencias definidas en `requirements.txt`.

## Instalación

```powershell
git clone https://github.com/yesid95/capresoca-data-automation.git
cd capresoca-data-automation

python -m venv venv
.\venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Uso

1. Activa el entorno virtual.
2. Abre el proyecto en VS Code o inicia JupyterLab:

   ```powershell
   jupyter lab
   ```

3. Consulta el [índice de notebooks](notebooks/README.md) y abre el proceso que
   necesites.
4. Verifica las rutas y los parámetros de entrada antes de ejecutar las celdas.
5. Revisa los resultados generados en `out/` o en la ruta configurada por el
   notebook.

También existe un ejemplo de uso de la configuración compartida en
[`notebooks/ejemplo_uso_config.ipynb`](notebooks/ejemplo_uso_config.ipynb).

> **Importante:** los notebooks pueden procesar información sensible. No
> confirmes cambios que incluyan datos personales, credenciales, rutas locales,
> salidas de ejecución o archivos de entrada confidenciales.

## Desarrollo

- Ubica la lógica reutilizable en `src/` y evita duplicarla entre notebooks.
- Sigue PEP 8 y el límite de 88 caracteres configurado para Black.
- Agrega pruebas en `tests/` cuando migres o incorpores reglas de negocio.
- Documenta los nuevos procesos en `docs/`.
- Añade cada notebook nuevo al [índice](notebooks/README.md).

## Contacto

- Responsable: Osmar Yesid Rincón
- Correo: rincon3259@gmail.com

> Última actualización: 23 de junio de 2026.
