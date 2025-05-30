from setuptools import setup, find_packages

setup(
    name="capresoca_data_automation",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas",
        "numpy",
        # Agrega otras dependencias necesarias aquí
    ],
    entry_points={
        "console_scripts": [
            # Define scripts ejecutables si es necesario
        ],
    },
    description="Automatización de validaciones y procesos para Capresoca",
    author="Osmar Yesid Rincon Z",
    author_email="rincon3259@gmail.com",
    url="https://github.com/yesid95/capresoca-data-automation.git",  
)